from blockchain.rich_coin import BlockChain
from uuid import uuid4


class RichCoinService:
    def __init__(self):
        self._node_address = str(uuid4()).replace('-', '')
        self._blockChain = BlockChain()

    def get_chains(self):
        response = {
            "chain": self._blockChain.get_chain(),
            "length": len(self._blockChain.get_chain())
        }
        return response

    def mine_block(self):
        previous_block = self._blockChain.get_previous_block()
        previous_proof = previous_block["proof"]
        new_proof = self._blockChain.proof_of_work(previous_proof)
        previous_hash = self._blockChain.hash_block(previous_block)
        self._blockChain.add_transaction(sender=self._node_address, receiver='Oscar', amount=2)
        new_block = self._blockChain.create_block(new_proof, previous_hash)
        response = {
            "message": "Congratulations You just mined a block!",
            "index": new_block['index'],
            "timestamp": new_block['timestamp'],
            "proof": new_block['proof'],
            "previous_hash": new_block['previous_hash'],
            "transactions": new_block["transactions"]
        }
        return response

    def add_transaction(self, transaction):
        block_index = self._blockChain.add_transaction(transaction['sender'], transaction['receiver'],
                                                       transaction['amount'])
        response = {
            "message": "This Transaction will be added to the block",
            "block_index": block_index
        }
        return response

    def connect_nodes(self, nodes):
        for node in nodes:
            self._blockChain.add_nodes(node)
        response = {
            "message": "Nodes connected to The RichCoin Blockchain",
            "nodes": list(self._blockChain.get_nodes())
        }
        return response

    def validate_chain(self):
        return self._blockChain.is_chain_valid()

    def replace_chain(self):
        return self._blockChain.replace_chain()
