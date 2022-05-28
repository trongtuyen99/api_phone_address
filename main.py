from flask import Flask, jsonify, request
from module import Extractor
import logging

LOG_FILE = './logs/log.txt'
logging.basicConfig(
                    format="%(asctime)s, %(msecs)d %(name)s %(levelname)s [ %(filename)s-%(module)s-%(lineno)d ]  : "
                           "%(message)s",
                    datefmt="%H:%M:%S",
                    handlers=[logging.FileHandler(LOG_FILE, 'a', 'utf-8')],
                    level=logging.WARNING)

logger = logging.getLogger("main_logger")
app = Flask(__name__)
extractor = Extractor()


@app.route('/get_phone_address', methods=['POST', 'GET'])
def json_example():
    request_data = request.get_json()
    message = request_data['message']
    username = request_data['username']
    chatfuel_id = request_data['chatfuel_id']
    result = extractor.process(message)

    message_log = f"{username}|{chatfuel_id}|{message}|{result['set_attributes']['phone_number']}|" \
                  f"{result['set_attributes']['ship_address']}"
    logger.info(message_log)
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
