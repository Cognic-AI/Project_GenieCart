from flask import Flask, request, jsonify
from flask_cors import CORS
import firestoreAutoDB as db


app = Flask(__name__)
CORS(app)


@app.route('/api/delete', methods=['GET'])
def delete():
    database = db.FirestoreDB()
    database.deleteExpired()
    return jsonify({'message': 'Expired documents deleted'}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=False, port=9000, threaded=True, use_reloader=False)