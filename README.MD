# ES_QLIK_WRAPPER
This Python project es a simple wrapper to use ElasticSearch scrolling API into QLIKSENSE

This project has been tested with Elasticsearch 6.4 and QLIK Sense Desktop September 2018

You should modify .flaskenv file to setup your es connection.

```
ES_HOST="http://192.168.217.128:9200"
```


In order to run this app you must install dependencies and then run flask  

```bash
pip install -r requirements.txt
flask run
````

## How to setup Qlik Sense 

You must setup a new REST Connector with the pagination config  as follows:

- Pagination type: *Next Url*
- 'Next Url' path: *root/nextUrl*

The request must be a POST requests with the following url:
```
http://<es_qlik_wrapper>:5000/<es_index>
```

In the body you'll be able to add your ES Query inside the parameter *es_params*:

```
{"es_params":{"query": {"match_all": {}}, "size": 3}}
```
In order to follow the standard you should add the *Content-Type* header as *application/json*

## TODO

- Modify the wrapper to support https in elasticsearch
- Enable https/basic auth on the frontend