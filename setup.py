# coding: utf-8

from setuptools import setup, find_packages

setup(
	name = 'thumbor_ceph',
	version = "1",
	description = 'Thumbor Ceph Rados extensions',
	author = 'Laurent Barbe',
	author_email = 'laurent@ksperis.com',
	zip_safe = False,
	include_package_data = True,
	packages=find_packages(),
	requires=['thumbor']
)