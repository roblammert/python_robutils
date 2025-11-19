import os
import shutil
from pathlib import Path
import hashlib
import tempfile
from typing import List, Union, Optional, Tuple, Dict
import time

# --- Configuration & Helpers ---

def get_path_object(path: Union[str, Path]) -> Path:
    """Converts a string or Path object into a Path object."""
    if isinstance(path, str):
        return Path(path)
    return path

# --- File Operations (Read/Write/Checksum/Metadata) ---

def read_file_content(filepath: Union[str, Path], encoding: str = 'utf-8') -> Optional[str]:
    """
    Reads the entire content of a text file.

    Args:
        filepath: The path to the file.
        encoding: The character encoding to use (default: 'utf-8').

    Returns:
        The content of the file as a string, or None if an error occurs.
    """
    file_path_obj = get_path_object(filepath)
    try:
        with open(file_path_obj, 'r', encoding=encoding) as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return None

def write_file_content(filepath: Union[str, Path], content: str, encoding: str = 'utf-8', overwrite: bool = True) -> bool:
    """
    Writes content to a text file. Creates the file if it doesn't exist.
    Will create parent directories if they don't exist.

    Args:
        filepath: The path to the file.
        content: The string content to write.
        encoding: The character encoding to use (default: 'utf-8').
        overwrite: If True (default), overwrites existing content. If False,
                   raises a FileExistsError if the file already exists.

    Returns:
        True if successful, False otherwise.
    """
    file_path_obj = get_path_object(filepath)
    mode = 'w' if overwrite else 'x'
    
    try:
        # Ensure parent directories exist
        if file_path_obj.parent:
            file_path_obj.parent.mkdir(parents=True, exist_ok=True)
            
        with open(file_path_obj, mode, encoding=encoding) as f:
            f.write(content)
        return True
    except FileExistsError:
        print(f"Error: File already exists at {filepath}. Set overwrite=True to force overwrite.")
        return False
    except Exception as e:
        print(f"Error writing to file {filepath}: {e}")
        return False

def atomic_write_file_content(filepath: Union[str, Path], content: str, encoding: str = 'utf-8') -> bool:
    """
    Writes content to a file safely using a temporary file and atomic rename.
    This prevents data corruption if the write operation is interrupted.

    Args:
        filepath: The final destination path for the file.
        content: The string content to write.
        encoding: The character encoding to use (default: 'utf-8').

    Returns:
        True if successful, False otherwise.
    """
    final_path = get_path_object(filepath)
    
    try:
        # 1. Ensure parent directories exist
        if final_path.parent:
            final_path.parent.mkdir(parents=True, exist_ok=True)

        # 2. Write to a temporary file in the same directory (for better atomicity)
        temp_dir = final_path.parent or None
        with tempfile.NamedTemporaryFile(mode='w', encoding=encoding, delete=False, dir=temp_dir) as tmp_file:
            tmp_file.write(content)
            temp_path = Path(tmp_file.name)
        
        # 3. Atomically replace the final file with the temporary file
        os.replace(temp_path, final_path)
        return True
    except Exception as e:
        print(f"Error during atomic write to {filepath}: {e}")
        # Ensure the temporary file is cleaned up if rename fails
        if 'temp_path' in locals() and temp_path.exists():
            delete_path(temp_path)
        return False

def get_file_size(filepath: Union[str, Path]) -> Optional[int]:
    """
    Gets the size of a file in bytes.

    Args:
        filepath: The path to the file.

    Returns:
        The size in bytes (integer), or None if the path is not a file or an error occurs.
    """
    file_path_obj = get_path_object(filepath)
    try:
        if file_path_obj.is_file():
            return file_path_obj.stat().st_size
        else:
            print(f"Error: Path {filepath} is not a file.")
            return None
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None
    except Exception as e:
        print(f"Error getting file size for {filepath}: {e}")
        return None

