import logging

from pi_info.repository.GroupDeviceDTO import GroupDeviceDTO
logger = logging.getLogger('dynamoDBRepository')


def put_item(table, item: GroupDeviceDTO):
    table.put_item(item)


def put_item_batch(table, items: [GroupDeviceDTO]):
    table.batch_write(items)
