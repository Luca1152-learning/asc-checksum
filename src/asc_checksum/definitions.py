import pathlib

ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent.parent
DATABASE_DIR = ROOT_DIR / "out" / "database.json"