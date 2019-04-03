# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='NaturalLanguage',
    version='0.0.1',
    description='LSTM markov',
    long_description=readme,
    author='mokky',
    author_email='',
    install_requires=['keras', 'numpy', 'mecab-python3', 'markovify', 'pymongo'],
    url='https://github.com/kennethreitz/samplemod',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    test_suite='tests'
)
