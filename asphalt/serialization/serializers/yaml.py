from typeguard import check_argument_types
from typing import Any, Dict

import yaml

from ..api import Serializer


class YAMLSerializer(Serializer):
    """
    Serializes objects to and from YAML format.

    .. warning:: This serializer is insecure in unsafe mode because it allows execution of
      arbitrary code when deserializing.

    .. seealso:: `PyYAML documentation <http://pyyaml.org/wiki/PyYAMLDocumentation>`_

    :param safe: ``True`` to (de)serialize in safe mode, ``False`` to enable extended tags
    :param dumper_options: a dictionary of keyword arguments given to ``yaml.dump()``
    """

    __slots__ = '_dumper_class', '_loader_class', '_dumper_options'

    def __init__(self, safe: bool=True, dumper_options: Dict[str, Any]=None):
        assert check_argument_types()
        self._dumper_class = yaml.SafeDumper if safe else yaml.Dumper
        self._loader_class = yaml.SafeLoader if safe else yaml.Loader
        self._dumper_options = dumper_options or {}
        self._dumper_options.setdefault('encoding', 'utf-8')

    def serialize(self, obj) -> bytes:
        return yaml.dump(obj, Dumper=self._dumper_class, **self._dumper_options)

    def deserialize(self, payload: bytes):
        return yaml.load(payload, Loader=self._loader_class)

    @property
    def mimetype(self):
        return 'text/yaml'

    @property
    def safe(self):
        """Returns ``True`` if the safe mode is being used with (de)serialization."""
        return self._dumper_class is yaml.SafeDumper
