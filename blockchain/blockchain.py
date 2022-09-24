import hashlib
import json
from datetime import datetime
from flask import Flask, jsonify
import logging


class BlockChain:

    def __init__(self):
        self._chain = []
        self.create_block(proof=1, previous_hash='0')
        self._difficulty = 4
        self._leading_zeroes = "0000"

    def set_difficulty(self, difficulty):
        if difficulty > self._difficulty:
            self._difficulty = difficulty
            for i in range(self._difficulty + 1):
                self._leading_zeroes += "0"

    def get_difficulty(self):
        return self._leading_zeroes

    def get_chain(self):
        return self._chain

    def create_block(self, proof, previous_hash):
        block = {
            "index": len(self._chain) + 1,
            "timestamp": str(datetime.now()),
            "proof": proof,
            "previous_hash": previous_hash
        }
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
        for i in range(len(self._chain)-1):
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



blockChain = BlockChain()
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


@app.route('/chains', methods=['GET'])
def get_chains():
    response = {
        "chain": blockChain.get_chain(),
        "length": len(blockChain.get_chain())
    }
    return jsonify(response), 200


@app.route('/mine-block', methods=['GET'])
def mine_block():
    response = mine()
    return jsonify(response), 200


@app.route("/validate-chain", methods=['GET'])
def validate_chain():
    isValid = blockChain.is_chain_valid()
    response = None
    if isValid:
        response = {
            "message": "Chain Integrity Successful"
        }
    else:
        response = {
            "message": "Chain Integrity Failed, We have a problem"
        }
    return jsonify(response), 200


@app.route("/get-block/<index>", methods=['GET'])
def get_block(index):
    chain = blockChain.get_chain()
    block = chain[int(index)]
    response = {
        "message": "Block Retrived Successfully",
        "block": block
    }
    return jsonify(response)


def mine():
    previous_block = blockChain.get_previous_block()
    previous_proof = previous_block["proof"]
    new_proof = blockChain.proof_of_work(previous_proof)
    logging.info(f"New proof{new_proof}")
    response = None
    if new_proof > 1:
        previous_hash = blockChain.hash_block(previous_block)
        new_block = blockChain.create_block(new_proof, previous_hash)
        response = {
            "message": "Congratulations You just mined a block!",
            "index": new_block['index'],
            "timestamp": new_block['timestamp'],
            "proof": new_block['proof'],
            "previous_hash": new_block['previous_hash']
        }
    else:
        response = {
            "message": "Keep Trying!",
        }
    return response


def run():
    app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    run()
