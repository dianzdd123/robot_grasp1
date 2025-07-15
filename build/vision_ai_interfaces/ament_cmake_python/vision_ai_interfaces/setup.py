from setuptools import find_packages
from setuptools import setup

setup(
    name='vision_ai_interfaces',
    version='0.0.0',
    packages=find_packages(
        include=('vision_ai_interfaces', 'vision_ai_interfaces.*')),
)
