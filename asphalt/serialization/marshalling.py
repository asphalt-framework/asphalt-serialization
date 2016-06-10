from typing import Dict, Any

from asphalt.core import qualified_name


def default_marshaller(obj):
    """
    Marshal the given object.

    Calls the ``__getstate__()`` method of the object if available, otherwise returns the
    ``__dict__`` of the object.

    :param obj: the object to marshal

    """
    if hasattr(obj, '__getstate__'):
        return obj.__getstate__()
    elif hasattr(obj, '__dict__'):
        return obj.__dict__
    else:
        raise TypeError('{!r} has no __dict__ attribute and does not implement __getstate__()'
                        .format(qualified_name(obj.__class__)))


def default_unmarshaller(state: Dict[str, Any], cls: type):
    """
    Umarshal an object from the given state.

    An empty instance is first created by calling ``__new__()`` on the class.
    Then, if the ``__setstate__()`` method exists on the class, it is called with the state object
    as the argument. Otherwise, its ``__dict__`` is replaced with ``state``.

    :param cls: the class the state belongs to
    :param state: the state object, as returned by :func:`default_marshaller`
    :return: an instance of ``cls``

    """
    instance = cls.__new__(cls)
    if hasattr(cls, '__setstate__'):
        instance.__setstate__(state)
    else:
        instance.__dict__ = state

    return instance
