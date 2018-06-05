from setuptools import setup, find_packages

# import unittest
# import doctest
requirements = ["numpy"]

setup(
    name='testzd',
    version="0.0.1",
    install_requires=requirements,
    author='Nikoleta Glynatsi',
    author_email=('glynatsine@cardiff.ac.uk'),
    packages=find_packages('src'),
    package_dir={"": "src"},
    description='A package used in the study of memory one strategies.',
)
