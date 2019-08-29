from configparser import NoOptionError
from os.path import dirname, basename, splitext

import logging

from extendparser import Get

from . import __name__
from . classes import ForkingServer, ThreadingServer, PoorServer, environ

LOG_HANDLERS = ("syslog", "file")
LOG_FORMAT = "%(asctime)s %(levelname)s: %(name)s: %(message)s "\
             "{%(funcName)s() %(filename)s:%(lineno)d}"
ACCES_FORMAT = ""


def check_level(value):
    if value not in ("CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"):
        raise NoOptionError("Invalid value %s" % value)
    return value


def check_server(value):
    if value not in ("single", "threading", "forking"):
        raise NoOptionError("Invalid value %s" % value)
    return value


class Config(Get):
    """Config object."""
    def __init__(self, args):
        super(Config, self).__init__()
        self.optionxform = str  # case insensitive
        if args.config:
            self.read(args.config)

        # [daemon]
        if args.pidfile:
            self.pid_file = args.pidfile
        else:
            self.pid_file = self.get(
                "daemon", "pidfile", fallback="/var/run/poorhttpd.pid")

        self.user = self.get("daemon", "user", fallback="nobody")
        self.group = self.get("daemon", "group", fallback="nogroup")

        # [logging]
        self.error_log = self.get(
            "logging", "errorlog", fallback="/var/log/poorhttp-error.log")
        self.access_log = self.get(
            "logging", "accesslog", fallback="/var/log/poorhttp-access.log")
        if args.debug:
            self.log_level = "DEBUG"
        elif args.verbose:
            self.log_level = "INFO"
        else:
            self.log_level = self.get_option(
                "logging", "level", checker=check_level, fallback="WARNING")
        self.log_format = self.get("logging", "format", fallback=LOG_FORMAT)

        formatter = logging.Formatter(self.log_format)

        if logging.root.handlers:
            logging.root.handlers[0].setFormatter(formatter)
        else:
            handler = logging.StreamHandler()
            handler.setFormatter(formatter)
            logging.root.addHandler(handler)

        logger = logging.getLogger(__name__)
        logger.setLevel(self.log_level)

        # [http]
        if args.address:
            self.address = args.address
        else:
            self.address = self.get("http", "address", fallback="127.0.0.1")
        if args.port:
            self.port = args.port
        else:
            self.port = self.get_option("http", "port", target=int,
                                        fallback=8080)

        self.webmaster = self.get(
            "http", "webmaster", fallback="root@localhost")
        self.type = self.get_option(
            "http", "type", checker=check_server, fallback="single")
        if self.type == "forking":
            self.klass = ForkingServer
        elif self.type == "threading":
            self.klass = ThreadingServer
        else:
            self.klass = PoorServer

        # [python]
        self.path = self.get_option(
            "python", "path", target=list, delimiter=':', fallback=["./"])

        self.optimize = self.get_option("python", "optimize", target=int,
                                        fallback=1)
        self.debug = self.get_option("python", "debug", target=bool,
                                     fallback=False)

        module = None
        if args.wsgi:
            module = args.wsgi
        elif args.config:
            module = self.get("python", "module")
        else:
            raise RuntimeError("No python module is set.")
        self.path.insert(0, dirname(module))
        self.module = splitext(basename(module))[0]

        # [environ]
        if "environ" in self:
            for option in self.options("environ"):
                environ[option] = self.get("environ", option)
