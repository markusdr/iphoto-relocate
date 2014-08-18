## Synopsis

Is your iPhoto library using too much space?

This `iphoto-relocate.py` script relocates the photos and videos from
your iPhoto library to an external drive (e.g., a NAS drive).

To ensure that iPhoto works 100% correctly, the iPhoto library itself
(incl. various DBs, the thumbnail files, etc.) stays where it is --
only the 'masters' are relocated. Each original file in the iPhoto
library is replaced by a symbolic link that points to the new file
location on the external drive.

So the script simulates a missing "relocate masters" or "relocate
originals" functionality for iPhoto.

Note that the alternative, simpler method of just copying the whole
iPhoto library to your NAS drive is not recommended and may result in
data loss. See a discussion
[here](https://discussions.apple.com/thread/54372780).

## Usage

Usage example:

    ./iphoto-relocate.py "~/Pictures/iPhoto Library" "/Volumes/external-drive/iphoto"

This creates a `Masters` directory on the external drive (the
`/Volumes/external-drive/iphoto` directory), which contains all
'master' image and video files from the iPhoto library.

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
photos over to the external drive. It will recognize which files are
already symbolic links and which files are new and need to be moved to
the external drive.

## Deleting photos in iPhoto

After you run the script, all masters will be on the external drive;
iPhoto will only see symbolic links in its local iPhoto
library. Consequently, when you delete a photo in iPhoto, it will only
delete the link, but not the original photo on the external drive.

The following procedure is recommended: Whenever you get a new batch
of photos from your camera, they will be in your local iPhoto library
as usual. Go through them and delete some photos. Then run the script
to move all remaining photos to the external drive.

## Installation

You can run the script from the command line on your Mac (e.g.,
`iTerm`), provided you have Python installed.

Currently, no GUI is provided.

## Contributors

Markus Dreyer, markus.dreyer@gmail.com

## License

Copyright 2014 Markus Dreyer

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
