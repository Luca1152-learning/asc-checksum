import glob
import json
import os
import pathlib

from src.asc_checksum.definitions import DATABASE_DIR
from src.asc_checksum.scripts.checksum import checksum


class Database:
    _database = dict()

    def __init__(self):
        self.load()

    def load(self):
        """Load the database of files and their SHA256s into memory"""

        try:
            self._database = json.loads(DATABASE_DIR.read_text(encoding="utf-8"))
        except FileNotFoundError:
            self._database = dict()

    def _add_file(self, file_path):
        if file_path in self._database:
            print(f"The path '{file_path}' already is in the database (use 'update' to overwrite)")
        else:
            self._database[file_path] = checksum(file_path)

    @staticmethod
    def _get_files_from_directory(path):
        # Remove '/' from the end of the directory, if it has one
        path = pathlib.Path(path)

        # Get all files from the directory
        os.chdir(path)
        files = [f"{path}/{file}" for file in glob.glob("**", recursive=True) if os.path.isfile(file)]

        return files

    def add(self, path):
        """
        Add a path in the database to keep track of its hash.
        If it's a directory, its files will be added instead.
        """

        # The path is a file
        if os.path.isfile(path):
            self._add_file(path)

        # The path is a directory
        else:
            files = self._get_files_from_directory(path)
            for file in files:
                self._add_file(file)

    def get_modified_files(self):
        """Return the paths of the files with a different SHA256 from the one in the database"""

        modified_files = []
        for path, old_hash in self._database.items():
            new_hash = checksum(path)
            if new_hash != old_hash:
                modified_files.append(path)
        return modified_files

    def remove(self, path):
        """
        Remove a path from the database.
        If it's a directory, its files will be removed instead, if found in the database.
        """

        # The path a file
        if os.path.isfile(path):
            if path in self._database:
                self._database.pop(path)
                print(f"The file path '{path}' was removed from the database")
            else:
                print(f"The file path '{path}' was not found in the database")

        # The path is a directory
        else:
            files = self._get_files_from_directory(path)
            for file in files:
                self._database.pop(file)
            print(f"The directory path '{path}' was removed from the database")

    def save(self):
        """Write the entire database to a JSON file"""

        DATABASE_DIR.write_text(json.dumps(self._database, indent=4))
