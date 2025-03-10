import threading
import os.path
import tarfile
import time
import os
from io import BytesIO

import requests
import requests.auth
import requests_toolbelt.sessions

from .base import OutputBase


class UploaderThread(threading.Thread):
    def __init__(self, session: requests.Session, url: str, read_f):
        super().__init__()
        self._s = session
        self._url = url
        self._f = read_f

        self.resp: requests.Response | None = None
        self.exc: Exception | None = None

    def run(self):
        try:
            self.resp = self._s.post(self._url, data=self._f, timeout=60,
                                      headers={'Content-Type': 'application/x-tar'})
        except Exception as e:
            self._f.close()  # terminate the writing end
            self.exc = e
            return


class WebployOutput(OutputBase):

    def __init__(self, url: str, site_name: str, username: str, password: str, meta: str | None):
        # setup requests session
        self._s = requests_toolbelt.sessions.BaseUrlSession(url)
        self._s.auth = requests.auth.HTTPBasicAuth(username, password)

        # create the deployment on the Webploy server
        payload = {}
        if meta:
            payload['meta'] = meta

        self._site_name = site_name
        r = self._s.post(f"sites/{self._site_name}/deployments", json=payload, timeout=30)

        if r.status_code != 201:
            print(" > error:", r.status_code, r.content.decode("utf-8"))
            raise Exception("unexpected status code", r.status_code)

        self._deployment_id = r.json()['id']
        print(" > deployment id:", self._deployment_id)

        # setup piping
        self._read_fd, self._write_fd = os.pipe()
        self._read_f = os.fdopen(self._read_fd, "rb")
        self._write_f = os.fdopen(self._write_fd, 'wb')

        # setup tar streamer magic
        self._tar = tarfile.open(
            name=None,
            mode="w|",
            fileobj=self._write_f,
            format=tarfile.PAX_FORMAT,
            pax_headers={"webploy": "1"}
        )
        self._mtime = time.time()

        # setup streamer
        self._uploader = UploaderThread(
            self._s,
            f"sites/{self._site_name}/deployments/{self._deployment_id}/uploadTar",
            self._read_f
        )
        self._uploader.start()

    def __set_default_tarinfo(self, tarinfo: tarfile.TarInfo):
        # These are just defaults, so we'll get a valid Tar file, webploy will override these while deploying the site
        tarinfo.mtime = self._mtime
        tarinfo.gid = 0
        tarinfo.uid = 0
        tarinfo.gname = ""
        tarinfo.uname = ""
        tarinfo.mode = 0o644

    def _add_file_impl(self, src: str, dst: str):
        tarinfo = self._tar.gettarinfo(src, dst)
        self.__set_default_tarinfo(tarinfo)
        with open(src, "rb") as f:
            self._tar.addfile(tarinfo, f)

    def _write_file_impl(self, content: str, dst: str):
        data = content.encode("utf-8")
        tarinfo = tarfile.TarInfo(name=dst)
        self.__set_default_tarinfo(tarinfo)
        tarinfo.size = len(data)
        self._tar.addfile(tarinfo, BytesIO(data))

    def _finish_tar_upload(self):
        print(" > waiting for upload to finish...")
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

        if self._uploader.resp.status_code != 201:
            print(" > upload error:", self._uploader.resp.status_code, self._uploader.resp.content.decode("utf-8"))
            raise Exception("tar upload failed")

    def close(self):
        print(" > closing...")
        self._finish_tar_upload()

        r = self._s.post(f"sites/{self._site_name}/deployments/{self._deployment_id}/finish", timeout=30)

        if r.status_code != 200:
            print(" > close error:", r.status_code, r.content.decode("utf-8"))
            raise Exception("unexpected status code", r.status_code)

        print(" > finished:", r.content.decode("utf-8"))

        print(" > upload successful")

    def abort(self):
        print(" > aborting...")
        try:
            self._finish_tar_upload()
        except Exception as e:
            print(" > there was an error during upload, ignoring...", str(e))

        r = self._s.delete(f"sites/{self._site_name}/deployments/{self._deployment_id}", timeout=30)

        if r.status_code != 204:
            print(" > delete error:", r.status_code, r.content.decode("utf-8"))
            raise Exception("unexpected status code", r.status_code)

        print(" > aborted deployment")
