API reference
=============

.. py:currentmodule:: asphalt.serialization

Component
---------

.. autoclass:: SerializationComponent

Serializer API
--------------

.. autoclass:: Serializer
.. autoclass:: CustomizableSerializer
.. autoclass:: CustomTypeCodec

Marshalling callbacks
---------------------

.. autofunction:: default_marshaller
.. autofunction:: default_unmarshaller

Custom type codecs
------------------

.. autoclass:: DefaultCustomTypeCodec

Serializers
-----------

.. autoclass:: asphalt.serialization.serializers.cbor.CBORSerializer
.. autoclass:: asphalt.serialization.serializers.json.JSONSerializer
.. autoclass:: asphalt.serialization.serializers.msgpack.MsgpackSerializer
.. autoclass:: asphalt.serialization.serializers.pickle.PickleSerializer
.. autoclass:: asphalt.serialization.serializers.yaml.YAMLSerializer
