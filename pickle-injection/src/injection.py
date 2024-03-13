from io import BytesIO, BufferedReader
from fickling.fickle import Pickled


def inject(data: bytes, code: str) -> bytes:
    with BytesIO(data) as f:
        p = Pickled.load(f)
        p.insert_python_exec(code)
        new_file_like = BytesIO()
        p.dump(new_file_like)
        new_file_like.seek(0)
        return new_file_like.read()
