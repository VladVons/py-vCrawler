import os

def write_with_region_lock(filepath, offset, data):
    """
    Write data to a specific offset with a locked region to prevent conflicts.
    """
    with open(filepath, "r+b") as file:  # Open in read-write binary mode
        # Move the file pointer to the desired offset
        file.seek(offset)

        # Lock the specific region starting at the offset for the length of the data
        os.lockf(file.fileno(), os.F_LOCK, len(data))
        print(f"Region locked: Offset={offset}, Length={len(data)}")

        try:
            # Write the data at the offset
            file.write(data)
            file.flush()  # Ensure data is written to disk
            print(f"Data written at Offset={offset}: {data.decode()}")
        finally:
            # Unlock the region after the critical operation
            file.seek(offset)  # Reposition to the start of the locked region
            os.lockf(file.fileno(), os.F_ULOCK, len(data))
            print(f"Region unlocked: Offset={offset}, Length={len(data)}")


datafile_path = "/tmp/region_lock_example.txt"
write_with_region_lock(datafile_path, 100, b"Data at offset 100")
write_with_region_lock(datafile_path, 10, b"Data at offset 10")
