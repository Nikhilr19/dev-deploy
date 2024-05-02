from flask import Flask, jsonify, request
import boto3

app = Flask(__name__)
dynamodb = boto3.resource('dynamodb')

# Assume you have a table 'historymanager' with a primary key 'subject_id'
table = dynamodb.Table('historymanager')

@app.route('/historymanager', methods=['POST'])
def create_item():
    item_data = request.get_json()
    table.put_item(Item=item_data)
    return jsonify(message='Item created successfully', data=item_data), 201

@app.route('/historymanager/<string:item_subject_id>', methods=['GET'])
def get_item(item_subject_id):
    response = table.get_item(Key={'subject_id': item_subject_id})
    item = response.get('Item')
    if not item:
        return jsonify(message='Item not found'), 404
    return jsonify(item=item)

@app.route('/historymanager/<string:item_subject_id>', methods=['PUT'])
def update_item(item_subject_id):
    item_data = request.get_json()
    response = table.update_item(
        Key={'subject_id': item_subject_id},
        UpdateExpression='set info = :i',
        ExpressionAttributeValues={
            ':i': item_data['info']
        },
        ReturnValues='UPDATED_NEW'
    )
    return jsonify(message='Item updated', updated_attributes=response['Attributes'])

@app.route('/historymanager/<string:item_subject_id>', methods=['DELETE'])
def delete_item(item_subject_id):
    table.delete_item(Key={'subject_id': item_subject_id})
    return jsonify(message='Item deleted')
    
@app.route('/')
def home():
    return jsonify(message="Welcome to the History Manager API"), 200


if __name__ == '__main__':
    app.run(debug=True)
