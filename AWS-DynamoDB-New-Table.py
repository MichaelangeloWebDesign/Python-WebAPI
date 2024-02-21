import boto3
# Set up AWS credentials (you can also use environment variables or IAM roles)
dynamodb = boto3.resource('dynamodb', region_name='eu-central-1', aws_access_key_id='YOUR_KEY', aws_secret_access_key='YOUR_SECRET')

# Create the DynamoDB table.
table = dynamodb.create_table(
    TableName='TABLE_NAME',
    KeySchema=[
        {
            'AttributeName': 'id',
            'KeyType': 'HASH'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'id',
            'AttributeType': 'N'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

# Wait until the table exists.
table.wait_until_exists()

# Print out some data about the table.
print(table.item_count)
