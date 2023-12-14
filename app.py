import logging
logging.basicConfig(level=logging.INFO)
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods = ['GET','POST'])
def HEALTH_CHECK():
    return jsonify({
        'status_code': 200,
        'status_msg': 'success'
    })

@app.route('/chat/<string:version>', methods = ['POST'])
def chatbot(version:str = 'v1'):
    from main import chat
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

    # ========================= POST =========================
    if request.method == 'POST':
        try:
            response["data_layer"] = chat(version, request_body)
            response["status_code"] = 200
            response["status_msg"] = "Success"
        
        except Exception as e:
            err_msg = f"{e}"
            logging.error(err_msg, exc_info=True)
            response["status_code"] = 500
            response["status_msg"] = err_msg
    # ========================= Other =========================
    else:
        response["status_code"] = 405
        response["status_msg"] = 'Method Not Allowed'
    
    return jsonify(response)


    
if __name__ == '__main__':
    app.run(debug = True)