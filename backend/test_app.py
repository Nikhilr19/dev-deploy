import pytest
from app import app, dynamodb

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def setup_module(module):
    """ Setup any state specific to the execution of the given module."""
    global table
    table = dynamodb.Table('historymanager')
    # Optionally create the table here if it does not exist
    # This would require more setup, including defining the schema

def teardown_module(module):
    """Teardown any state that was previously setup with a setup_module
    method."""
    # Cleanup the table to remove all items
    # Scan and delete can be expensive, better approach is to delete the table itself if that's feasible
    response = table.scan()
    items = response['Items']
    for item in items:
        table.delete_item(Key={'subject_id': item['subject_id']})

def test_create_item(client):
    """Test creating an item."""
    response = client.post('/historymanager', json={'subject_id': '123', 'info': 'test info'})
    assert response.status_code == 201
    assert response.json['message'] == 'Item created successfully'
    print('itemcreated')

def test_get_item(client):
    """Test getting an item."""
    # Assuming the item '123' has been added in a prior test or setup
    response = client.get('/historymanager/123')
    assert response.status_code == 200
    # Adjust the assertion to correctly reference the nested structure
    assert response.json['item'] == {'subject_id': '123', 'info': 'test info'}


def test_update_item(client):
    """Test updating an item."""
    response = client.put('/historymanager/123', json={'info': 'updated info'})
    assert response.status_code == 200
    assert response.json['message'] == 'Item updated'
    assert response.json['updated_attributes']['info'] == 'updated info'

def test_delete_item(client):
    """Test deleting an item."""
    response = client.delete('/historymanager/123')
    assert response.status_code == 200
    assert response.json['message'] == 'Item deleted'
