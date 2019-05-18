# -*- coding: utf-8 -*-

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
    author='',
    author_email='',
    install_requires=['keras', 'numpy', 'mecab-python3', 'mecab-python-windows', 'markovify', 'pymongo'],
    url='',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    test_suite='tests'
)
