from setuptools import setup

setup(
    name='webanalysis',
    packages=['app'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)