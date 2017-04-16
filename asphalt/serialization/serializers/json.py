from json.decoder import JSONDecoder
from json.encoder import JSONEncoder
from typing import Dict, Any, Union

from typeguard import check_argument_types

from asphalt.core import resolve_reference
from asphalt.serialization.api import CustomizableSerializer
from asphalt.serialization.object_codec import DefaultCustomTypeCodec


class JSONTypeCodec(DefaultCustomTypeCodec):
    """Default state wrapper implementation for :class:`~.JSONSerializer`."""

    def register_object_encoder_hook(self, serializer: 'JSONSerializer') -> None:
        self.serializer = serializer
        serializer.encoder_options['default'] = self.default_encoder
        serializer._encoder = JSONEncoder(**serializer.encoder_options)

    def register_object_decoder_hook(self, serializer: 'JSONSerializer') -> None:
        self.serializer = serializer
        serializer.decoder_options['object_hook'] = self.default_decoder
        serializer.decoder_options.pop('object_pairs_hook', None)
        serializer._decoder = JSONDecoder(**serializer.decoder_options)


class JSONSerializer(CustomizableSerializer):
    """
    Serializes objects using JSON (JavaScript Object Notation).

    See the :mod:`json` module documentation in the standard library for more information on
    available options.

    Certain options can resolve references to objects:

    * ``encoder_options['default']``
    * ``decoder_options['object_hook']``
    * ``decoder_options['object_pairs_hook']``

    :param encoder_options: keyword arguments passed to :class:`~json.JSONEncoder`
    :param decoder_options: keyword arguments passed to :class:`~json.JSONDecoder`
    :param encoding: the text encoding to use for converting to and from bytes
    :param custom_type_codec: wrapper to use to wrap custom types after marshalling
    """

    __slots__ = ('encoder_options', 'decoder_options', 'encoding', 'custom_type_codec',
                 '_encoder', '_decoder', '_marshallers', '_unmarshallers')

    def __init__(self, encoder_options: Dict[str, Any] = None,
                 decoder_options: Dict[str, Any] = None, encoding: str = 'utf-8',
                 custom_type_codec: Union[JSONTypeCodec, str] = None):
        assert check_argument_types()
        super().__init__(resolve_reference(custom_type_codec) or JSONTypeCodec())
        self.encoding = encoding

        self.encoder_options = encoder_options or {}
        self.encoder_options['default'] = resolve_reference(self.encoder_options.get('default'))
        self._encoder = JSONEncoder(**self.encoder_options)

        self.decoder_options = decoder_options or {}
        self.decoder_options['object_hook'] = resolve_reference(
            self.decoder_options.get('object_hook'))
        self.decoder_options['object_pairs_hook'] = resolve_reference(
            self.decoder_options.get('object_pairs_hook'))
        self._decoder = JSONDecoder(**self.decoder_options)

    def serialize(self, obj) -> bytes:
        return self._encoder.encode(obj).encode(self.encoding)

    def deserialize(self, payload: bytes):
        payload = payload.decode(self.encoding)
        return self._decoder.decode(payload)

    @property
    def mimetype(self):
        return 'application/json'
