.. image:: https://img.shields.io/pypi/v/PoorHTTP.svg
    :target: https://pypi.python.org/pypi/poorhttp/
    :alt: Latest version

.. image:: https://img.shields.io/pypi/pyversions/PoorHTTP.svg
    :target: https://pypi.python.org/pypi/poorhttp/
    :alt: Supported Python versions

.. image:: https://img.shields.io/pypi/status/PoorHTTP.svg
    :target: https://pypi.python.org/pypi/poorhttp/
    :alt: Development Status

.. image:: https://img.shields.io/pypi/l/PoorHTTP.svg
    :target: https://pypi.python.org/pypi/poorhttp/
    :alt: License

PoorHTTP
========
PoorHTTP server is standalone HTTP/WSGI server, which is designed
for using Python web applications. Unlike other projects, this is
not framework, but single server type application.

For more information see
`Project homepage <http://poorhttp.zeropage.cz/poorhttp>`_

Running
-------
**Daemon mode:**

.. code:: sh

    poorhttp --pidfile=/my/pidfile.pid --config=/my/config.ini start

**Foreground (docker) mode:**

.. code:: sh

    python3 -OO -m poorhttp -a localhost -w simple.py -f -i

Installation
------------
This software depends on two libraries ``python-daemon`` and ``lockfile`` which
are installed automatically by pip.

**From source:**

    * Release tarbal on https://github.com/PoorHttp/PoorHTTP/releases
    * Git with account on `<git@github.com:PoorHttp/PoorHTTP.git>`_
    * Git over http on https://github.com/PoorHttp/PoorHTTP.git

**PyPI:**

.. code:: sh

    pip3 install poorhttp
