from flask import Blueprint, render_template, request, redirect, url_for
from .blockchain import Blockchain

from . import db, blocks
import sys
import hashlib
import json
from time import time
from uuid import uuid4
from flask import Flask, jsonify, request
from flask_login import login_user, logout_user, login_required, current_user

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
        response.append({
            'id': block.last_block['property'][-1]['id'],
            'address': block.last_block['property'][-1]['address'],
            'date': block.last_block['timestamp'],
            'name_surname': block.last_block['property'][-1]['name_surname'],
            'condition': block.last_block['property'][-1]['condition'],
        })

    return jsonify(response), 200



@views.route('/edit', methods=['POST'])
def new_transaction():  # Tu są dodawane wartości ze strony
# get the value passed in from the client
    values = request.get_json()
# check that the required fields are in the POST'ed data
    required_fields = ['id', 'address', 'name_surname', 'condition']
    if not all(k in values for k in required_fields):
        return ('Missing fields', 400)
    # create a new transaction
    id = int(values['id'])

    if not blocks[id].valid_new(id):
        response = {
            'Message: The validity of the block was checked by other nodes and rejected.'
        }
        print( 'The validity of the block was checked by other nodes and rejected.')
        return (jsonify(response), 201)
    print('The validity of the block was checked by other nodes')
    try:
        mine_block(blocks[id], values['id'], values['address'], values['name_surname'], values['condition'])
        print('Block was mined to the blockchain')
    except:
        print('Failed to add block to blockchain')
    try:
        neighbours = blocks[id].nodes
        for node in neighbours:
            #blocks[id].update_blockchain(id)
            requests.get(f'http://{node}//nodes/sync/{id}')
    except:
         print("Masz problem")
    response = {'Block was successfully added'}
    return (jsonify(response), 201)

@views.route('/add', methods=['POST'])
def new_transaction2():  #TODO Tu są dodawane wartości ze strony
# get the value passed in from the client
    values = request.get_json()
# check that the required fields are in the POST'ed data
    required_fields = ['id', 'address', 'name_surname', 'condition']
    if not all(k in values for k in required_fields):
        return ('Missing fields', 400)
    # create a new transaction
    id = int(values['id'])
    new_blockchain = Blockchain()
    blocks.append(new_blockchain)

    try:
        mine_block(blocks[-1], values['id'], values['address'], values['name_surname'], values['condition'])
        print('Block was mined')
    except:
        print('Failed to add block to blockchain')

    try:
        blocks[-1].add_node("https://127.0.0.1:5000")
        blocks[-1].add_node("https://127.0.0.1:5001")
        blocks[-1].add_node("https://127.0.0.1:5002")
        blocks[-1].add_node("https://127.0.0.1:5003")
        neighbours = blocks[id].nodes
        for node in neighbours:
            # blocks[id].update_blockchain(id)
            requests.get(f'http://{node}//nodes/sync/{id}')
    except:
        print("Masz problem")
    response = {'Block was successfully added'}


    return (jsonify(response), 201)


