from flask import Blueprint, render_template, request, redirect, url_for
from .blockchain import Blockchain

from . import db
import sys
import hashlib
import json
from time import time
from uuid import uuid4
from flask import Flask, jsonify, request
import requests
from urllib.parse import urlparse

views = Blueprint("views", __name__)
blockchain = Blockchain()


@views.route("/")
@views.route("/home")
def home():
    response = blockchain.last_block["transactions"]
    print(response)
    return jsonify(response), 200

@views.route('/blockchain', methods=['GET']) #TODO Jako historia zmian?? Chcemy??
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
        }
    return jsonify(response), 200
@views.route('/mine', methods=['GET'])
def mine_block():
# the miner must receive a reward for finding the proof
# the sender is "0" to signify that this node has mined a
# new coin.
    blockchain.add_transaction(
        id =  "id",
        address =  "address",
        name_surname = "name_surname",
        condition =  "condition",
    )
# obtain the hash of last block in the blockchain
    last_block_hash = blockchain.hash_block(blockchain.last_block)
# using PoW, get the nonce for the new block to be added
# to the blockchain
    index = len(blockchain.chain)
    nonce = blockchain.proof_of_work(index, last_block_hash, blockchain.current_transactions)
# add the new block to the blockchain using the last block
# hash and the current nonce
    block = blockchain.append_block(nonce, last_block_hash)
    response = {
        'message': "New Block Mined",
        'index': block['index'],
        'hash_of_previous_block': block['hash_of_previous_block'],
        'nonce': block['nonce'],
        'transactions': block['transactions'],
    }
    return jsonify(response), 200


@views.route('/transactions/new', methods=['POST'])
def new_transaction():  #TODO Tu są dodawane wartości ze strony
# get the value passed in from the client
    values = request.get_json()
# check that the required fields are in the POST'ed data
    required_fields = ['id', 'address', 'name_surname', 'condition']
    if not all(k in values for k in required_fields):
        return ('Missing fields', 400)
    # create a new transaction
    index = blockchain.add_transaction(
        values['id'],
        values['address'],
        values['name_surname'],
        values['condition'],
    )
    response = {'message': f'Transaction will be added to Block {index}'}
    return (jsonify(response), 201)
@views.route('/nodes/add_nodes', methods=['POST'])
def add_nodes():
# get the nodes passed in from the client
    values = request.get_json()
    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Missing node(s) info", 400
    for node in nodes:
        Blockchain.add_node(node)
    response = {
        'message': 'New nodes added',
        'nodes': list(blockchain.nodes),
        }
    return jsonify(response), 201
@views.route('/nodes/sync', methods=['GET'])
def sync():
    updated = Blockchain.update_blockchain()
    if updated:
        response = {
            'message': 'The blockchain has been updated to the latest',
            'blockchain': blockchain.chain
            }
    else:
        response = {
            'message': 'Our blockchain is the latest',
            'blockchain': blockchain.chain
        }
    return jsonify(response), 200

