import logging
from typing import Dict, Any

from asphalt.core import Component, Context, PluginContainer, merge_config
from typeguard import check_argument_types

from asphalt.serialization.api import Serializer, CustomizableSerializer

serializer_types = PluginContainer('asphalt.serialization.serializers', Serializer)
logger = logging.getLogger(__name__)


class SerializationComponent(Component):
    """
    Creates one or more serializer resources.

    Every serializer resource will be available in the context as the following types:

    * :class:`~asphalt.serialization.api.Serializer`
    * :class:`~asphalt.serialization.api.CustomizableSerializer` (if the serializer implements it)
    * its actual type

    Serializers can be configured in two ways:

    #. a single serializer, with configuration supplied directly as keyword arguments to this
        component's constructor (with the resource name being ``default`` and the context attribute
        matching the backend name)
    #. multiple serializers, by providing the ``serializers`` option where each key is the resource
        name and each value is a dictionary containing that serializer's configuration (with the
        context attribute matching the resource name by default)

    Each serializer configuration has two special options that are not passed to the constructor of
    the backend class:

    * backend: entry point name of the serializer backend class (required)
    * context_attr: name of the context attribute of the serializer resource

    :param serializers: a dictionary of resource name ⭢ constructor arguments for the chosen
        backend class
    :param default_serializer_args: default values for constructor keyword arguments
    """

    def __init__(self, serializers: Dict[str, Dict[str, Any]] = None, **default_serializer_args):
        assert check_argument_types()
        if not serializers:
            default_serializer_args.setdefault(
                'context_attr', default_serializer_args.get('backend'))
            serializers = {'default': default_serializer_args}

        self.serializers = []
        for resource_name, config in serializers.items():
            config = merge_config(default_serializer_args, config or {})
            type_ = config.pop('backend', resource_name)
            context_attr = config.pop('context_attr', resource_name)
            serializer = serializer_types.create_object(type_, **config)
            self.serializers.append((resource_name, context_attr, serializer))

    async def start(self, ctx: Context):
        for resource_name, context_attr, serializer in self.serializers:
            types = [Serializer, type(serializer)]
            if isinstance(serializer, CustomizableSerializer):
                types.append(CustomizableSerializer)

            ctx.add_resource(serializer, resource_name, context_attr, types=types)
            logger.info('Configured serializer (%s / ctx.%s; type=%s)', resource_name,
                        context_attr, serializer.mimetype)
