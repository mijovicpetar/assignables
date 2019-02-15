"""Setup script."""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="assignables",
    version="0.0.1",
    author="Petar Mijovic",
    author_email="petar@psoftware.co",
    description="Helper package for assigning values to DB model objects.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mijovicpetar/assignables",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
