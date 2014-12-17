#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor ceph storage
# https://github.com/ksperis/thumbor_ceph

from thumbor.storages import BaseStorage
from thumbor.utils import logger
import rados
import hashlib
from json import loads, dumps


class Storage(BaseStorage):
  def __init__(self, context, conffile=None):
    if conffile is None:
      conffile = '/etc/ceph/ceph.conf'

    super(Storage, self).__init__(context)

    if not self.context.config.CEPH_STORAGE_POOL:
      raise RuntimeError("CEPH_STORAGE_POOL undefined")
    self.cluster = rados.Rados(conffile=conffile)
    self.cluster.connect()
    logger.debug('INIT RADOS Storage (ID:' + self.cluster.get_fsid() + ')')
    self.storage = self.cluster.open_ioctx(self.context.config.CEPH_STORAGE_POOL)

  def put(self, path, bytes):
    file_abspath = self.normalize_path(path)
    logger.debug('PUT ' + path + ' (' + file_abspath + ')')
    self.storage.write_full(file_abspath,bytes)
    return file_abspath

  def put_crypto(self, path):
    file_abspath = self.normalize_path(path)
    logger.debug('PUT CRYPTO ' + path + ' (' + file_abspath + ') : ' + self.context.config.SECURITY_KEY)
    if not self.context.config.STORES_CRYPTO_KEY_FOR_EACH_IMAGE:
      return

    if not self.context.config.SECURITY_KEY:
      raise RuntimeError("STORES_CRYPTO_KEY_FOR_EACH_IMAGE can't be True if no SECURITY_KEY specified")

    self.storage.set_xattr(file_abspath, "CRYPTO", self.context.config.SECURITY_KEY)

  def put_detector_data(self, path, data):
    key = self.normalize_path(path) + "-detector"
    self.storage.write_full(key, dumps(data))
    return key

  def get(self, path):
    file_abspath = self.normalize_path(path)
    logger.debug('GET ' + path + ' (' + file_abspath + ')')
    try:
      return self.storage.read(file_abspath, self.storage.stat(file_abspath)[0])
    except rados.ObjectNotFound:
      return None

  # get signature key
  def get_crypto(self, path):
    file_abspath = self.normalize_path(path)
    logger.debug('GET CRYPTO ' + path + ' (' + file_abspath + ')')
    if not self.context.config.STORES_CRYPTO_KEY_FOR_EACH_IMAGE:
      return None
    return self.storage.get_xattr(file_abspath, "CRYPTO")

  def get_detector_data(self, path):
    key = self.normalize_path(path) + "-detector"
    try:
      data = self.storage.read(key)
    except rados.ObjectNotFound:
      return None
    if not data:
      return None
    return loads(data)

  def exists(self, path):
    file_abspath = self.normalize_path(path)
    try:
      self.storage.stat(file_abspath)
      logger.debug('EXIST (result) ' + path + ' (' + file_abspath + ') : YES')
      return True
    except rados.ObjectNotFound:
      logger.debug('EXIST (result) ' + path + ' (' + file_abspath + ') : NO')
      return False

  def normalize_path(self, path):
    path = hashlib.sha1(path.encode('utf-8')).hexdigest()
    return path
