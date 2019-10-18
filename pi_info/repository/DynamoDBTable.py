import json
import boto3

from pi_info.repository.GroupDeviceDTO import GroupDeviceDTO


class DynamoDBTable:
    MAX_BATCH_REQUEST_SIZE = 25

    def __init__(self, table_name: str) -> None:
        self.table_name = table_name
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        self.table = dynamodb.Table(table_name)

    def put_item(self, item):
        response = self.table.put_item(Item=item.__dict__)

        print("PutItem succeeded:")
        print(json.dumps(response, indent=4))
        return response

    def batch_write(self, items: [GroupDeviceDTO]):
        with self.table.batch_writer() as batch_writer:
            for b in batch(items, self.MAX_BATCH_REQUEST_SIZE):
                for item in b:
                    item.group_id = str(item.group_id)
                    item_to_put = item.__dict__
                    batch_writer.put_item(Item=item_to_put)

    def update_item(self, item: GroupDeviceDTO):
        response = self.table.update_item(
            Key={
                'group_id': str(item.group_id),
                'device_id': str(item.device_id)
            },
            UpdateExpression="set d_name = :name, d_location=:location, delay=:delay",
            ExpressionAttributeValues={
                ':name': item.name,
                ':location': item.location,
                ':delay': item.delay
            },
            ReturnValues="UPDATED_NEW"
        )

        print("UpdateItem succeeded:")
        print(json.dumps(response, indent=4))


def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]
