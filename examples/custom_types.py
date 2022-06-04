"""An example that demonstrates how to serialize custom types."""
from __future__ import annotations

import asyncio
from dataclasses import dataclass

from asphalt.core import ContainerComponent, Context, run_application

from asphalt.serialization.api import CustomizableSerializer


@dataclass
class Book:
    name: str
    author: str
    year: int
    isbn: str
    sequel: Book | None = None


class ApplicationComponent(ContainerComponent):
    async def start(self, ctx: Context) -> None:
        self.add_component("serialization", backend="json")
        await super().start(ctx)

        serializer = ctx.require_resource(CustomizableSerializer)
        serializer.register_custom_type(Book, typename="Book")  # typename is optional
        book2 = Book("The Fall of Hyperion", "Dan Simmons", 1995, "978-0553288209")
        book1 = Book("Hyperion", "Dan Simmons", 1989, "978-0553283686", book2)
        payload = serializer.serialize(book1)
        print("JSON serialized dict:", payload.decode())
        asyncio.get_event_loop().stop()


run_application(ApplicationComponent())
