import abc
import datetime
import sqlite3
import os
import sys
import socket
import json
import time 
import glob
from typing import List, Dict, Any, Optional

# --- Configuration Constants ---
# Updated LOG_FORMAT to include space for context data if available
LOG_FORMAT = "{timestamp} [{level}] {message}{context_str}"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_LEVELS = {'DEBUG': 10, 'INFO': 20, 'WARNING': 30, 'ERROR': 40, 'CRITICAL': 50}


# --- 1. Filter Mechanism ---

class AbstractFilter(abc.ABC):
    """Abstract base class for all log filters."""

    @abc.abstractmethod
    def filter(self, logger_name: str, level: str, message: str, context: Optional[Dict[str, Any]]) -> bool:
        """
        Determines if the log record should be processed.
        Returns True if the record is allowed, False otherwise.
        """
        pass

class LevelFilter(AbstractFilter):
    """Filters logs based on a minimum severity level."""

    def __init__(self, min_level: str):
        self.min_level = min_level.upper()
        self.min_level_val = LOG_LEVELS.get(self.min_level, 0)
        if self.min_level_val == 0 and self.min_level not in LOG_LEVELS:
             raise ValueError(f"Invalid log level specified for filter: {min_level}")

    def filter(self, logger_name: str, level: str, message: str, context: Optional[Dict[str, Any]]) -> bool:
        """Allow log records whose level is >= min_level."""
        log_level_val = LOG_LEVELS.get(level.upper(), 0)
        return log_level_val >= self.min_level_val

class NameFilter(AbstractFilter):
    """Filters logs based on the logger's name (only allows logs from specified names)."""

    def __init__(self, allowed_names: List[str]):
        self.allowed_names = set(n.lower() for n in allowed_names)

    def filter(self, logger_name: str, level: str, message: str, context: Optional[Dict[str, Any]]) -> bool:
        """Allow log records only if the logger_name is in the allowed list."""
        return logger_name.lower() in self.allowed_names

class ContextFilter(AbstractFilter):
    """Filters logs based on required key-value pairs in the context dictionary."""

    def __init__(self, required_context: Dict[str, Any]):
        self.required_context = required_context

    def filter(self, logger_name: str, level: str, message: str, context: Optional[Dict[str, Any]]) -> bool:
        """Allow log records only if they contain all required context key-value pairs."""
        
        if not context and bool(self.required_context):
            return False

        for key, value in self.required_context.items():
            if context is None or context.get(key) != value:
                return False
        return True


# --- 2. Abstract Handler ---

