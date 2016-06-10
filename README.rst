.. image:: https://travis-ci.org/asphalt-framework/asphalt-serialization.svg?branch=master
  :target: https://travis-ci.org/asphalt-framework/asphalt-serialization
  :alt: Build Status
.. image:: https://coveralls.io/repos/github/asphalt-framework/asphalt-serialization/badge.svg?branch=master
  :target: https://coveralls.io/github/asphalt-framework/asphalt-serialization?branch=master
  :alt: Code Coverage

This Asphalt framework component provides a standardized interface for a number of different
serialization algorithms:

* CBOR_ (using `cbor2 <http://pypi.python.org/pypi/cbor2>`_)
* JSON_ (using the Python standard library ``json`` module)
* msgpack_ (using `msgpack-python <https://pypi.python.org/pypi/msgpack-python>`_)
* Pickle_ (using the Python standard library ``pickle`` module)
* YAML_ (using `PyYAML <https://pypi.python.org/pypi/PyYAML>`_)

Additional backends may be provided through third party plugins.

Some serializers also provide hooks for safely (un)marshalling custom types and this mechanism
can easily be plugged into a third party marshalling library.

Project links
-------------

* `Documentation`_
* `Help and support`_
* `Source code`_
* `Issue tracker`_

.. _CBOR: http://cbor.io/
.. _JSON: http://wikipedia.org/wiki/JSON
.. _msgpack: http://msgpack.org/
.. _Pickle: https://docs.python.org/3/library/pickle.html
.. _YAML: http://wikipedia.org/wiki/YAML
.. _Documentation: http://asphalt-serialization.readthedocs.org/
.. _Help and support: https://github.com/asphalt-framework/asphalt/wiki/Help-and-support
.. _Source code: https://github.com/asphalt-framework/asphalt-serialization
.. _Issue tracker: https://github.com/asphalt-framework/asphalt-serialization/issues
