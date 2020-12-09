import glob
import json
import logging
import os
import pathlib

from src.asc_checksum.definitions import DATABASE_PATH
from src.asc_checksum.scripts.checksum import checksum


class Database:
    _database = dict()

    def __init__(self, logger):
        self._logger = logger
        self.load()

    def load(self):
        """Load the database of files and their SHA256s into memory"""

        try:
            self._database = json.loads(DATABASE_PATH.read_text(encoding="utf-8"))
        except FileNotFoundError:
            self._database = dict()

    @staticmethod
    def _get_files_from_directory(path):
        # Remove '/' from the end of the directory, if it has one
        path = pathlib.Path(path)

        # Get all files from the directory
        os.chdir(path)
        files = [f"{path}/{file}" for file in glob.glob("**", recursive=True) if os.path.isfile(file)]

        return files

    def _add_file(self, file_path):
        if file_path in self._database:
            self._logger.log_to_console(
                f"The path '{file_path}' already is in the database (use 'update' to overwrite)", logging.WARNING
            )
            return False
        else:
            self._database[file_path] = checksum(file_path)
            return True

    def add(self, path):
        """
        Add a path in the database to keep track of its hash.
        If it's a directory, its files will be added instead.
        """

        # The path is a file
        if os.path.isfile(path):
            path_was_added = self._add_file(path)
            if path_was_added:
                self._logger.log_to_file(f"The file path '{path}' was added to the database")

        # The path is a directory
        else:
            added_any_path = False

            files = self._get_files_from_directory(path)
            for file in files:
                path_was_added = self._add_file(file)
                if path_was_added:
                    added_any_path = True

            if added_any_path:
                self._logger.log_to_file(f"The directory path '{path}' was added to the database")

        self.save()

    def check_integrity(self):
        """Checks whether the hash of the files in the database has changed"""

        found_discrepancy = False
        for path, old_hash in self._database.items():
            try:
                new_hash = checksum(path)
                if new_hash != old_hash:
                    if not found_discrepancy:
                        found_discrepancy = True
                        self._logger.log_to_file_and_console("Performed integrity check: FAIL")
                    self._logger.log_to_file_and_console(
                        f"The hash of the file at '{path}' has changed", logging.CRITICAL
                    )
            except FileNotFoundError:
                # The file was deleted

                if not found_discrepancy:
                    found_discrepancy = True
                    self._logger.log_to_file_and_console("Performed integrity check: FAIL")
                self._logger.log_to_file_and_console(
                    f"The file at '{path}' doesn't exist anymore", logging.CRITICAL
                )
        if not found_discrepancy:
            self._logger.log_to_file_and_console("Performed integrity check: OK")

    def update(self):
        """Update the SHA256s of all the files from the paths in the database"""

        paths_to_remove = []
        for path, old_hash in self._database.items():
            try:
                new_hash = checksum(path)
                if new_hash != old_hash:
                    self._database[path] = new_hash
                    self._logger.log_to_file_and_console(f"The hash of the file at '{path}' was updated")
            except FileNotFoundError:
                # The file doesn't exist anymore
                paths_to_remove.append(path)

        for path in paths_to_remove:
            self._database.pop(path)
            self._logger.log_to_file_and_console(
                f"The path '{path}' was removed from the database because the file doesn't exist anymore",
                logging.WARNING
            )

        self.save()

    def remove(self, path):
        """
        Remove a path from the database.
        If it's a directory, its files will be removed instead (if found in the database).
        """

        # The path a file
        if os.path.isfile(path):
            if path in self._database:
                self._database.pop(path)
                self._logger.log_to_file(f"The file path '{path}' was removed from the database")
            else:
                self._logger.log_to_console(f"The file path '{path}' was not found in the database", logging.WARNING)

        # The path is a directory
        else:
            removed_any_path = False

            files = self._get_files_from_directory(path)
            for file in files:
                path = self._database.pop(file, None)
                if path != None:
                    removed_any_path = True

            if removed_any_path:
                self._logger.log_to_file(f"The directory path '{path}' was removed from the database")

        self.save()

    def clear(self):
        """Remove all paths from the database"""

        self._database = dict()
        self.save()

        self._logger.log_to_file_and_console("Removed all paths from the database")

    def save(self):
        """Write the entire database to a JSON file"""

        DATABASE_PATH.write_text(json.dumps(self._database, indent=4))
