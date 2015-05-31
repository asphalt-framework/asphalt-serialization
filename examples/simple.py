"""A simple example that serializes a dictionary and prints out the result."""

from asphalt.core.component import ContainerComponent
from asphalt.core.context import Context
from asphalt.core.runner import run_application
from asphalt.core.util import stop_event_loop


class DemoSerializerComponent(ContainerComponent):
    def start(self, ctx: Context):
        self.add_component('serialization')
        yield from super().start(ctx)
        payload = ctx.json.serialize({'a': 1, 'b': 5.03, 'c': [1, 2, 3], 'd': {'x': 'nested'}})
        print('JSON serialized dict:', payload.decode())
        stop_event_loop()

run_application(DemoSerializerComponent())
