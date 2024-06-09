import json

class JSONSerializer:
    @staticmethod
    def serialize(data):
        return json.dumps(data)

    @staticmethod
    def deserialize(data):
        if isinstance(data, bytes):
            data = data.decode('utf-8')
        return json.loads(data)
