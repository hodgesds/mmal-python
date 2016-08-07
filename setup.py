from setuptools import setup, find_packages

setup(
    name             = "mmal",
    description      = "Meteorological Middleware Application Layer",
    url              = "https://github.com/hodgesds/mmal-python",
    version          = "0.0.1",
    author           = "Daniel Hodges",
    author_email     = "hodges.daniel.scott@gmail.com",
    scripts          = [ "bin/mmal" ],
    install_requires = [ "mmal-proto", "grpcio" ],
    test_suite       = "",
    tests_require    = [ "tox", "nose" ],
    packages         = find_packages(
        where        = '.',
        exclude      = ('tests*', 'bin*'),
    ),
)
