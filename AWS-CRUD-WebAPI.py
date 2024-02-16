# Installs
# pip install Flask
# pip install boto3

from flask import Flask, jsonify, request
import boto3

# Enable webapi
app = Flask(__name__)

# Set up AWS credentials (you can also use environment variables or IAM roles)
dynamodb = boto3.resource('dynamodb', region_name='eu-central-1', aws_access_key_id='YOUR_KEY', aws_secret_access_key='YOUR_SECRET')
table = dynamodb.Table('demo')

# Endpoint to get all items from DynamoDB table
@app.route('/api/items', methods=['GET'])
def get_all_items():
    try:
        response = table.scan()
        items = response.get('Items', [])
        return jsonify(items)
    except Exception as e:
        print(e)
        return jsonify({'error': 'Internal Server Error'}), 500

# Endpoint to get a specific item by ID
@app.route('/api/items/<item_id>', methods=['GET'])
def get_item(item_id):
    try:
        response = table.get_item(Key={'id': int(item_id)})
        item = response.get('Item')
        if item:
            return jsonify(item)
        else:
            return jsonify({'error': 'Item not found'}), 404
    except Exception as e:
        print(e)
        return jsonify({'error': 'Internal Server Error'}), 500
    
# Endpoint to add a new item to DynamoDB
@app.route('/api/items', methods=['POST'])
def add_item():
    try:
        data = request.get_json()
        new_item = {
            'id': int(data['id']),
            'test': data['test'],
            # Add other attributes as needed
        }
        table.put_item(Item=new_item)
        return jsonify({'message': 'Item added successfully'}), 201
    except Exception as e:
        print(e)
        return jsonify({'error': 'Internal Server Error'}), 500

# Endpoint to update an existing item in DynamoDB
@app.route('/api/items/<item_id>', methods=['PUT'])
def update_item(item_id):
    try:
        data = request.get_json()
        update_expression = 'SET '
        expression_attribute_values = {}

        for key, value in data.items():
            update_expression += f'{key} = :{key}, '
            expression_attribute_values[f':{key}'] = value

        update_expression = update_expression.rstrip(', ')

        table.update_item(
            Key={'id': int(item_id)},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values
        )

        return jsonify({'message': 'Item updated successfully'}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': 'Internal Server Error'}), 500

# Endpoint to delete an item from DynamoDB
@app.route('/api/items/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    try:
        
        table.delete_item(Key={'id': int(item_id)})
        return jsonify({'message': 'Item deleted successfully'}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(debug=True)