"""Daemon class."""
from os import access, R_OK, W_OK, X_OK, fchown, dup2
from os.path import isdir, dirname, abspath, exists
from grp import getgrnam
from pwd import getpwnam
from wsgiref.simple_server import make_server
from time import sleep
from signal import Signals

import logging
import sys

from . import __name__
from .classes import WebRequestHandler


class Daemon():
    """HTTP Daemon."""
    def __init__(self, config):
        self.cfg = config
        self.logger = logging.getLogger(__name__)

    def check(self, daemon=True):
        """Check configuration."""
        if daemon:
            for afile in (self.cfg.error_log, self.cfg.access_log,
                          self.cfg.pid_file):
                if not isdir(dirname(afile)) or \
                        not access(dirname(afile), X_OK | W_OK) or \
                        (exists(afile) and not access(afile, R_OK | W_OK)):
                    raise RuntimeError("Could not access to %s" % afile)

            try:
                self.uid = getpwnam(self.cfg.user).pw_uid
                self.gid = getgrnam(self.cfg.group).gr_gid
            except KeyError:
                raise RuntimeError("Group od user not found on system")

            self.stderr = open(self.cfg.error_log, "a")
            self.stdout = open(self.cfg.access_log, "a")

        for path in reversed(self.cfg.path):
            sys.path.insert(0, abspath(path))

    def set_chown(self):
        fchown(self.error_log.fileno(), self.uid, self.gid)
        fchown(self.access_log.fileno(), self.uid, self.gid)

    def run(self, daemon=True):
        self.logger.info('Starting server type %s at %s:%d',
                         self.cfg.type, self.cfg.address, self.cfg.port)

        while True:
            wsgi = __import__(self.cfg.module, globals=globals())
            self.logger.info("Python module %s loaded.", wsgi.__file__)
            self.logger.info("Running %s", wsgi.application)

            try:
                httpd = make_server(self.cfg.address,
                                    self.cfg.port,
                                    wsgi.application,
                                    server_class=self.cfg.klass,
                                    handler_class=WebRequestHandler
                                    )

                httpd.timeout = 0.5
                httpd.serve_forever()
                return 0
            except Exception as exc:
                self.logger.exception(exc)
                if not daemon:
                    return 1
            sleep(1)

    def logrotate(self, signum, frame):
        """Signal handler for termination."""
        self.logger.info("Reopening logs with signal %s", Signals(signum).name)
        self.stdout.flush()
        self.stdout.close()
        self.stdout = open(self.cfg.access_log, "a")
        dup2(self.stdout.fileno(), sys.stdout.fileno())
        self.stderr.flush()
        self.stderr.close()
        self.stderr = open(self.cfg.error_log, "a")
        dup2(self.stderr.fileno(), sys.stderr.fileno())

    def shutdown(self, signum, frame):
        """Signal handler for termination."""
        self.logger.info("Shutting down with signal %s", Signals(signum).name)
        exit(1)

    def __del__(self):
        if hasattr(self, "stdout"):
            self.stdout.flush()
            self.stdout.close()
            self.stderr.flush()
            self.stderr.close()
