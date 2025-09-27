
# DNG RAW File Fixer

I use this script to fix DNG files that are not readable by Darktable.

## Usage

```
./dng_fixer.py -i <input>.DNG -o <output>.DNG
```

You can use -f to force overwriting the original file, but I advise against it. RAW files should always be kept.

## Related Issues

[0.3% of Leica M10 files cannot be opened](https://github.com/darktable-org/darktable/issues/11695)

Tested on
 * Leica M10
 * Leica M10-R (should work on parallel series such as -P -D and even Monochrom)

## Technical Background

Mostly, the `StripByteCounts` field in these DNGs is wrong, and Darktable enforces strict checking. Thus, if the markers are not aligned with `StripByteCounts`, the file won't open.