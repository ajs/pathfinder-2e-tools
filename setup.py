"""
Setup for the Pathfinder 2e tools
"""

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='pathfinder-2e-tools',
    version='1.0.0',
    description='Pathfinder 2e tools',
    long_description='A collection of tools for Pathfinder 2e',
    url='https://github.com/ajs/pathfinder-2e-tools',
    author='Aaron Sherman',
    author_email='ajs@ajs.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Gamers',
        'Topic :: Gaming :: Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='tools gaming pathfinder d20',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    python_requires='>=3.5, <4',
    install_requires=[],
    extras_require={
        'dev': [],
        'test': ['pytest'],
    },
    package_data={
        'rules': ['rules.json'],
    },
    entry_points={  # Optional
        'console_scripts': [
            'pf2e-encounter=pf2e.encounter:main',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/ajs/pathfinder-2e-tools/issues',
        'Source': 'https://github.com/ajs/pathfinder-2e-tools/',
        'Rules': 'https://2e.aonprd.com/Rules.aspx',
        'Official': 'https://paizo.com/pathfinder',
    },
)
