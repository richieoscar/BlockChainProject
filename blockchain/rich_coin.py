import hashlib
import json
import logging
from datetime import datetime
from urllib.parse import urlparse
import requests


class BlockChain:

    def __init__(self):
        self._chain = []
        self._transactions = []
        self.create_block(proof=1, previous_hash='0')
        self._difficulty = 4
        self._leading_zeroes = "0000"
        self._nodes = set()

    def set_difficulty(self, difficulty):
        if difficulty > self._difficulty:
            self._difficulty = difficulty
            for i in range(self._difficulty + 1):
                self._leading_zeroes += "0"

    def get_difficulty(self):
        return self._leading_zeroes

    def get_chain(self):
        return self._chain


    def get_nodes(self):
        return self._nodes

    def create_block(self, proof, previous_hash):
        block = {
            "index": len(self._chain) + 1,
            "timestamp": str(datetime.now()),
            "proof": proof,
            "previous_hash": previous_hash,
            "transactions": self._transactions
        }
        self._transactions.clear()
        self._chain.append(block)
        return block

    def get_previous_block(self):
        return self._chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof - previous_proof).encode()).hexdigest()
            logging.info(f"Difficulty{self._difficulty}")
            logging.info(f"HashOperation = {hash_operation}")
            if hash_operation[:self._difficulty] == self._leading_zeroes:
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash_block(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self):
        if len(self._chain) == 1:
            return True
        previous_block = self._chain[0]
        block_index = 1
        for i in range(len(self._chain) - 1):
            current_block = self._chain[block_index]
            if current_block["previous_hash"] != self.hash_block(previous_block):
                return False
            previous_proof = previous_block["proof"]
            current_block_proof = current_block["proof"]
            hash_operation = hashlib.sha256(str(current_block_proof - previous_proof).encode()).hexdigest()
            if hash_operation[:self._difficulty] != self._leading_zeroes:
                return False
            previous_block = current_block
            block_index += 1

        return True

    def chain_valid(self, chain):
        if len(chain) == 1:
            return True
        previous_block = chain[0]
        block_index = 1
        for i in range(len(chain) - 1):
            current_block = chain[block_index]
            if current_block["previous_hash"] != self.hash_block(previous_block):
                return False
            previous_proof = previous_block["proof"]
            current_block_proof = current_block["proof"]
            hash_operation = hashlib.sha256(str(current_block_proof - previous_proof).encode()).hexdigest()
            if hash_operation[:self._difficulty] != self._leading_zeroes:
                return False
            previous_block = current_block
            block_index += 1

        return True

    def add_transaction(self, sender, receiver, amount):
        self._transactions.append({
            "sender": sender,
            "receiver": receiver,
            "amount": amount
        })
        previous_block = self.get_previous_block()
        return previous_block["index"] + 1

    def add_nodes(self, address):
        parsed_url = urlparse(address)
        self._nodes.add(parsed_url.netloc)

    def replace_chain(self):
        # consensus check
        network = self._nodes
        longest_chain = None
        max_length = len(self._chain)
        # make request to get chain
        for node in network:
            response = requests.get(f"http://{node}/get-chain")
            if response.status_code == 200:
                chain = response.json()["chain"]
                length = response.json()["length"]
                if length > max_length and self.chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self._chain = longest_chain
            return True
        return False
