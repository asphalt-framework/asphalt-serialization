Version history
===============

This library adheres to `Semantic Versioning <http://semver.org/>`_.

**3.0.0**

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
