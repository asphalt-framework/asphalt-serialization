Configuration
=============

This component supports configuration of one or more serializer resources.
The available backends are:

======= ====================================================================
Alias   Backend class
======= ====================================================================
json    :class:`asphalt.serialization.serializers.json.JSONSerializer`
msgpack :class:`asphalt.serialization.serializers.msgpack.MsgpackSerializer`
pickle  :class:`asphalt.serialization.serializers.pickle.PickleSerializer`
yaml    :class:`asphalt.serialization.serializers.yaml.YAMLSerializer`
======= ====================================================================

The minimal configuration is as follows:

.. code-block:: yaml

    components:
      serialization: {}

This will publish a resource of type :class:`asphalt.serialization.api.Serializer`, named
``default``. The resource will be an instance of
:class:`~asphalt.serialization.serializers.json.JSONSerializer` and will appear in the context as
the ``json`` attribute.

What if you want to use, say, ``msgpack`` for serialization?
You can then configure the component a bit differently:

.. code-block:: yaml

    components:
      serialization:
        type: msgpack


Multiple serializers
--------------------

If you need to configure multiple serializers, you can do so by using the ``serializers``
configuration option:

.. code-block:: yaml

    components:
      serialization:
        serializers:
          json: {}
          msgpack: {}
          pickle: {}
          foobar:
            type: json
            context_attr: foo
            encoding: iso-8859-15

The above configuration creates 4 resources of type :class:`asphalt.serialization.api.Serializer`:

* ``json`` as ``ctx.json``
* ``msgpack`` as ``ctx.msgpack``
* ``pickle`` as ``ctx.pickle``
* ``foobar`` as ``ctx.foo``
