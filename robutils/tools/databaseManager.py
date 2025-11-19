import sqlite3
from typing import Any, Dict, List, Optional, Tuple

# Note: The 'sqlite3' module is part of Python's standard library and is imported here.
# External drivers for MySQL and PostgreSQL are now imported conditionally within
# their respective connect() methods to support the "dependency-on-demand" pattern.

# --- 1. Custom Exception ---

class DBNotSupportedError(Exception):
    """Custom exception raised when an unsupported database type is requested."""
    pass

class DBConnectionError(Exception):
    """Custom exception raised for connection failures due to missing dependencies or bad configuration."""
    pass

# --- 2. Abstract/Base Connection Interface ---

class DBConnection:
    """
    Abstract Base Class for Database Connection Handlers.

    Defines the standard interface for connecting, executing queries,
    and closing the connection, ensuring consistency across different SQL backends.
    """
    def __init__(self, config: Dict[str, Any]):
        """Initialize the connection configuration."""
        self.config = config
        self.connection: Optional[Any] = None
        self.cursor: Optional[Any] = None

    def connect(self):
        """Establishes the database connection."""
        raise NotImplementedError("Subclasses must implement the 'connect' method.")

    def close(self):
        """Closes the database connection."""
        if self.connection and hasattr(self.connection, 'close'):
            print(f"Closing connection for {self.__class__.__name__}...")
            # Safely close the connection object if it exists
            self.connection.close()
            self.connection = None
            self.cursor = None

    def execute(self, query: str, params: Optional[Tuple] = None, commit: bool = True) -> Optional[int]:
        """
        Executes a query and optionally commits the transaction.

        Returns the row count or None if the operation failed.
        """
        if not self.cursor:
            print(f"Error: Connection not established for {self.__class__.__name__}.")
            return None

        try:
            params = params or ()
            self.cursor.execute(query, params)
            if commit and self.connection and hasattr(self.connection, 'commit'):
                self.connection.commit()
            return self.cursor.rowcount
        except Exception as e:
            print(f"Database Error during execution in {self.__class__.__name__}: {e}")
            if self.connection and hasattr(self.connection, 'rollback'):
                self.connection.rollback()
            return None

    def fetch_all(self, query: str, params: Optional[Tuple] = None) -> List[Tuple]:
        """Executes a query and returns all results."""
        if not self.cursor:
            print(f"Error: Connection not established for {self.__class__.__name__}.")
            return []

        try:
            params = params or ()
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Database Error during fetch in {self.__class__.__name__}: {e}")
            return []

    def fetch_advanced(self,
                       select_fields: str,
                       table: str,
                       join_clause: Optional[str] = None,
                       where_clause: Optional[str] = None,
                       order_by: Optional[str] = None,
                       limit: Optional[int] = None) -> List[Tuple]:
        """
        Executes an advanced SELECT query using structured options to handle common SQL clauses.

        This method abstracts the following:
        - JOINs: Using the `join_clause` argument.
        - TOP N / LIMIT: Using the `limit` argument.
        - Sorting: Using the `order_by` argument (e.g., 'name ASC' for ascending, 'age DESC' for descending).

        Args:
            select_fields: Comma-separated list of columns (e.g., 'id, name').
            table: The main table name.
            join_clause: Optional JOIN clause (e.g., 'INNER JOIN orders ON users.id = orders.user_id').
            where_clause: Optional WHERE clause (e.g., 'age > 25 AND city = "London"').
            order_by: Optional ORDER BY clause (e.g., 'name ASC', 'price DESC').
            limit: Optional integer to limit the number of rows (TOP N).

        Returns:
            A list of tuples containing the query results.
        """
        query_parts = [f"SELECT {select_fields} FROM {table}"]

        if join_clause:
            query_parts.append(join_clause)

        if where_clause:
            query_parts.append(f"WHERE {where_clause}")

        if order_by:
            query_parts.append(f"ORDER BY {order_by}")

        if limit is not None and limit > 0:
            # LIMIT is the standard SQL keyword used by SQLite, MySQL, and PostgreSQL for TOP/N.
            query_parts.append(f"LIMIT {limit}")

        full_query = " ".join(query_parts) + ";"

        print(f"Executing advanced query: {full_query}")

        # Re-use the existing fetch_all implementation
        return self.fetch_all(full_query)

