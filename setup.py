from setuptools import find_packages, setup

import bottle_postgresql
import os

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
    install_requires=[
        'dbutils',
        'psycopg2-binary',
        'pystache'
    ],
    keywords='database postgresql psycopg2 queries',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    name='bottle-postgresql',
    packages=find_packages(),
    platforms='any',
    url='https://github.com/bernardocouto/bottle-postgresql',
    version=bottle_postgresql.__version__
)
