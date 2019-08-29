"""Server and Handler Classes

Main server classes for handling request and Log class, which works create
logs like from Apache.
"""
from wsgiref.simple_server import WSGIRequestHandler, WSGIServer, ServerHandler
from socketserver import ForkingMixIn, ThreadingMixIn
from logging import getLogger

import sys

from . import __name__, __version__

environ = {}

log = getLogger(__name__)


class PoorServer(WSGIServer):
    type = "Single"

    def handle_error(self, request, client_address):
        log.exception("Error for client %s", client_address[0])


class ForkingServer(ForkingMixIn, PoorServer):
    type = "Forking"


class ThreadingServer(ThreadingMixIn, PoorServer):
    type = "Threading"


class WebRequestHandler(WSGIRequestHandler):
    server_version = "%s/%s" % (__name__, __version__)

    def log_message(self, format, *args):
        sys.stdout.write(
            '%s %s - [%s] %s\n' %
            (self.server.server_name,       # TODO: HTTP_HOST
             self.address_string(),
             self.log_date_time_string(),
             format % args))

    def log_error(self, *args):
        log.error(args, self.address_string())
        self.log_message(*args)

    def handle(self):
        """Handle a single HTTP request"""

        self.raw_requestline = self.rfile.readline()
        if not self.parse_request():
            # An error code has been sent, just exit
            log.error("An error code has been sent.")
            return

        handler = PoorServerHandler(
            self.rfile, self.wfile, sys.stderr, self.get_environ()
        )
        handler.request_handler = self      # backpointer for logging
        handler.run(self.server.get_app())


class PoorServerHandler(ServerHandler):

    server_software = __name__
    os_environ = environ

    def run(self, application):
        """ServerHandler.run, then log the request when broken pipe"""
        try:
            ServerHandler.run(self, application)
        finally:
            if self.status:     # when broken pipe
                self.request_handler.log_request(
                        self.status.split(' ', 1)[0], self.bytes_sent)

    def log_exception(self, exc_info):
        """Just skip old stderr functionality."""
        log.exception("Error handling")
