from __future__ import annotations

from json.decoder import JSONDecoder
from json.encoder import JSONEncoder
from typing import Any

from asphalt.core import resolve_reference

from ..api import CustomizableSerializer
from ..object_codec import DefaultCustomTypeCodec


class JSONTypeCodec(DefaultCustomTypeCodec["JSONSerializer"]):
    """Default state wrapper implementation for :class:`~.JSONSerializer`."""

    def register_object_encoder_hook(self, serializer: JSONSerializer) -> None:
        self.serializer = serializer
        serializer.encoder_options["default"] = self.default_encoder
        serializer._encoder = JSONEncoder(**serializer.encoder_options)

    def register_object_decoder_hook(self, serializer: JSONSerializer) -> None:
        self.serializer = serializer
        serializer.decoder_options["object_hook"] = self.default_decoder
        serializer.decoder_options.pop("object_pairs_hook", None)
        serializer._decoder = JSONDecoder(**serializer.decoder_options)


class JSONSerializer(CustomizableSerializer):
    """
    Serializes objects using JSON (JavaScript Object Notation).

    See the :mod:`json` module documentation in the standard library for more
    information on available options.

    Certain options can resolve references to objects:

    * ``encoder_options['default']``
    * ``decoder_options['object_hook']``
    * ``decoder_options['object_pairs_hook']``

    :param encoder_options: keyword arguments passed to :class:`~json.JSONEncoder`
    :param decoder_options: keyword arguments passed to :class:`~json.JSONDecoder`
    :param encoding: the text encoding to use for converting to and from bytes
    :param custom_type_codec: wrapper to use to wrap custom types after marshalling
    """

    __slots__ = (
        "encoder_options",
        "decoder_options",
        "encoding",
        "custom_type_codec",
        "_encoder",
        "_decoder",
        "_marshallers",
        "_unmarshallers",
    )

    def __init__(
        self,
        encoder_options: dict[str, Any] | None = None,
        decoder_options: dict[str, Any] | None = None,
        encoding: str = "utf-8",
        custom_type_codec: JSONTypeCodec | str | None = None,
    ):
        super().__init__(resolve_reference(custom_type_codec) or JSONTypeCodec())
        self.encoding: str = encoding

        self.encoder_options: dict[str, Any] = encoder_options or {}
        self.encoder_options["default"] = resolve_reference(
            self.encoder_options.get("default")
        )
        self._encoder = JSONEncoder(**self.encoder_options)

        self.decoder_options: dict[str, Any] = decoder_options or {}
        self.decoder_options["object_hook"] = resolve_reference(
            self.decoder_options.get("object_hook")
        )
        self.decoder_options["object_pairs_hook"] = resolve_reference(
            self.decoder_options.get("object_pairs_hook")
        )
        self._decoder = JSONDecoder(**self.decoder_options)

    def serialize(self, obj: Any) -> bytes:
        return self._encoder.encode(obj).encode(self.encoding)

    def deserialize(self, payload: bytes) -> Any:
        text_payload = payload.decode(self.encoding)
        return self._decoder.decode(text_payload)

    @property
    def mimetype(self) -> str:
        return "application/json"
