import hashlib
import json
from time import time
from uuid import uuid4

import requests
from flask import Flask, jsonify, request
from urllib.parse import urlparse

class Blockchain():

	def __init__(self):
		self.chain = []
		self.current_transactions = []
		self.nodes = set()
		# Create the genesis block
		self.new_block(previous_hash=1, proof=100)

	def register_node(self, address):
		parsed_url = urlparse(address)
		self.nodes.add(parsed_url.netloc)

	def valid_chain(self, chain):
		last_block = chain[0]
		current_index = 1
		while current_index < len(chain):
			block = chain[current_index]
			print('{}'.format(block))
			print('{}'.format(last_block))
			print("\n----------\n")
			if block['previous_hash'] != self.hash(last_block):
				return False
			if not self.valid_proof(last_block['proof'], block['proof']):
				return False
			last_block = block
			current_index += 1
		return True

	def resolve_conflicts(self):
		neighbours = self.nodes
		new_chain = None
		max_length = len(self.chain)
		for node in neighbours:
			response = requests.get('http://{}/chain'.format(node))
			if response.status_code == 200:
				length = response.json()['chain']
				chain = response.json()['chain']
				if length > max_length and self.valid_chain(str(chain)):
					max_length = length
					new_chain = chain
		if new_chain:
			self.chain = new_chain
			return True
		return False


	def new_block(self, proof, previous_hash=None):
		# Creates a new Block and adds it to the chain
		"""
		Create a new Block in the Blockchain

		:param proof: <int> The proof given by the Proof of Work algorithm
		:param previous_hash: (Optional) <str> Hash of previous Block
		:return: <dict> New Block
		"""

		block = {
			'index': len(self.chain),
			'timestamp': time(),
			'transactions': self.current_transactions,
			'proof': proof,
			'previous_hash': previous_hash or self.hash(self.chain[-1]),
		}

		# Reset the current list of transactions
		self.current_transactions = []
		self.chain.append(block)
		return block

	def new_transaction(self, user, diary):
		# Adds a new transaction to the list of transactions
		"""
		Creates a new transaction to go into the next mined Block

		:param sender: <str> Adress of the Sender
		:param recipient: <str> Address of the Recipient
		:param amount: <int> Amount
		:return: <int> The index of the Block that will hold this transaction
		"""

		self.current_transactions.append({
				'user': user,
				'diary': diary,
			})

		return self.last_block['index'] + 1

	@staticmethod
	def hash(block):
		# Hashes a Block
		"""
		Creates a SHA-256 hash of a Block

		:param block: <dict> Block
		:return: <str>
		"""

		# We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
		block_string = json.dumps(block, sort_keys=True).encode()
		return hashlib.sha256(block_string).hexdigest()

	@property
	def last_block(self):
		# Returns the last Block in the chain
		return self.chain[-1]

	def proof_of_work(self, last_proof):
		"""
		Simple Proof of Work Algorithm:
		- Find a number p' such that hash(pp') contains leading 4 zeros, where p is the previous p'
		- p is the previous proof, and p' is the new proof

		:param last_proof: <int>
		:return: <int>
		"""

		proof = 0
		while self.valid_proof(last_proof, proof) is False:
			proof += 1

		return proof

	@staticmethod
	def valid_proof(last_proof, proof):
		"""
		Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?

		:param last_proof: <int> Previous Proof
		:param proof: <int> current Proof
		:return: <bool> True if correct, False if not.
		"""

		guess = '{}{}'.format(last_proof,proof).encode()
		guess_hash = hashlib.sha256(guess).hexdigest()
		return guess_hash[:4] == "0000"

# Instantiate our Node
app = Flask(__name__)
app.debug = True

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
	# We run the proof of work algorithm to get the next proof...
	last_block = blockchain.last_block
	last_proof = last_block['proof']
	proof = blockchain.proof_of_work(last_proof)

	# We must receive a reward for finding the proof.
	# The sender is "0" to signify that this node has mined a new coin.
	blockchain.new_transaction(
		user="0",
		diary=node_identifier,
	)

	# Forge the new Block by adding it to the chain
	previous_hash = blockchain.hash(last_block)
	block = blockchain.new_block(proof, previous_hash)

	response = {
		'message': "New Block Forged",
		'index': block['index'],
		'transaction': block['transactions'],
		'proof': block['proof'],
		'previous_hash': block['previous_hash'],
	}
	return jsonify(response), 200


#@app.route('/tansactions/get')

def get_transactions():
	user_info = {'user': 0, 'diary': 10}
	content_type = {'content-type': 'application/json'}
	requests.post("http://localhost:5001/tansactions/new",
				   data=json.dumps(user_info),
				   headers = content_type)

@app.route('/tansactions/new', methods=['POST'])
def new_transaction():
	#get_transactions()
	values = request.get_json()

	# Check that the required fields are in the POST'ed data
	required = ['user', 'diary']
	if not all(k in values for k in required):
		return 'Missing values', 400

	# Create a new Transaction
	index = blockchain.new_transaction(values['user'], values['diary'])

	response = {'message': 'Transaction will be added to the Block {}'.format(index)}
	return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def full_chain():
	response = {
		'chain': blockchain.chain,
		'length':len(blockchain.chain),
	}
	return jsonify(response), 200

#@app.route('/address')
#def get_address():
#	Address = {'nodes'}
#	content_type = {'content-type': 'application/json'}
#    r = requests.post("http://localhost:5001/nodes/register", data=json.dumps(Address), headers = content_type)
#	return r

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
	values = request.get_json()
	nodes = values.get('nodes')
	if nodes is None:
		return "Error: Please supply a valid list of nodes", 400
	for node in nodes:
		blockchain.register_node(node)
	response = {
		'message': 'New nodes have been added',
		'total_nodes': list(blockchain.nodes),
	}
	return jsonify(response), 201

@app.route('/nodes/resolve', methods=['GET'])
def consensus():
	replaced = blockchain.resolve_conflicts()
	if replaced:
		response = {
			'message': 'Our chain was replaced',
			'new_chain': blockchain.chain
		}
	else:
		response = {
			'message': 'Our chain is authoritative',
			'chain': blockchain.chain
		}
	return jsonify(response), 200


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5001)
