from utils import Logger
logger = Logger.setup_logger(__name__)
from backend import Backend
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods = ['GET','POST'])
def health_check():
    return jsonify({
        'status_code': 200,
        'status_msg': 'success'
    })

@app.route('/chat/<string:version>', methods = ['POST'])
def chat(version:str = 'v1'):
    # =================== Default Response ===================
    response = {
        "status_code" : int(),
        "status_msg" : str(),
        "data_layer" : dict()
    }
    # ==================== Payload Process =====================
    try:
        request_body= request.get_json(force = True)
    except:
        request_body = dict()

    try:
        logger.info(f"----------------------Start To Get Response----------------------")
        response["data_layer"] = Backend(version, request_body)
        response["status_code"] = 200
        response["status_msg"] = "Success"
        logger.info(f"----------------------Successfully GET Response----------------------")
    except Exception as e:
        logger.error(str(e), exc_info=True)
        response["status_code"] = 500
        response["status_msg"] = str(e)

    return jsonify(response)


    
if __name__ == '__main__':
    app.run(debug = True)