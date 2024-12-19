import fcntl
import os
import time

datafile_path = "/tmp/region_lock_example.txt"

def acquire_partial_lock(file, offset, length):
    """
    Acquires an exclusive lock on a specific region of the file.
    """
    try:
        # Move to the desired offset
        file.seek(offset)
        # Lock the region from the offset for the specified length
        fcntl.lockf(file, fcntl.LOCK_EX, length)
        print(f"Lock acquired on region {offset} to {offset + length}.")
    except IOError as e:
        raise RuntimeError(f"Could not acquire lock: {e}")

def release_partial_lock(file, offset, length):
    """
    Releases the lock on the specified region of the file.
    """
    try:
        file.seek(offset)
        # Unlock the region
        fcntl.lockf(file, fcntl.LOCK_UN, length)
        print(f"Lock released on region {offset} to {offset + length}.")
    except IOError as e:
        raise RuntimeError(f"Could not release lock: {e}")

def write_to_region(file, offset, length, data):
    """
    Writes data to the specific region of the file.
    """
    file.seek(offset)
    Data = data.ljust(length)
    file.write(Data)  # Ensure the region is fully written
    #file.flush()  # Ensure the data is written to disk
    print(f"Data written to region {offset} to {offset + length}: {data}")

# Main flow
try:
    with open(datafile_path, "r+b") as file:
        Data = "Critical Data 1".encode()
        offset = 100  # Starting position for the lock
        length = len(Data)  # Length of the region to lock

        # Acquire a lock on the specific region
        print('acquire_partial_lock')
        #acquire_partial_lock(file, offset, length)

        # Perform critical work in the locked region
        print('write_to_region')
        write_to_region(file, offset, length, Data)

        # Simulate processing
        print('sleep')
        #time.sleep(5)  # Simulate some work

        # Release the lock
        print('release_partial_lock')
        #release_partial_lock(file, offset, length)

except RuntimeError as e:
    print(str(e))
