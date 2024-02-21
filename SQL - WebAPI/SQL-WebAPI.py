#pip install sqlalchemy
#pip install Flask
#pip install pyodbc

from flask import Flask, jsonify
from sqlalchemy import create_engine, MetaData, Table, Column, String

app = Flask(__name__)

# Connect to the SQL Server database
engine = create_engine('mssql+pyodbc://username:password@server/database_name?driver=ODBC+Driver+17+for+SQL+Server')

# Define the 'countries' table
metadata = MetaData()
countries = Table('countries', metadata,
    Column('id', String, primary_key=True),
    Column('name', String),
    Column('capital', String)
)

# Route to get all items from SQL Server
@app.route('/api/items', methods=['GET'])
def get_all_items():
    try:
        # Create a database connection
        connection = engine.connect()

        # Execute a SELECT query
        result = connection.execute(countries.select())

        # Fetch all rows from the result
        items = [{'name': row['name'], 'capital': row['capital']} for row in result]

        # Close the database connection
        connection.close()

        return jsonify({"items": items})

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Route to get an item by name from SQL Server
@app.route('/api/items/<string:country_name>', methods=['GET'])
def get_item_by_name(country_name):
    try:
        # Create a database connection
        connection = engine.connect()

        # Execute a SELECT query with a WHERE clause
        result = connection.execute(countries.select().where(countries.c.name.ilike(country_name)))

        # Fetch the first row from the result
        row = result.fetchone()

        # Close the database connection
        connection.close()

        if row:
            item = {'name': row['name'], 'capital': row['capital']}
            return jsonify({"item": item})
        else:
            return jsonify({"message": "Country not found"}), 404

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
