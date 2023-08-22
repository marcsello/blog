import io
import threading
from abc import ABC, abstractmethod
import os.path
import shutil
import tarfile
import time
import os
from io import BytesIO

import requests

from .config import Config


class OutputBase(ABC):

    def add_file(self, src: str, dst: str):
        """
        Add an already existing file to the output
        :param src: Real Path to an existing file on the local machine
        :param dst: Destination in the output, relative to webroot
        """
        # some output modules may copy filenames as-is which could cause problems later on
        norm_dst = os.path.normpath(dst)
        assert norm_dst != ".", "dest path would be the root dir"

        print(" >", src, "->", norm_dst)
        self._add_file_impl(src, norm_dst)

    def write_file(self, content: str, dst: str):
        """
        Write string to a file in the output
        :param content: String to be written
        :param dst: Destination in the output, relative to webroot
        """
        norm_dst = os.path.normpath(dst)
        assert norm_dst != ".", "dest path would be the root dir"

        print(" >", "[GENERATED]", "->", norm_dst)
        self._write_file_impl(content, norm_dst)

    def add_folder(self, src_folder: str, dst: str):
        for root, _, files in os.walk(src_folder):
            for file in files:
                full_src_path = os.path.join(root, file)
                rel_dst_path = os.path.relpath(full_src_path, src_folder)
                full_dst_path = os.path.join(dst, rel_dst_path)
                self.add_file(full_src_path, full_dst_path)

    @abstractmethod
    def _add_file_impl(self, src: str, dst: str):
        pass

    @abstractmethod
    def _write_file_impl(self, src: str, dst: str):
        pass

    @abstractmethod
    def close(self):
        """
        Close the output
        """
        pass


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


class WebployOutput(OutputBase):
    seal_filename = "__SEAL__"

    class UploaderThread(threading.Thread):
        def __init__(self, url: str, key: str, read_f):
            super().__init__()
            self._url = url
            self._key = key
            self._f = read_f

            self._success = False
            self.resp: requests.Response | None = None
            self.exc: Exception | None = None

        def run(self):
            try:
                r = requests.post(self._url, data=self._f, timeout=30, headers={
                    'Content-Type': 'application/gzip',
                    'Authorization': 'Key ' + self._key
                })
            except Exception as e:
                self.exc = e
                return

            self.resp = r

    def __init__(self, url: str, key: str):
        self._read_fd, self._write_fd = os.pipe()
        self._read_f = os.fdopen(self._read_fd, "rb")
        self._write_f = os.fdopen(self._write_fd, 'wb')
        self._tar = tarfile.open(
            name=None,
            mode="w|gz",
            fileobj=self._write_f,
            format=tarfile.PAX_FORMAT,
            pax_headers={"webploy": "1"}
        )
        self._uploader = WebployOutput.UploaderThread(url, key, self._read_f)
        self._uploader.start()
        self._mtime = time.time()

    def __set_default_tarinfo(self, tarinfo: tarfile.TarInfo):
        tarinfo.mtime = self._mtime
        tarinfo.gid = 0
        tarinfo.uid = 0
        tarinfo.gname = ""
        tarinfo.uname = ""
        tarinfo.mode = 0o644

    def _add_file_impl(self, src: str, dst: str):
        assert dst != self.seal_filename  # Prevent bogus seal
        tarinfo = self._tar.gettarinfo(src, dst)
        self.__set_default_tarinfo(tarinfo)
        with open(src, "rb") as f:
            self._tar.addfile(tarinfo, f)

    def _write_file_impl(self, content: str, dst: str):
        assert dst != self.seal_filename  # Prevent bogus seal
        data = content.encode("utf-8")
        tarinfo = tarfile.TarInfo(name=dst)
        self.__set_default_tarinfo(tarinfo)
        tarinfo.size = len(data)
        self._tar.addfile(tarinfo, BytesIO(data))

    def __write_seal(self):
        # Seal is currently used to ensure that the whole archive has been sent without problem.
        # Seal should be the "last" file in the archive, once it is written, the archive should be closed
        # This could be later used to integrity checking
        tarinfo = tarfile.TarInfo(name=self.seal_filename)
        self.__set_default_tarinfo(tarinfo)
        tarinfo.size = 0
        self._tar.addfile(tarinfo)

    def close(self):
        print(" > sealing")
        self.__write_seal()  # Write the seal, as the last thing

        print(" > finishing upload...")
        # close the archive
        self._tar.close()

        # in theory tar.close should call the close function... but it does get trough to the fileobj
        # This have to be called so the read part closes as well, causing the POST request to finish
        self._write_f.flush()  # <- this isn't needed because closing automatically flushes it, but whatever
        self._write_f.close()

        # wait for the POST request to finalize
        self._uploader.join()

        if self._uploader.exc:
            raise self._uploader.exc

        print("==== Webploy output ====")
        print(self._uploader.resp.status_code, self._uploader.resp.reason)
        print()
        print(self._uploader.resp.content.decode("utf-8"))
        print("========================")

        if self._uploader.resp.status_code != 201:
            raise Exception("upload failed")

        print(" > upload successful")

def init_output() -> OutputBase:
    print(" > init", Config.OUTPUT_MODULE)
    if Config.OUTPUT_MODULE == "local":
        if not Config.OUTPUT_LOCAL_DIR:
            raise ValueError("Config.OUTPUT_LOCAL_DIR unset")

        return LocalDirOutput(Config.OUTPUT_LOCAL_DIR)

    elif Config.OUTPUT_MODULE == "webploy":
        if not Config.OUTPUT_WEBPLOY_URL:
            raise ValueError("Config.OUTPUT_WEBPLOY_URL unset")

        if not Config.OUTPUT_WEBPLOY_KEY:
            raise ValueError("Config.OUTPUT_WEBPLOY_KEY unset")

        return WebployOutput(Config.OUTPUT_WEBPLOY_URL, Config.OUTPUT_WEBPLOY_KEY)

    else:
        raise ValueError("unknown output module")
