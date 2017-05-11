from asphalt.core.context import Context
import pytest

from asphalt.serialization.api import Serializer
from asphalt.serialization.component import SerializationComponent
from asphalt.serialization.serializers.json import JSONSerializer


@pytest.mark.asyncio
async def test_component_start():
    component = SerializationComponent(serializers={
        'json': {'encoder_options': {'allow_nan': False}},
        'msgpack': {'unpacker_options': {'encoding': 'iso-8859-1'}},
        'pickle': {'protocol': 3},
        'yaml': {'safe': False}
    })
    async with Context() as ctx:
        await component.start(ctx)

        assert ctx.json
        assert ctx.msgpack
        assert ctx.pickle
        assert ctx.yaml


@pytest.mark.asyncio
async def test_default_config():
    component = SerializationComponent(backend='json')
    async with Context() as ctx:
        await component.start(ctx)

        resource = ctx.require_resource(Serializer)
        assert isinstance(resource, JSONSerializer)
        assert ctx.json is resource


@pytest.mark.asyncio
async def test_null_configs():
    component = SerializationComponent(serializers={
        'json': None,
        'msgpack': None,
        'pickle': None,
        'yaml': None
    })
    async with Context() as ctx:
        await component.start(ctx)

        assert ctx.json
        assert ctx.msgpack
        assert ctx.pickle
        assert ctx.yaml
