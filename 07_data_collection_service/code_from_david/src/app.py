from concurrent.futures import process
import json
from flask import request, Flask, jsonify, make_response
from flasgger import Swagger
import os
import random

import datastructure
import idgenerator
import tracemalloc
import psutil
import os
import logging

app = Flask(__name__)
swagger = Swagger(app)  # Swagger UI served at /apidocs by default

def load_environment():
    """
    Load environment variables from jsonfile
    """
    try:
        env_var = os.environ['WORKING_ENV']
    except:
        env_var = 'dev_env.json'

    with open(env_var) as f:
        env_values = json.loads(f.read())

    # every environment file must define these keys, otherwise startup is broken
    required_keys = ('database_url', 'database_port', 'database_username',
                     'database_password', 'log_level', 'log_file')
    missing = [key for key in required_keys if key not in env_values]
    assert not missing, f'{env_var} is missing required keys: {missing}'

    return env_values


@app.route('/', methods=['GET'])
def index():
    """Simple method to get some information about the software"""
    return json.dumps({'name': 'David',
                       'mail': 'fhnw@roche.ch',
                       'System': 'Digital Biomarker Course Project',
                       'Server Component': 'v1_0_0',
                       'Date': '7-Apr-2026'})


@app.route('/experiment', methods=['POST', 'GET'])
def experiment_action():
    process = psutil.Process(os.getpid())
    memory = process.memory_info().rss / 1024 / 1024
    logging.debug('Memory Usage: %s MB', memory)
    ds = datastructure.DataStorage()
    if request.method == 'POST':
        body = request.get_json()
        name = body['name']
        experiment_obj = datastructure.Experiment(name)
        ds.add_experiment(experiment_obj)
        logging.info('Created experiment %s (%s)', experiment_obj.id, name)
        return jsonify(experiment_obj.__dict__)
    if request.method == 'GET':
        id = request.args.get('id')
        result = ds.get_experiment(id)
        if result == None:
            logging.warning('Experiment %s not found', id)
            return make_response(jsonify('experiment not found'), 404)
        else:
            return make_response(jsonify(result.__dict__), 200)


@app.route('/patient', methods=['POST', 'GET'])
def patient_action():
    """
    Add or retrieve a patient.
    ---
    tags:
      - patients
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
          properties:
            name:
              type: string
              example: John Doe
    responses:
      200:
        description: Patient created successfully
        schema:
          type: object
          properties:
            id:
              type: string
            name:
              type: string
      404:
        description: Patient not found
    """
    ds = datastructure.DataStorage()
    if request.method == 'POST':
        body = request.get_json()
        name = body['name']
        patient_obj = datastructure.Patient(name)
        ds.add_patient(patient_obj)
        logging.info('Created patient %s (%s)', patient_obj.id, name)
        return jsonify(patient_obj.__dict__)
    if request.method == 'GET':
        id = request.args.get('id')
        result = ds.get_patient(id)
        if result == None:
            logging.warning('Patient %s not found', id)
            return make_response(jsonify('patient not found'), 404)
        else:
            return make_response(jsonify(result.__dict__), 200)


@app.route('/patients', methods=['GET'])
def patients_action():
    ds = datastructure.DataStorage()
    return json.dumps(ds.patients, cls=datastructure.PatientEncoder)


@app.route('/experiments', methods=['GET'])
def experiments_action():
    ds = datastructure.DataStorage()
    return json.dumps(ds.experiments, cls=datastructure.ExperimentEncoder)


@app.route('/store', methods=['POST'])
def store_data():
    ds = datastructure.DataStorage()
    ds.store_data()
    return make_response(jsonify("True"), 200)


@app.route('/upload', methods=['POST'])
def upload_data():
    ds = datastructure.DataStorage()
    if request.method == 'POST':
        body = request.get_json()
        logging.debug(body)
        patient_id = body['patientId']
        experiment_id = body['experimentId']
        data = body
        data_obj = datastructure.DataPoint(patient_id, experiment_id, data)
        ds.add_data(data_obj)
        logging.info('Stored data point %s for patient %s / experiment %s',
                     data_obj.id, patient_id, experiment_id)
        return make_response('', 200)


if __name__ == '__main__':
    # load environment
    env_variables = load_environment()

    # configure logging based on the environment (log level and log file)
    log_level = getattr(logging, env_variables.get('log_level', 'info').upper(), logging.INFO)
    log_file = env_variables.get('log_file', 'backendservice.log')

    logging.basicConfig(level=log_level,
        format='%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ])

    logging.info('Starting service, logging to %s', log_file)

    # check if there are data files for patients and experiments available
    ds = datastructure.DataStorage()

    ds.load_data()

    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
