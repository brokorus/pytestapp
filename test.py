import psycopg2
import http.server
import socketserver
import json
import os
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
verify=False

vault_address = os.environ['VAULT_ADDR']
gitorg = os.environ['GITORG']
appname = os.environ['APPNAME']
dc = os.environ['DC']
role_id = os.environ['ROLE_ID']
secret_id = os.environ['SECRET_ID']


data = {"role_id": role_id, "secret_id": secret_id}
login_secret = requests.post("{}/v1/auth/{}/{}/login".format(vault_address,gitorg,appname), data=data, verify=False)
vault_token = json.loads(login_secret.content)['auth']['client_token']

headers = {
    'X-Vault-Token': vault_token,
}

simple_secret = requests.get("{}/v1/{}/{}/{}/kv/secret-thing".format(vault_address,gitorg,appname,dc), verify=False, headers=headers)
db_secret = requests.get("{}/v1/{}/{}/{}/postgres/creds/{}-{}-{}".format(vault_address,gitorg,appname,dc,gitorg,appname,dc), verify=False, headers=headers)
print(db_secret.content)
#print(simple_secret.content)
#print(json.loads(simple_secret.content)['data']['gitorg'])

DBPASS = json.loads(db_secret.content)['data']['password']
DBUSERNAME= json.loads(db_secret.content)['data']['username']
DBHOSTNAME = "localhost"
DBPORT = "5432"
DBTABLE = "{}persons".format(gitorg)

try:
    connect_str = f"port=5432 dbname={gitorg} user={DBUSERNAME} host={DBHOSTNAME} password={DBPASS}"
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * from {DBTABLE}")
    conn.commit() # <--- makes sure the change is shown in the database
    rows = cursor.fetchall()
    data = rows
    print(rows)
    cursor.close()
    conn.close()
except Exception as e:
    print("Uh oh, can't connect. Invalid dbname, user or password?")
    print(e)


with open("index.html", "w") as w:
    w.write(f"""\
<html>
    <head>
        <title>Python is awesome!</title>
    </head>
    <body>
        <h1>Vault Demo</h1>
        <p>Gitorg: {gitorg}</p>
        <p>Appname: {appname}</p>
        <p>DataCenter: {dc}</p>
        <p>Role_ID: {role_id}</p>
        <p>Secret_ID: {secret_id}</p>
        <p>Token: {vault_token}</p>
        <p>Temporary DBPassword: {DBPASS}</p>
        <p>Temporary DBUsername: {DBUSERNAME}</p>
        <p>Database information</p>
        <p>{data[:10]}</p>
    </body>
</html>
""")

PORT = 8080
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving on {PORT}")
    httpd.serve_forever()
