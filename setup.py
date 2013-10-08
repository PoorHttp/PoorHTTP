#!/usr/bin/python

from distutils.core import setup
from distutils.command.build_scripts import build_scripts
from distutils.command.build import build

from os import path, makedirs
from shutil import copyfile
from subprocess import call

class X_build_scripts(build_scripts):
    def run(self):
        if not path.exists('build/_scripts_'):
            makedirs('build/_scripts_')
        copyfile('poorhttp.py', 'build/_scripts_/poorhttp')
        build_scripts.run(self)     # run original build

class X_build(build):
    def run(self):
        print "creating documentation"
        if not path.exists('build/_html_'):
            makedirs('build/_html_')
        if call(['jinja24doc', '-v','_poorhttp.html', 'doc'],
                        stdout=file('build/_html_/index.html', 'w')):
            raise IOError(1, 'jinja24doc failed')
        if call(['jinja24doc', '-v', '_licence.html', 'doc'],
                        stdout=file('build/_html_/licence.html', 'w')):
            raise IOError(1, 'jinja24doc failed')
        copyfile('doc/style.css', 'build/_html_/style.css')
        build.run(self)             # run original build

setup(
    name                = "poorhttp",
    version             = "20120305",
    description         = "Poor Http server for Python",
    author              = "Ondrej Tuma",
    author_email        = "mcbig@zeropage.cz",
    url                 = "http://poorhttp.zeropage.cz/",
    packages            = ['poorhttp'],
    scripts             = ['build/_scripts_/poorhttp'],
    data_files          = [('/etc/init.d', ['init.d/poorhttp']),
                           ('/etc', ['etc/poorhttp.ini']),
                           ('/var/run', []), ('/var/log', []),
                           ('share/poorhttp/app', ['simple.py']),
                           ('share/doc/poorhttp/html', [
                                'build/_html_/index.html',
                                'build/_html_/license.html',
                                'build/_html_/style.css'])
                        ],
    license             = "BSD",
    long_description    =
            """
            Poor Http Server is standalone wsgi/http server, which is designed
            for using python web applications. Unlike other projects, this is
            not framework, but single server type application. It is not
            depended on another special technologies or frameworks, only on base
            python library.
            """,
    classifiers         = [
                            "Development Status :: 4 - Beta",
                            "Environment :: No Input/Output (Daemon)",
                            "Intended Audience :: Customer Service",
                            "Intended Audience :: Developers",
                            "License :: OSI Approved :: BSD License",
                            "Natural Language :: English",
                            "Natural Language :: Czech",
                            "Natural Language :: English",
                            "Programming Language :: Python :: 2",
                            "Topic :: Internet :: WWW/HTTP :: WSGI :: Server" ],
    cmdclass            = {'build_scripts': X_build_scripts,
                           'build': X_build },
)
