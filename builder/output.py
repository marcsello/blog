import os.path
import shutil
from abc import ABC, abstractmethod


class OutputBase(ABC):
    @abstractmethod
    def add_file(self, src: str, dst: str):
        pass

    @abstractmethod
    def write_file(self, content: str, dst: str):
        pass

    def add_folder(self, src_folder: str, dst: str):
        for root, _, files in os.walk(src_folder):
            for file in files:
                full_src_path = os.path.join(root, file)
                rel_dst_path = os.path.relpath(full_src_path, src_folder)
                full_dst_path = os.path.join(dst, rel_dst_path)
                self.add_file(full_src_path, full_dst_path)


class LocalDirOutput(OutputBase):

    def __init__(self, local_dir: str):
        self._local_dir = local_dir
        os.mkdir(self._local_dir)

    def _compile_path(self, dst: str) -> str:
        return os.path.join(self._local_dir, dst)

    def add_file(self, src: str, dst: str):
        print(" >", src, "->", dst)
        dst_full_path = self._compile_path(dst)
        dst_dir_name = os.path.dirname(dst_full_path)
        os.makedirs(dst_dir_name, exist_ok=True)
        shutil.copyfile(src, dst_full_path)

    def write_file(self, content: str, dst: str):
        print(" >", "[GENERATED]", "->", dst)
        dst_full_path = self._compile_path(dst)
        dst_dir_name = os.path.dirname(dst_full_path)
        os.makedirs(dst_dir_name, exist_ok=True)
        with open(dst_full_path, "w") as f:
            f.write(content)
