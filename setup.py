import os
import re
from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

version = ""
with open(os.path.join('tsih', '__init__.py')) as f:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE
    ).group(1)
    assert version


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    with open(filename, 'r') as f:
        lineiter = list(line.strip() for line in f)
    return [line for line in lineiter if line and not line.startswith("#")]


install_reqs = parse_requirements("requirements.txt")
test_reqs = parse_requirements("test-requirements.txt")
extras_require={}
extras_require['all'] = [dep for package in extras_require.values() for dep in package]


setup(
    name='tsih',
    packages=['tsih'],  # this must be the same as the name above
    version=version,
    description=("A lightweight library to store an object's history into a SQL database"),
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='J. Fernando Sanchez',
    author_email='jf.sanchez@upm.es',
    url='https://github.com/balkian/tsih',  # use the URL to the github repo
    download_url='https://github.com/balkian/tsih/archive/{}.tar.gz'.format(
        version),
    keywords=['history', 'sql', 'records'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3'],
    install_requires=install_reqs,
    extras_require=extras_require,
    tests_require=test_reqs,
    setup_requires=['pytest-runner', ],
    include_package_data=True,
)
