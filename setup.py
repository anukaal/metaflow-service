from os.path import dirname, join, exists
from setuptools import setup, find_packages


def open_and_read_if_exists(path: str):
    try:
        with open(join(dirname(__file__), path)) as f:
            return f.read()
    except:
        return ""


requirements = []
for service in ['metadata_service', 'migration_service']:
    requirements += open_and_read_if_exists(
        "services/{}/requirements.txt".format(service)).splitlines()

requirements_tests = open_and_read_if_exists(
    'requirements.dev.txt').splitlines()

long_description = open_and_read_if_exists(
    'README.md')

setup(
    name='metadata_service',
    version='2.0.5',
    license='Apache License 2.0',
    description='Metadata Service: backend service for Metaflow',
    long_description=long_description,
    author='Machine Learning Infrastructure Team at Netflix',
    author_email='help@metaflow.org',
    url='https://github.com/Netflix/metaflow-service',
    keywords=['metaflow', 'machinelearning', 'ml'],
    py_modules=['services.metadata_service'],
    packages=find_packages(exclude=('tests',)),
    entry_points='''
        [console_scripts]
        metadata_service=services.metadata_service.server:main
        migration_service=services.migration_service.migration_server:main
   ''',
    install_requires=requirements,
    tests_require=requirements + requirements_tests,
    extras_require={
        'test': requirements + requirements_tests
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
