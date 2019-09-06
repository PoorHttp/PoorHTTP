What is PoorHTTP
================

PoorHTTP is part of Poor Http package of web publishing tools for application
developers. HTTP means that is HTTP / WSGI server. It is based on Python
Simple Server from ``wsgiref`` package. In history, PoorHTTP and PoorWSGI was be
one Poor Http project, but with coming WSGI servers, they was be separated.

PoorHTTP is easy to use. There are few Python files as library, which this server
use. Server supported ini configuration file, and in package, there is init.d
(system V) script, which can start this server on most POSIX systems.

It is not installed to production environment what i know, but it could be
fine for developing. It knows user switching, error and access logging like big
servers like Apache. It is write in Python, so no compilation is needed.
At this time, it support three type of request handling. Single, Forking and
Threading server type.

Running
=======
There are some command line arguments, which you can put to your server script.
After info options like ``-v`` or ``-h``, you can put path to configuration ini
file, path to pidfile, address and port, application and much more.

::

    usage: poorhttp [options] command

    HTTP/WSGI server for Python

    positional arguments:
      command               Daemon action (start|stop|logrotate|restart|status)

    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         only print server version
      -f, --foreground      Run as script on foreground
      -c <FILE>, --config <FILE>
                            Path to config file.
      -p <FILE>, --pidfile <FILE>
                            Path to pid file
      -a <ADDRESS>, --address <ADDRESS>
                            IP listening address (host or IP)
      -b <PORT>, --port <PORT>
                            TCP/IP listening port
      -w <MODULE>, --wsgi <MODULE>
                            wsgi application (Python module or file)
      -i, --info            More verbose logging level INFO is set.
      -d, --debug           DEBUG logging level is set.

You can run like this:

.. code:: sh

    poorhttp --pidfile=/my/pidfile.pid --config=/my/config.ini start

If you want to run with in optimize mode, you must run with Python command:

.. code:: sh

    python3 -OO -m poorhttp -a localhost -w simple.py -f -i

init.d script
-------------
There is init.d script in package. You can fork this script as simple init
script for your projects. You can configure simple with a few variables at
head of it, or you can use as init.d script for one instance PoorHTTP in your
system. But your POSIX system have probably own init.d scripts with more
functionality then this simple example script.

.. code:: bash

    #!/bin/sh
    poorhttp=/usr/bin/poorhttp       # path to poorhttp Python script
    pidfile=/var/run/poorhttp.pid    # default path to pid file
    config=/etc/poorhttp.ini         # default path to configuration file

    python=python3.7                 # Python interpreter command
    ...

Installation
============
This software depends on two libraries ``python-daemon`` and ``lockfile`` which are
installed automatically by pip.

**From source:**

    * Release tarbal on https://github.com/PoorHttp/PoorHTTP/releases
    * Git with account on `<git@github.com:PoorHttp/PoorHTTP.git>`_
    * Git over http on https://github.com/PoorHttp/PoorHTTP.git

**PyPI:**

.. code:: sh

    pip3 install poorhttp

Configuration
=============

[daemon]
--------
Next variables are used only on daemon mode. So in foreground mode, no pidfile
is created, and server run with user which run the PoorHTTP.


pidfile
~~~~~~~
File which server store its pid to. Default value is ``/var/run/poorhttp.pid``,
and it is write with user, under which is server start - real user. This option
could be set/override by command line option:

    -p <FILE>, --pidfile <FILE>   Path to pid file

user & group
~~~~~~~~~~~~
This variables works only on posix system. User and group is effective user
and group, which process run under. Mechanism is simple, if you run server
under root privileges, and one of these variable is set, daemon do this:

    1) create pid file
    2) change log owner user and group to effective    
    3) change effective group
    4) change effective user
    5) bind address and port
    6) run server

Variables have no default values. It could be strings and it is use only if
real user which run daemon have privileges to change its effective user.
Concretely it must be root with id 0.

[logging]
---------
level
~~~~~
PoorHTTP use Python ``logging`` module. So level is one of uppercase logging
level (``DEBUG|INFO|WARNING|ERROR|CRITICAL``). Default level is ``WARNING``.

You can override/set this by command line options:

    -i, --info      More verbose logging level ``INFO`` is set.
    -d, --debug     ``DEBUG`` logging level is set.

errorlog
~~~~~~~~
Path to error log file. File must be writable to process user. Default value
is ``/var/log/poorhttp-error.log``.

In foreground mode ``stderr`` is used instead.

accesslog
~~~~~~~~~
Path to access log file. File must be writable to process user. Default value
is ``/var/log/poorhttp-access.log``. Access log style is similar to other big
servers style like Apache.
    
::

    client.host server.host - [18/Sep/2013 23:29:01] "GET / HTTP/1.1" 200 514

In foreground mode ``stdout`` is used instead.

[http]
------

port
~~~~
TCP/IP port. Default is 8080. Value could be set/override by command line
option:

    -b <PORT>, --port <PORT>  TCP/IP listening port

address
~~~~~~~
Address, where server is listen on. What support wsgiref simple server, that
support PoorHTTP too. Default value is 127.0.0.1, and like as port, value could
be set/override by command line option:

    -a <ADDRESS>, --address <ADDRESS>   IP listening address (host or IP)

webmaster
~~~~~~~~~
Email address which is set as ``SERVER_ADMIN`` environment variable. Default
value is ``root@localhost``.

type
~~~~
One of server type. Values could be ``single``, ``forking`` or ``threading``.
Default value is ``single``.

[python]
--------
module
~~~~~~
Python importable file, which have `WSGI <https://www.python.org/dev/peps/pep-0333/>`_
``application``. If file is with path, the path is insert on first position
to Python module searching paths. Value could be set/override with option:

    -w <MODULE>, --wsgi <MODULE>    WSGI application (Python module or file)

path
~~~~
Additional Python path, which is a insert to Python path environment. Default
value is current path. If you want to add more paths, separate them with colon.
For example:

.. code:: ini

    path = ./:/my/app/:/my/app/lib      # add to path ./, /my/app and /my/app/lib

optimize
~~~~~~~~
Python optimize type. This option is used with init.d script only. If you want to
run server directly from command line, use Python ``-ON`` options.

debug
~~~~~
This option is used only in init.d script. If is set false, ``-O`` optimize
parameter is use.

[environ]
---------
There is environ section in configuration ini file. In this section, wsgi
environs are set. You can simple set as variable = value. Last variable
value is used.

.. code:: ini

    [environ]
    app_email = noreply@application.com     # app_email variable is set to ``noreply@application.com``
    poor_Debug = On                         # poor_Debug from Poor WSGI connector is set to ``On``
    author = Top Secret                     # author variable is set to ``Top Secret``

History and Future
==================

As is write at top of this documentation, PoorHTTP is only WSGI Server part
of Poor Http project. I don't know if some functionality will be add to this
server component. There are some another good wsgi servers. If you found some
good one, use uWsgi at http://projects.unbit.it/uwsgi/

Poor HTTP is not full http server, it is only daemon, which can run Python
wsgi application on HTTP protocol. It is really fast. But be careful, with
putting it to production environment. It is important to be hidden after some
http proxy, like Lighttpd or Nginx.

But when it's based only on Python libraries, it could be use on Python
supported light systems like routers, NAS or virtual machines.
