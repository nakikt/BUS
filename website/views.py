from flask import Blueprint
from .blockchain import Blockchain
from . import blocks, PORT
from flask import jsonify, request
import requests
from .methods import mine_block, New_blockchains

views = Blueprint("views", __name__)

@views.route("/")
@views.route("/home")
def home():
    response =[]

    for block in blocks:
        response.append(str( {
            'id': block.last_block['property'][-1]['id'],
            'address': block.last_block['property'][-1]['address'],
            'time': block.last_block['timestamp'],
            'name_surname': block.last_block['property'][-1]['name_surname'],
            'condition': block.last_block['property'][-1]['condition'],
        }))

    return jsonify(response), 200

@views.route("/history")
def history():
    response =[]
    for block in blocks:
        response.append(str({
            'id': block.last_block['property'][-1]['id'],
            'address': block.last_block['property'][-1]['address'],
            'time': block.last_block['timestamp'],
            'name_surname': block.last_block['property'][-1]['name_surname'],
            'condition': block.last_block['property'][-1]['condition'],
        }))
        if len(block.chain)> 1:
            for i in range(len(block.chain)-2):
                response.append(str({
                    'id': block.chain[i+1]['property'][-1]['id'],
                    'address': block.chain[i+1]['property'][-1]['address'],
                    'time': block.chain[i+1]['timestamp'],
                    'name_surname': block.chain[i+1]['property'][-1]['name_surname'],
                    'condition': block.chain[i+1]['property'][-1]['condition'],
                }))

    return jsonify(response), 200


@views.route('/edit', methods=['GET', 'POST'])
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
        response = str({
            'Message: The validity of the block was checked by other nodes and rejected.'
        })
        print( 'The validity of the block was checked by other nodes and rejected.')
        return (jsonify(response), 201)
    print('The validity of the block was checked by other nodes')
    try:
        mine_block(blocks[id], values['id'], values['address'], values['name_surname'], values['condition'])
        print('Block was mined to the blockchain')
    except:
        print('Failed to add block to blockchain')
    try:
        neighbours = blocks[int(id)].nodes
        for node in neighbours:
            #blocks[id].update_blockchain(id)
            requests.get(f'http://{node}//nodes/sync/{id}')

    except:
         print("Problem with sync")
    response = str({'Block was successfully added'})
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
    try:
        new_blockchain = New_blockchains(f'new_blockchain{id}')
        new_blockchain.name = Blockchain()
        blocks.append(new_blockchain.name)
        # new = Blockchain()
        # blocks.append(new[-1])
        print(f'Blockchain #{id} has been added')
    except:
        print('Problem with adding new blockchain')
    # for block in blocks:
    #     print(block.chain)
    try:

        mine_block(blocks[-1], values['id'], values['address'], values['name_surname'], values['condition'])
        print('Block was mined')
    except:
        print('Failed to add block to blockchain')
    # try:

    blocks[int(id)].add_node("http://127.0.0.1:5000")
    blocks[int(id)].add_node("http://127.0.0.1:5001")
    blocks[int(id)].add_node("http://127.0.0.1:5002")
    blocks[int(id)].add_node("http://127.0.0.1:5003")
    neighbours = blocks[int(id)].nodes
    for node in neighbours:
        print(node)
        if node != '127.0.0.1:5000':
            requests.get(f'http://{node}//addblockchain/{id}')

    response = {'message' :'Block was successfully added'}


    return (jsonify(response), 201)


