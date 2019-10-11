import boto3
import json

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

table_name = 'dev-devices'
table = dynamodb.Table(table_name)

response = table.put_item(
    Item={
        'group_id': '113',
        'device_id': '113',
        'name': 'one light',
        'is_group': False,
    }
)

print("PutItem succeeded:")
print(json.dumps(response, indent=4))

