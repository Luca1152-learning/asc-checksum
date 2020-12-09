import pathlib

ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent.parent
DATABASE_PATH = ROOT_DIR / "out" / "database.json"