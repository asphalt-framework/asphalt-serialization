from __future__ import annotations

import logging
from typing import Any

from asphalt.core import Component, Context, PluginContainer

from .api import CustomizableSerializer, Serializer

serializer_types: PluginContainer = PluginContainer(
    "asphalt.serialization.serializers", Serializer
)
logger = logging.getLogger(__name__)


class SerializationComponent(Component):
    """
    Creates a serializer resource.

    The serializer resource will be available in the context as the following types:

    * :class:`~asphalt.serialization.api.Serializer`
    * :class:`~asphalt.serialization.api.CustomizableSerializer` (if the serializer
      implements it)
    * its actual type

    :param backend: the name of the serializer backend
    :param resource_name: the name of the serializer resource
    :param options: a dictionary of keyword arguments passed to the serializer backend
        class
    """

    def __init__(
        self,
        backend: str,
        resource_name: str = "default",
        options: dict[str, Any] | None = None,
    ):
        options = options or {}
        self.resource_name = resource_name
        self.serializer: Serializer = serializer_types.create_object(backend, **options)

    async def start(self, ctx: Context) -> None:
        types: list[type] = [Serializer, type(self.serializer)]
        if isinstance(self.serializer, CustomizableSerializer):
            types.append(CustomizableSerializer)

        ctx.add_resource(self.serializer, self.resource_name, types=types)
        logger.info(
            "Configured serializer (%s; type=%s)",
            self.resource_name,
            self.serializer.mimetype,
        )
