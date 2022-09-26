import hashlib
import json
import logging
from datetime import datetime


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


