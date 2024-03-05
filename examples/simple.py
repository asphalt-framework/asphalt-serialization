"""A simple example that serializes a dictionary and prints out the result."""

# isort: off
from __future__ import annotations

import anyio
from asphalt.core import CLIApplicationComponent, run_application, require_resource
from asphalt.serialization import Serializer


class ApplicationComponent(CLIApplicationComponent):
    async def start(self) -> None:
        self.add_component("serialization", backend="json")
        await super().start()

    async def run(self) -> int | None:
        serializer = require_resource(Serializer)
        payload = serializer.serialize(
            {"a": 1, "b": 5.03, "c": [1, 2, 3], "d": {"x": "nested"}}
        )
        print("JSON serialized dict:", payload.decode())
        return None


anyio.run(run_application, ApplicationComponent())
