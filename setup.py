import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pychirp",
    version="0.2.0",
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
