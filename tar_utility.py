#! /usr/bin/env python

import tarfile
import os
import logging


log = logging.getLogger('atlassian-admin-tools')

def check_if_exists(tarfile_dest):
    return os.path.isfile(tarfile_dest)


def create_tar(dest_file, parent_dir, backup_dir):
    '''
    Create tar file

    Args:
    @dest_file    : tarfile name and path for storage
    @parent_dir  : source file parent dir
    @backup_dir  : source file (file/dir to tar)
    '''

    if check_if_exists(dest_file):
        log.warn("%s already exists" % dest_file)
        return None

    log.info("Creating %s from %s/%s" % (dest_file, parent_dir, backup_dir))

    os.chdir(parent_dir)    

    try:
        tar = tarfile.open(dest_file, 'w:gz')
        tar.add(backup_dir)
        log.info('Tar file creation successful')
    except OSError, e:
        log.error('Tar file creation failed with error: ' + str(e))
        print e


def extract_tar(dest_dir, tar_file):
    '''
    Extract tar file inside dest dir
    '''
    try:
        log.info("Extract tar file %s into %s directory".format(tar_file, dest_dir))
        tar = tarfile.open(tar_file,'r:gz')
        for item in tar:
            print item
            tar.extract(item, path=dest_dir)
        tar.close()
    except OSError, e:
        print e
        log.error('Tar file extraction failed with error: ' + str(e))
    except IOError, e:
        print e
        log.error('Tar file extraction failed with error: ' + str(e))


if __name__ == '__main__':
    pass
    
