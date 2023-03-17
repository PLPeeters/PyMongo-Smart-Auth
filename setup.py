from setuptools import setup

setup(name='pymongo_smart_auth',
      version='2.0.0',
      description='This package extends PyMongo to provide built-in smart authentication.',
      url='https://github.com/PLPeeters/PyMongo-Smart-Auth',
      author='Pierre-Louis Peeters',
      author_email='PLPeeters@users.noreply.github.com',
      license='MIT',
      packages=['pymongo_smart_auth'],
      python_requires='>=3.6',
      install_requires=[
          'pymongo<5,>3'
      ],
      keywords=['mongo', 'pymongo', 'authentication', 'seamless'],
      zip_safe=True)
