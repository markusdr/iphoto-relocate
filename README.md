## Synopsis

Is your iPhoto library using too much space?

This `iphoto-relocate.py` script relocates the photos and videos from
your iPhoto library to an external drive (e.g., a NAS drive).

To ensure that iPhoto works correctly, the iPhoto library itself
(incl. various DBs, the thumbnail files, etc.) stays where it is --
only the 'masters' are relocated. Each original file in the iPhoto
library is replaced by a symbolic link that points to the new file
location on the external drive.

It simulates a missing "relocate masters" or "relocate originals"
functionality for iPhoto.

Note that the alternative, simpler method of just copying the whole
iPhoto library to your NAS drive is not recommended and may result in
data loss. See a discussion
[here](https://discussions.apple.com/thread/54372780).

## Usage

Usage example:

    ./iphoto-relocate.py "~/Pictures/iPhoto Library" "/Volumes/external-drive/iphoto"

This creates a `Masters` directory on my external drive (the
`/Volumes/external-drive/iphoto` directory), which contains all
'master' image and video files from my iPhoto library.

The `Masters` directory in the iPhoto library `~/Pictures/iPhoto
Library` is changed to contain symbolic links only.

As a precaution, you should make a backup of your iPhoto library
before running the script.

See also:

    ./iphoto-relocate.py --help

If your library is large it will take many hours for the script to
move all files over. It is recommended to connect your drive directly
to the computer the first time you run the script (as opposed to a
slower wireless connection).

On subsequent calls, the script will only copy new files over, so it
will run much faster than the first time.

You can, for example, run the script every month to move your latest
photos over to the external drive.

## Deleting photos in iPhotos

After you run the script, all masters will be on the external drive;
iPhoto will only see symbolic links. When you delete a photo in
iPhoto, it will only delete the link, but not the original photo on
the external drive.

The following procedure is recommended: Whenever you get a new batch
of photos from your camera, they will be local in your iPhoto library,
as normal. You can then go through them and delete some photos. Then
run the script to move all remaining photos to the external drive.

## Installation

You can run the script from the command line on your Mac (e.g.,
`iTerm`), provided you have Python installed.

## Contributors

Markus Dreyer, markus.dreyer@gmail.com

## License

A short snippet describing the license (MIT, Apache, etc.)
