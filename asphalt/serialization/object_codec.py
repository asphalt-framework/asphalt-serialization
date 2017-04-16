from typing import Callable, Any, Dict, Tuple, Union  # noqa

from asphalt.core import qualified_name
from typeguard import check_argument_types

from asphalt.serialization.api import CustomTypeCodec, CustomizableSerializer  # noqa


class DefaultCustomTypeCodec(CustomTypeCodec):
    """
    Provides default wrappers for implementing :class:`~asphalt.serialization.api.CustomTypeCodec`.

    :ivar CustomizableSerializer serializer: the associated serializer

    :param type_key: dict key for the type name
    :param state_key dict key for the marshalled state
    """

    def __init__(self, type_key: str = '__type__', state_key: str = 'state'):
        assert check_argument_types()
        self.type_key = type_key
        self.state_key = state_key
        self.serializer = None  # type: CustomizableSerializer
        self.wrap_callback = self.wrap_state_dict  # type: Callable[[str, Any], Any]
        self.unwrap_callback = self.unwrap_state_dict  # type: Callable[[Any], Any]

    def default_encoder(self, obj):
        obj_type = obj.__class__
        try:
            typename, marshaller, wrap_state = self.serializer.marshallers[obj_type]
        except KeyError:
            raise LookupError('no marshaller found for type "{}"'
                              .format(qualified_name(obj_type))) from None

        state = marshaller(obj)
        return self.wrap_callback(typename, state) if wrap_state else state

    def default_decoder(self, obj):
        """Handle a dict that might contain a wrapped state for a custom type."""
        typename, marshalled_state = self.unwrap_callback(obj)
        if typename is None:
            return obj

        try:
            cls, unmarshaller = self.serializer.unmarshallers[typename]
        except KeyError:
            raise LookupError('no unmarshaller found for type "{}"'.format(typename)) from None

        if cls is not None:
            instance = cls.__new__(cls)
            unmarshaller(instance, marshalled_state)
            return instance
        else:
            return unmarshaller(marshalled_state)

    def wrap_state_dict(self, typename: str, state) -> Dict[str, Any]:
        """
        Wrap the marshalled state in a dictionary.

        The returned dictionary has two keys, corresponding to the ``type_key`` and ``state_key``
        options. The former holds the type name and the latter holds the marshalled state.

        :param typename: registered name of the custom type
        :param state: the marshalled state of the object
        :return: an object serializable by the serializer

        """
        return {self.type_key: typename, self.state_key: state}

    def unwrap_state_dict(self, obj: Dict[str, Any]) -> Union[Tuple[str, Any], Tuple[None, None]]:
        """Unwraps a marshalled state previously wrapped using :meth:`wrap_state_dict`."""
        if len(obj) == 2:
            typename = obj.get(self.type_key)
            state = obj.get(self.state_key)
            if typename is not None:
                return typename, state

        return None, None
