import csv
import os
import time # Needed for advisory file locking mechanism

# --- Configuration Constants for Advisory File Locking ---
LOCK_TIMEOUT_SECONDS = 5
LOCK_RETRY_DELAY_SECONDS = 0.2
# --------------------------------------------------------

class CSVManager:
    """
    A pure-Python library class for handling, managing, creating, updating,
    and modifying data in Comma Separated Value (CSV) files.

    Data is stored internally as a list of dictionaries, making manipulation easy.
    Now includes advanced features for quoting/escaping and advisory file locking.
    """

    def __init__(self, filepath=None, headers=None, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL):
        """
        Initializes the CSVManager.

        :param filepath: Optional. Path to an existing CSV file to load.
        :param headers: Optional. List of headers for a new file, if no filepath is provided.
        :param delimiter: The character used to separate values (default is ',').
        :param quotechar: The character used to quote fields containing special chars (default is '"').
        :param quoting: Controls when quotes are generated. Should be a constant from the 'csv' module 
                        (e.g., csv.QUOTE_MINIMAL, csv.QUOTE_ALL, csv.QUOTE_NONE, csv.QUOTE_NONNUMERIC).
        """
        self.filepath = filepath
        self.delimiter = delimiter
        self.quotechar = quotechar
        self.quoting = quoting
        self.data = []  # Internal storage: list of dictionaries
        self.headers = headers if headers is not None else []

        if filepath and os.path.exists(filepath):
            self.load_from_file(filepath)
        elif headers:
            print(f"Initialized new CSV manager with headers: {headers}")

    def load_from_file(self, filepath):
        """
        Reads data from a specified CSV file into the internal data structure.
        Uses the first row as headers.

        :param filepath: Path to the CSV file.
        """
        self.filepath = filepath
        self.data = []
        try:
            with open(filepath, mode='r', newline='', encoding='utf-8') as f:
                # Use DictReader for easy handling of headers. It automatically handles quoting based on file content.
                reader = csv.DictReader(f, delimiter=self.delimiter, quotechar=self.quotechar)
                self.headers = reader.fieldnames if reader.fieldnames else []
                for row in reader:
                    self.data.append(dict(row))
            print(f"Successfully loaded {len(self.data)} rows from {filepath}")
        except FileNotFoundError:
            print(f"Error: File not found at {filepath}. Initializing with empty data.")
        except Exception as e:
            print(f"An error occurred during file loading: {e}")

    def _acquire_lock(self, lock_file):
        """
        Advisory file locking mechanism using a .lock file.
        Attempts to create the lock file exclusively.
        """
        max_retries = int(LOCK_TIMEOUT_SECONDS / LOCK_RETRY_DELAY_SECONDS) if LOCK_RETRY_DELAY_SECONDS > 0 else 1
        
        for attempt in range(max_retries):
            try:
                # 'x' mode means exclusive creation, fails if the file already exists
                with open(lock_file, 'x'):
                    return True
            except FileExistsError:
                # Lock file exists, wait and retry
                time.sleep(LOCK_RETRY_DELAY_SECONDS)
            except Exception as e:
                print(f"Lock acquisition error: {e}")
                return False
        return False

    def _release_lock(self, lock_file):
        """Releases the advisory lock by deleting the lock file."""
        try:
            os.remove(lock_file)
            return True
        except FileNotFoundError:
            # Lock was probably never acquired or already removed
            return True
        except Exception as e:
            print(f"Error releasing lock: {e}")
            return False

    def save_to_file(self, filepath=None):
        """
        Writes the current internal data structure back to a CSV file.
        Uses advisory file locking to ensure write operations are safe.

        :param filepath: Optional. Path to save the file. If None, uses the initialized path.
        """
        path_to_save = filepath if filepath else self.filepath
        if not path_to_save:
            print("Error: No filepath specified for saving.")
            return

        if not self.headers and self.data:
            # Infer headers from the first row if not explicitly set
            self.headers = list(self.data[0].keys())
        elif not self.headers and not self.data:
             print("Warning: No data or headers to save. Skipping file creation.")
             return

        lock_file = path_to_save + '.lock'
        
        if not self._acquire_lock(lock_file):
            print(f"Error: Could not acquire lock for {path_to_save} after {LOCK_TIMEOUT_SECONDS} seconds. Save aborted.")
            return
            
        try:
            # The DictWriter handles escaping (quoting) based on self.quoting and self.quotechar
            with open(path_to_save, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(
                    f, 
                    fieldnames=self.headers, 
                    delimiter=self.delimiter, 
                    quotechar=self.quotechar, 
                    quoting=self.quoting
                )
                writer.writeheader()
                writer.writerows(self.data)
            print(f"Successfully saved {len(self.data)} rows to {path_to_save} (Quoting: {self.quoting}, QuoteChar: '{self.quotechar}')")
        except Exception as e:
            print(f"An error occurred during file saving: {e}")
        finally:
            self._release_lock(lock_file)


    def get_data(self):
        """Returns the current list of data rows (list of dictionaries)."""
        return self.data

    def add_row(self, row_data):
        """
        Adds a new row to the data.

        :param row_data: A dictionary representing the new row.
                         Keys should match the existing headers.
        """
        if not self.headers and row_data:
            self.headers = list(row_data.keys())
        
        # Ensure the row has all current headers, filling missing fields with empty string
        new_row = {header: row_data.get(header, '') for header in self.headers}
        self.data.append(new_row)
        print(f"Added new row: {new_row}")

    def update_row(self, filter_key, filter_value, updates):
        """
        Updates fields in rows matching a specific criteria.

        :param filter_key: The key (column name) to filter on.
        :param filter_value: The value in that column that identifies the row(s).
        :param updates: A dictionary of {column: new_value} to apply.
        :return: The number of rows updated.
        """
        count = 0
        for row in self.data:
            if str(row.get(filter_key)) == str(filter_value):
                for key, value in updates.items():
                    if key in self.headers:
                        row[key] = value
                count += 1
        print(f"Updated {count} row(s) matching {filter_key}={filter_value}")
        return count

    def delete_row(self, filter_key, filter_value):
        """
        Deletes rows matching a specific criteria.

        :param filter_key: The key (column name) to filter on.
        :param filter_value: The value in that column that identifies the row(s).
        :return: The number of rows deleted.
        """
        initial_count = len(self.data)
        # Recreate the list, keeping only rows that DO NOT match the criteria
        self.data = [
            row for row in self.data 
            if str(row.get(filter_key)) != str(filter_value)
        ]
        deleted_count = initial_count - len(self.data)
        print(f"Deleted {deleted_count} row(s) matching {filter_key}={filter_value}")
        return deleted_count

    def get_column(self, column_name):
        """
        Extracts all values from a specific column.

        :param column_name: The name of the column (header).
        :return: A list of values from that column.
        """
        if column_name not in self.headers:
            print(f"Error: Column '{column_name}' not found in headers.")
            return []

        return [row.get(column_name, '') for row in self.data]

    def filter_data(self, filter_criteria):
        """
        Filters the data based on multiple key-value criteria.

        :param filter_criteria: A dictionary where keys are column names and
                                values are the exact values to match.
        :return: A list of dictionaries (rows) that match all criteria.
        """
        results = []
        for row in self.data:
            match = True
            for key, expected_value in filter_criteria.items():
                if str(row.get(key)) != str(expected_value):
                    match = False
                    break
            if match:
                results.append(row)
        return results

    def __str__(self):
        """String representation of the manager and its data."""
        return f"CSVManager(Headers={self.headers}, Rows={len(self.data)})"

# --- Demonstration and Usage Example ---

def demonstration():
    """Demonstrates the usage of the CSVManager class, including new features."""
    
    DEMO_FILE = 'sample_data.csv'

    # Clean up previous demo file and lock file if they exist
    if os.path.exists(DEMO_FILE):
        os.remove(DEMO_FILE)
    if os.path.exists(DEMO_FILE + '.lock'):
        os.remove(DEMO_FILE + '.lock')

    print("--- 1. Creating and Adding Data (Including Text Needing Escaping) ---")
    # Initialize a new manager with headers
    manager = CSVManager(
        headers=['ID', 'Name', 'Description', 'Notes'], 
        quoting=csv.QUOTE_MINIMAL # Default quoting strategy
    )
    print(manager)

    # Add data rows. The 'Description' field contains commas and newlines, requiring quoting/escaping.
    manager.add_row({'ID': 1, 'Name': 'Product A', 'Description': 'This item is red, large, and shiny.', 'Notes': 'OK'})
    manager.add_row({'ID': 2, 'Name': 'Product B', 'Description': 'A new product\nwith multiple lines.', 'Notes': 'Check'})
    manager.add_row({'ID': 3, 'Name': 'Product C', 'Description': 'Contains the quote char "', 'Notes': 'Done'})

    # Save the initial data to a file
    manager.save_to_file(DEMO_FILE)

    print("\n--- 2. Advisory Locking Test (Simulated Concurrent Access) ---")
    lock_file = DEMO_FILE + '.lock'
    
    # Manually create a lock file to simulate another process holding the lock
    print(f"Attempting to manually acquire advisory lock ({lock_file})...")
    
    # We use the internal method here for simulation purposes
    if manager._acquire_lock(lock_file):
        print("Manual lock acquired successfully.")
        
        # Try to save the file while the lock is held
        print("Attempting to save data while lock is held (should fail)...")
        manager.save_to_file(DEMO_FILE) # This will fail to acquire the lock
        
        # Release the lock
        manager._release_lock(lock_file)
        print("Manual lock released.")
    else:
        print("Failed to acquire manual lock in simulation setup.")


    print("\n--- 3. Loading and Verifying Escaped Data ---")
    # Load the data back to see that escaping was handled correctly
    new_manager = CSVManager(filepath=DEMO_FILE)
    
    print("\nVerifying Description from ID 2:")
    product_b = new_manager.filter_data({'ID': '2'})
    if product_b:
        print(f"Retrieved Description: '{product_b[0].get('Description')}'")


    # Save again (should work now)
    print("\nAttempting final save (should succeed)...")
    new_manager.save_to_file(DEMO_FILE)
    
    print("\nFinal Data:")
    for row in new_manager.get_data():
        print(row)

    # Clean up the demo file and lock file
    os.remove(DEMO_FILE)
    if os.path.exists(lock_file):
        os.remove(lock_file)
    print(f"\nCleaned up {DEMO_FILE} and {lock_file}")

# Execute the demonstration when the script is run directly
if __name__ == "__main__":
    demonstration()