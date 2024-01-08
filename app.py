"""
Flask App
"""

from flask import Flask, request, jsonify  # Import Flask and other necessary modules at the top
from utils import Logger
from backend import Backend

app = Flask(__name__)

logger = Logger.setup_logger()
error_logger = Logger.setup_logger('error')


@app.route('/', methods=['GET', 'POST'])
def health_check():
    """
    Health Check
    """
    return jsonify({
        'status_code': 200,
        'status_msg': 'success'
    })


@app.route('/chat/<string:version>', methods=['POST'])
def chat(version: str = 'v1'):
    """
    The main chat function
    """
    # Default Response
    response = {
        "status_code": 0,  # Initialize to 0
        "status_msg": "",  # Initialize to an empty string
        "data_layer": {}  # Initialize to an empty dictionary
    }

    # Payload Process
    try:
        request_body = request.get_json(force=True)
    except:
        request_body = {}

    try:
        logger.info("----------------------Start To Get Response----------------------")
        response["data_layer"] = Backend(version, request_body)
        response["status_code"] = 200
        response["status_msg"] = "Success"
        logger.info("----------------------Successfully GET Response----------------------")
    except Exception as e:
        error_logger.error(str(e), exc_info=True)
        response["status_code"] = 500
        response["status_msg"] = str(e)

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=False)