from abc import ABC, abstractmethod
from zipfile import ZipFile
from io import BytesIO
from loguru import logger
import pickletools
from typing import List, BinaryIO
from sys import stdout


class HiddenOutput(object):
    def __init__(self, *args, **kwargs):
        pass

    def write(self, *args, **kwargs):
        pass


class PickleImplementation(ABC):
    data: bytes = None

    @abstractmethod
    def __init__(self, filename):
        raise NotImplementedError

    @abstractmethod
    def dump(self, file_like: BinaryIO):
        raise NotImplementedError

    def set_data(self, data: bytes):
        self.data = data


# This is actually just a blank picklefile
class PTFile(PickleImplementation):
    def __init__(self, filename, show_symbols=False):
        try:
            # new stream to dump the contents to without printing to console
            with open(filename, "rb") as f:
                # Symbolic disassembley, will throw exception if not a pickle file
                pickletools.dis(f, out=HiddenOutput() if not show_symbols else stdout)
                f.seek(0)
                self.data = f.read()
        except UnicodeDecodeError as ude:
            logger.info(
                "This isn't a pickle, PyTorch may have used `_use_new_zipfile_serialization`"
            )
            raise ude

    def dump(self, file_like: BinaryIO):
        file_like.write(self.data)


class ZippedPTFile(PickleImplementation):
    def __init__(self, filename, show_symbols=False):
        self.files: List = None
        self.pickle_files: List = None

        input_zip = ZipFile(filename)
        self.files = [
            {"name": name, "data": input_zip.read(name)}
            for name in input_zip.namelist()
        ]

        self.pickled_index = None
        for f in self.files:
            if ".pkl" in f["name"]:
                self.pickled_index = self.files.index(f)
                break

        file_like = BytesIO(self.files[self.pickled_index]["data"])
        # Symbolic disassembley, will throw exception if not a pickle file
        pickletools.dis(file_like, out=HiddenOutput() if not show_symbols else stdout)
        file_like.seek(0)
        self.data = file_like.read()
        # Save the rest so it can be dumped to a new file

    def dump(self, file_like: BinaryIO):
        zip_buffer = BytesIO()
        with ZipFile(zip_buffer, "w") as zip_file:
            for i, o in enumerate(self.files):
                if i != self.pickled_index:
                    zip_file.writestr(o["name"], o["data"])
            zip_file.writestr(self.files[self.pickled_index]["name"], self.data)
        file_like.write(zip_buffer.getvalue())


class PickleImplementationFactory:
    @staticmethod
    def get_pickle(filename: str, show_symbols: bool = False) -> PickleImplementation:
        pt = None
        try:
            pt = PTFile(filename, show_symbols)
        except UnicodeDecodeError:
            pt = ZippedPTFile(filename, show_symbols)

        return pt
