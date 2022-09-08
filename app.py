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
    'api_endpoint': 'us-central1-aiplatform.googleapis.com'
})
aip_endpoint_name = f'projects/{os.environ["PROJECT_ID"]}/locations/us-central1/endpoints/{os.environ["ENDPOINT_ID"]}'


app = Flask(__name__)


@app.route('/')
def home():
    response = aip_client.predict(endpoint=aip_endpoint_name,
                                  instances=['first', 'second', 'third'])
    return str(response[0])  # render_template('index.html')


# run server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
