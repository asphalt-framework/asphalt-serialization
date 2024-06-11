import pytest
from asphalt.core import Context, get_resource_nowait, start_component

from asphalt.serialization import (
    CustomizableSerializer,
    SerializationComponent,
    Serializer,
)
from asphalt.serialization.serializers.json import JSONSerializer
from asphalt.serialization.serializers.msgpack import MsgpackSerializer
from asphalt.serialization.serializers.pickle import PickleSerializer

pytestmark = pytest.mark.anyio


async def test_customizable_serializer() -> None:
    async with Context():
        await start_component(SerializationComponent, {"backend": "json"})

        resource = get_resource_nowait(Serializer)
        assert isinstance(resource, JSONSerializer)

        resource2 = get_resource_nowait(CustomizableSerializer)
        assert resource2 is resource

        resource3 = get_resource_nowait(JSONSerializer)
        assert resource3 is resource


async def test_non_customizable_serializer() -> None:
    async with Context():
        await start_component(SerializationComponent, {"backend": "pickle"})

        resource = get_resource_nowait(Serializer)
        assert isinstance(resource, PickleSerializer)

        assert not get_resource_nowait(CustomizableSerializer, optional=True)

        resource2 = get_resource_nowait(PickleSerializer)
        assert resource2 is resource


async def test_resource_name() -> None:
    async with Context():
        await start_component(
            SerializationComponent, {"backend": "msgpack", "resource_name": "alternate"}
        )

        resource = get_resource_nowait(Serializer, "alternate")
        assert isinstance(resource, MsgpackSerializer)

        resource2 = get_resource_nowait(CustomizableSerializer, "alternate")
        assert resource2 is resource

        resource3 = get_resource_nowait(MsgpackSerializer, "alternate")
        assert resource3 is resource
