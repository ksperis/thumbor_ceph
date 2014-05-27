from thumbor.result_storages import BaseStorage
from thumbor.utils import logger
import rados, sys
import hashlib


class Storage(BaseStorage):
  cluster = rados.Rados(conffile="/etc/ceph/ceph.conf")
  cluster.connect()
  logger.debug('INIT RADOS Result Storage (ID:' + cluster.get_fsid() + ')')

  def __init__(self,context):
    BaseStorage.__init__(self, context)
    if not self.context.config.CEPH_RESULT_STORAGE_POOL:
      raise RuntimeError("CEPH_RESULT_STORAGE_POOL undefined")
    self.storage = self.cluster.open_ioctx(self.context.config.CEPH_RESULT_STORAGE_POOL)

  def put(self, bytes):
    file_abspath = self.normalize_path(self.context.request.url)
    logger.debug('PUT (result) ' + self.context.request.url + ' (' + file_abspath + ')')
    self.storage.write_full(file_abspath,bytes)

  def get(self):
    path = self.context.request.url
    file_abspath = self.normalize_path(path)
    logger.debug('GET (result) ' + path + ' (' + file_abspath + ')')
    try:
      return self.storage.read(file_abspath, self.storage.stat(file_abspath)[0])
    except rados.ObjectNotFound:
      return None

  def normalize_path(self, path):
      digest = hashlib.sha1(path.encode('utf-8')).hexdigest()
      return digest
