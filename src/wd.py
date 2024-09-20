import os
import ctypes
import ctypes.util
import struct

# Load inotify from libc
libc = ctypes.CDLL(ctypes.util.find_library('c'), use_errno=True)

# Constants from inotify.h
IN_MODIFY = 0x00000002
IN_DELETE = 0x00000200
IN_CREATE = 0x00000100

# Create inotify instance
inotify_init = libc.inotify_init
inotify_init.restype = ctypes.c_int
inotify_fd = inotify_init()

if inotify_fd == -1:
    raise OSError("Failed to initialize inotify")

# Watch a file (not a directory)
file_to_watch = b"./vCrawler.log"  # Replace with the actual file path

# Add the file to the inotify watch list
inotify_add_watch = libc.inotify_add_watch
inotify_add_watch.restype = ctypes.c_int
watch_descriptor = inotify_add_watch(inotify_fd, file_to_watch, IN_MODIFY | IN_DELETE | IN_CREATE)

if watch_descriptor == -1:
    raise OSError(f"Failed to add watch for file: {file_to_watch.decode()}")

print(f"Watching {file_to_watch.decode()} for changes...")

# Read events
event_size = struct.calcsize('iIII')  # Event struct size
try:
    while True:
        buffer = os.read(inotify_fd, event_size + 512)  # Buffer to hold event data

        wd, mask, cookie, name_len = struct.unpack('iIII', buffer[:event_size])

        if mask & IN_MODIFY:
            print(f"File {file_to_watch.decode()} has been modified")
        elif mask & IN_DELETE:
            print(f"File {file_to_watch.decode()} has been deleted")
        elif mask & IN_CREATE:
            print(f"File {file_to_watch.decode()} has been created")
except KeyboardInterrupt:
    print("Stopped watching.")
finally:
    os.close(inotify_fd)
