from flask import Flask, jsonify
import service

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


@app.route('/chains', methods=['GET'])
def get_chains():
    return jsonify(service.get_chains()), 200


@app.route('/mine-block', methods=['GET'])
def mine_block():
    response = service.mine_block()
    return jsonify(response), 200


def run():
    app.run(host='0.0.0.0', port=5000)
