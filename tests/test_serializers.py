import re
from types import SimpleNamespace

import pytest
from msgpack import ExtType

from asphalt.serialization.serializers.cbor import CBORSerializer
from asphalt.serialization.serializers.json import JSONSerializer
from asphalt.serialization.serializers.msgpack import MsgpackSerializer
from asphalt.serialization.serializers.pickle import PickleSerializer
from asphalt.serialization.serializers.yaml import YAMLSerializer


class SimpleType:
    def __init__(self, value_a, value_b):
        self.value_a = value_a
        self.value_b = value_b

    def __eq__(self, other):
        if isinstance(other, SimpleType):
            return other.value_a == self.value_a and other.value_b == self.value_b
        return NotImplemented


class SlottedSimpleType:
    __slots__ = 'value_a', 'value_b'

    def __init__(self, value_a, value_b):
        self.value_a = value_a
        self.value_b = value_b

    def __getstate__(self):
        return {'value_a': self.value_a, 'value_b': self.value_b}

    def __setstate__(self, state):
        self.value_a = state['value_a']
        self.value_b = state['value_b']

    def __eq__(self, other):
        if isinstance(other, SlottedSimpleType):
            return other.value_a == self.value_a and other.value_b == self.value_b
        return NotImplemented


class CustomStateSimpleType(SimpleType):
    def unmarshal(self, state):
        self.value_a, self.value_b = state

    def marshal(self):
        return self.value_a, self.value_b


class UnserializableSimpleType:
    __slots__ = 'value_a', 'value_b'

    def __init__(self, value_a, value_b):
        self.value_a = value_a
        self.value_b = value_b


@pytest.fixture(params=['cbor', 'json', 'msgpack', 'pickle', 'yaml'])
def serializer_type(request):
    return request.param


@pytest.fixture
def serializer(serializer_type):
    return {
        'cbor': CBORSerializer,
        'json': JSONSerializer,
        'msgpack': MsgpackSerializer,
        'pickle': PickleSerializer,
        'yaml': YAMLSerializer
    }[serializer_type]()


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


@pytest.mark.parametrize('serializer_type', ['cbor', 'pickle', 'yaml'])
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


@pytest.mark.parametrize('serializer_type', ['cbor', 'msgpack', 'json'])
class TestCustomTypes:
    @pytest.mark.parametrize('cls', [SimpleType, SlottedSimpleType], ids=['normal', 'slotted'])
    def test_marshal_unmarshal(self, serializer, cls):
        serializer.register_custom_type(cls)
        testval = cls(1, {'a': 1})
        testval2 = cls(2, testval)
        output = serializer.serialize(testval2)
        outval = serializer.deserialize(output)
        assert outval == testval2

    def test_custom_state(self, serializer):
        """Test that marshallers and umarshallers can be embedded into the relevant class."""
        serializer.register_custom_type(CustomStateSimpleType, CustomStateSimpleType.marshal,
                                        CustomStateSimpleType.unmarshal)
        testval = CustomStateSimpleType('a', 1)
        output = serializer.serialize(testval)
        outval = serializer.deserialize(output)
        assert outval == testval

    def test_missing_getattr(self, serializer):
        testval = UnserializableSimpleType(1, 'a')
        serializer.register_custom_type(UnserializableSimpleType)
        exc = pytest.raises(TypeError, serializer.serialize, testval)
        assert str(exc.value) == ("'test_serializers.UnserializableSimpleType' has no __dict__ "
                                  "attribute and does not implement __getstate__()")

    def test_missing_setattr(self, serializer):
        testval = UnserializableSimpleType(1, 'a')
        serializer.register_custom_type(UnserializableSimpleType, lambda instance: {})
        serialized = serializer.serialize(testval)
        exc = pytest.raises(Exception, serializer.deserialize, serialized)
        assert str(exc.value).endswith(
            "'test_serializers.UnserializableSimpleType' has no __dict__ attribute and does not "
            "implement __setstate__()")

    def test_missing_marshaller(self, serializer_type, serializer):
        serializer.register_custom_type(SlottedSimpleType)
        testval = SimpleType(1, 'a')
        exc = pytest.raises(Exception, serializer.serialize, testval)
        if serializer_type == 'cbor':
            assert str(exc.value).endswith('cannot serialize type SimpleType')
        else:
            assert str(exc.value) == 'no marshaller found for type "test_serializers.SimpleType"'

    def test_missing_unmarshaller(self, serializer):
        serializer.register_custom_type(SlottedSimpleType)
        serializer.register_custom_type(SimpleType, unmarshaller=None)
        testval = SimpleType(1, 'a')
        serialized = serializer.serialize(testval)
        exc = pytest.raises(Exception, serializer.deserialize, serialized)
        assert str(exc.value).endswith(
            'no unmarshaller found for type "test_serializers.SimpleType"')


def test_mime_types(serializer):
    assert re.match('[a-z]+/[a-z]+', serializer.mimetype)


@pytest.mark.parametrize('safe', [True, False], ids=['safe', 'unsafe'])
def test_yaml_safe_attribute(safe):
    serializer = YAMLSerializer(safe=safe)
    assert serializer.safe is safe


@pytest.mark.parametrize('serializer_type', ['msgpack'])
def test_msgpack_exttype_passthrough(serializer):
    serializer.register_custom_type(SlottedSimpleType)
    ext = ExtType(6, b'somedata')
    data = serializer.serialize(ext)
    obj = serializer.deserialize(data)
    assert isinstance(obj, ExtType)
    assert obj.code == 6
    assert obj.data == b'somedata'


@pytest.mark.parametrize('serializer_type', ['cbor'])
def test_cbor_self_referential_objects(serializer):
    value1 = SimpleNamespace()
    value1.val = 1
    value1.next = value2 = SimpleNamespace()
    value2.val = 2
    value2.previous = value1

    serializer.register_custom_type(SimpleNamespace, typename='Simple')
    data = serializer.serialize(value1)
    obj = serializer.deserialize(data)
    assert obj.val == 1
    assert obj.next.val == 2
    assert obj.next.previous is obj
