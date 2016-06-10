from collections import OrderedDict
from functools import partial
from typing import Dict, Any, Callable, Union

import cbor2
from asphalt.core.util import qualified_name
from typeguard import check_argument_types

from asphalt.serialization.api import CustomizableSerializer
from asphalt.serialization.marshalling import default_marshaller, default_unmarshaller


class CBORSerializer(CustomizableSerializer):
    """
    Serializes objects using CBOR (Concise Binary Object Representation).

    To use this serializer backend, the ``cbor2`` library must be installed.
    A convenient way to do this is to install ``asphalt-serialization`` with the ``cbor``
    extra:

    .. code-block:: shell

        $ pip install asphalt-serialization[cbor]

    .. seealso:: `cbor2 documentation <https://pypi.io/project/cbor2/>`_

    :param encoder_options: keyword arguments passed to ``cbor2.dumps()``
    :param decoder_options: keyword arguments passed to ``cbor2.loads()``
    :param custom_type_tag: semantic tag used for marshalling of registered custom types
    """

    __slots__ = ('encoder_options', 'decoder_options', 'custom_type_tag', '_marshallers',
                 '_unmarshallers')

    def __init__(self, encoder_options: Dict[str, Any] = None,
                 decoder_options: Dict[str, Any] = None, custom_type_tag: int = 4554):
        assert check_argument_types()
        self.encoder_options = encoder_options or {}
        self.decoder_options = decoder_options or {}
        self.custom_type_tag = custom_type_tag
        self._marshallers = OrderedDict()  # class -> (typename, marshaller function)
        self._unmarshallers = OrderedDict()  # typename -> (class, unmarshaller function)

    def serialize(self, obj) -> bytes:
        return cbor2.dumps(obj, **self.encoder_options)

    def deserialize(self, payload: bytes):
        return cbor2.loads(payload, **self.decoder_options)

    def register_custom_type(
            self, cls: type, marshaller: Union[Callable[[Any], Any], bool] = True,
            unmarshaller: Union[Callable[[Any], Any], bool] = True, *,
            typename: str = None) -> None:
        assert check_argument_types()
        typename = typename or qualified_name(cls)

        if marshaller:
            if isinstance(marshaller, bool):
                marshaller = default_marshaller

            self._marshallers[cls] = typename, marshaller
            encoders = self.encoder_options.setdefault('encoders', {})
            encoders[cls] = self._encode_custom_type

        if unmarshaller:
            if isinstance(unmarshaller, bool):
                unmarshaller = partial(default_unmarshaller, cls=cls)

            self._unmarshallers[typename] = cls, unmarshaller
            decoders = self.decoder_options.setdefault('semantic_decoders', {})
            decoders[self.custom_type_tag] = self._decode_custom_type

    def _encode_custom_type(self, encoder, obj):
        obj_type = obj.__class__
        typename, marshaller = self._marshallers[obj_type]
        state = marshaller(obj)
        return encoder.encode_semantic(self.custom_type_tag, [typename, state])

    def _decode_custom_type(self, decoder, value):
        typename, state = value
        try:
            cls, unmarshaller = self._unmarshallers[typename]
        except KeyError:
            raise LookupError('no unmarshaller found for type "{}"'.format(typename)) from None

        return unmarshaller(state)

    @property
    def mimetype(self):
        return 'application/cbor'
