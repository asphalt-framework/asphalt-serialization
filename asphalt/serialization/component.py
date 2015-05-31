from asyncio.coroutines import coroutine

from typing import Dict, Any
import logging

from asphalt.core.component import Component
from asphalt.core.context import Context
from asphalt.core.util import PluginContainer

from .api import Serializer

serializer_backends = PluginContainer('asphalt.serialization.serializers', Serializer)

logger = logging.getLogger(__name__)


class SerializationComponent(Component):
    """
    Creates :class:`Serializer` instances and publishes them as resources and context attributes.

    Without any arguments, a single JSON serializer resource named ``default`` is published.

    :param serializers: a dictionary of serializer alias -> :meth:`create_serializer` arguments
    :param default_serializer_args: :meth:`create_serializer` arguments for the default serializer
    """

    def __init__(self, serializers: Dict[str, Dict[str, Any]]=None, **default_serializer_args):
        if serializers and default_serializer_args:
            raise ValueError('specify either a "serializers" dictionary or the default '
                             'serializer\'s options directly, but not both')

        if not serializers:
            default_serializer_args.setdefault('type', 'json')
            serializers = {'default': default_serializer_args}

        self.serializers = []
        for resource_name, config in serializers.items():
            config.setdefault('type', resource_name)
            config.setdefault('context_attr', config['type'])
            self.serializers.append((resource_name,) + self.create_serializer(**config))

    @staticmethod
    def create_serializer(type: str, context_attr: str, **backend_args):
        """
        Configure a serializer backend.

        If ``type`` is omitted, the resource name will be used instead.
        If ``context_attr`` is omitted, ``type`` will be used instead.

        :param type: type name used to look up the backend class
        :param context_attr: context attribute of the serializer
        :param backend_args: keyword arguments passed to the constructor of the backend class

        """
        return context_attr, serializer_backends.create_object(type, **backend_args)

    @coroutine
    def start(self, ctx: Context):
        for resource_name, context_attr, serializer in self.serializers:
            yield from ctx.publish_resource(serializer, resource_name, context_attr,
                                            types=Serializer)
            logger.info('Configured serializer (%s / ctx.%s; type=%s)', resource_name,
                        context_attr, serializer.mimetype)
