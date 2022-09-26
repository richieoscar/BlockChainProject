from blockchain.block_chain import BlockChain


class BlocChainService:
    def __init__(self):
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
        new_block = self._blockChain.create_block(new_proof, previous_hash)
        response = {
            "message": "Congratulations You just mined a block!",
            "index": new_block['index'],
            "timestamp": new_block['timestamp'],
            "proof": new_block['proof'],
            "previous_hash": new_block['previous_hash']
        }
        return response
