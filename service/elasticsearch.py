
# from elasticsearch import Elasticsearch
import requests
from requests.auth import HTTPBasicAuth 
import json
from bs4 import BeautifulSoup

def find_product(keyword):
  headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
  
  data = '''
  {
    "query": {
      "match": {
        "title":{
          "query": "'''+keyword+'''",
          "operator": "or"
        }
      }
    },
    "from" : 0,
    "size" : 1000
  }
  '''
  data = data.encode('utf-8')
  x = requests.get('https://e6142e75eaa441aca21a0455d8261f3c.us-central1.gcp.cloud.es.io:9243/ecommerce_title/_search',headers = headers, data=data, auth=HTTPBasicAuth('giang0','123456789'))
  
  results = json.loads(x.text, encoding='utf-8')['hits']['hits']
  product_list = []
  for r in results[::]:
    product_list.append(r['_source']['title'])
  return product_list

if __name__ == "__main__":
  print(find_product('quan'))  