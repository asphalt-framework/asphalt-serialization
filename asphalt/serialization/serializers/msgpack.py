from typing import Dict, Any, Optional, Union, Tuple

from asphalt.core import resolve_reference
from msgpack import packb, unpackb, ExtType
from typeguard import check_argument_types

from asphalt.serialization.api import CustomizableSerializer
from asphalt.serialization.object_codec import DefaultCustomTypeCodec


class MsgpackTypeCodec(DefaultCustomTypeCodec):
    """
    Default custom type codec implementation for :class:`~.MsgpackSerializer`.

    Wraps marshalled state in either msgpack's ExtType objects (the default) or dicts (with
    ``type_code=None``).

    :param type_code: msgpack type code to use, or ``None`` to use JSON compatible dict-based
        wrapping
    """

    def __init__(self, type_code: Optional[int] = 119, **kwargs) -> None:
        assert check_argument_types()
        super().__init__(**kwargs)
        self.type_code = type_code

        if type_code:
            self.wrap_callback = self.wrap_state_ext_type
            self.unwrap_callback = self.unwrap_state_ext_type

    def register_object_decoder_hook(self, serializer: 'MsgpackSerializer') -> None:
        self.serializer = serializer
        serializer.packer_options['default'] = self.default_encoder

    def register_object_encoder_hook(self, serializer: 'MsgpackSerializer') -> None:
        self.serializer = serializer
        if self.type_code:
            serializer.unpacker_options['ext_hook'] = self.ext_hook
        else:
            serializer.unpacker_options['object_hook'] = self.default_decoder

    def ext_hook(self, code: int, data: bytes):
        if code == self.type_code:
            return self.default_decoder(data)
        else:
            return ExtType(code, data)

    def wrap_state_ext_type(self, typename: str, state):
        data = typename.encode('utf-8') + b':' + self.serializer.serialize(state)
        return ExtType(self.type_code, data)

    def unwrap_state_ext_type(
            self, wrapped_state: bytes) -> Union[Tuple[str, Any], Tuple[None, None]]:
        typename, payload = wrapped_state.split(b':', 1)
        return typename.decode('utf-8'), self.serializer.deserialize(payload)


class MsgpackSerializer(CustomizableSerializer):
    """
    Serializes objects using the msgpack library.

    The following defaults are passed to packer/unpacker and can be overridden by setting values
    for the options explicitly:

    * ``use_bin_type=True`` (packer)
    * ``raw=False`` (unpacker)

    To use this serializer backend, the ``msgpack`` library must be installed.
    A convenient way to do this is to install ``asphalt-serialization`` with the ``msgpack``
    extra:

    .. code-block:: shell

        $ pip install asphalt-serialization[msgpack]

    .. seealso:: `Msgpack web site <http://msgpack.org/>`_

    :param packer_options: keyword arguments passed to :func:`msgpack.packb`
    :param unpacker_options: keyword arguments passed to :func:`msgpack.unpackb`
    :param custom_type_codec: wrapper to use to wrap custom types after marshalling, or ``None`` to
        return marshalled objects as-is
    """

    __slots__ = ('packer_options', 'unpacker_options', 'custom_type_codec', '_marshallers',
                 '_unmarshallers')

    def __init__(
            self, packer_options: Dict[str, Any] = None, unpacker_options: Dict[str, Any] = None,
            custom_type_codec: Union[MsgpackTypeCodec, str] = None) -> None:
        assert check_argument_types()
        super().__init__(resolve_reference(custom_type_codec) or MsgpackTypeCodec())
        self.packer_options = packer_options or {}
        self.packer_options.setdefault('use_bin_type', True)
        self.unpacker_options = unpacker_options or {}
        self.unpacker_options.setdefault('raw', False)

    def serialize(self, obj) -> bytes:
        return packb(obj, **self.packer_options)

    def deserialize(self, payload: bytes):
        return unpackb(payload, **self.unpacker_options)

    @property
    def mimetype(self):
        return 'application/msgpack'
