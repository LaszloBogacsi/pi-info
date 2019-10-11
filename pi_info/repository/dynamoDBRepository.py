import boto3
import json

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

table_name = 'dev-devices'
table = dynamodb.Table(table_name)

response = table.put_item(
    Item={
        'group_id': '222',
        'device_id': '22',
        'name': 'one lights',
        'is_group': False,
        'location': 'living room',
        'delay': 0
    }
)

print("PutItem succeeded:")
print(json.dumps(response, indent=4))

