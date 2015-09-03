== What is Poor HTTP ==
Poor HTTP is part of Poor Http package of web publishing tools for application
developers. HTTP means thet is HTTP / WSGI server. It is based on Python
Simple Server from wsgiref package. In history, Poor HTTP and Poor WSGI was be
one Poor Http project, but with comming wsgi servers, they was be separeted.
It is easy to use. There are few python files as library, which this server
use. Server supported ini configuration file, and in package, there is init
script, which can start this server.

It is not installed to production environment what i know, but it could be
fine for developing. It knows user swithing, error access logging like big
servers like Appache. It is write in python, so no compilation is needed.
There was be smart importing mechanism, but it was not work, because it could
be so hard in python. At this time, it support three type of request handling.
Single, Forking and Threading server type.

== Running ==

There are some arguments, which you can put to poorhttp server script. After
info options like {-v} or {-h}, you can put path to config file, path to
pidfile, address and port which server listen on.

    #!text
    Poor http - python web server
    Usage: 
         poorhttp [options]

    Options:
         -h, --help                        only print this help text
         -v, --version                     only print server version

         --config=/etc/poorhttp.ini        config file, default ./poorhttp.ini
         --pidfile=/var/run/poorhttp.pid   pid file, by default gets from config
         --address=127.0.0.1               listening address, by default gets from
                                           config
         --port=8080                       listening port, by default gets from
                                           config

You can run like this:

    #!text
    poorhttp --pidfile=/my/pidfile.pid --config=/my/config.ini &

If you want to run with in optimize mode, you must run with python command:

    #!text
    python -O poorhttp --pidfile=/my/pidfile.pid --config=/my/config.ini &

=== init.d script ===
There is init.d script in pacakge. You can fork this script as simple init
script for your projects. You can configure the simple with a few variables at
head of it, or you can use as init script for one instance Poor HTTP in your
system. But your posix system have probably own init.d scripts with more
functionality then this simple example script.

    #!ini
    #!/bin/sh
    poorhttp=/usr/bin/poorhttp              # path to poorhttp python script
    pidfile=/var/run/poorhttp.pid           # default path to pid file
    config=/etc/poorhttp.ini                # default path to configuration file

    python=python                           # python interpretre, could be pytho2.6 for example
    ...

== Get Poor HTTP ==
==== Source tarball ====


    #!text
    Not yet

==== Source from git ====


    #!text
    ~$ git clone git@github.com:PoorHttp/PoorHTTP.git
    or
    ~$ git clone https://github.com/PoorHttp/PoorHTTP.git

==== Install from PyPI ====


    #!text
    Not yet

== Configuration ==
In configuration file, there are know too sections, first http is for Poor
HTTP server. Here you can set:

==== port ====
If port is set in command line, this variable will be ignored. Default value
is 8080 is not set.

==== address ====
Address, where server is listen on. What support wsgiref simple server, that
support Poor HTTP too. Default value is 127.0.0.1, and like as port, if this
value is set in command line argument, value from config file was be ignored.

==== pidfile ====
File which server store its pid to. Default value is /var/run/poorhttp.pid,
and it is write with user, under which is server start - real user. Like as
port or address, value in config file is ignored, if is set in command line
arguments.

==== user & group ====
This variables works only on posix system. User and group is effective user
and group, which process run under. Mechanism is simple, if you run server
under root privileges, and one of these variable is set, daemon do this:
    1) create pid file
    2) bind address and port 
    3) change log owner user and group to effective
    4) change effective group
    5) change effective user
    6) run server

Variables have no default values. It could be strings and it is use only if
real user which run daemon have privileges to change its effective user.
Concretely it must be root with id 0.

==== webmaster ====
Email address which is set as SERVER_ADMIN environment variable. Default
value is root@localhost.

==== errorlog ====
Path to error log file. File must be writable to process user. Default value
is {/var/log/poorhttp-error.log}.

==== accesslog ====
Path to access log file. File must be writable to process user. Default value
is {/var/log/poorhttp-access.log}. Access log style is similar to other big
servers style like Apache.
    
    #!text
    client.host server.host - [18/Sep/2013 23:29:01] "GET / HTTP/1.1" 200 514

==== type ====
One of server type. Values could be {single, forking or threading}. Default
value is single.

==== application ====
Path to python file, to the web wsgi application. By default value is empty.
With application, to python path application path is insert. So Poor HTTP server
import this file as module from python path.

==== path ====
Additional python path, which is a insert to python path environment. Default
value is {./}. If you want to add more paths, separate them with colon. For
example:
    
    #!ini
    path = ./:/my/app/:/my/app/lib      # add to path ./, /my/app and /my/app/lib

==== optimize ====
Python optimize type. This option is not use yet, and optimize is set as {-O}
in init.d sctipt, if debug is not set.

==== debug ====
This option is read only in init.d script. If is set false, {-O} optimize
parameter is use.

=== environ ===
There is environ section in configuration ini file. In this section, wsgi
environs are set. You can simple set as variable = environ. Last variable
value is used.

    #!ini
    [environ]
    app_email = noreply@application.com     # app_email variable is set to {noreply@application.com}
    poor_Debug = On                         # poor_Debug from Poor WSGI connector is set to {On}
    author = Top Secret                     # author variable is set to {Top Secret}

== History and Future ==

As is write and top of this documentation, Poor HTTP is only WSGI Server path
of Poor Http project. I don't know if some functionality will be add to this
server component. There are some another good wsgi servers. If you found some
good one, use uWsgi at http://projects.unbit.it/uwsgi/

Poor HTTP is not full http server, it is only daemon, which can run python
wsgi application on HTTP protocol. It is really fast. But be careful, with
putting it to production environment. It is important to be hidden after some
http proxy, like Lighttpd or Nginx.

=== ChangeLog ===
pre-release
    * Poor Http has it's own repository
    * Big code review and preparing for self package.  
    * delete importing - didn't work 
    * daemon user and group support 
    * python package with distutils 
    * configuration review 
    * right pid self cleaning 
    * working user environment setting 
    * some additional comments
    
20121130
    * Webmaster mail bug fix
    * Logging bug fix
    * Poorwsgi could return files or directory index, so no dispatch_table.py
      could not be error
    * Poorhttp is simple wsgi server
    * rename http to phttp
    * Document Listing and get file support
    * users handler error calling
    * Bug fix 
    * Environment fix
    * Flushing buffer bug fix
    * Some bug fix for run with uWsgi
    * Poorhttp is only wsgi server now.
    * And poorwsgi is python wsgi framework which coud be connect with anotger
      wsgi servers.
    * Method setreq is pre_process now.
    * Another post_process method is available.
    * Default handler as default_handler is available for other uri which is not
      in handlers list.
    * Read method for request in poorhttp.
    * Cookie bug fix with expire time and multiple cookie header support in
      poorhttp
    * fce support for getlist FieldStorage method
    * Directory listing, more compatible sendfile method and default it works
      html page.
    * Example is move to /app as default 'it works' example code. 

20120211
    * File listing support as default handler for directory if new config
      option index is enabled.
    * Little bugfix with document config option.

20111208:
    * convertor in FieldStorage
    * html error update
    * Doxygen support
    * example code
    * comments and documentation
    * bug fixes

20100729:
    * apache compatibility
    * single / forking / thrading mode
    * bugfixing and error handlers captching and loging
    * more status codes

20091130:
    * cookie session id is generate from expirydate by crypting
    * new method renew in cookie session

20091126:
    * new configurable value server secret key added
    * new function hidden in session module for text crypting
    * handled config error exception
    * bug fix in loging
