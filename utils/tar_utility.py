#!/usr/bin/env python

"""Tar utility tasks"""

import tarfile
import os
import logging


LOG = logging.getLogger('atlassian-admin-tools')


class TarUtilityError(Exception):
    """An exception that occurs when performing tarfile operations"""
    pass


def create_tar(dest_file, parent_dir, backup_dir):
    """Create tar file

    Args:
        dest_file  : tarfile name and path for storage
        parent_dir : source file parent dir
        backup_dir : source file (file/dir to tar)

    Returns:
        None

    Raises:
       TarUtilityError: Raise for OSError and IOError to be handled
                     in controller.
    """

    if os.path.isfile(dest_file):
        LOG.warn("%s already exists", dest_file)
    else:
        os.chdir(parent_dir)
        LOG.info("Creating tar %s from %s/%s" % (dest_file, parent_dir, backup_dir))
        tar = tarfile.open(dest_file, 'w:gz')
        # Nesting required to use 'finally' prior to python 2.5
        try:
            try:
                tar.add(backup_dir)
                LOG.info("%s creation successful", dest_file)
            except (OSError, IOError), e:
                os.remove(dest_file)
                raise TarUtilityError(
                    "Tar file creation failed with error  %s" % str(e))
        finally:
            tar.close()
