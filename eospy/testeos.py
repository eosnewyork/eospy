import os
import yaml
from .cleos import Cleos
from .schema import TestDocSchema
from .keys import EOSKey

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
    
    def _get_rslt(self, rslt, message, exception):
        return {
            'result': rslt,
            'message': message,
            'exception': exception
            }

    def run_query(self, ce, query):
        ret_rslt = []
        eval_str = 'ce.{}(**query["parameters"])'.format(query['query'])
        try :
            query_rslt = eval(eval_str)
            print(query_rslt)
            # check all results
            for rslt in query['results'] :
                try:
                    if not eval('query_rslt{}'.format(rslt)):
                        ret_rslt.append(self._get_rslt(False, 'result "{}" failed'.format(rslt), ''))
                    else: 
                        ret_rslt.append(self._get_rslt(True, 'result "{}" successful'.format(rslt), ''))
                except Exception as ex:
                    ret_rslt.append(self._get_rslt(False, 'failed', str(ex)))
        except Exception as ex:
            ret_rslt.append(self._get_rslt(False, 'failed', str(ex)))
        return ret_rslt

    def run_test(self, url, test):
        print('Running: {}'.format(test['name']))
        
        ce = Cleos(url)
        for action in test['actions']:
            rslts = {
                    'name': test['name'], 
                    'action': action['action'], 
                    'contract': action['contract'], 
                    'results': True, 
                    'message': 'successful', 
                    'comment': '' }
            # add comment
            if 'comment' in action:
                rslts['comment'] = action['comment']
            if 'authorization' not in action:
                authorization = test['authorization']
            else:
                authorization = action['authorization']
            payload = {
                "account": action['contract'],
                "name": action['action'],
                "authorization": [{
                    "actor": authorization['actor'],
                    "permission": authorization['permission'],
                }],
            }
            data = ce.abi_json_to_bin(payload['account'], payload['name'], action['parameters'])
            payload['data']=data['binargs']
            trx = {'actions': [payload]}
            try:
                ce.push_transaction(trx, EOSKey(authorization['key']))
            except Exception as ex:
                if(not action['exception']):
                    rslts['results'] = False
                    rslts['message'] = str(ex)
            # process queries
            query_rslts = []
            if 'queries' in action:
                for query in action['queries']: 
                    query_rslts += self.run_query(ce, query)
                # check for failed results
                failed_queries = list(filter(lambda x: not x['result'], query_rslts))
                if len(failed_queries) > 0:
                    rslts['results'] = False
                    rslts['message'] = 'queries failed'
                rslts['queries'] = query_rslts

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