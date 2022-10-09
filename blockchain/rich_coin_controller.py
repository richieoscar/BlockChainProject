from flask import Flask, jsonify, request
import rich_coin_service
import logging

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

serv = rich_coin_service.RichCoinService()


@app.route('/chains', methods=['GET'])
def get_chains():
    return jsonify(serv.get_chains()), 200


@app.route('/mine-block', methods=['GET'])
def mine_block():
    logging.info("Inside- mineBlock() controoler")
    response = serv.mine_block()
    return jsonify(response), 200


##add new transactions to the blockchain
@app.route('/add-transaction', methods=['POST'])
def add_transaction():
    transaction_request = request.get_json()
    transaction_keys = ['sender', 'receiver', 'amount']
    if not all(key in transaction_request for key in transaction_keys):
        return jsonify("Missing key field"), 400
    response = serv.add_transaction(transaction_request)
    return jsonify(response), 201


#connecting node
@app.route('/connect-nodes', methods=['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get("nodes")
    if nodes is None:
        return "No Nodes", 400
    response = serv.connect_nodes(nodes)
    return jsonify(response), 200

@app.route('/validate-chain', methods=['GET'])
def validate_chain():
    is_valid = serv.validate_chain()
    if is_valid:
        response = {'message': 'All good. The Blockchain is valid.'}
    else:
        response = {'message': 'Houston, we have a problem. The Blockchain is not valid.'}
    return jsonify(response), 200



def run():
    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    logging.info("Inside- mineBlock() controller")
    run()
