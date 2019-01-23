from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

about = {}
with open(os.path.join(here, 'eospy', '__version__.py'), 'r') as f:
    exec(f.read(), about)

setup(name='libeospy',
      version=os.getenv('BUILD_VERSION', about['__version__']),
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
          'six',
          'pyyaml',
      ],
      entry_points = {
          'console_scripts' :[
              'validate_chain = eospy.command_line:validate_chain',
              'pycleos = eospy.command_line:cleos',
              'pytesteos = eospy.command_line:testeos',
          ],
      }
)
