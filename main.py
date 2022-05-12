from flask import Flask, jsonify, request


app = Flask(__name__)


@app.route('/get_phone_address', methods=['POST', 'GET'])
def json_example():
    request_data = request.get_json()

    return jsonify(request_data)


if __name__ == '__main__':
    app.run(debug=True)