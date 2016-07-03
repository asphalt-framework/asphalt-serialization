import logging
from typing import Dict, Any

from typeguard import check_argument_types

from asphalt.core.component import Component, Context, PluginContainer, merge_config
from asphalt.serialization.api import Serializer, CustomizableSerializer

serializer_backends = PluginContainer('asphalt.serialization.serializers', Serializer)
logger = logging.getLogger(__name__)


class SerializationComponent(Component):
    """
    Publishes one or more serializer resources.

    Every serializer resource will be published using the following types:

    * :class:`~asphalt.serialization.api.Serializer`
    * :class:`~asphalt.serialization.api.CustomizableSerializer` (if the serializer implements it)
    * its actual class

    If more than one serializer is to be configured, provide a ``serializers`` argument as a
    dictionary where the key is the resource name and the value is a dictionary of keyword
    arguments to :meth:`configure_serializer`. Otherwise, directly pass those keyword arguments to
    the component constructor itself.

    If ``serializers`` is defined, any extra keyword arguments are used as default values for
    :meth:`configure_serializer` for all serializers (:func:`~asphalt.core.util.merge_config` is
    used to merge the per-serializer arguments with the defaults). Otherwise, a single serializer
    is created based on the provided default arguments, with ``context_attr`` defaulting to the
    name of the chosen backend.

    :param serializers: a dictionary of resource name ⭢ :meth:`configure_serializer` arguments
    :param default_serializer_args: default values for omitted :meth:`configure_serializer`
        arguments
    """

    def __init__(self, serializers: Dict[str, Dict[str, Any]] = None, **default_serializer_args):
        assert check_argument_types()
        if not serializers:
            default_serializer_args.setdefault('context_attr',
                                               default_serializer_args.get('backend'))
            serializers = {'default': default_serializer_args}

        self.serializers = []
        for resource_name, config in serializers.items():
            config = merge_config(default_serializer_args, config or {})
            config.setdefault('backend', resource_name)
            config.setdefault('context_attr', resource_name)
            context_attr, serializer = self.configure_serializer(**config)
            self.serializers.append((resource_name, context_attr, serializer))

    @classmethod
    def configure_serializer(cls, context_attr: str, backend: str, **backend_args):
        """
        Configure a serializer.

        :param context_attr: context attribute of the serializer (if omitted, the resource name
            will be used instead)
        :param backend: entry point name used to look up the backend class (if omitted, the
            resource name will be used instead)
        :param backend_args: keyword arguments passed to the constructor of the backend class

        """
        assert check_argument_types()
        return context_attr, serializer_backends.create_object(backend, **backend_args)

    async def start(self, ctx: Context):
        for resource_name, context_attr, serializer in self.serializers:
            types = [Serializer, type(serializer)]
            if isinstance(serializer, CustomizableSerializer):
                types.append(CustomizableSerializer)

            ctx.publish_resource(serializer, resource_name, context_attr, types=types)
            logger.info('Configured serializer (%s / ctx.%s; type=%s)', resource_name,
                        context_attr, serializer.mimetype)
