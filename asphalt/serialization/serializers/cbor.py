from typing import Dict, Any, Optional, Union

import cbor2
from asphalt.core import qualified_name, resolve_reference
from typeguard import check_argument_types

from asphalt.serialization.api import CustomizableSerializer
from asphalt.serialization.object_codec import DefaultCustomTypeCodec


class CBORTypeCodec(DefaultCustomTypeCodec):
    """
    Default custom type codec implementation for :class:`~.CBORSerializer`.

    Wraps marshalled state in either CBORTag objects (the default) or dicts (with
    ``type_tag=None``).

    :param type_tag: CBOR tag number to use, or ``None`` to use JSON compatible dict-based
        wrapping

    .. note:: Custom wrapping hooks are ignored when CBORTags are used.
    """

    def __init__(self, type_tag: Optional[int] = 4554, **kwargs):
        super().__init__(**kwargs)
        self.type_tag = type_tag

    def register_object_encoder_hook(self, serializer: 'CBORSerializer') -> None:
        self.serializer = serializer
        if self.type_tag:
            serializer.encoder_options['default'] = cbor2.shareable_encoder(self.cbor_tag_encoder)
        else:
            serializer.encoder_options['default'] = self.cbor_default_encoder

    def register_object_decoder_hook(self, serializer: 'CBORSerializer') -> None:
        self.serializer = serializer
        if self.type_tag:
            serializer.decoder_options['tag_hook'] = self.cbor_tag_decoder
        else:
            serializer.decoder_options['object_hook'] = self.cbor_default_decoder

    def cbor_tag_encoder(self, encoder: cbor2.CBOREncoder, obj):
        try:
            typename, marshaller, wrap_state = self.serializer.marshallers[obj.__class__]
        except KeyError:
            raise LookupError('no marshaller found for type "{}"'
                              .format(qualified_name(type(obj)))) from None

        marshalled_state = marshaller(obj)
        if wrap_state:
            serialized_state = encoder.encode_to_bytes(marshalled_state)
            wrapped_state = [typename, serialized_state]
            with encoder.disable_value_sharing():
                encoder.encode(cbor2.CBORTag(self.type_tag, wrapped_state))
        else:
            encoder.encode(marshalled_state)

    def cbor_tag_decoder(self, decoder: cbor2.CBORDecoder, tag: cbor2.CBORTag,
                         shareable_index: int = None):
        if tag.tag != self.type_tag:
            return tag

        typename, serialized_state = tag.value
        try:
            cls, unmarshaller = self.serializer.unmarshallers[typename]
        except KeyError:
            raise LookupError('no unmarshaller found for type "{}"'.format(typename)) from None

        if cls is not None:
            instance = cls.__new__(cls)
            decoder.set_shareable(shareable_index, instance)
            marshalled_state = decoder.decode_from_bytes(serialized_state)
            unmarshaller(instance, marshalled_state)
            return instance
        else:
            marshalled_state = decoder.decode_from_bytes(serialized_state)
            return unmarshaller(marshalled_state)

    def cbor_default_encoder(self, encoder: cbor2.CBOREncoder, obj):
        encoded = self.default_encoder(obj)
        encoder.encode(encoded)

    def cbor_default_decoder(self, decoder: cbor2.CBORDecoder, obj):
        return self.default_decoder(obj)


class CBORSerializer(CustomizableSerializer):
    """
    Serializes objects using CBOR (Concise Binary Object Representation).

    To use this serializer backend, the ``cbor2`` library must be installed.
    A convenient way to do this is to install ``asphalt-serialization`` with the ``cbor`` extra:

    .. code-block:: shell

        $ pip install asphalt-serialization[cbor]

    .. seealso:: `cbor2 documentation <https://pypi.io/project/cbor2/>`_

    :param encoder_options: keyword arguments passed to ``cbor2.dumps()``
    :param decoder_options: keyword arguments passed to ``cbor2.loads()``
    :param custom_type_codec: wrapper to use to wrap custom types after marshalling, or ``None`` to
        return marshalled objects as-is
    """

    __slots__ = ('encoder_options', 'decoder_options', 'custom_type_codec', 'marshallers',
                 'unmarshallers')

    def __init__(self, encoder_options: Dict[str, Any] = None,
                 decoder_options: Dict[str, Any] = None,
                 custom_type_codec: Union[CBORTypeCodec, str] = None):
        assert check_argument_types()
        super().__init__(resolve_reference(custom_type_codec) or CBORTypeCodec())
        self.encoder_options = encoder_options or {}
        self.decoder_options = decoder_options or {}

    def serialize(self, obj) -> bytes:
        return cbor2.dumps(obj, **self.encoder_options)

    def deserialize(self, payload: bytes):
        return cbor2.loads(payload, **self.decoder_options)

    @property
    def mimetype(self):
        return 'application/cbor'
