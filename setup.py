from setuptools import setup, Extension

module = Extension('distance_module',
                   sources=['distance_module.cpp'],
                   language='c++',
                   extra_compile_args=['-std=c++11'])

setup(name='DistanceModule',
      version='1.0',
      description='Distance calculation C++ module',
      ext_modules=[module])