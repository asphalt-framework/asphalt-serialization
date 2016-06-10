"""An example that demonstrates how to serialize custom types."""
import asyncio

from asphalt.core import ContainerComponent, Context, run_application


class Book:
    def __init__(self, name, author, year, isbn, sequel=None):
        self.name = name
        self.author = author
        self.year = year
        self.isbn = isbn
        self.sequel = sequel


class ApplicationComponent(ContainerComponent):
    async def start(self, ctx: Context):
        self.add_component('serialization', backend='json')
        await super().start(ctx)

        ctx.json.register_custom_type(Book, typename='Book')  # typename is optional
        book2 = Book('The Fall of Hyperion', 'Dan Simmons', 1995, '978-0553288209')
        book1 = Book('Hyperion', 'Dan Simmons', 1989, '978-0553283686', book2)
        payload = ctx.json.serialize(book1)
        print('JSON serialized dict:', payload.decode())
        asyncio.get_event_loop().stop()

run_application(ApplicationComponent())
