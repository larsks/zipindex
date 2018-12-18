from setuptools import setup, find_packages

setup(
    name='zipindex',
    version='0.1',
    author='Lars Kellogg-Stedman',
    author_email='lars@oddbit.com',
    url='https://github.com/larsks/zipindex',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'zipindex = zipindex.zipindex:zipindex',
        ],
    }
)
