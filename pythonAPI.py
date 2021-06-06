#Importing the required libraries
import os
import requests
import json
import mariadb
from ldap3 import Server, Connection, SAFE_SYNC
from flask_cors import CORS
from flask import Flask, render_template, jsonify, request
from flask_restful import Resource, Api


#Setting up the Flask app
app = Flask(__name__)
app.config["DEBUG"] = False
api = Api(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}}) 

@app.route('/fetchUser')
def fetch_user(email):
    server = Server('india.rsystems.com')
    conn = Connection(server, 'ITHelpdeskChatBot', 'Welcome#@234rs', client_strategy=SAFE_SYNC, auto_bind=True)
    bind_response = conn.bind()
    search_base = 'DC=india,DC=rsystems,DC=com'
    search_filter = '(mail='+str(email)+')'
    status, result, response, _ = conn.search(search_base=search_base, search_filter=search_filter, search_scope='SUBTREE')
    if status == True:
        ls = str(response[0]['raw_dn']).split(',')
        u = ls[0].split('=')[1]
        return jsonify(u)
    else:
        return (None)

@app.route('/fetchDetails')
def fetch_details(email):
    # Module Imports

    try:
        conn = mariadb.connect(
        user="root",
        password="root@123",
        host="10.131.253.170",
        port=3306,
        database="rsystems"
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    cur = conn.cursor()
    q = "SELECT * from rsystems.rsi_user_email e, rsystems.rsi_user__cdata d where e.address='" + email + "' and e.user_id = d.user_id;"
    cur.execute(q)
    ls = []
    for i in cur:
        ls.append(i)
    if ls == []:
        return(None)
    else:
        r = {}
        r['mobile'] = ls[0][7]
        r['user_ip_phone'] = ls[0][8]
        r['location'] = ls[0][10]
        r['seat'] = ls[0][11]
        r['ip'] = ls[0][12]
        return jsonify(r)


@app.route('/createTicket', methods=['POST'])
def createTicket(self, dispatcher, tracker, domain):
    payload = json.loads(request.data)
    print(payload)
    url = "http://helpdeskchatbot.india.rsystems.com/api/http.php/tickets.json"
    payload = json.dumps(payload)
    headers = {
        'X-API-Key': '7EC22D6D61C7D21046152E86B7237D0E',
        'Content-Type': 'application/json'
        }
 
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    return jsonify(response.text)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)