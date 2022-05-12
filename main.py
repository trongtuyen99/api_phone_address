from flask import Flask, jsonify, request
from module import Extractor


app = Flask(__name__)
extractor = Extractor()


@app.route('/get_phone_address', methods=['POST', 'GET'])
def json_example():
    request_data = request.get_json()
    message = request_data['message']
    result = extractor.process(message)
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)