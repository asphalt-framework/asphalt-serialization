from __future__ import annotations

import pickle
from typing import Any

from ..api import Serializer


class PickleSerializer(Serializer):
    """
    Serializes objects using the standard library :mod:`pickle` module.

    .. warning:: This serializer is insecure because it allows execution of arbitrary
        code when deserializing. Avoid using this if at all possible.

    :param protocol: pickle protocol level to use (defaults to the highest possible)
    """

    __slots__ = "protocol"

    def __init__(self, protocol: int = pickle.HIGHEST_PROTOCOL):
        assert (
            0 <= protocol <= pickle.HIGHEST_PROTOCOL
        ), f'"protocol" must be between 0 and {pickle.HIGHEST_PROTOCOL}'

        self.protocol: int = protocol

    def serialize(self, obj: Any) -> bytes:
        return pickle.dumps(obj, protocol=self.protocol)

    def deserialize(self, payload: bytes) -> Any:
        return pickle.loads(payload)

    @property
    def mimetype(self) -> str:
        return "application/python-pickle"
