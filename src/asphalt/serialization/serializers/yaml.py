from __future__ import annotations

from io import StringIO

from ruamel.yaml import YAML
from typeguard import check_argument_types

from asphalt.serialization.api import Serializer


class YAMLSerializer(Serializer):
    """
    Serializes objects to and from YAML format.

    To use this serializer backend, the ``ruamel.yaml`` library must be installed.
    A convenient way to do this is to install ``asphalt-serialization`` with the ``yaml``
    extra:

    .. code-block:: shell

        $ pip install asphalt-serialization[yaml]

    .. warning:: This serializer is insecure in unsafe mode because it allows execution of
      arbitrary code when deserializing.

    .. seealso:: `PyYAML documentation <http://pyyaml.org/wiki/PyYAMLDocumentation>`_

    :param safe: ``True`` to (de)serialize in safe mode, ``False`` to enable extended tags
    """

    __slots__ = "_yaml", "_dumper_options"

    def __init__(self, safe: bool = True):
        assert check_argument_types()
        self._yaml = YAML(typ="safe" if safe else "unsafe")

    def serialize(self, obj) -> bytes:
        buffer = StringIO()
        self._yaml.dump(obj, buffer)
        return buffer.getvalue().encode("utf-8")

    def deserialize(self, payload: bytes):
        return self._yaml.load(payload)

    @property
    def mimetype(self):
        return "text/yaml"

    @property
    def safe(self):
        """Returns ``True`` if the safe mode is being used with (de)serialization."""
        return "safe" in self._yaml.typ
