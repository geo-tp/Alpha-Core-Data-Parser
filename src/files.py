from os import path

class File:
    def __init__(self, filepath):
        self.filepath = filepath
        self.content = ""

    def load(self):
        with open(self.filepath, "r") as f:
            self.content = f.read()

        return self.content  

    def save(self, content, method="w"):
        if not path.exists(self.filepath):
            method = "w"

        self.content = content
        with open(self.filepath, method) as f:
            f.write(content)