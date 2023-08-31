class FileParser:
    
    def __init__(self, adapter, database):
        self.adapter = adapter(database)

    def parse(self, file_data):
        return self.adapter.parse(file_data)
