from setuptools import find_packages, setup

import bottle_postgresql
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open(os.path.abspath('README.md')) as file:
    long_description = file.read()

setup(
    author=bottle_postgresql.__author__,
    author_email=bottle_postgresql.__author_email__,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Database'
    ],
    description='Bottle PostgreSQL is a simple adapter for PostgreSQL with connection pooling.',
    include_package_data=True,
    install_requires=[
        'dbutils',
        'psycopg2-binary',
        'pystache'
    ],
    keywords='bottle database postgresql psycopg2',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    name='bottle-postgresql',
    packages=find_packages(),
    platforms='any',
    py_modules=['bottle_postgresql'],
    url='https://github.com/bernardocouto/bottle-postgresql',
    version=bottle_postgresql.__version__
)
