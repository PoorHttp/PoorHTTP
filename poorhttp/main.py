"""main() command line input function."""

from signal import SIGTERM, SIGHUP
from socket import error as SocketError
from traceback import format_exc
from argparse import ArgumentParser
from logging import getLogger
from os import geteuid, kill

from daemon import DaemonContext
from lockfile.pidlockfile import PIDLockFile

from . import __name__, __version__
from . config import Config
from . daemon import Daemon


log = getLogger(__name__)


def main():
    """Standard main function."""
    parser = ArgumentParser(
        description="HTTP/WSGI server for Python",
        usage="poorhttp [options] command"
    )
    parser.add_argument(
        "command", nargs='?', default="start", type=str,
        help="Daemon action (start|stop|logrotate|restart|status)")
    parser.add_argument(
        "-v", "--version", action="store_true",
        help="only print server version")

    parser.add_argument(
        "-f", "--foreground", action="store_true",
        help="Run as script on foreground")
    parser.add_argument(
        "-c", "--config", type=str,
        help="Path to config file.", metavar="<FILE>")
    parser.add_argument(
        "-p", "--pidfile", type=str,
        help="Path to pid file", metavar="<FILE>")
    parser.add_argument(
        "-a", "--address", type=str,
        help="IP listening address (host or IP)", metavar="<ADDRESS>")
    parser.add_argument(
        "-b", "--port", type=str,
        help="TCP/IP listening port", metavar="<PORT>")
    parser.add_argument(
        "-w", "--wsgi", type=str,
        help="wsgi application (Python module or file)", metavar="<MODULE>")
    parser.add_argument(
        "-i", "--info", action="store_true",
        help="More verbose logging level INFO is set.")
    parser.add_argument(
        "-d", "--debug", action="store_true",
        help="DEBUG logging level is set.")

    args = parser.parse_args()
    if args.version:
        print("%s %s version." % (__name__, __version__))
        return 0

    try:
        config = Config(args)

        pid_file = PIDLockFile(config.pid_file)

        if args.command == "stop":
            if pid_file.is_locked():
                log.info(
                    "Stoping service with pid %d", pid_file.read_pid())
                kill(pid_file.read_pid(), SIGTERM)
            return 0
        elif args.command == "status":
            if pid_file.is_locked():
                log.info(
                    "Service running with pid %d", pid_file.read_pid())
                return 0
            log.info("Service not running")
            return 1
        elif args.command == "logrotate":
            if pid_file.is_locked():
                log.info(
                    "Reopening service logs")
                kill(pid_file.read_pid(), SIGHUP)
                return 0
            log.info("Service not running")
            return 1
        elif args.command == "restart":
            if pid_file.is_locked():
                log.info(
                    "Restarting service with pid %d", pid_file.read_pid())
                kill(pid_file.read_pid(), SIGTERM)
        elif args.command == "start":
            pass
        elif not args.foreground:
            parser.error("Unknown command %s")
            return 1

        daemon = Daemon(config)
        daemon.check(not args.foreground)

        if args.foreground:
            return daemon.run(False)

        context = DaemonContext(
            working_directory="./",
            pidfile=pid_file,
            stderr=daemon.stderr, stdout=daemon.stdout,
            signal_map={SIGTERM: daemon.shutdown,
                        SIGHUP: daemon.logrotate},
            files_preserve=[daemon.stderr, daemon.stdout])

        if geteuid() == 0:
            context.uid = config.uid
            context.gid = config.gid
            daemon.set_chown()

        with context:
            daemon.logger.info(
                "Starting service with pid %d", pid_file.read_pid())
            daemon.run()
        return 0

    except KeyboardInterrupt:
        log.info('Shotdown server (keyboard interrupt)')
        return 1
    except SocketError:
        log.exception("Shutdown by SocketError")
        return 1
    except Exception as err:
        log.info("%s", args)
        log.debug("%s", format_exc())
        log.fatal("%s", err)
        parser.print_usage()
        return 1
