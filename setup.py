from setuptools import setup, find_packages
import os

setup(name='eospy',
      #version=os.getenv('BUILD_VERSION', 'DEV'),
      version='1.0.0',
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
              'validate_chain = eospy.command_line:validate_chain',
              'create_account = eospy.command_line:create_account',
              'spammer = eospy.command_line:spam_up_in_here',
              'pycleos = eospy.command_line:cleos',
              'get_info = eospy.command_line:get_info',
              'get_block = eospy.command_line:get_block',
              'get_account = eospy.command_line:get_account',
              'get_code = eospy.command_line:get_code',
              'get_abi = eospy.command_line:get_abi',
              'get_table = eospy.command_line:get_table'
          ],
      }
)
