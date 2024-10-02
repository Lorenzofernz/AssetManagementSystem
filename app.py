from flask import Flask, request, jsonify # type: ignore
import psycopg2 # type: ignore
import xmltodict # type: ignore

app = Flask(__name__)

# Connect to the database
def connect_db():
    return psycopg2.connect(
        dbname='am_system_db',
        host='localhost',
        user='postgres',
        password=''
        )

# Fetch Asset data
@app.route('/assets', methods=['GET'])
def get_assets():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM assets')
    assets = cur.fetchall()
    conn.close()
    return jsonify(assets)


#Example of converting XML to JSON
@app.route('/assets/xml', methods=['POST'])
def add_asset_from_xml():
    xml_data = request.data
    json_data = xmltodict.parse(xml_data)
    asset_name = json_data['asset']['name']
    # asset_name to insert into the database
    

def test_get_assets():
    response = app.test_client().get('/assets')
    assert response.status_code == 200
    assert len(response.json) > 0