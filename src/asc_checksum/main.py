import argparse
import sys

from src.asc_checksum.files.Database import Database
from src.asc_checksum.files.Logger import Logger


def _init_argparse():
    parser = argparse.ArgumentParser("checksum the files on your computer")

    # Arguments
    parser.add_argument("-a", "--add", metavar="PATH", type=str,
                        help="add a new path to the checksum database")
    parser.add_argument("-c", "--check", action="store_true",
                        help="check the integrity of the files in the database")
    parser.add_argument("-u", "--update", action="store_true",
                        help="update the hashes of the files in the database")
    parser.add_argument("-l", "--list", action="store_true",
                        help="list all the paths added to the database")
    parser.add_argument("-r", "--remove", metavar="PATH", type=str,
                        help="remove a path from the checksum database")
    parser.add_argument("--clear", action="store_true",
                        help="clear the entire checksum database")

    # Show the help message by default when arguments aren't provided
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    if args.add:
        database.add(args.add)
    elif args.check:
        database.check_integrity()
    elif args.update:
        database.update()
    elif args.list:
        database.list()
    elif args.remove:
        database.remove(args.remove)
    elif args.clear:
        database.clear()


if __name__ == "__main__":
    database = Database(Logger())
    _init_argparse()
