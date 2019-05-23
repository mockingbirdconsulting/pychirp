import os
import setuptools

# Find the true path of a filename
def __path(filename):
    return os.path.join(os.path.dirname(__file__),
                        filename)

# Set the long description from the README
with open("README.rst", "r") as fh:
    long_description = fh.read()

# Set the build to 0
build = 0

# Automatically update minor releases based on the Jenkins build ID
if os.path.exists(__path('build.info')):
    build = open(__path('build.info')).read().strip()

version= '0.2.{}'.format(build)

setuptools.setup(
    name="pychirp",
    version=version,
    author="Mockingbird Consulting Ltd",
    author_email="info+pychirp@mockingbirdconsulting.co.uk",
    description="A python library for interacting with chirpstack.io.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mockingbirdconsulting/pychirp",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "requests>=2.21.0"
    ]
)
