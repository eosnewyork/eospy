#
# python library cleos
#
import requests

class DynamicUrl :
    #def __init__(self, url='http://localhost:8888', version='v1', cache=None) :
    def __init__(self, url='http://localhost:8888', version='v1', cache=None) :
        self._cache = cache or []
        self._baseurl = url
        self._version = version

    def __getattr__(self, name) :
        return self._(name)

    def __del__(self) :
        pass

    def _(self, name) :
        return DynamicUrl(url=self._baseurl, version=self._version, cache=self._cache+[name])

    def method(self) :
        return self._cache
    
    def create_url(self):
        url_str = '{0}/{1}'.format(self._baseurl,self._version)
        for obj in self.method() :
            url_str = '{0}/{1}'.format(url_str, obj)
        return url_str

    def get_url(self, url, params=None, json=None) :
        # get request
        r = requests.get(url,params=params, json=json)
        r.raise_for_status()
        return r.json()

    def post_url(self, url, params=None, json=None) :
        # post request
        r = requests.post(url,params=params, json=json)
        r.raise_for_status()
        return r.json()
