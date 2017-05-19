from setuptools import setup

setup(name='pymongo_smart_auth',
      version='0.1.6',
      description='This package extends PyMongo to provide built-in smart authentication.',
      url='https://github.com/PLPeeters/PyMongo-Smart-Auth',
      author='Pierre-Louis Peeters',
      author_email='PLPeeters@users.noreply.github.com',
      license='MIT',
      packages=['pymongo_smart_auth'],
      install_requires=[
          'pymongo'
      ],
      zip_safe=True)
