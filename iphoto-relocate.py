#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Markus Dreyer, markus.dreyer@gmail.com

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

# from http://blogs.blumetech.com/blumetechs-tech-blog/2011/05/faster-python-file-copy.html
def copy_file(src, dst, buffer_size=10485760):
    '''
    Copies a file to a new location. Much faster performance than Apache Commons due to use of larger buffer
    @param src:    Source File
    @param dst:    Destination File (not file path)
    @param buffer_size:    Buffer size to use during copy
    @param perserveFileDate:    Preserve the original file date
    '''
    dstParent, dstFileName = os.path.split(dst)
    if not os.path.exists(dstParent):
        os.makedirs(dstParent)
    
    # Optimize the buffer for small files
    buffer_size = min(buffer_size, os.path.getsize(src))
    if(buffer_size == 0):
        buffer_size = 1024
    
    for fn in [src, dst]:
        try:
            st = os.stat(fn)
        except OSError:
            pass  # File most likely does not exist
        else:
            # TODO: What about other special files? (sockets, devices...)
            if shutil.stat.S_ISFIFO(st.st_mode):
                raise shutil.SpecialFileError("`%s` is a named pipe" % fn)

    fsrc = open(src, 'rb')
    fdst = open(dst, 'wb')
    shutil.copyfileobj(fsrc, fdst, buffer_size)
    shutil.copystat(src, dst)

def is_media_file(fname):
    """True for filenames with image or video extensions"""
    f = fname.lower()
    return f.endswith('.jpg') or f.endswith('.gif') or f.endswith('.tiff') or f.endswith('.png') or f.endswith('.mpg') or f.endswith('.mov') or f.endswith('.divx') or f.endswith('.mp4') or f.endswith('.wmv')

def maybe_copy(src, dst, do_copy, dry_run):
    """Copy file over unless options don't allow it. Returns true if copied (even in dry run)"""
    if os.path.isfile(dst): # Okay, file already exists
        if not os.path.getsize(src) == os.path.getsize(dst):
            raise Exception('File sizes differ: {0} vs {1}'.format(src, dst) )
        return False
    if os.path.isdir(dst):
        raise Exception('Already exists as directory: ' + dst)
    if not do_copy:
        raise Exception('File does not exist in target location, but option --nocopy prevents us from copying it over')
    LOG.debug('Copying ' + src + " to " + dst)
    if not dry_run:
        copy_file(src, dst)
    return True

def main(argv):
    """Relocate iPhoto Masters files to free up space."""

    parser = optparse.OptionParser("Usage: %prog [options] <iphoto-library-path> <target-path>",
                                   version="%prog 1.0")

    parser.add_option("--debug",
                      dest="debug",
                      action="store_true",
                      default=False,
                      help="enable debug logging")

    parser.add_option("--nocopy",
                      dest="nocopy",
                      action="store_true",
                      default=False,
                      help="Use this option if all files are already in the target directory (e.g., after copying iPhoto library over by hand, using rsync, etc.)")

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

    dry_run = opts.dry_run
    do_copy = not opts.nocopy

    old = os.path.abspath(args[0] + "/Masters")
    new = os.path.abspath(args[1] + "/Masters")

    if not os.path.isdir(old):
        raise Exception('Could not find ' + old)
    if not os.path.isdir(new):
        os.makedirs(new)

    num_copied = 0
    num_linked = 0
    os.chdir(old)
    for dirpath, dirnames, filenames in os.walk('.'):
        for f in filenames:
            if is_media_file(f):
                old_file = dirpath + '/' + re.sub('^\./', '', f)
                if not os.path.islink(old_file): # could already be a link, e.g. due to previous run of this script
                    new_file = os.path.realpath(new + '/' + old_file)
                    if maybe_copy(old_file, new_file, do_copy, dry_run):
                        num_copied += 1
                    if not dry_run:
                        os.remove(old_file)
                        os.symlink(new_file, old_file)
                    num_linked += 1

    LOG.debug('Copied {0} files'.format(num_copied))
    LOG.debug('Linked {0} files'.format(num_linked))
                    
if __name__ == "__main__":
    main(sys.argv[1:])
