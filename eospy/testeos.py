import os
import yaml
from .cleos import Cleos
from .schema import TestDocSchema

class TestEos:

    def __init__(self, yaml_location):
        self._documents = []
        self._results = []
        if os.path.isdir(yaml_location):
            for file in os.listdir(yaml_location):
                if file.endswith('.yml') or file.endswith('.yaml'):
                    full_path = os.path.join(yaml_location, file)
                    with open(full_path) as yaml_file:
                        self._documents += yaml.load_all(yaml_file)
        else:
            with open(yaml_location) as yaml_file:
                self._documents += yaml.load_all(yaml_file)
        validator = TestDocSchema()
        for doc in self._documents:
            validator.deserialize(doc)
    
    def run_test(self, url, test):
        print('Running: {}'.format(test['name']))
        rslts = {'name': test['name'], 'results': True, "message": "successful" }
        ce = Cleos(url)
        for action in test['actions']:
            payload = {
                "account": action['contract'],
                "name": action['action'],
                "authorization": [{
                    "actor": action['authorization']['actor'],
                    "permission": action['authorization']['permission'],
                }],
            }
            data = ce.abi_json_to_bin(payload['account'], payload['name'], action['parameters'])
            payload['data']=data['binargs']
            trx = {'actions': [payload]}
            try:
                ce.push_transaction(trx, action['authorization']['key'])
            except Exception as ex:
                if(not action['exception']):
                    rslts['results'] = False
                    rslts['message'] = str(ex)
            self._results.append(rslts)

    def run_test_one(self, name):
        for doc in self._documents:
            url = doc['environment']['url']
            for test in doc['tests']:
                if test['name'] == name:
                    self.run_test(url, test)

    def run_test_all(self):
        for doc in self._documents:
            url = doc['environment']['url']
            for test in doc['tests']:
                self.run_test(url, test)

    def _get_results(self, successful=True, failed=True):
        return_rslts = []
        for rslt in self._results:
            if not rslt['results'] and failed:
                return_rslts.append(rslt)
            if rslt['results'] and successful:
                return_rslts.append(rslt)
        return return_rslts

    def get_all_results(self):
        return self._get_results(True, True)

    def get_failed_results(self):
        return self._get_results(False, True)

    def get_successful_results(self):
        return self._get_results(True, False)