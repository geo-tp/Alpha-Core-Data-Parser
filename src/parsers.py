class FileParser:
    
    def __init__(self, adapter, general_timestamp, database):
        self.adapter = adapter(general_timestamp, database)

    def parse(self, file_data):
        return self.adapter.parse(file_data)