class AbstractHandler(abc.ABC):
    """Abstract base class for all log handlers, now supporting filters."""

    def __init__(self):
        self._filters: List[AbstractFilter] = []

    def add_filter(self, filter_obj: AbstractFilter) -> None:
        """Adds a filter to this specific handler."""
        self._filters.append(filter_obj)

    def is_allowed(self, logger_name: str, level: str, message: str, context: Optional[Dict[str, Any]]) -> bool:
        """Checks if the log record passes all associated filters."""
        for filter_obj in self._filters:
            if not filter_obj.filter(logger_name, level, message, context):
                return False
        return True

    @abc.abstractmethod
    def emit(self, logger_name: str, level: str, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        """Process the log record and send it to the final output."""
        pass

    def format_log(self, logger_name: str, level: str, message: str, context: Optional[Dict[str, Any]]) -> str:
        """Formats the log record into a string, including context if present."""
        timestamp = datetime.datetime.now().strftime(DATE_FORMAT)
        
        context_str = ""
        if context:
             # Only show context for console/file if it contains actual data
             context_str = f" | Context: {json.dumps(context)}"
             
        full_message = f"[{logger_name}] {message}"
        
        return LOG_FORMAT.format(
            timestamp=timestamp, 
            level=level, 
            message=full_message,
            context_str=context_str
        )


# --- 3. Concrete Handler Implementations ---

class ConsoleHandler(AbstractHandler):
    """Writes log records to standard output (stdout)."""

    def emit(self, logger_name: str, level: str, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        if not self.is_allowed(logger_name, level, message, context):
            return 

        formatted_log = self.format_log(logger_name, level, message, context)
        sys.stdout.write(f"CONSOLE: {formatted_log}\n")
        sys.stdout.flush()

class MemoryHandler(AbstractHandler):
    """Stores log records in a list in memory."""

    def __init__(self):
        super().__init__()
        self.log_records: List[str] = []

    def emit(self, logger_name: str, level: str, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        if not self.is_allowed(logger_name, level, message, context):
            return

        formatted_log = self.format_log(logger_name, level, message, context)
        self.log_records.append(formatted_log)

    def get_records(self) -> List[str]:
        """Returns all logs currently stored in memory."""
        return self.log_records

class FileHandler(AbstractHandler):
    """Writes log records to a file."""

    def __init__(self, filename: str, mode: str = 'a'):
        super().__init__()
        self.filename = filename
        self.mode = mode

    def emit(self, logger_name: str, level: str, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        if not self.is_allowed(logger_name, level, message, context):
            return

        formatted_log = self.format_log(logger_name, level, message, context)
        try:
            with open(self.filename, self.mode) as f:
                f.write(formatted_log + '\n')
        except IOError as e:
            print(f"ERROR: Could not write to file {self.filename}: {e}")

class RotatingFileHandler(FileHandler):
    """
    Writes log records to a file, rotating the file when it reaches a certain size.
    It keeps a configurable number of backup files.
    """
    def __init__(self, filename: str, max_bytes: int = 1048576, backup_count: int = 5):
        # max_bytes default is 1MB
        super().__init__(filename, 'a')
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        self.base_filename = filename

    def _do_roll_over(self) -> None:
        """Performs the log file rotation."""
        
        # 1. Rename existing backups (e.g., file.log.4 -> file.log.5)
        for i in range(self.backup_count - 1, 0, -1):
            s_name = f"{self.base_filename}.{i}"
            d_name = f"{self.base_filename}.{i + 1}"
            if os.path.exists(s_name):
                if os.path.exists(d_name):
                    os.remove(d_name)
                os.rename(s_name, d_name)

        # 2. Move current file to backup 1 (e.g., file.log -> file.log.1)
        if os.path.exists(self.base_filename):
            d_name = f"{self.base_filename}.1"
            if os.path.exists(d_name):
                os.remove(d_name)
            os.rename(self.base_filename, d_name)
            
        print(f"INFO: Log file rotated: {self.base_filename}")
        
    def emit(self, logger_name: str, level: str, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        if not self.is_allowed(logger_name, level, message, context):
            return

        formatted_log = self.format_log(logger_name, level, message, context)
        
        # Check if rollover is necessary before writing
        if os.path.exists(self.base_filename) and os.path.getsize(self.base_filename) >= self.max_bytes:
            self._do_roll_over()

        # Write to the file (uses the parent's file writing logic)
        try:
            with open(self.base_filename, self.mode) as f:
                f.write(formatted_log + '\n')
        except IOError as e:
            print(f"ERROR: Could not write to rotating file {self.base_filename}: {e}")


class SQLiteHandler(AbstractHandler):
    """Writes log records to a SQLite database."""

    def __init__(self, db_name: str = 'app_logs.db', table_name: str = 'logs'):
        super().__init__()
        self.db_name = db_name
        self.table_name = table_name
        self._ensure_table_exists()

    def _ensure_table_exists(self):
        """Creates the log table if it doesn't exist."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            logger_name TEXT,
            level TEXT,
            message TEXT,
            context_json TEXT
        );"""
        cursor.execute(create_table_sql)
        conn.commit()
        conn.close()

    def emit(self, logger_name: str, level: str, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        if not self.is_allowed(logger_name, level, message, context):
            return

        timestamp = datetime.datetime.now().strftime(DATE_FORMAT)
        context_json = json.dumps(context) if context else "{}" 

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        insert_sql = f"""
        INSERT INTO {self.table_name} (timestamp, logger_name, level, message, context_json)
        VALUES (?, ?, ?, ?, ?);
        """
        try:
            cursor.execute(insert_sql, (timestamp, logger_name, level.upper(), message, context_json))
            conn.commit()
        except sqlite3.Error as e:
            print(f"ERROR: SQLite write error: {e}")
        finally:
            conn.close()

class SocketHandler(AbstractHandler):
    """Sends log records over a TCP socket to a remote logging server."""

    def __init__(self, host: str, port: int):
        super().__init__()
        self.host = host
        self.port = port

    def emit(self, logger_name: str, level: str, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        if not self.is_allowed(logger_name, level, message, context):
            return

        # Prepare a JSON object for network transfer
        log_record = {
            'timestamp': datetime.datetime.now().strftime(DATE_FORMAT),
            'logger_name': logger_name,
            'level': level,
            'message': message,
            'context': context
        }
        data = (json.dumps(log_record) + '\n').encode('utf-8')

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.1) 
                s.connect((self.host, self.port))
                s.sendall(data)
            print(f"SUCCESS: SocketHandler sent log to {self.host}:{self.port}")
        except (ConnectionRefusedError, socket.timeout):
            pass # Silent failure for example, as listener is rarely running
        except Exception as e:
            print(f"ERROR: SocketHandler unexpected error: {e}")

class HTTPHandler(AbstractHandler):
    """Sends log records as a JSON POST request to a remote HTTP endpoint."""

    def __init__(self, url: str):
        super().__init__()
        self.url = url

    def emit(self, logger_name: str, level: str, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        if not self.is_allowed(logger_name, level, message, context):
            return

        log_payload = {
            'timestamp': datetime.datetime.now().isoformat(),
            'logger': logger_name,
            'severity': level.upper(),
            'message': message,
            'data': context if context else {}
        }
        
        # --- HTTP Post Simulation ---
        payload_json = json.dumps(log_payload, indent=2)
        print(f"\n--- HTTPHandler (POST to {self.url}) ---")
        print(f"Simulating POST request with payload:\n{payload_json}")
        time.sleep(0.01) 
        print("---------------------------------")


# --- 4. The Logger (Main Dispatcher) ---

class Logger:
    """
    The main Logger class that dispatches log records to multiple handlers.
    Users should typically retrieve instances using LoggerManager.getLogger().
    """

    def __init__(self, name: str, level: str = 'INFO'):
        self.name = name
        self.level = level.upper()
        self.handlers: List[AbstractHandler] = []

    def add_handler(self, handler: AbstractHandler) -> None:
        """Adds a handler to the logger."""
        self.handlers.append(handler)

    def set_level(self, level: str) -> None:
        """Sets the minimum log level for this logger."""
        self.level = level.upper()

    def log(self, level: str, message: str, **kwargs) -> None:
        """The core logging method that checks the logger's level and dispatches to handlers."""
        level = level.upper()
        
        # 1. Logger Level Check (The global minimum level)
        if LOG_LEVELS.get(level, 0) < LOG_LEVELS.get(self.level, 0):
            return

        # 2. Dispatch to all registered handlers
        for handler in self.handlers:
            handler.emit(self.name, level, message, context=kwargs)

    # Convenience methods
    def debug(self, message: str, **kwargs):
        self.log('DEBUG', message, **kwargs)

    def info(self, message: str, **kwargs):
        self.log('INFO', message, **kwargs)

    def warning(self, message: str, **kwargs):
        self.log('WARNING', message, **kwargs)

    def error(self, message: str, **kwargs):
        self.log('ERROR', message, **kwargs)

    def critical(self, message: str, **kwargs):
        self.log('CRITICAL', message, **kwargs)


# --- 5. Logger Manager (Singleton & Configuration API) ---

class LoggerManager:
    """
    Manages the creation and retrieval of Logger instances, ensuring singleton behavior
    for named loggers and centralizing handler configuration.
    """
    _instance = None
    _loggers: Dict[str, Logger] = {}
    _handlers: List[AbstractHandler] = []
    
    DEFAULT_LEVEL = 'INFO'

    def __new__(cls, *args, **kwargs):
        """Ensures LoggerManager is a singleton."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_logger(cls, name: str = 'root') -> Logger:
        """Retrieves or creates a named logger instance."""
        if name not in cls._loggers:
            new_logger = Logger(name=name, level=cls.DEFAULT_LEVEL)
            # Add all centrally configured handlers
            for handler in cls._handlers:
                new_logger.add_handler(handler)
            cls._loggers[name] = new_logger
        return cls._loggers[name]

    @classmethod
    def add_handler(cls, handler: AbstractHandler) -> None:
        """Adds a handler to the central configuration. Will be added to all future and existing loggers."""
        cls._handlers.append(handler)
        # Apply handler to existing loggers
        for logger in cls._loggers.values():
            logger.add_handler(handler)
            
    @classmethod
    def configure_logging(cls, config: Dict[str, Any]) -> None:
        """
        High-level function to configure the entire logging system from a dictionary.
        
        Example config structure:
        {
            'default_level': 'INFO',
            'handlers': {
                'console': {'type': 'ConsoleHandler', 'filters': []},
                'file_log': {'type': 'RotatingFileHandler', 'filename': 'app.log', 'max_bytes': 1000, 'backup_count': 3, 'filters': [{'type': 'LevelFilter', 'min_level': 'DEBUG'}]},
                'http_alerts': {'type': 'HTTPHandler', 'url': 'http://alert.io', 'filters': [{'type': 'LevelFilter', 'min_level': 'ERROR'}]},
            },
            'loggers': {
                'root': {'level': 'INFO', 'handlers': ['console', 'file_log']},
                'payment': {'level': 'WARNING', 'handlers': ['file_log', 'http_alerts']},
            }
        }
        """
        
        # Clear existing configuration
        cls._loggers.clear()
        cls._handlers.clear()
        
        # Set default level
        cls.DEFAULT_LEVEL = config.get('default_level', 'INFO').upper()
        
        # 1. Instantiate Handlers and Filters
        handler_instances = {}
        for handler_name, h_config in config.get('handlers', {}).items():
            handler_type = h_config.pop('type')
            
            # Extract filters first
            filter_configs = h_config.pop('filters', [])
            
            # Instantiate handler
            try:
                if handler_type == 'ConsoleHandler':
                    handler = ConsoleHandler(**h_config)
                elif handler_type == 'MemoryHandler':
                    handler = MemoryHandler(**h_config)
                elif handler_type == 'FileHandler':
                    handler = FileHandler(**h_config)
                elif handler_type == 'RotatingFileHandler':
                    handler = RotatingFileHandler(**h_config)
                elif handler_type == 'SQLiteHandler':
                    handler = SQLiteHandler(**h_config)
                elif handler_type == 'SocketHandler':
                    handler = SocketHandler(**h_config)
                elif handler_type == 'HTTPHandler':
                    handler = HTTPHandler(**h_config)
                else:
                    print(f"WARNING: Unknown handler type: {handler_type}. Skipping.")
                    continue
                
                # Apply filters to handler
                for f_config in filter_configs:
                    filter_type = f_config.pop('type')
                    if filter_type == 'LevelFilter':
                        handler.add_filter(LevelFilter(**f_config))
                    elif filter_type == 'NameFilter':
                        handler.add_filter(NameFilter(**f_config))
                    elif filter_type == 'ContextFilter':
                        handler.add_filter(ContextFilter(**f_config))
                    else:
                        print(f"WARNING: Unknown filter type: {filter_type}. Skipping filter on {handler_name}.")
                        
                handler_instances[handler_name] = handler
                cls.add_handler(handler) # Add to central list for unlisted loggers
                
            except Exception as e:
                print(f"ERROR configuring handler {handler_name}: {e}")

        # 2. Configure specific Loggers
        for logger_name, l_config in config.get('loggers', {}).items():
            logger = cls.get_logger(logger_name) # Uses cached or newly created logger
            
            if 'level' in l_config:
                logger.set_level(l_config['level'])
                
            # Clear default handlers and add specific ones
            if 'handlers' in l_config:
                logger.handlers = [] # Clear the default handlers added by get_logger
                for h_name in l_config['handlers']:
                    if h_name in handler_instances:
                        logger.add_handler(handler_instances[h_name])
                    else:
                        print(f"WARNING: Handler '{h_name}' not found for logger '{logger_name}'.")


class StreamHandler(ConsoleHandler):
    pass


def get_logger(name: str = 'root') -> Logger:
    return LoggerManager.get_logger(name)

# --- 6. Example Usage Demonstrating Configuration Simplicity and New Functionality ---

if __name__ == "__main__":
    
    # --- Cleanup from previous runs ---
    for f in glob.glob("test_log.*") + glob.glob("test_log") + ["app_database.db"]:
        try:
            os.remove(f)
        except OSError:
            pass
            
    # --- 1. Define Configuration Dictionary ---
    LOGGING_CONFIG = {
        'default_level': 'INFO',
        'handlers': {
            'console_only_critical': {
                'type': 'ConsoleHandler', 
                'filters': [{'type': 'LevelFilter', 'min_level': 'CRITICAL'}]
            },
            'rotating_file': {
                'type': 'RotatingFileHandler', 
                'filename': 'test_log.log', 
                'max_bytes': 200, # Very small size for quick demo
                'backup_count': 2,
                'filters': [{'type': 'LevelFilter', 'min_level': 'DEBUG'}]
            },
            'db_errors': {
                'type': 'SQLiteHandler', 
                'db_name': 'app_database.db',
                'filters': [{'type': 'LevelFilter', 'min_level': 'ERROR'}]
            },
            'http_audit': {
                'type': 'HTTPHandler',
                'url': 'https://audit.example.com',
                'filters': [{'type': 'ContextFilter', 'required_context': {'user_id': 123}}]
            }
        },
        'loggers': {
            'root': {
                'level': 'DEBUG', 
                'handlers': ['console_only_critical', 'rotating_file']
            },
            'transactions': {
                'level': 'INFO',
                'handlers': ['db_errors', 'http_audit']
            }
        }
    }
    
    print("--- 1. Configuring Logging System ---")
    LoggerManager.configure_logging(LOGGING_CONFIG)
    
    # --- 2. Retrieve Loggers ---
    root_logger = LoggerManager.get_logger("root") 
    tx_logger = LoggerManager.get_logger("transactions")
    
    print("\n--- 2. Generating Logs for Rollover Demo ---")
    
    # Log 1 & 2: Root DEBUG/INFO (Goes to file)
    root_logger.debug("Starting application setup.")
    root_logger.info("Configuration loaded successfully.")
    
    # Log 3: Tx INFO - Has context user_id=123 (Goes to HTTP)
    tx_logger.info("Transaction 101 started.", user_id=123, status="pending")
    
    # Log 4: Tx ERROR - No context (Goes to SQLite)
    tx_logger.error("Transaction 101 failed! Database lock detected.", transaction_id=101)
    
    # Log 5: Root DEBUG (Goes to file) - This should trigger file rollover since max_bytes is 200
    root_logger.debug("Writing second block of data to force rollover.")
    
    # Log 6: Tx WARNING - Has context user_id=123 (Goes to HTTP)
    tx_logger.warning("User 123 attempted large transaction.", user_id=123, limit=1000)

    # Log 7: Root CRITICAL (Goes to Console and File)
    root_logger.critical("System shutdown imminent.")
    
    print("\n--- 3. Verifying Outputs ---")
    
    # Check Rollover
    print(f"\nFiles found after rotation: {sorted(glob.glob('test_log*'))}")
    
    # Check Console (Expected: Only Log 7)
    print("\nConsole Handler output checked above (should only show CRITICAL).")
    
    # Check SQLite (Expected: Only Log 4)
    print("\n--- SQLite Logs (Expected: Log 4) ---")
    conn = sqlite3.connect('app_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT logger_name, level, message, context_json FROM logs ORDER BY id ASC")
    for row in cursor.fetchall():
        print(f"DB Record: [{row[0]}] [{row[1]}] {row[2]} ({row[3]})")
    conn.close()
    
    # Check HTTP (Expected: Log 3 and Log 6)
    print("\nHTTP Handler output checked above (should show two POST simulations).")
    
    # --- Cleanup after example ---
    for f in glob.glob("test_log*") + ["app_database.db"]:
        try:
            os.remove(f)
        except OSError:
            pass