# --- 3. Concrete Implementation: SQLite (Natively Supported) ---

class SQLiteConnection(DBConnection):
    """
    Handles SQLite database connections using the built-in 'sqlite3' module.
    """
    def connect(self):
        """Establishes connection to the SQLite database file."""
        db_path = self.config.get('database')
        if not db_path:
            raise ValueError("SQLite configuration must include 'database' path.")

        try:
            # Set connection and cursor
            self.connection = sqlite3.connect(db_path)
            self.cursor = self.connection.cursor()
            print(f"Successfully connected to SQLite database: '{db_path}'")
        except sqlite3.Error as e:
            raise DBConnectionError(f"SQLite connection failed: {e}") from e

# --- 4. Concrete Implementation: MySQL (Conditional Dependency) ---

class MySQLConnection(DBConnection):
    """
    Handles MySQL database connections. Requires 'mysql-connector-python' or 'PyMySQL'.
    The import is handled within this method.
    """
    def connect(self):
        """Attempts to establish the MySQL database connection."""
        try:
            # Conditional Import
            import mysql.connector as db_driver

            # The full config dictionary is passed to the driver
            self.connection = db_driver.connect(**self.config)
            self.cursor = self.connection.cursor()
            print("Successfully connected to MySQL database.")

        except ImportError as e:
            raise DBConnectionError(
                "MySQL driver not found. Please install the necessary library "
                "(e.g., 'pip install mysql-connector-python' or 'pip install PyMySQL')."
            ) from e
        except Exception as e:
            raise DBConnectionError(f"MySQL connection failed with configuration error: {e}") from e

# --- 5. Concrete Implementation: PostgreSQL (Conditional Dependency) ---

class PostgreSQLConnection(DBConnection):
    """
    Handles PostgreSQL database connections. Requires 'psycopg2' (or similar driver).
    The import is handled within this method.
    """
    def connect(self):
        """Attempts to establish the PostgreSQL database connection."""
        try:
            # Conditional Import
            import psycopg2 as db_driver

            # The full config dictionary is passed to the driver
            # psycopg2 uses different keyword arguments (e.g., dbname instead of database)
            # We map generic keys to psycopg2 keys for demonstration purposes.
            pg_config = {
                'host': self.config.get('host'),
                'database': self.config.get('database'),
                'user': self.config.get('user'),
                'password': self.config.get('password'),
                'port': self.config.get('port', 5432)
            }
            self.connection = db_driver.connect(**pg_config)
            self.cursor = self.connection.cursor()
            print("Successfully connected to PostgreSQL database.")

        except ImportError as e:
            raise DBConnectionError(
                "PostgreSQL driver not found. Please install the necessary library "
                "(e.g., 'pip install psycopg2-binary')."
            ) from e
        except Exception as e:
            raise DBConnectionError(f"PostgreSQL connection failed with configuration error: {e}") from e

# --- 6. Database Manager/Factory ---

class DatabaseManager:
    """
    Factory class responsible for creating and providing the correct
    DBConnection instance based on the specified database type.
    """
    DB_TYPES = {
        'sqlite': SQLiteConnection,
        'mysql': MySQLConnection,
        'postgres': PostgreSQLConnection
    }

    @staticmethod
    def get_connection(db_type: str, config: Dict[str, Any]) -> DBConnection:
        """
        Retrieves an instance of the appropriate DBConnection class.
        """
        db_type_lower = db_type.lower()
        ConnectionClass = DatabaseManager.DB_TYPES.get(db_type_lower)

        if not ConnectionClass:
            raise DBNotSupportedError(f"Database type '{db_type}' is not supported by this manager.")

        return ConnectionClass(config)

# --- 7. Example Usage ---

