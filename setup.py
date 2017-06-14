from setuptools import setup

setup(name='pymongo_smart_auth',
      version='0.4.0',
      description='This package extends PyMongo to provide built-in smart authentication.',
      url='https://github.com/PLPeeters/PyMongo-Smart-Auth',
      author='Pierre-Louis Peeters',
      author_email='PLPeeters@users.noreply.github.com',
      license='MIT',
      packages=['pymongo_smart_auth'],
      install_requires=[
          'pymongo'
      ],
      keywords=['mongo', 'pymongo', 'authentication', 'seamless'],
      zip_safe=True)
