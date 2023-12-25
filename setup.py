import os
from setuptools import setup
import re

directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(os.path.join('bazos', '__init__.py'), encoding='utf-8') as f:
    version = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.M).group(1)

setup(
    name='bazos',
    version=os.environ.get('VERSION', version),
    use_scm_version=True,
    description='Bazos API, that allows you to scrape bazos and upload products to bazos website.',
    author='Zdenek Lapes',
    author_email='lapes.zdenek@gmail.com',
    # url='', # TODO
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords="bazos api bazos.cz bazos.sk bazos.pl bazos.at scrapper webscrapper bazos-webscrapper bazos-api",
    # packages=find_packages(),
    packages=['bazos'],
    entry_points={'console_scripts': ['bazos=bazos:main']},
    classifiers=[
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        "License :: OSI Approved :: MIT License",
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        'Operating System :: OS Independent',
        'Topic :: Web Scraping',
    ],
    install_requires=[],
    python_requires='>=3.10',
    include_package_data=True,
    # TODO: tests
    # cmdclass={'test': tests},
    # test_suite="unitest.py",
)
