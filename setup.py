import os
from setuptools import setup, find_packages

directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='cash_balance',
    version='0.0.2',
    description='Cash balance',
    author='Zdenek Lapes',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages = find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
    ],
    install_requires=[],
    python_requires='>=3.10',
    extras_require={},
    include_package_data=True
)
