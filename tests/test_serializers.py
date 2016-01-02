import re

import pytest

from asphalt.serialization.serializers.cbor import CBORSerializer
from asphalt.serialization.serializers.json import JSONSerializer
from asphalt.serialization.serializers.msgpack import MsgpackSerializer
from asphalt.serialization.serializers.pickle import PickleSerializer
from asphalt.serialization.serializers.yaml import YAMLSerializer


@pytest.fixture(params=[
    CBORSerializer,
    JSONSerializer,
    MsgpackSerializer,
    PickleSerializer,
    YAMLSerializer
], ids=['cbor', 'json', 'msgpack', 'pickle', 'yaml'])
def serializer(request):
    return request.param()


@pytest.mark.parametrize('input', [
    'åäö',
    -8,
    5.06,
    [1, 'test', 1.23],
    {'x': 'foo', 'bar': 'baz'}
], ids=['str', 'int', 'float', 'list', 'dict'])
def test_basic_types_roundtrip(serializer, input):
    output = serializer.serialize(input)
    assert isinstance(output, bytes)

    deserialized = serializer.deserialize(output)
    assert deserialized == input


@pytest.mark.parametrize('serializer', [PickleSerializer(), YAMLSerializer()],
                         ids=['pickle', 'yaml'])
def test_circular_reference(serializer):
    a = {'foo': 1}
    b = {'a': a}
    a['b'] = b

    output = serializer.serialize(a)
    assert isinstance(output, bytes)

    other_a = serializer.deserialize(output)
    assert other_a['foo'] == 1
    other_b = other_a['b']
    assert other_b['a'] is other_a


def test_mime_types(serializer):
    assert re.match('[a-z]+/[a-z]+', serializer.mimetype)


@pytest.mark.parametrize('safe', [True, False], ids=['safe', 'unsafe'])
def test_yaml_safe_attribute(safe):
    serializer = YAMLSerializer(safe=safe)
    assert serializer.safe is safe
