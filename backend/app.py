from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

conn = psycopg2.connect(
database='joyous-orca-1109.decovid',
user='ankita',
password='trojangupta@1',
host='free-tier.gcp-us-central1.cockroachlabs.cloud',
port=26257
)
conn.set_session(autocommit=True)


@app.route('/user/add',  methods=['GET'])
def addUser():
    name = request.args.get('name')
    email = request.args.get('email')
    lat = request.args.get("lat")
    long = request.args.get("long")
    status = request.args.get("status")

    cur = conn.cursor()
    cur.execute(
        "UPSERT INTO USERS (email, name, longitude, latitude, status) VALUES ('"+email+"','"+name+"','"+long+"','"+lat+"','"+status+"')"
    )
    return {'status': 'Success'}

@app.route('/user/update', methods=['GET'])
def updateUser():
    email = request.args.get('email')
    status = request.args.get('status')

    cur = conn.cursor()
    cur.execute(
        "UPDATE USERS SET status = '"+status+"' WHERE email = '"+email+"'"
    )
    return {'status': 'Success'}

@app.route('/user/get')
def getUsers():
    cur = conn.cursor()
    cur.execute("SELECT email, name, latitude, longitude, status  FROM USERS")
    rows = cur.fetchall()
    row_array = []
    for row in rows:
        row_array.append([str(cell) for cell in row])
    response = jsonify({"users": row_array})
    return response

# if __name__ == '__main__':
#     app.run(debug=True, host='127.0.0.1', port='5000')
