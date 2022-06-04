Configuration
=============

.. highlight:: yaml
.. py:currentmodule:: asphalt.serialization

To configure a serializer for your application, you need to choose a backend and then specify
any necessary configuration values for it. The following backends are provided out of the box:

* :mod:`~.serializers.cbor` (**recommended**)
* :mod:`~.serializers.json`
* :mod:`~.serializers.msgpack`
* :mod:`~.serializers.pickle`
* :mod:`~.serializers.yaml`

Other backends may be provided by other components.

Once you've selected a backend, see its specific documentation to find out what configuration
values you need to provide, if any. Configuration values are expressed as constructor arguments
for the backend class::

    components:
      serialization:
        backend: json

This configuration publishes a :class:`~.api.Serializer` resource named
``default`` using the JSON backend. The same can be done directly in Python code as
follows:

.. code-block:: python

    class ApplicationComponent(ContainerComponent):
        async def start(ctx: Context) -> None:
            self.add_component('serialization', backend='json')
            await super().start()


Multiple serializers
--------------------

If you need to configure multiple serializers, you will need to use multiple instances
of the serialization component::

    components:
      serialization:
        backend: cbor
      serialization2:
        type: serialization
        backend: msgpack
        resource_name: msgpack

The above configuration creates two serializer resources, available under 6 different
combinations:

* :class:`~.api.Serializer` / ``default``
* :class:`~.api.CustomizableSerializer` / ``default``
* :class:`~.serializers.cbor.CBORSerializer` / ``default``
* :class:`~.api.Serializer` / ``msgpack``
* :class:`~.api.CustomizableSerializer` / ``msgpack``
* :class:`~.serializers.msgpack.MsgpackSerializer` / ``msgpack``
