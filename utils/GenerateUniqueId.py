import uuid


def generate_uuid():
    id = uuid.uuid1()
    return str(id)
