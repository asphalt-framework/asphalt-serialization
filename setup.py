import os.path

from setuptools import setup

here = os.path.dirname(__file__)
readme_path = os.path.join(here, 'README.rst')
readme = open(readme_path).read()

setup(
    name='asphalt-serialization',
    use_scm_version={
        'local_scheme': 'dirty-tag'
    },
    description='Serialization component for the Asphalt framework',
    long_description=readme,
    author='Alex Grönholm',
    author_email='alex.gronholm@nextday.fi',
    url='https://github.com/asphalt-framework/asphalt-serialization',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
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
        'asphalt < 2.0.0'
    ],
    extras_require={
        'msgpack': 'msgpack-python >= 0.4.6'
    },
    entry_points={
        'asphalt.components': [
            'serialization = asphalt.serialization.component:SerializationComponent'
        ],
        'asphalt.serialization.serializers': [
            'json = asphalt.serialization.serializers.json:JSONSerializer',
            'msgpack = asphalt.serialization.serializers.msgpack:MsgpackSerializer',
            'pickle = asphalt.serialization.serializers.pickle:PickleSerializer',
            'yaml = asphalt.serialization.serializers.yaml:YAMLSerializer'
        ]
    }
)