if __name__ == '__main__':
    # ----------------------------------------------------
    # A. SQLite Example (Fully Functional)
    # ----------------------------------------------------

    print("\n" + "=" * 60)
    print("DEMO A: SQLite (Fully Functional with built-in library)")
    print("=" * 60)

    SQLITE_CONFIG = {'database': 'test_data.db'}
    db_sqlite = None

    try:
        # 1. Get Connection
        db_sqlite = DatabaseManager.get_connection('sqlite', SQLITE_CONFIG)

        # 2. Connect
        db_sqlite.connect()

        # 3. Execute: Create Table (and a second one for joins)
        create_users_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER
        );
        """
        db_sqlite.execute(create_users_table_query)

        create_orders_table_query = """
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            user_id INTEGER,
            amount REAL
        );
        """
        db_sqlite.execute(create_orders_table_query)
        print("Tables 'users' and 'orders' created (if they didn't exist).")

        # 4. Execute: Insert Data
        insert_user_query = "INSERT INTO users (id, name, age) VALUES (?, ?, ?);"
        db_sqlite.execute(insert_user_query, (1, "Alice", 30))
        db_sqlite.execute(insert_user_query, (2, "Bob", 25))
        db_sqlite.execute(insert_user_query, (3, "Charlie", 40))
        db_sqlite.execute(insert_user_query, (4, "Zoe", 20))

        insert_order_query = "INSERT INTO orders (user_id, amount) VALUES (?, ?);"
        db_sqlite.execute(insert_order_query, (1, 99.99))
        db_sqlite.execute(insert_order_query, (3, 45.00))
        db_sqlite.execute(insert_order_query, (1, 20.50))
        print("Data inserted.")

        # 5. Fetch Advanced Data (TOP 2, sorted descending by age)
        print("\n--- Advanced Query Demo: TOP 2, Descending Sort (age) ---")
        advanced_results_limit = db_sqlite.fetch_advanced(
            select_fields="name, age",
            table="users",
            order_by="age DESC", # Decending sort
            limit=2 # Top 2
        )
        print(f"Fetched Top 2 users (Count: {len(advanced_results_limit)}):")
        for row in advanced_results_limit:
            print(f"  Name: {row[0]}, Age: {row[1]}")

        # 6. Fetch Advanced Data (All, ascending name)
        print("\n--- Advanced Query Demo: Ascending Sort (name) ---")
        advanced_results_asc = db_sqlite.fetch_advanced(
            select_fields="name",
            table="users",
            order_by="name ASC" # Ascending sort
        )
        print(f"Fetched all users sorted by name (Count: {len(advanced_results_asc)}):")
        for row in advanced_results_asc:
            print(f"  Name: {row[0]}")

        # 7. Fetch Advanced Data (JOIN Example)
        print("\n--- Advanced Query Demo: JOIN and WHERE ---")
        advanced_results_join = db_sqlite.fetch_advanced(
            select_fields="T1.name, T2.amount",
            table="users T1",
            join_clause="INNER JOIN orders T2 ON T1.id = T2.user_id",
            where_clause="T2.amount > 40"
        )
        print(f"Fetched users with orders > 40 (Count: {len(advanced_results_join)}):")
        for row in advanced_results_join:
            print(f"  User: {row[0]}, Order Amount: {row[1]}")

    except (DBNotSupportedError, DBConnectionError, ValueError) as e:
        print(f"An error occurred in SQLite demo: {e}")
    finally:
        if db_sqlite:
            db_sqlite.close()


    # ----------------------------------------------------
    # B. MySQL Example (Demonstrates Dependency-on-Demand)
    # ----------------------------------------------------

    print("\n" + "=" * 60)
    print("DEMO B: MySQL (Expected to fail without 'mysql-connector-python' installed)")
    print("=" * 60)

    MYSQL_CONFIG = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': 'mysecretpassword',
        'database': 'app_db'
    }
    db_mysql = None
    try:
        db_mysql = DatabaseManager.get_connection('mysql', MYSQL_CONFIG)
        db_mysql.connect()
        # Example of using the new advanced method on MySQL (if driver is installed)
        # db_mysql.fetch_advanced(
        #     select_fields="item_name, price",
        #     table="products",
        #     order_by="price DESC",
        #     limit=10
        # )

    except DBConnectionError as e:
        # This is the expected path if the external library isn't installed
        print(f"\n--- GRACEFUL FAILURE ---")
        print(f"Connection failed gracefully: {e}")
        print("--- GRACEFUL FAILURE ---\n")
    except DBNotSupportedError as e:
        print(f"An error occurred in MySQL demo: {e}")
    finally:
        if db_mysql:
            # Attempting to close will gracefully fail if connection wasn't established
            db_mysql.close()