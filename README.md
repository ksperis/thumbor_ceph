thumbor_ceph
============

Thumbor Ceph RADOS extensions

For thumbor installation : https://github.com/thumbor/thumbor

Install Extention :
-------------------

	apt-get install git python-ceph
	git clone https://github.com/ksperis/thumbor_ceph.git
	cd thumbor_ceph
	python setup.py install


Configuration :
---------------

Section File Storage in /etc/thumbor

	################################# File Storage #################################
	STORAGE = 'thumbor_ceph.storages.ceph_storage'
	CEPH_STORAGE_POOL = 'thumbor'


Section Upload

	#################################### Upload ####################################
	UPLOAD_PHOTO_STORAGE = 'thumbor_ceph.storages.ceph_storage'


Section Result Storage

	################################ Result Storage ################################
	RESULT_STORAGE = 'thumbor_ceph.result_storages.ceph_storage'
	CEPH_RESULT_STORAGE_POOL = 'thumbor'



Launch thumbor
--------------

	# thumbor -l debug
	2014-05-27 10:27:24 thumbor:DEBUG INIT RADOS Storage (ID:c3eb3343-d06c-438f-ae49-cf998468824d)
	2014-05-27 10:27:24 thumbor:DEBUG INIT RADOS Result Storage (ID:c3eb3343-d06c-438f-ae49-cf998468824d)
	2014-05-27 10:27:24 root:DEBUG thumbor running at 0.0.0.0:8888
