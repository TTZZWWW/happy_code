
from flask import Flask
from flask import request
from genesis import *
import json

node = Flask(__name__)
this_nodes_transactions = []


@node.route('/txion', methods=['POST'])
def transaction():
    if request.method == 'POST':
        new_txion = request.get_json()
        this_nodes_transactions.append(new_txion)
        print('New transaction')
        print('From: {}'.format(new_txion['from']))
        print('To: {}'.format(new_txion['to']))
        print('Amount: {}'.format(new_txion['amount']))
        return 'Transaction submission successful\n'


node.run()

miner_address = 'q3nf394hjg-random-miner-address-34nf3i4nflkn3oi'


def proof_of_work(last_proof):
    incrementor = last_proof + 1
    while not (incrementor % 9 == 0) and (incrementor % last_proof == 0):
        incrementor += 1
    return incrementor


@node.route('/mine', methods=['GET'])
def mine():
    last_block = block_chain[-1]
    last_proof = last_block.data['proof-of-work']
    proof = proof_of_work(last_proof)
    this_nodes_transactions.append(
        {'from': 'network', 'to': miner_address, 'amount': 1})
    new_block_data = {
        'proof-of-work': proof,
        'transactions': list(this_nodes_transactions)
    }
    new_block_index = last_block.index + 1
    new_block_timestamp = date.datetime.now()
    last_block_hash = last_block.hash
    this_nodes_transactions[:] = []
    mined_block = Block(new_block_index, new_block_timestamp, new_block_data, last_block_hash)
    block_chain.append(mined_block)
    return json.dumps(
        {
            'index': new_block_index,
            'timestamp': str(new_block_timestamp),
            'data': new_block_data,
            'hash': last_block_hash
        }
    ) + '\n'


@node.route('/blocks', methods=['GET'])
def get_blocks():
    chain_to_send = block_chain
    for block in chain_to_send:
        block_index = str(block.index)
        block_timestamp = str(block.timestamp)
        block_data = str(block.data)
        block_hash = block.hash
        block = {
            'index': block_index,
            'timestamp': block_timestamp,
            'data': block_data,
            'hash': block_hash
        }
    chain_to_send = json.dumps(chain_to_send)
    return chain_to_send


def find_new_chains():
    other_chains = []
    for node_url in peer_nodes:
        block = requests.get(node_url + '/blocks').content
        block = json.loads(block)
        other_chains.append(block)
    return other_chains


def consensus():
    other_chains = find_new_chains()
    longest_chain = block_chain
    for chain in other_chains:
        if len(longest_chain) < len(chain):
            longest_chain = chain
    block_chain = longest_chain






















