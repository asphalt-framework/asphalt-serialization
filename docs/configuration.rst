Configuration
=============

To configure a serializer for your application, you need to choose a backend and then specify
any necessary configuration values for it. The following backends are provided out of the box:

* :mod:`~asphalt.serialization.serializers.cbor` (**recommended**)
* :mod:`~asphalt.serialization.serializers.json`
* :mod:`~asphalt.serialization.serializers.msgpack`
* :mod:`~asphalt.serialization.serializers.pickle`
* :mod:`~asphalt.serialization.serializers.yaml`

Other backends may be provided by other components.

Once you've selected a backend, see its specific documentation to find out what configuration
values you need to provide, if any. Configuration values are expressed as constructor arguments
for the backend class:

.. code-block:: yaml

    components:
      serialization:
        backend: json

This configuration publishes a :class:`asphalt.serialization.api.Serializer` resource named
``default`` using the JSON backend, accessible as ``ctx.serializer``. The same can be done directly
in Python code as follows::

    class ApplicationComponent(ContainerComponent):
        async def start(ctx: Context):
            self.add_component('serialization', backend='json')
            await super().start()


Multiple serializers
--------------------

If you need to configure multiple serializers, you can do so by using the ``serializers``
configuration option:

.. code-block:: yaml

    components:
      serialization:
        serializers:
          cbor:
          json:
          msgpack:
          pickle:
          foobar:
            backend: json
            context_attr: foo
            encoding: iso-8859-15

The above configuration creates 5 resources of type :class:`asphalt.serialization.api.Serializer`:

* ``cbor`` as ``ctx.cbor``
* ``json`` as ``ctx.json``
* ``msgpack`` as ``ctx.msgpack``
* ``pickle`` as ``ctx.pickle``
* ``foobar`` as ``ctx.foo``
