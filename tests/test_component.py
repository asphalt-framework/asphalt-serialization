import pytest
from asphalt.core.context import Context

from asphalt.serialization.api import CustomizableSerializer, Serializer
from asphalt.serialization.component import SerializationComponent
from asphalt.serialization.serializers.json import JSONSerializer
from asphalt.serialization.serializers.msgpack import MsgpackSerializer


@pytest.mark.asyncio
async def test_component_start() -> None:
    component = SerializationComponent(backend="json")
    async with Context() as ctx:
        await component.start(ctx)

        resource = ctx.require_resource(Serializer)
        assert isinstance(resource, JSONSerializer)

        resource2 = ctx.require_resource(CustomizableSerializer)
        assert resource2 is resource

        resource3 = ctx.require_resource(JSONSerializer)
        assert resource3 is resource


@pytest.mark.asyncio
async def test_resource_name() -> None:
    component = SerializationComponent(backend="msgpack", resource_name="alternate")
    async with Context() as ctx:
        await component.start(ctx)

        resource = ctx.require_resource(Serializer, "alternate")
        assert isinstance(resource, MsgpackSerializer)

        resource2 = ctx.require_resource(CustomizableSerializer, "alternate")
        assert resource2 is resource

        resource3 = ctx.require_resource(MsgpackSerializer, "alternate")
        assert resource3 is resource
