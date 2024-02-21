import boto3
# Set up AWS credentials (you can also use environment variables or IAM roles)
dynamodb = boto3.resource('dynamodb', region_name='eu-central-1', aws_access_key_id='AKIA3JDNG3KJK5AL6LHP', aws_secret_access_key='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')
table = dynamodb.Table('demo')


# Create the DynamoDB table.
table = dynamodb.create_table(
    TableName='tabletest',
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