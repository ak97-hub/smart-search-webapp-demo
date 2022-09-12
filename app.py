from flask import Flask, Response, jsonify, render_template, logging, request
import logging
from operator import itemgetter
import os

from flask import jsonify
from google.cloud import aiplatform
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value
import requests


aip_client = aiplatform.gapic.PredictionServiceClient(client_options={
    'api_endpoint': f'{os.environ["LOCATION"]}-aiplatform.googleapis.com'
})
aip_endpoint_name = f'projects/{os.environ["PROJECT_ID"]}/locations/{os.environ["LOCATION"]}/endpoints/{os.environ["ENDPOINT_ID"]}'


def get_prediction(instances):
    print('Sending prediction request to AI Platform ...')
    try:
        print('Logging instance ...' + str(instances))
        response = aip_client.predict(endpoint=aip_endpoint_name,
                                      instances=instances)
        print('Logging Response ...' + str(response))
        return list(response.predictions)
    except Exception as err:
        print(f'Prediction request failed: {type(err)}: {err}')
        return None


app = Flask(__name__)


@app.route('/')
def home():
    response = get_prediction(instances=['first', 'second', 'third'])
    print(response)
    return render_template('index.html')


# run server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
