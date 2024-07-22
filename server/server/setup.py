from setuptools import find_packages, setup

dependencies = [
    'pandas',
    'numpy',
    'matplotlib',
    'mealpy',
    'imageio',
    'Django',
    'djangorestframework'
]

setup(
    name='scheduler_alg',
    version='0.1.0',
    packages=find_packages(),
    install_requires=dependencies
)