def get_file_checksum(filepath: Union[str, Path], algorithm: str = 'sha256') -> Optional[str]:
    """
    Calculates the cryptographic checksum (hash) of a file's content.

    Args:
        filepath: The path to the file.
        algorithm: The hashing algorithm to use (e.g., 'md5', 'sha1', 'sha256', 'sha512').

    Returns:
        The hexadecimal digest string, or None if an error occurs.
    """
    file_path_obj = get_path_object(filepath)
    if not file_path_obj.is_file():
        print(f"Error: File not found or not a file at {filepath}")
        return None

    try:
        # Create hash object based on algorithm
        hash_func = hashlib.new(algorithm)
    except ValueError:
        print(f"Error: Unsupported hashing algorithm '{algorithm}'.")
        return None

    try:
        # Read file in chunks to handle large files efficiently
        with open(file_path_obj, 'rb') as f:
            while chunk := f.read(4096):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    except Exception as e:
        print(f"Error calculating checksum for {filepath}: {e}")
        return None

def get_file_times(filepath: Union[str, Path]) -> Optional[Dict[str, float]]:
    """
    Retrieves file creation and modification timestamps.

    Args:
        filepath: The path to the file or directory.

    Returns:
        A dictionary containing 'modified' and 'created' timestamps (as seconds
        since the epoch), or None if an error occurs.
    """
    file_path_obj = get_path_object(filepath)
    try:
        stat_info = file_path_obj.stat()
        # st_ctime is typically creation time on Unix/macOS, but might be
        # last metadata change time. st_mtime is consistently last modification time.
        return {
            'modified': stat_info.st_mtime,
            'created': stat_info.st_ctime,
        }
    except FileNotFoundError:
        print(f"Error: Path not found at {filepath}")
        return None
    except Exception as e:
        print(f"Error getting file times for {filepath}: {e}")
        return None


# --- Directory and Path Management ---

def create_directory(dirpath: Union[str, Path], exist_ok: bool = True) -> bool:
    """
    Creates a directory, including any necessary intermediate directories.

    Args:
        dirpath: The path to the directory to create.
        exist_ok: If True, does not raise an error if the directory already exists.

    Returns:
        True if the directory exists (was created or already existed), False otherwise.
    """
    dir_path_obj = get_path_object(dirpath)
    try:
        dir_path_obj.mkdir(parents=True, exist_ok=exist_ok)
        return True
    except FileExistsError:
        # Should only happen if exist_ok=False
        print(f"Error: Directory already exists at {dirpath}")
        return False
    except Exception as e:
        print(f"Error creating directory {dirpath}: {e}")
        return False

def create_temp_directory() -> Optional[str]:
    """
    Creates a secure, temporary directory and returns its absolute path.
    The caller is responsible for cleaning up the directory when finished.

    Returns:
        The absolute path string of the created temporary directory, or None on error.
    """
    try:
        temp_dir = tempfile.mkdtemp()
        return temp_dir
    except Exception as e:
        print(f"Error creating temporary directory: {e}")
        return None

def delete_path(path: Union[str, Path]) -> bool:
    """
    Deletes a file or an entire directory tree.

    Args:
        path: The path to the file or directory to delete.

    Returns:
        True if successful, False otherwise.
    """
    path_obj = get_path_object(path)
    if not path_obj.exists():
        print(f"Warning: Path not found, nothing to delete at {path}")
        return True # Considered successful if the target doesn't exist

    try:
        if path_obj.is_file():
            path_obj.unlink()
        elif path_obj.is_dir():
            shutil.rmtree(path_obj)
        else:
            # Handle symlinks or other exotic file types
            os.remove(path_obj)
        return True
    except PermissionError:
        print(f"Error: Permission denied when trying to delete {path}.")
        return False
    except Exception as e:
        print(f"Error deleting path {path}: {e}")
        return False

def list_directory_contents(dirpath: Union[str, Path], include_files: bool = True, include_dirs: bool = True) -> List[str]:
    """
    Lists the names (not full paths) of files and/or directories in a given directory.

    Args:
        dirpath: The path to the directory to list.
        include_files: Whether to include files in the result.
        include_dirs: Whether to include directories in the result.

    Returns:
        A list of names (strings) of the contents.
    """
    dir_path_obj = get_path_object(dirpath)
    if not dir_path_obj.is_dir():
        print(f"Error: Path {dirpath} is not a directory.")
        return []

    contents = []
    try:
        for item in dir_path_obj.iterdir():
            if include_files and item.is_file():
                contents.append(item.name)
            elif include_dirs and item.is_dir():
                contents.append(item.name)
        return contents
    except Exception as e:
        print(f"Error listing contents of {dirpath}: {e}")
        return []

