from flask import Blueprint,redirect, render_template, url_for
from .blockchain import Blockchain
from . import blocks, PORT
from flask import jsonify, request
from .models import User
import requests
from .methods import mine_block, New_blockchains
from flask_login import login_user, current_user, login_required
from.encryption import decryption, encryption


views = Blueprint("views", __name__)
#Strona główna; daje możliwość zalogowania opis do czego służy

@views.route("/")
@views.route("/home")
def home():
    return render_template("index.html")


#Wyświetla wszystkie książeczki zdrowia - uprawnienia do jej wyświetlania ma tylko doctor, doktor w tym widoku może wybrać, którego pacjenta chce podejrzeć książeczkę zdrowia
@views.route("/doctor")
@login_required
def doctor():
    response =[]
    # sprawdzenie czy zalogowana osoba to lekarz
    # user = User.query.filter_by(id=current_user.id).first()
    #if user.role != "A":
    #    return redirect(url_for("views.home"))
    for block in blocks:
        response.append( {
            'id': block.last_block['health_card'][-1]['id'],
            'name_surname': decryption(block.last_block['health_card'][-1]['name_surname']),
                # 'time': block.last_block['timestamp'],
            'birth_date': decryption(block.last_block['health_card'][-1]['birth_date']),
            'diseases': decryption(block.last_block['health_card'][-1]['diseases']),
            'vaccinations': decryption(block.last_block['health_card'][-1]['vaccinations']),
        })

    return render_template("doctor.html", response=response)
#Wyświetla wybraną książeczkę zdrowia

@views.route("/patient", methods=['GET'])
@login_required
def patient():
    #TODO sprawdzenie czy user to pacjent
    response = []

    user =current_user

    if user.role == 'D':
        return redirect(url_for('views.home'))

    id = user.blockchain_id

    id = int(id)

    response.append({
        'id': blocks[id].last_block['health_card'][-1]['id'],
        'name_surname': decryption(blocks[id].last_block['health_card'][-1]['name_surname']),
        'time': blocks[id].last_block['timestamp'],
        'birth_date': decryption(blocks[id].last_block['health_card'][-1]['birth_date']),
        'diseases': decryption(blocks[id].last_block['health_card'][-1]['diseases']),
        'vaccinations': decryption(blocks[id].last_block['health_card'][-1]['vaccinations']),
    })
    return render_template("patient.html", response=response)



@views.route("/doctor/<id>", methods=['GET','POST'])
@login_required
def doctor_view(id):
    response = []
    #TODO sprawdzenie czy to doktor

    id = int(id)
    if request.method=="GET":
        response.append({
            'id': blocks[id].last_block['health_card'][-1]['id'],
            'name_surname': decryption(blocks[id].last_block['health_card'][-1]['name_surname']),
            'time': blocks[id].last_block['timestamp'],
            'birth_date': decryption(blocks[id].last_block['health_card'][-1]['birth_date']),
            'diseases': decryption(blocks[id].last_block['health_card'][-1]['diseases']),
            'vaccinations': decryption(blocks[id].last_block['health_card'][-1]['vaccinations']),
        })
        return render_template("doctor_edit.html", response=response)
    elif request.method=="POST":
        disease = request.form.get("disease", None)
        vaccination = request.form.get("vaccination", None)

        # check that the required fields are in the POST'ed data
        # required_fields = ['id', 'name_surname', 'birth_date', 'diseases', 'vaccinations']
        # if not all(k in values for k in required_fields):
        #     print('Missing fields')
        # create a new transaction
        if disease is None:
            disease = blocks[id].last_block['health_card'][-1]['diseases']
        elif str(decryption(blocks[id].last_block['health_card'][-1]['diseases'])) == 'brak':
            disease = f'{encryption(disease)}'
        else:
            disease= str(decryption(blocks[id].last_block['health_card'][-1]['diseases'])) + ', ' + disease
            disease= f'{encryption(disease)}'

        if vaccination is None:
            vaccination = blocks[id].last_block['health_card'][-1]['vaccinations']
        elif str(decryption(blocks[id].last_block['health_card'][-1]['vaccinations'])) == 'brak':
            vaccination = f'{encryption(vaccination)}'
        else:
            vaccination = str(decryption(blocks[id].last_block['health_card'][-1]['vaccinations'])) + ', ' + vaccination
            vaccination = f'{encryption(vaccination)}'

        if not blocks[id].valid_new(id):
            response = str({
                'Message: The validity of the block was checked by other nodes and rejected.'
            })
            print('The validity of the block was checked by other nodes and rejected.')
        print('The validity of the block was checked by other nodes')

        try:
            mine_block(blocks[id], blocks[id].last_block['health_card'][-1]['id'], blocks[id].last_block['health_card'][-1]['name_surname'], blocks[id].last_block['health_card'][-1]['birth_date'], disease, vaccination)
            print('Block was mined to the blockchain')
        except:
            print('Failed to add block to blockchain')
        try:
            neighbours = blocks[int(id)].nodes
            for node in neighbours:
                # blocks[id].update_blockchain(id)
                requests.get(f'http://{node}//nodes/sync/{id}')

        except:
            print("Problem with sync")
        # response = str({'Block was successfully added'})
        response.append({
            'id': blocks[id].last_block['health_card'][-1]['id'],
            'name_surname': decryption(blocks[id].last_block['health_card'][-1]['name_surname']),
            'time': blocks[id].last_block['timestamp'],
            'birth_date': decryption(blocks[id].last_block['health_card'][-1]['birth_date']),
            'diseases': decryption(blocks[id].last_block['health_card'][-1]['diseases']),
            'vaccinations': decryption(blocks[id].last_block['health_card'][-1]['vaccinations']),
        })
        return render_template("doctor_edit.html", response=response)

# @views.route("/doctor/edit", methods=['GET', 'POST'])
# #@login_required
# def doctor_edit():
#     #TODO sprawdzenie czy to doktor
#     # get the value passed in from the client
#     values = request.get_json()
#     # check that the required fields are in the POST'ed data
#     required_fields = ['id','name_surname', 'birth_date', 'diseases', 'vaccinations']
#     if not all(k in values for k in required_fields):
#         return ('Missing fields', 400)
#     # create a new transaction
#     id = int(values['id'])
#     if not blocks[id].valid_new(id):
#         response = str({
#             'Message: The validity of the block was checked by other nodes and rejected.'
#         })
#         print('The validity of the block was checked by other nodes and rejected.')
#         return (jsonify(response), 201)
#     print('The validity of the block was checked by other nodes')
#     try:
#         mine_block(blocks[id], values['id'], values['name_surname'], values['birth_date'], values['diseases'], values['vaccinations'])
#         print('Block was mined to the blockchain')
#     except:
#         print('Failed to add block to blockchain')
#     try:
#         neighbours = blocks[int(id)].nodes
#         for node in neighbours:
#             # blocks[id].update_blockchain(id)
#             requests.get(f'http://{node}//nodes/sync/{id}')
#
#     except:
#         print("Problem with sync")
#     response = str({'Block was successfully added'})
#     return (jsonify(response), 201)
#
#
#
#
#
