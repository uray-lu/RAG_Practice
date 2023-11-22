import json

class JsonEncoder(json.JSONEncoder):
    
    def default(self, obj):
        
        if isinstance(obj, set):
            return list(obj)
        
        return json.JSONEncoder.default(self, obj)
    
class JsonLoader:

    @staticmethod
    def load(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    @staticmethod
    def save(file_path, data):
        with open(file_path, 'w', encoding="utf-8") as file:
            json.dump(data, file)

