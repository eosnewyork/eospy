from setuptools import setup, find_packages
import os

setup(name='eospy',
      version=os.getenv('BUILD_VERSION', 'DEV'),
      description='Python library for the eosio REST API',
      author='deck',
      author_email='deck@eosnewyork.io',
      url='https://github.com/eosnewyork/eospy',
      packages=find_packages(),
      install_requires=[
          'requests'
      ],
      entry_points = {
          'console_scripts' :[
              'vote_for_bps = eospy.command_line:vote_for_bps',
              'validate_chain = eospy.command_line:validate_chain'
          ],
      }
)
