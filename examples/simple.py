"""A simple example that serializes a dictionary and prints out the result."""
import asyncio

from asphalt.core import ContainerComponent, Context, run_application

from asphalt.serialization.api import Serializer


class ApplicationComponent(ContainerComponent):
    async def start(self, ctx: Context) -> None:
        self.add_component("serialization", backend="json")
        await super().start(ctx)

        serializer = ctx.require_resource(Serializer)
        payload = serializer.serialize(
            {"a": 1, "b": 5.03, "c": [1, 2, 3], "d": {"x": "nested"}}
        )
        print("JSON serialized dict:", payload.decode())
        asyncio.get_event_loop().stop()


run_application(ApplicationComponent())
