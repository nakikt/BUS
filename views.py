from flask import Blueprint, render_template, request, redirect, url_for
from .blockchain import Blockchain

from . import db, blocks
import sys
import hashlib
import json
from time import time
from uuid import uuid4
from flask import Flask, jsonify, request
import requests
from urllib.parse import urlparse
from .methods import mine_block
views = Blueprint("views", __name__)



@views.route("/")
@views.route("/home")
def home():
    response =[]
    for block in blocks:
        # print(block.last_block)
        response.append(str( {
            'id': block.last_block['property'][-1]['id'],
            'address': block.last_block['property'][-1]['address'],
            'time': block.last_block['timestamp'],
            'name_surname': block.last_block['property'][-1]['name_surname'],
            'condition': block.last_block['property'][-1]['condition'],
        }))

    return jsonify(response), 200



@views.route('/', methods=['POST'])
def new_transaction():  #TODO Tu są dodawane wartości ze strony


# get the value passed in from the client
    values = request.get_json()
# check that the required fields are in the POST'ed data
    required_fields = ['id', 'address', 'name_surname', 'condition']
    if not all(k in values for k in required_fields):
        return ('Missing fields', 400)
    # create a new transaction
    id = int(values['id'])
#check if our blockchain is valid

    if not blocks[id].valid_new(id):
        response = {'message': f'Property cant be added to Block '}
        return (jsonify(response), 201)
    mine_block(blocks[id], values['id'], values['address'],values['name_surname'], values['condition'] )
    response = {'message': f'Property added to Block '}
    # try:

    neighbours = blocks[id].nodes
    for node in neighbours:
        #blocks[id].update_blockchain(id)
        requests.get(f'http://{node}//nodes/sync/{id}')
    # except:
    #     print("Masz problem")
    response = "sukces"

    return (jsonify(response), 201)



