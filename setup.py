from setuptools import setup

setup(
    name='PDPlatform',
    version='0.1.0',
    packages=['PDPlatform'],
    include_package_data=True,
    install_requires=[
        'arrow==0.13.0',
        'bs4==0.0.1',
        'Flask==2.3.2',
        'requests==2.21.0',
        'sh==1.12.14',
    ],
)