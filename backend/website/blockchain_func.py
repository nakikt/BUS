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

blockchain_func = Blueprint("blockchain_func", __name__)


@blockchain_func.route("/nodes/sync/<id>", methods=['GET'])
def sync(id):
    updated = blocks[int(id)].update_blockchain(id)
    if updated:
        response = {
            'message':
                'The blockchain has been updated to the latest',
        }
    else:
        response = {
            'message': 'Our blockchain is the latest',

        }
    return response, 200


@blockchain_func.route("/blockchain/<id>", methods=['GET'])
def full_chain(id):

    response = {
            'chain': blocks[int(id)].chain,
            'length': len(blocks[int(id)].chain),
        }

    return jsonify(response), 200