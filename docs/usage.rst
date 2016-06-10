Using serializers
=================

Using serializers is quite straightforward::

    async def handler(ctx):
        payload = ctx.json.serialize({'foo': 'example JSON object'})
        original = ctx.json.deserialize(payload)  # {'foo': 'example JSON object'}

This example assumes a configuration where a JSON serializer is present as ``ctx.json``.

To see what Python types can be serialized by every serializer, consult the documentation of the
abstract :class:`~asphalt.serialization.api.Serializer` class.


Registering custom objects with serializers
-------------------------------------------

An application may sometimes need to send instances of classes over the wire that are not normally
handled by the chosen serializer. In order to do that, a process called *marshalling* is used to
reduce the object to something naturally serializable by the serializer. Conversely, the process
of restoring the original object from a naturally serializable object is called *unmarshalling*.
So marshalling happens before serialization and unmarshalling happens after deserialization.

The ``pickle`` serializer automatically serializes the ``__dict__`` of an object, or calls
``__getstate__()`` to obtain the information. This, however, comes at the cost of a major security
problem, because pickle's deserializer can be made to execute any arbitrary code.

A better way is to use one of the ``cbor``, ``msgpack`` or ``json`` serializers and register each
type intended for serialization using
:meth:`~asphalt.serialization.api.CustomizableSerializer.register_custom_type`. This method lets
the user register marshalling/unmarshalling functions that are called whenever the serializer
encounters an instance of the registered type, or when the deserializer needs to reconstitute an
object of that type using the state object previously returned by the marshaller callback.

The default marshalling callback mimics pickle's behavior by returning the ``__dict__`` of an
object or by calling its ``__getstate__()`` method. Likewise, the default unmarshalling callback
calls ``__setstate__()`` with the state object, or simply sets the ``__dict__`` of an empty
instance of the registered class.

Rather than blindly serializing every attribute in the object, you could set up your custom
marshalling/unmarshalling callbacks::

    from datetime import datetime

    from asphalt.serialization.serializers.json import JSONSerializer


    class User(object):
        def __init__(self, name, email, password):
            self.name = name
            self.email = email
            self.password = password
            self.created_at = datetime.now()

        def marshal(self):
            # Omit the "password" and "created_at" attributes
            return {
                'name': self.name,
                'email': self.email
            }

        @classmethod
        def unmarshal(cls, state):
            state['password'] = None
            return cls(**state)

    serializer = JSONSerializer()
    serializer.register_custom_type(User, User.marshal, User.unmarshal)

.. hint:: If a component depends on the ability to register custom types, it can request a resource
 of type :class:`~asphalt.serialization.api.CustomizableSerializer` instead of
 :class:`~asphalt.serialization.api.Serializer`.

Integrating with a third party marshaller
-----------------------------------------

If you want, you can use a third party object marshalling framework, such as marshmallow_, to
handle the marshalling. Here is a simple example that demonstrates how to hook up schema of a
class to the serializer::

    from datetime import date

    from asphalt.serialization.serializers.json import JSONSerializer
    from marshmallow import Schema, fields
    from marshmallow.decorators import post_load


    class User(object):
        def __init__(self, name, email, created_at=None):
            self.name = name
            self.email = email
            self.created_at = created_at or date.today()


    class UserSchema(Schema):
        name = fields.Str()
        email = fields.Email()
        created_at = fields.DateTime()

        @post_load
        def make_user(self, data):
            return User(**data)

    schema = UserSchema()
    serializer = JSONSerializer()
    serializer.register_custom_type(User, lambda obj: schema.dump(obj).data,
                                    lambda state: schema.load(state).data)

Now you can happily serialize any User object and it all goes through ``UserSchema``::

    user = User('Test person', 'test@example.org')
    data = serializer.serialize(user)
    user2 = serializer.deserialize(data)
    assert user2.created_at == user.created_at


.. _marshmallow: http://marshmallow.readthedocs.io/en/latest/
