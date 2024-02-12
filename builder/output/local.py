import os
import shutil

from .base import OutputBase


class LocalDirOutput(OutputBase):

    def __init__(self, local_dir: str):
        self._local_dir = local_dir
        os.mkdir(self._local_dir)

    def _compile_path(self, dst: str) -> str:
        return os.path.join(self._local_dir, dst)

    def _add_file_impl(self, src: str, dst: str):
        dst_full_path = self._compile_path(dst)
        dst_dir_name = os.path.dirname(dst_full_path)
        os.makedirs(dst_dir_name, exist_ok=True)
        shutil.copyfile(src, dst_full_path)

    def _write_file_impl(self, content: str, dst: str):
        dst_full_path = self._compile_path(dst)
        dst_dir_name = os.path.dirname(dst_full_path)
        os.makedirs(dst_dir_name, exist_ok=True)
        with open(dst_full_path, "w") as f:
            f.write(content)

    def close(self):
        pass

    def abort(self):
        # delete broken files
        shutil.rmtree(self._local_dir)
