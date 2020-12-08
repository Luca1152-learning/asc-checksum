import json

from src.asc_checksum.definitions import DATABASE_DIR
from src.asc_checksum.scripts.checksum import checksum


class Database:
    _database = dict()

    def __init__(self):
        self.load()

    def load(self):
        """Load the files-to-checksum database into memory"""

        try:
            self._database = json.loads(DATABASE_DIR.read_text(encoding="utf-8"))
        except FileNotFoundError:
            self._database = dict()

    def add(self, path):
        """Add a path (file or directory) in the database to keep track of its hash"""

        if path in self._database:
            print(f"The path '{path}' is already in the database")
        else:
            self._database[path] = checksum(path)

    def remove(self, path):
        """Remove a path (file or directory) from the database"""

        if path in self._database:
            self._database.pop(path)
        else:
            print(f"The path '{path}' was not found in the database")

    def save(self):
        """Write the entire database to a JSON file"""

        DATABASE_DIR.write_text(json.dumps(self._database, indent=4))
