import pytest
from asphalt.core import Context, get_resource, require_resource

from asphalt.serialization.api import CustomizableSerializer, Serializer
from asphalt.serialization.component import SerializationComponent
from asphalt.serialization.serializers.json import JSONSerializer
from asphalt.serialization.serializers.msgpack import MsgpackSerializer
from asphalt.serialization.serializers.pickle import PickleSerializer

pytestmark = pytest.mark.anyio


async def test_customizable_serializer() -> None:
    component = SerializationComponent(backend="json")
    async with Context():
        await component.start()

        resource = require_resource(Serializer)
        assert isinstance(resource, JSONSerializer)

        resource2 = require_resource(CustomizableSerializer)
        assert resource2 is resource

        resource3 = require_resource(JSONSerializer)
        assert resource3 is resource


async def test_non_customizable_serializer() -> None:
    component = SerializationComponent(backend="pickle")
    async with Context():
        await component.start()

        resource = require_resource(Serializer)
        assert isinstance(resource, PickleSerializer)

        assert not get_resource(CustomizableSerializer)

        resource2 = require_resource(PickleSerializer)
        assert resource2 is resource


async def test_resource_name() -> None:
    component = SerializationComponent(backend="msgpack", resource_name="alternate")
    async with Context():
        await component.start()

        resource = require_resource(Serializer, "alternate")
        assert isinstance(resource, MsgpackSerializer)

        resource2 = require_resource(CustomizableSerializer, "alternate")
        assert resource2 is resource

        resource3 = require_resource(MsgpackSerializer, "alternate")
        assert resource3 is resource
