from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data
data = [
    {"id": 1, "name": "yoni"},
    {"id": 2, "name": "moshe"},
    {"id": 3, "name": "shmulik"}
]

# Route to get all items
@app.route('/api/items', methods=['GET'])
def get_items():
    return jsonify({"items": data})

# Route to get a specific item by ID
@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((item for item in data if item['id'] == item_id), None)
    if item:
        return jsonify({"item": item})
    else:
        return jsonify({"message": "Item not found"}), 404

# Route to add a new item
@app.route('/api/items', methods=['POST'])
def add_item():
    new_item = request.get_json()
    new_item['id'] = len(data) + 1
    data.append(new_item)
    return jsonify({"message": "Item added successfully"})

# Route to delete an item by ID
@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global data
    data = [item for item in data if item['id'] != item_id]
    return jsonify({"message": "Item deleted successfully"})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)