def walk_directory_contents(dirpath: Union[str, Path], pattern: str = '*', recursive: bool = True) -> List[str]:
    """
    Recursively lists paths within a directory based on a glob pattern.

    Args:
        dirpath: The path to the directory to start walking from.
        pattern: The glob pattern to match (e.g., '*.txt', 'logs/*'). Default is '*' (all contents).
        recursive: If True (default), searches recursively into subdirectories.

    Returns:
        A list of full path strings matching the pattern.
    """
    dir_path_obj = get_path_object(dirpath)
    if not dir_path_obj.is_dir():
        print(f"Error: Path {dirpath} is not a directory.")
        return []

    glob_method = dir_path_obj.rglob if recursive else dir_path_obj.glob
    
    try:
        # Use rglob for recursive search, glob for non-recursive
        # Note: glob/rglob yields Path objects, convert to string list
        return [str(p) for p in glob_method(pattern)]
    except Exception as e:
        print(f"Error walking directory {dirpath}: {e}")
        return []

def get_directory_size(dirpath: Union[str, Path]) -> Optional[int]:
    """
    Calculates the total size of a directory in bytes, including all files and subdirectories.

    Args:
        dirpath: The path to the directory.

    Returns:
        The total size in bytes (integer), or None if an error occurs.
    """
    dir_path_obj = get_path_object(dirpath)
    if not dir_path_obj.is_dir():
        print(f"Error: Path {dirpath} is not a directory.")
        return None

    total_size = 0
    try:
        # Recursively glob all files and directories
        for item in dir_path_obj.rglob('*'):
            if item.is_file():
                # Safely get size, handling potential errors for specific files
                try:
                    total_size += item.stat().st_size
                except Exception as e:
                    # Log error but continue calculation
                    print(f"Warning: Could not get size for file {item}: {e}")
        return total_size
    except Exception as e:
        print(f"Error calculating directory size for {dirpath}: {e}")
        return None

def move_path(src: Union[str, Path], dst: Union[str, Path]) -> bool:
    """
    Moves a file or directory from source (src) to destination (dst).

    Args:
        src: The source path.
        dst: The destination path.

    Returns:
        True if successful, False otherwise.
    """
    src_obj = get_path_object(src)
    dst_obj = get_path_object(dst)
    
    if not src_obj.exists():
        print(f"Error: Source path does not exist at {src}")
        return False

    try:
        # shutil.move handles both files and directories
        shutil.move(src_obj, dst_obj)
        return True
    except Exception as e:
        print(f"Error moving path from {src} to {dst}: {e}")
        return False

def copy_path(src: Union[str, Path], dst: Union[str, Path]) -> bool:
    """
    Copies a file or a directory tree from source (src) to destination (dst).
    For directories, this performs a recursive copy.

    Args:
        src: The source path.
        dst: The destination path.

    Returns:
        True if successful, False otherwise.
    """
    src_obj = get_path_object(src)
    dst_obj = get_path_object(dst)
    
    if not src_obj.exists():
        print(f"Error: Source path does not exist at {src}")
        return False

    try:
        if src_obj.is_file():
            # Copy a single file
            shutil.copy2(src_obj, dst_obj) # copy2 preserves metadata
        elif src_obj.is_dir():
            # Copy directory tree
            shutil.copytree(src_obj, dst_obj)
        else:
            # Handle special cases like symbolic links
            shutil.copy2(src_obj, dst_obj)
        return True
    except Exception as e:
        print(f"Error copying path from {src} to {dst}: {e}")
        return False

# --- Path Utility Functions ---

