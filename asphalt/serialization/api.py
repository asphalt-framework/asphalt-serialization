from abc import ABCMeta, abstractmethod
from typing import Callable, Any, Union


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


class CustomizableSerializer(Serializer):
    """
    This abstract class defines an interface for registering custom types on a serializer so that
    the the serializer can be extended to (de)serialize a broader array of classes.
    """

    @abstractmethod
    def register_custom_type(
            self, cls: type, marshaller: Union[Callable[[Any], Any], bool] = True,
            unmarshaller: Union[Callable[[Any], Any], bool] = True, *,
            typename: str = None) -> None:
        """
        Register a marshaller and/or unmarshaller for the given class.

        The state object returned by the marshaller and passed to the unmarshaller can be any
        serializable type. Usually a dictionary mapping of attribute names to values is used.

        :param cls: the class to register
        :param marshaller: either:
            * a callable that takes the object to be marshalled as the argument and
              returns a state object
            * ``True``, which means that the default marshaller should be used
            * ``False``, which means that no marshaller should be registered
        :param unmarshaller: either:
            * a callable that takes the state object as argument and returns the unmarshalled
              object
            * ``True``, which means that the default unmarshaller should be used
            * ``False``, which means that no unmarshaller should be registered
        :param typename: a unique identifier for the type (defaults to the ``module:varname``
            reference to the class)

        .. warning:: Registering any custom types will override any encoding/decoding hooks already
            in place!
        """
