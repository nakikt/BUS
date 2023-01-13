import sys
import hashlib
import json
from time import time
from uuid import uuid4
from flask import Flask, jsonify, request
import requests
from urllib.parse import urlparse

class Blockchain(object):
    difficulty_target = "0000"
    def hash_block(self, block):
# encode the block into bytes and then hashes it;
# ensure that the dictionary is sorted, or you'll
# have inconsistent hashes
        block_encoded = json.dumps(block,sort_keys=True).encode()
        return hashlib.sha256(block_encoded).hexdigest()
    def __init__(self):
        self.nodes = set()
# stores all the blocks in the entire blockchain
        self.chain = []
# temporarily stores the transactions for the current
# block
        self.current_transactions = []
# create the genesis block with a specific fixed hash
# of previous block genesis block starts with index 0
        genesis_hash = self.hash_block("genesis_block")
        self.append_block(hash_of_previous_block = genesis_hash, nonce = self.proof_of_work(0, genesis_hash, []))
# use PoW to find the nonce for the current block
    def proof_of_work(self, index, hash_of_previous_bloc, transactions, hash_of_previous_block=None):
# try with nonce = 0
        nonce = 0
# try hashing the nonce together with the hash of the
# previous block until it is valid
        while self.valid_proof(index, hash_of_previous_block, transactions, nonce) is False:
            nonce += 1
        return nonce
# check if the block's hash meets the difficulty target
    def valid_proof(self, index, hash_of_previous_block,transactions, nonce):
# create a string containing the hash of the previous
# block and the block content, including the nonce
        content = f'{index}{hash_of_previous_block}{transactions}{nonce}'.encode()
# hash using sha256
        content_hash = hashlib.sha256(content).hexdigest()
# check if the hash meets the difficulty target
        return content_hash[:len(self.difficulty_target)] == self.difficulty_target
# creates a new block and adds it to the blockchain
    def append_block(self, nonce, hash_of_previous_block):
        block = {
            'index': len(self.chain),
            'timestamp': time(),
            'transactions': self.current_transactions,
            'nonce': nonce,
            'hash_of_previous_block': hash_of_previous_block
            }
# reset the current list of transactions
        self.current_transactions = []
        # add the new block to the blockchain
        self.chain.append(block)
        return block
    def add_transaction(self, id, address,  name_surname, condition):
# adds a new transaction to the current list of
# transactions
        self.current_transactions.append({
            'id': id,
            'address': address,
            'name_surname': name_surname,
            'condition': condition,
            })
# get the index of the last block in the blockchain
# and add one to it this will be the block that the
# current transaction will be added to
        return self.last_block['index'] + 1
    @property
    def last_block(self):
    # returns the last block in the blockchain
        return self.chain[-1]
# --------------------
# add a new node to the list of nodes e.g.

    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
        print(parsed_url.netloc)
# determine if a given blockchain is valid
    def valid_chain(self, chain):
        last_block = chain[0] # the genesis block
        current_index = 1 # starts with the second block
        while current_index < len(chain):
# get the current block
            block = chain[current_index]
# check that the hash of the previous block is
# correct by hashing the previous block and then
# comparing it with the one recorded in the
# current block
            if block['hash_of_previous_block'] != self.hash_block(last_block):
                return False
# check that the nonce is correct by hashing the
# hash of the previous block together with the
# nonce and see if it matches the target
            if not self.valid_proof(current_index, block['hash_of_previous_block'],block['transactions'],block['nonce']):
                return False
# move on to the next block on the chain
            last_block = block
            current_index += 1
# the chain is valid
        return True
    def update_blockchain(self):
# get the nodes around us that has been registered
        neighbours = self.nodes
        new_chain = None
    # for simplicity, look for chains longer than ours
        max_length = len(self.chain)
    # grab and verify the chains from all the nodes in
    # our network
        for node in neighbours:
    # get the blockchain from the other nodes
            response = requests.get(f'http://{node}/blockchain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
        # check if the length is longer and the chain
        # is valid
            if length > max_length and self.valid_chain(chain):
                max_length = length
                new_chain = chain
# replace our chain if we discovered a new, valid
# chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True
        return False



