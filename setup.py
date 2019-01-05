from setuptools import setup, find_packages
import os

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup(name='libeospy',
      #version=os.getenv('BUILD_VERSION', 'DEV'),
      version='1.1.8',
      description='Python library for the eos.io REST API',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='deck',
      author_email='deck@eosnewyork.io',
      url='https://github.com/eosnewyork/eospy',
      packages=find_packages(),
      test_suite = 'nose.collector',
      install_requires=[
          'requests',
          'base58',
          'ecdsa',
          'colander',
          'pytz',
          'six'
      ],
      entry_points = {
          'console_scripts' :[
              'validate_chain = eospy.command_line:validate_chain',
              'pycleos = eospy.command_line:cleos'
          ],
      }
)
