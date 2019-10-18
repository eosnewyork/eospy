import os
from eospy import testeos


cwd = os.path.dirname(os.path.realpath(__file__))
tester = testeos.TestEos(cwd)

tester.run_test_one('test_transfer_success')
tester.run_test_one('test_transfer_fail')
tester.run_test_one('test_voting_producers')

tester.run_test_all()

rslts = tester.get_all_results()
print(rslts)
rslts = tester.get_failed_results()
print(rslts)
rslts = tester.get_successful_results()
print(rslts)