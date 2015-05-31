Using serializers
=================

Using serializers is quite straightforward:

.. code:: python

    def handler(ctx):
        payload = ctx.json.serialize({'foo': 'example JSON object'})
        original = ctx.json.deserialize(payload)  # {'foo': 'example JSON object'}

This example assumes the default configuration, in which ``ctx.json`` is a JSON serializer.

To see what Python types can be serialized by every serializer, consult the documentation of the
abstract :class:`~asphalt.serialization.api.Serializer` class.
