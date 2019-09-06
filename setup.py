from setuptools import setup

from distutils.core import Command
from distutils.command.install_data import install_data
from distutils.dir_util import remove_tree
from distutils import log

from os import path, makedirs, walk
from shutil import copyfile
from subprocess import call

from poorhttp import __version__, __name__


REQUIRES = []
with open("requirements.txt", "r") as requires:
    for line in requires:
        REQUIRES.append(line.strip())


def doc():
    with open('README.rst', 'r') as readme:
        return readme.read().strip()


def find_data_files(directory, target_folder=""):
    rv = []
    for root, dirs, files in walk(directory):
        if target_folder:
            rv.append((target_folder,
                       list(root+'/'+f
                            for f in files if f[0] != '.' and f[-1] != '~')))
        else:
            rv.append((root,
                       list(root+'/'+f
                            for f in files if f[0] != '.' and f[-1] != '~')))
    log.info(str(rv))
    return rv


class build_doc(Command):
    description = "build html documentation, need jinja24doc >= 1.1.0"
    user_options = [
            ('build-base=', 'b',
             "base build directory (default: 'build.build-base')"),
            ('html-temp=', 't', "temporary documentation directory"),
            ('public', 'p', "build as part of public poorhttp web")
        ]

    def initialize_options(self):
        self.build_base = None
        self.html_temp = None
        self.public = False

    def finalize_options(self):
        self.set_undefined_options('build',
                                   ('build_base', 'build_base'))
        if self.html_temp is None:
            self.html_temp = path.join(self.build_base, 'html')

    def page(self, in_name, out_name=None):
        """Generate page."""
        if out_name is None:
            out_name = in_name
        if call(['jinja24doc', '-v', '--var', 'public=%s' % self.public,
                 '_%s.html' % in_name, 'doc'],
                stdout=open(self.html_temp + '/%s.html' % out_name, 'w')):
            raise IOError(1, 'jinja24doc failed')

    def run(self):
        log.info("building html documentation")
        if self.public:
            log.info("building as public part of poorhttp web")
        if self.dry_run:
            return

        if not path.exists(self.html_temp):
            makedirs(self.html_temp)
        self.page('poorhttp', 'index')
        self.page('changelog')
        self.page('licence')
        copyfile('doc/style.css', self.html_temp+'/style.css')
        copyfile('doc/web.css', self.html_temp+'/web.css')
        copyfile('doc/small-logo.png', self.html_temp+'/small-logo.png')


class clean_doc(Command):
    description = "clean up temporary files from 'build_doc' command"
    user_options = [
            ('build-base=', 'b',
             "base build directory (default: 'build-html.build-base')"),
            ('html-temp=', 't',
             "temporary documentation directory")
        ]

    def initialize_options(self):
        self.build_base = None
        self.html_temp = None

    def finalize_options(self):
        self.set_undefined_options('build_doc',
                                   ('build_base', 'build_base'),
                                   ('html_temp', 'html_temp'))

    def run(self):
        if path.exists(self.html_temp):
            remove_tree(self.html_temp, dry_run=self.dry_run)
        else:
            log.warn("'%s' does not exist -- can't clean it", self.html_temp)


class install_doc(install_data):
    description = "install html documentation"
    user_options = install_data.user_options + [
        ('build-base=', 'b',
         "base build directory (default: 'build-html.build-base')"),
        ('html-temp=', 't',
         "temporary documentation directory"),
        ('skip-build', None, "skip the build step"),
        ]

    def initialize_options(self):
        self.build_base = None
        self.html_temp = None
        self.skip_build = None
        install_data.initialize_options(self)

    def finalize_options(self):
        self.set_undefined_options('build_doc',
                                   ('build_base', 'build_base'),
                                   ('html_temp', 'html_temp'))
        self.set_undefined_options('install',
                                   ('skip_build', 'skip_build'))
        install_data.finalize_options(self)

    def run(self):
        if not self.skip_build:
            self.run_command('build_doc')
        self.data_files = find_data_files(self.html_temp,
                                          'share/doc/poorhttp/html')
        install_data.run(self)


setup(
    name=__name__,
    version=__version__,
    description="Http/WSGI server for Python",
    author="Ondřej Tůma",
    author_email="mcbig@zeropage.cz",
    maintainer="Ondrej Tuma",
    maintainer_email="mcbig@zeropage.cz",
    url="http://poorhttp.zeropage.cz/poorhttp",
    packages=['poorhttp'],
    data_files=[('/etc/init.d', ['init.d/poorhttp']),
                ('/etc', ['etc/poorhttp.ini']),
                ('/var/run', []), ('/var/log', []),
                ('share/poorhttp/example', ['simple.py']),
                ('share/doc/poorhttp', ['README.rst', 'ChangeLog', 'COPYING',
                 'doc/about.rst'])],
    license="BSD",
    long_description=doc(),
    classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Environment :: No Input/Output (Daemon)",
            "Intended Audience :: Customer Service",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: BSD License",
            "Natural Language :: English",
            "Natural Language :: Czech",
            "Programming Language :: Python :: 3 :: Only",
            "Topic :: Internet :: WWW/HTTP :: WSGI :: Server"],
    python_requires=">=3",
    install_requires=REQUIRES,
    cmdclass={'build_doc': build_doc,
              'clean_doc': clean_doc,
              'install_doc': install_doc},
    entry_points={
        'console_scripts': [
            'poorhttp = poorhttp.main:main'
        ]
    }
)
