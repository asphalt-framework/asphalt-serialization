Version history
===============

This library adheres to `Semantic Versioning 2.0 <http://semver.org/>`_.

**UNRELEASED**

- Dropped support for Python 3.7

**6.0.0** (2022-06-04)

- **BACKWARD INCOMPATIBLE** Bumped minimum Asphalt version to 4.8
- **BACKWARD INCOMPATIBLE** Refactored component to only provide a single serializer
  (you will have to add two components to get two serializers)
- **BACKWARD INCOMPATIBLE** Dropped the context attribute (use dependency injection
  instead)
- Dropped explicit run-time type checking
- Fixed msgpack encoder hooks being set where decoder hooks were supposed to be set, and
  vice versa

**5.0.1** (2022-04-14)

- Fixed overly restrictive dependency constraint on Asphalt core

**5.0.0** (2021-12-26)

- **BACKWARD INCOMPATIBLE** Upgraded dependencies:

  - ``ruamel.yaml`` ⟶ 0.15+
  - ``cbor2`` ⟶ ~5.0
  - ``msgpack`` ⟶ ~1.0
- **BACKWARD INCOMPATIBLE** Removed the ``dumper_options`` parameter to ``YAMLSerializer``, as
  ``ruamel.yaml`` does not seem to support this anymore
- Added support for Python 3.10
- Dropped support for Python 3.5 and 3.6

**4.0.3** (2018-11-21)

- Fixed msgpack deprecation warnings by replacing the ``encoding="utf-8"`` unpacker option with
  ``raw=False``

**4.0.2** (2017-06-04)

- Added compatibility with Asphalt 4.0

**4.0.1** (2017-05-11)

- Fixed ``None`` not being accepted in place of a serializer configuration dictionary

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
  `cbor2 <https://pypi.io/project/cbor2/>`_
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
