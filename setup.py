from setuptools import setup

VERSION = "0.0.1"
REQUIRES = ["requests>=2.6.0", "bottle==0.12.9", "WebTest==2.0.20"]

setup(
    name='pypact',
    packages=['pypact'],
    version=VERSION,
    description='Consumer driven contract testing library.',
    author='Rory Hart',
    author_email='hartror@gmail.com',
    url='http://github.com/hartror/pypact',
    download_url='https://github.com/hartror/pypact/tarball/0.0.1',
    keywords=['testing'],
    classifiers=[],
    install_requires=REQUIRES)
