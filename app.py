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
    
    # Convert the result into JSON format
    assets = []
    for row in rows:
        asset = {
            'asset_id': row[0],
            'asset_name': row[1],
            'asset_type': row[2],
            'location': row[3],
            'status': row[4]
        }
        assets.append(asset)

    return jsonify(assets), 200



#Example of converting XML to JSON
@app.route('/assets/xml', methods=['POST'])
def add_asset_from_xml():
    xml_data = request.data
    json_data = xmltodict.parse(xml_data)
    
    # Extract asset details from XML
    asset_name = json_data['asset']['name']
    asset_type = json_data['asset']['type']
    location = json_data['asset']['location']
    status = json_data['asset']['status']
    
    # Insert the new asset into the database
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO assets (asset_name, asset_type, location, status) VALUES (%s, %s, %s, %s)",
            (asset_name, asset_type, location, status)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()  # If there’s an error, rollback the transaction
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()
    
    return jsonify({"message": "Asset added successfully"}), 201
    

def test_get_assets():
    with app.test_client() as client:
        response = client.get('/assets')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)  # Check that the response is a list
        assert len(data) > 0  # Ensure at least one asset is returned
        assert 'asset_name' in data[0]  # Ensure the asset structure is correct
        
        

if __name__ == '__main__':
    app.run(debug=True)