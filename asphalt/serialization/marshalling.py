from asphalt.core import qualified_name


def default_marshaller(obj):
    """
    Retrieve the state of the given object.

    Calls the ``__getstate__()`` method of the object if available, otherwise returns the
    ``__dict__`` of the object.

    :param obj: the object to marshal
    :return: the marshalled object state

    """
    if hasattr(obj, '__getstate__'):
        return obj.__getstate__()

    try:
        return obj.__dict__
    except AttributeError:
        raise TypeError('{!r} has no __dict__ attribute and does not implement __getstate__()'
                        .format(qualified_name(obj.__class__))) from None


def default_unmarshaller(instance, state) -> None:
    """
    Restore the state of an object.

    If the ``__setstate__()`` method exists on the instance, it is called with the state object
    as the argument. Otherwise, the instance's ``__dict__`` is replaced with ``state``.

    :param instance: an uninitialized instance
    :param state: the state object, as returned by :func:`default_marshaller`

    """
    if hasattr(instance, '__setstate__'):
        instance.__setstate__(state)
    else:
        try:
            instance.__dict__.update(state)
        except AttributeError:
            raise TypeError('{!r} has no __dict__ attribute and does not implement __setstate__()'
                            .format(qualified_name(instance.__class__))) from None
