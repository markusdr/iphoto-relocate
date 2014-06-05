#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Markus Dreyer, mdreyer@sdl.com

from __future__ import print_function
import optparse
import sys
import logging
import os
import glob
import re
import errno
import shutil

LOG = logging.getLogger(__name__)

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

# from http://blogs.blumetech.com/blumetechs-tech-blog/2011/05/faster-python-file-copy.html
def copy_file(src, dst, buffer_size=10485760):
    '''
    Copies a file to a new location. Much faster performance than Apache Commons due to use of larger buffer
    @param src:    Source File
    @param dst:    Destination File (not file path)
    @param buffer_size:    Buffer size to use during copy
    @param perserveFileDate:    Preserve the original file date
    '''
    #    Check to make sure destination directory exists. If it doesn't create the directory
    dstParent, dstFileName = os.path.split(dst)
    if not os.path.exists(dstParent):
        os.makedirs(dstParent)
    
    #    Optimize the buffer for small files
    buffer_size = min(buffer_size, os.path.getsize(src))
    if(buffer_size == 0):
        buffer_size = 1024
    
    for fn in [src, dst]:
        try:
            st = os.stat(fn)
        except OSError:
            # File most likely does not exist
            pass
        else:
            # XXX What about other special files? (sockets, devices...)
            if shutil.stat.S_ISFIFO(st.st_mode):
                raise shutil.SpecialFileError("`%s` is a named pipe" % fn)

    fsrc = open(src, 'rb')
    fdst = open(dst, 'wb')
    shutil.copyfileobj(fsrc, fdst, buffer_size)
    shutil.copystat(src, dst)

def main(argv):
    """Relocate iPhoto Masters files"""

    parser = optparse.OptionParser("usage: %prog [options] args",
                                   version="%prog 1.0")

    parser.add_option("--debug",
                      dest="debug",
                      action="store_true",
                      default=False,
                      help="enable debug logging")

    parser.add_option("--dry-run",
                      dest="dry_run",
                      action="store_true",
                      default=False,
                      help="dry run (don't do anything)")

    (opts, args) = parser.parse_args()

    if len(args) != 2:
        parser.error("Please give iPhoto library location and new Masters location as arguments")

    if opts.debug:
        logging.basicConfig(level=logging.DEBUG)
        LOG.debug("Enabled debug logging")
        LOG.debug("Options:\n" + str(opts))

    dry_run = True if opts.dry_run else False

    old = os.path.abspath(args[0] + "/Masters")
    new = os.path.abspath(args[1])

    if not os.path.isdir(old):
        raise Exception('Could not find ' + old)
    if not os.path.isdir(old):
        raise Exception('Could not find ' + old)

    num_copied = 0
    num_linked = 0
    os.chdir(old)
    for dirpath, dirnames, filenames in os.walk('.'):
        for f in filenames:
            f_low = f.lower()
            if f_low.endswith('.jpg') or f_low.endswith('.mpg') or f_low.endswith('.mov'):
                old_file = dirpath + '/' + re.sub('^\./', '', f)
                if not os.path.islink(old_file):
                    new_file = os.path.realpath(new + '/' + old_file)
                    if not os.path.isfile(new_file):
                        new_dir = new + '/' + os.path.dirname(old_file)
                        LOG.debug('mkdir ' + new_dir)
                        LOG.debug('copy ' + old_file + " to " + new_file)
                        if not dry_run:
                            mkdir_p(new_dir)
                            shutil.copyfile(old_file, new_file)
                            shutil.copystat(old_file, new_file)
                        num_copied += 1
                    LOG.debug(old_file + ' => ' + new_file)
                    if not dry_run:
                        os.remove(old_file)
                        os.symlink(new_file, old_file)
                    num_linked += 1

    LOG.debug('Copied {0} files'.format(num_copied))
    LOG.debug('Linked {0} files'.format(num_linked))
                    
if __name__ == "__main__":
    main(sys.argv[1:])
