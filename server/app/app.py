import redis
import config
import json
from flask import Flask, jsonify, request, make_response, abort
from flask_jwt import JWT, jwt_required, current_identity
from flask_cors import CORS
from user_auth import User, authenticate, identity

redis_server = redis.StrictRedis(
    host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_ID
)

User(1, "RCcar-Rpi", "lwjg#?kXTV&SCreh46")

app = Flask(__name__)
app.debug = True
CORS(app)
app.config["SECRET_KEY"] = "super-secret-key-zep-123"

jwt = JWT(app, authenticate, identity)


@app.route("/post-message", methods=["POST"])
@jwt_required()
def receive_message():

    if not request.json:
        abort(400)
    if "data" not in request.json:
        abort(400)

    payload = request.json

#    if not isinstance(payload["data"], list):
#        abort(400)

    try:
        redis_server.rpush(config.INPUT_QUEUE, json.dumps(payload))
    except Exception as e:
        app.logger.exception(e)

    return make_response(jsonify({"success": True}))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=False)