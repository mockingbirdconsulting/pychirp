import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyloraserver",
    version="0.1.5",
    author="Mockingbird Consulting Ltd",
    author_email="info+pyloraserver@mockingbirdconsulting.co.uk",
    description="A python library for interacting with Loraserver.io.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mockingbirdconsulting/pyloraserver",
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
