Version history
===============

This library adheres to `Semantic Versioning <http://semver.org/>`_.

**4.0.0** (2017-04-24)

- **BACKWARD INCOMPATIBLE** Migrated to Asphalt 3.0
- **BACKWARD INCOMPATIBLE** Upgraded cbor2 dependency to v4
- **BACKWARD INCOMPATIBLE** Improved the ability to customize the serialization of custom types in
  serializers implementing the ``CustomizableSerializer`` interface by specifying a value for the
  ``custom_type_codec`` option. This replaces the ``custom_type_key`` and ``wrap_state`` options.

**3.2.0** (2016-11-24)

- Added the ability to skip wrapping custom marshalled objects (by setting ``wrap_state=False`` in
  any of the customizable serializers)

**3.1.0** (2016-09-25)

- Allow parameterless unmarshaller callbacks that return a new instance of the target class
- Switched YAML serializer to use ruamel.yaml instead of PyYAML

**3.0.0** (2016-07-03)

- **BACKWARD INCOMPATIBLE** Switched the CBOR implementation to
  `cbor2 <https://pypi.io/project/cbor2/>`
- **BACKWARD INCOMPATIBLE** Switched msgpack's MIME type to ``application/msgpack``
- **BACKWARD INCOMPATIBLE** Switched the default context attribute name to the backend name,
  for consistency with asphalt-templating
- Added custom type handling for CBOR, msgpack and JSON serializers
- Serializer resources are now also published using their actual types (in addition the interfaces)

**2.0.0** (2016-05-09)

- **BACKWARD INCOMPATIBLE** Migrated to Asphalt 2.0
- **BACKWARD INCOMPATIBLE** A backend must be specified explicitly (it no longer defaults to JSON)
- Allowed combining ``serializers`` with default parameters

**1.1.0** (2016-01-02)

- Added support for CBOR (Concise Binary Object Representation)
- Added typeguard checks to fail early if arguments of wrong types are passed to functions

**1.0.0** (2015-05-31)

- Initial release
