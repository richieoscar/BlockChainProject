from flask import Flask, jsonify
import service
import logging

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

serv = service.BlocChainService()


@app.route('/chains', methods=['GET'])
def get_chains():
    return jsonify(serv.get_chains()), 200


@app.route('/mine-block', methods=['GET'])
def mine_block():
    logging.info("Inside- mineBlock() controoler")
    response = serv.mine_block()
    return jsonify(response), 200


def run():
    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    logging.info("Inside- mineBlock() controller")
    run()
