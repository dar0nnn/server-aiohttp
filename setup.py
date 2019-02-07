from setuptools import setup
from serverRt import __version__, __author__
setup(
    name='serverRt',
    version=__version__,
    description='test server for rt',
    author=__author__,
    author_email='plukyanov248@gmail.com',
    packages=['serverRt', 'tests'],
    install_requires=['pytest-runner', 'pytest', 'aiohttp', 'aiofiles'],
    test_suite='tests',
    tests_require=['pytest', 'pytest-aiohttp'],
    entry_points={
        'console_scripts':
            ['serverRt = serverRt.__main__:main']
    }
)