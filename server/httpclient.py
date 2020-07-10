import requests, json
import ssl
 
class HttpsClient:
 
    def __init__(self):
        pass
 
    @staticmethod
    def get(_url, _json):
        _resp = requests.get(_url, _json)
        return _resp.content
 
    @staticmethod
    def https_get(_url):
        _resp = requests.get(_url)
        return _resp.content

    @staticmethod
    def https_post(_url, _json_dict):
        _resp = requests.post(_url, _json_dict, verify=False)
        return _resp.text
 
    @staticmethod
    def https_post_with_header(_url, _json_dict, _headers):
        _resp = requests.post(_url, data=_json_dict, headers=_headers, verify=False)
        return _resp.text
 
''' 
if __name__ == '__main__':
    url = "https://101.37.149.55/SmartSite/v2/getToken.action"
    json_dict = '{"userName":"hfykcs", "password":"hfykcs"}'
    result = HttpsClient.https_post_with_header(url, json_dict, {"Content-type": "application/x-www-form-urlencoded"})
    print(result)
'''