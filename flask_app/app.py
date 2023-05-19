from flask import Flask, request, jsonify
from flask_cors import CORS
from classes import FORMS
from pymemcache.client.base import Client
import numpy as np
import json
import requests
import transformers

VERSION = 'v1'
app = Flask(__name__)
cors = CORS(app, resources={r"/v1/*": {"origins": "*"}})

# Setup Memcache global variables
class JsonSerde(object):
    def serialize(self, key, value):
        if isinstance(value, str):
            return value, 1
        return json.dumps(value), 2

    def deserialize(self, key, value, flags):
       if flags == 1:
           return value
       if flags == 2:
           return json.loads(value)
       raise Exception("Unknown serialization format")
MEMCACHE_CLIENT = Client(('memcache', 11211), no_delay=True, serde=JsonSerde())#Client(('memcache', 11211)
MEMCACHE_EXPIRE = 60 # cached object will expire in 60 seconds

# Tokenizer
MODEL_NAME = 'ai-forever/ruBert-base'
tokenizer = transformers.AutoTokenizer.from_pretrained(MODEL_NAME, from_pt=True)

# URI which points to the tensorflow-serving model
MODEL_URI = 'http://tf_serving:8501/v1/models/feed_forward:predict'


@app.route(f'/{VERSION}/predict', methods=['POST'])
def predict():
    input_text = request.form['text']

    if not input_text:
        return jsonify(message='Text is None.'), 406
    
    print(input_text)
    tokenized_text = regular_encoder(input_text, tokenizer, 100)
    memcache_key = str(abs(hash(input_text))) #str(abs(hash(input_text)))

    if MEMCACHE_CLIENT.get(memcache_key) is not None:
        cached_result = MEMCACHE_CLIENT.get(memcache_key)
        return jsonify(message="Cached Prediction", predictions=cached_result, status="OK")
    
    data = json.dumps({"instances": tokenized_text})
    response = requests.post(MODEL_URI, data=data)
    result = json.loads(response.text)
    predictions = result['predictions'][0]
    res = dict(zip(predictions, FORMS))
    sorted_data = sorted(res.items(), reverse=True)
    pred_res = {k: v for k, v in enumerate(sorted_data[:3])}

    MEMCACHE_CLIENT.add(memcache_key, pred_res, expire=MEMCACHE_EXPIRE, noreply=False)
    return jsonify(message="Prediction Success", predictions=pred_res, status="OK")

@app.route('/')
def index():
    return 'Welcome!'

def regular_encoder(texts, tokenizer, maxlen=512):
    enc_di = tokenizer.encode_plus(
        texts,
        return_token_type_ids=False,
        pad_to_max_length=True,
        max_length=maxlen,
        padding='max_length'
    )
    return [enc_di['input_ids']]

# if __name__ == '__main__':
#     app.run(debug=True)