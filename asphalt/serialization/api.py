from abc import ABCMeta, abstractmethod


class Serializer(metaclass=ABCMeta):
    """
    This abstract class defines the serializer API.

    Each serializer is required to support the serialization of the following Python types,
    at minimum:

    * :class:`str`
    * :class:`int`
    * :class:`float`
    * :class:`list`
    * :class:`dict` (with ``str`` keys)

    A subclass may support a wider range of types, along with hooks to provide serialization
    support for custom types.
    """

    __slots__ = ()

    @abstractmethod
    def serialize(self, obj) -> bytes:
        """Serialize a Python object into bytes."""

    @abstractmethod
    def deserialize(self, payload: bytes):
        """Deserialize bytes into a Python object."""

    @property
    @abstractmethod
    def mimetype(self) -> str:
        """Return the MIME type for this serialization format."""
