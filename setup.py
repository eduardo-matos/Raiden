#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='raiden',
    version='0.0.0',
    description='Let humans see progress',
    long_description='Let humans see progress',
    author='Eduardo Matos',
    author_email='eduardo.matos.silva@gmail.com',
    url='https://github.com/eduardo-matos/Raiden',
    packages=[
        'raiden',
    ],
    include_package_data=True,
    install_requires=[
    ],
    license='MIT',
    zip_safe=False,
    keywords='',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
    ],
)
