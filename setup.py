import os
from setuptools import setup, find_packages

directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='bazos',
    version='0.0.1',
    description='Bazos API, that allows you to scrape bazos and upload products to bazos website.',
    author='Zdenek Lapes',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    entry_points={'console_scripts': ['bazos=bazos:main']},
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
