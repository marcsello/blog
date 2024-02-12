from abc import ABC, abstractmethod

import os


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

    @abstractmethod
    def abort(self):
        """
        un-does the output in case of an error
        :return:
        """
        pass
