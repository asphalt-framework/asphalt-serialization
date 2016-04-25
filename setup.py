from pathlib import Path

from setuptools import setup

setup(
    name='asphalt-serialization',
    use_scm_version={
        'version_scheme': 'post-release',
        'local_scheme': 'dirty-tag'
    },
    description='Serialization component for the Asphalt framework',
    long_description=Path(__file__).parent.joinpath('README.rst').read_text('utf-8'),
    author='Alex Grönholm',
    author_email='alex.gronholm@nextday.fi',
    url='https://github.com/asphalt-framework/asphalt-serialization',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5'
    ],
    license='Apache License 2.0',
    zip_safe=False,
    packages=[
        'asphalt.serialization',
        'asphalt.serialization.serializers'
    ],
    setup_requires=[
        'setuptools_scm >= 1.7.0'
    ],
    install_requires=[
        'asphalt ~= 2.0'
    ],
    extras_require={
        'msgpack': 'msgpack-python >= 0.4.6',
        'cbor': 'cbor >= 1.0'
    },
    entry_points={
        'asphalt.components': [
            'serialization = asphalt.serialization.component:SerializationComponent'
        ],
        'asphalt.serialization.serializers': [
            'cbor = asphalt.serialization.serializers.cbor:CBORSerializer [cbor]',
            'json = asphalt.serialization.serializers.json:JSONSerializer',
            'msgpack = asphalt.serialization.serializers.msgpack:MsgpackSerializer [msgpack]',
            'pickle = asphalt.serialization.serializers.pickle:PickleSerializer',
            'yaml = asphalt.serialization.serializers.yaml:YAMLSerializer'
        ]
    }
)
