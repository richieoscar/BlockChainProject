from blockchain import blockchain


def get_chains():
    blockChain = blockchain.BlockChain()
    response = {
        "chain": blockChain.get_chain(),
        "length": len(blockChain.get_chain())
    }
    return blockChain.get_chain()


def mine_block():
    blockChain = blockchain.BlockChain()
    previous_block = blockChain.get_previous_block()
    previous_proof = previous_block["proof"]
    new_proof = blockChain.proof_of_work(previous_proof)
    previous_hash = blockChain.hash_block(previous_block)
    new_block = blockChain.create_block(new_proof, previous_hash)
    response = {
        "message": "Congratulations You just mined a block!",
        "index": new_block['index'],
        "timestamp": new_block['timestamp'],
        "proof": new_block['proof'],
        "previous_hash": new_block['previous_hash']
    }
    return response
