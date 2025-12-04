"""Tools utilities package for configuration, database, CSV, datetime, file operations, hashing, logging, and security."""

# Import classes and functions from configFactory module
from .configFactory import (
    BaseConfig,
    INIConfig,
    JSONConfig,
    XMLConfig
)

# Import class from CSVManager module
from .CSVManager import CSVManager

# Import classes and exceptions from databaseManager module
from .databaseManager import (
    DBConnection,
    DBNotSupportedError,
    DBConnectionError,
    SQLiteConnection,
    MySQLConnection,
    PostgreSQLConnection,
    DBManager
)

# Import class from datetimeManager module
from .datetimeManager import DateTimeManager

# Import functions from filesystemManager module
from .filesystemManager import (
    get_path_object,
    read_file_content,
    write_file_content,
    atomic_write_file_content,
    append_to_file,
    file_exists,
    get_file_size,
    get_file_checksum,
    copy_file,
    move_file,
    delete_file,
    create_directory,
    delete_directory,
    list_directory,
    get_directory_size,
    find_files,
    is_file,
    is_directory,
    get_file_info,
    get_absolute_path,
    get_relative_path,
    path_join,
    split_path,
    get_file_extension,
    get_file_name,
    get_directory_name,
    ensure_directory_exists,
    get_directory_tree
)

# Import class from HashTools module
from .HashTools import HashTools

# Import classes and functions from logger module
from .logger import (
    AbstractFilter,
    LevelFilter,
    NameFilter,
    ContextFilter,
    AbstractHandler,
    ConsoleHandler,
    FileHandler,
    SQLiteHandler,
    StreamHandler,
    Logger,
    get_logger
)

# Import functions and classes from passwordManager module
from .passwordManager import (
    hash_password,
    verify_password,
    generate_password,
    get_password_strength,
    is_strong_password,
    InvalidCredentialsError
)

__all__ = [
    # configFactory
    'BaseConfig',
    'INIConfig',
    'JSONConfig',
    'XMLConfig',
    # CSVManager
    'CSVManager',
    # databaseManager
    'DBConnection',
    'DBNotSupportedError',
    'DBConnectionError',
    'SQLiteConnection',
    'MySQLConnection',
    'PostgreSQLConnection',
    'DBManager',
    # datetimeManager
    'DateTimeManager',
    # filesystemManager
    'get_path_object',
    'read_file_content',
    'write_file_content',
    'atomic_write_file_content',
    'append_to_file',
    'file_exists',
    'get_file_size',
    'get_file_checksum',
    'copy_file',
    'move_file',
    'delete_file',
    'create_directory',
    'delete_directory',
    'list_directory',
    'get_directory_size',
    'find_files',
    'is_file',
    'is_directory',
    'get_file_info',
    'get_absolute_path',
    'get_relative_path',
    'path_join',
    'split_path',
    'get_file_extension',
    'get_file_name',
    'get_directory_name',
    'ensure_directory_exists',
    'get_directory_tree',
    # HashTools
    'HashTools',
    # logger
    'AbstractFilter',
    'LevelFilter',
    'NameFilter',
    'ContextFilter',
    'AbstractHandler',
    'ConsoleHandler',
    'FileHandler',
    'SQLiteHandler',
    'StreamHandler',
    'Logger',
    'get_logger',
    # passwordManager
    'hash_password',
    'verify_password',
    'generate_password',
    'get_password_strength',
    'is_strong_password',
    'InvalidCredentialsError'
]
