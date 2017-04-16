from abc import ABCMeta, abstractmethod
from inspect import signature
from typing import Callable, Any, Optional, Union, Dict  # noqa

from typeguard import check_argument_types, qualified_name

from asphalt.serialization.marshalling import default_marshaller, default_unmarshaller


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

    :ivar marshallers: a mapping of class -> (typename, marshaller callback)
    :vartype marshallers: Dict[str, Callable]
    :ivar unmarshallers: a mapping of class -> (typename, unmarshaller callback)
    :vartype unmarshallers: Dict[str, Callable]
    """

    __slots__ = ('custom_type_codec', 'marshallers', 'unmarshallers')

    def __init__(self, custom_type_codec: 'CustomTypeCodec'):
        self.custom_type_codec = custom_type_codec
        self.marshallers = {}  # type: Dict[str, Callable]
        self.unmarshallers = {}  # type: Dict[str, Callable]

    def register_custom_type(
            self, cls: type, marshaller: Optional[Callable[[Any], Any]] = default_marshaller,
            unmarshaller: Union[Callable[[Any, Any], None],
                                Callable[[Any], Any], None] = default_unmarshaller, *,
            typename: str = None, wrap_state: bool = True) -> None:
        """
        Register a marshaller and/or unmarshaller for the given class.

        The state object returned by the marshaller and passed to the unmarshaller can be any
        serializable type. Usually a dictionary mapping of attribute names to values is used.

        .. warning:: Registering marshallers/unmarshallers for any custom type will override any
            serializer specific encoding/decoding hooks (respectively) already in place!

        :param cls: the class to register
        :param marshaller: a callable that takes the object to be marshalled as the argument and
              returns a state object
        :param unmarshaller: a callable that either:

            * takes an uninitialized instance of ``cls`` and its state object as arguments and
              restores the state of the object
            * takes a state object and returns a new instance of ``cls``
        :param typename: a unique identifier for the type (defaults to the ``module:varname``
            reference to the class)
        :param wrap_state: ``True`` to wrap the marshalled state before serialization so that it
            can be recognized later for unmarshalling, ``False`` to serialize it as is

        """
        assert check_argument_types()
        typename = typename or qualified_name(cls)

        if marshaller:
            self.marshallers[cls] = typename, marshaller, wrap_state
            self.custom_type_codec.register_object_encoder_hook(self)

        if unmarshaller and self.custom_type_codec is not None:
            if len(signature(unmarshaller).parameters) == 1:
                cls = None

            self.unmarshallers[typename] = cls, unmarshaller
            self.custom_type_codec.register_object_decoder_hook(self)


class CustomTypeCodec(metaclass=ABCMeta):
    """Interface for customizing how custom types are encoded and decoded."""

    @abstractmethod
    def register_object_encoder_hook(self, serializer: CustomizableSerializer) -> None:
        """
        Register a custom encoder callback on the serializer.

        This callback would be called when the serializer encounters an object it cannot natively
        serialize. What the callback returns is specific to each serializer type.

        :param serializer: the serializer instance to use
        """

    @abstractmethod
    def register_object_decoder_hook(self, serializer: CustomizableSerializer) -> None:
        """
        Register a callback on the serializer for unmarshalling previously marshalled objects.

        :param serializer: the serializer instance to use
        """