def join_paths(*parts: str) -> str:
    """
    Joins path components into a single, correctly formatted path string.

    Args:
        *parts: Variable number of path components (strings).

    Returns:
        The resulting path as a string.
    """
    return str(Path(*parts))

def get_absolute_path(path: Union[str, Path]) -> str:
    """
    Returns the absolute path for the given path.

    Args:
        path: The relative or absolute path.

    Returns:
        The absolute path as a string.
    """
    return str(get_path_object(path).resolve())

def get_parent_directory(path: Union[str, Path]) -> str:
    """
    Returns the parent directory of a path.

    Args:
        path: The path (file or directory).

    Returns:
        The parent directory's path as a string.
    """
    return str(get_path_object(path).parent)

def get_filename_and_extension(filepath: Union[str, Path]) -> Tuple[str, str]:
    """
    Splits a filename into its base name and extension.

    Args:
        filepath: The path to the file.

    Returns:
        A tuple (name, extension), e.g., ('document', '.txt').
    """
    path_obj = get_path_object(filepath)
    return (path_obj.stem, path_obj.suffix)

def is_file(path: Union[str, Path]) -> bool:
    """Checks if the path is an existing file."""
    return get_path_object(path).is_file()

def is_directory(path: Union[str, Path]) -> bool:
    """Checks if the path is an existing directory."""
    return get_path_object(path).is_dir()

def path_exists(path: Union[str, Path]) -> bool:
    """Checks if the path exists (either file or directory)."""
    return get_path_object(path).exists()

# --- Example Usage (Self-Test) ---

if __name__ == '__main__':
    TEST_DIR = "test_fs_ops_temp"
    TEST_FILE = "data.txt"
    TEST_SUBDIR_A = "logs_A"
    TEST_SUBDIR_B = "logs_B"
    FULL_FILE_PATH = join_paths(TEST_DIR, TEST_SUBDIR_A, TEST_FILE)
    FULL_SUBDIR_PATH_A = join_paths(TEST_DIR, TEST_SUBDIR_A)
    FULL_SUBDIR_PATH_B = join_paths(TEST_DIR, TEST_SUBDIR_B)
    TEST_CONTENT = "Hello, world! This is a test file for integrity check."

    print("--- Filesystem Utilities Demo (Comprehensive) ---")

    # 1. Clean up and setup
    print(f"\n1. Cleaning up test environment: {delete_path(TEST_DIR)}")
    create_directory(FULL_SUBDIR_PATH_A)
    
    # 2. Atomic Write Demonstration
    print(f"\n2. Atomic Write Demonstration:")
    atomic_success = atomic_write_file_content(FULL_FILE_PATH, TEST_CONTENT)
    print(f"  Atomic write successful: {atomic_success}")

    # 3. Checksum and Integrity
    print(f"\n3. Checksum and Integrity Check:")
    sha256 = get_file_checksum(FULL_FILE_PATH, algorithm='sha256')
    md5 = get_file_checksum(FULL_FILE_PATH, algorithm='md5')
    print(f"  SHA256 Checksum: {sha256}")
    print(f"  MD5 Checksum:    {md5}")

    # 4. File Metadata (Times)
    print(f"\n4. File Metadata (Timestamps):")
    times = get_file_times(FULL_FILE_PATH)
    if times:
        print(f"  Last Modified: {time.ctime(times['modified'])}")
        print(f"  Creation/Metadata Change: {time.ctime(times['created'])}")

    # 5. Temporary Directory Management
    print(f"\n5. Temporary Directory Management:")
    temp_dir = create_temp_directory()
    if temp_dir:
        temp_file = join_paths(temp_dir, "temp_data.log")
        write_file_content(temp_file, "Temporary log entry.")
        print(f"  Created temporary directory: {temp_dir}")
        print(f"  Contents: {list_directory_contents(temp_dir)}")
        print(f"  Cleaning up temporary directory: {delete_path(temp_dir)}")

    # 6. Final Cleanup
    print(f"\n6. Final cleanup of test directory: {delete_path(TEST_DIR)}")
    print(f"Does '{TEST_DIR}' exist after cleanup? {path_exists(TEST_DIR)}")