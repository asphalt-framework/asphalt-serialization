from asphalt.core.context import Context
import pytest

from asphalt.serialization.api import Serializer
from asphalt.serialization.component import SerializationComponent
from asphalt.serialization.serializers.json import JSONSerializer


@pytest.mark.asyncio
def test_component_start():
    component = SerializationComponent(serializers={
        'json': {'encoder_options': {'allow_nan': False}},
        'msgpack': {'unpacker_options': {'encoding': 'iso-8859-1'}},
        'pickle': {'protocol': 3},
        'yaml': {'safe': False}
    })
    ctx = Context()
    yield from component.start(ctx)

    assert ctx.json
    assert ctx.msgpack
    assert ctx.pickle
    assert ctx.yaml


@pytest.mark.asyncio
def test_default_config():
    component = SerializationComponent()
    ctx = Context()
    yield from component.start(ctx)

    resource = yield from ctx.request_resource(Serializer)
    assert isinstance(resource, JSONSerializer)
    assert ctx.json is resource


def test_conflicting_config():
    exc = pytest.raises(ValueError, SerializationComponent, serializers={'default': {}},
                        type='json')
    assert str(exc.value) == ('specify either a "serializers" dictionary or the default '
                              'serializer\'s options directly, but not both')
