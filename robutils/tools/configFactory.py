import os
import json
import configparser
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod

# -----------------------------------------------------------
# 1. ABSTRACT BASE CLASS
# -----------------------------------------------------------

class BaseConfig(ABC):
    """
    Abstract Base Class for all configuration handlers.
    It provides common methods for data manipulation (get/set) 
    using dotted path notation. All implementations use only the 
    Python Standard Library.
    """
    
    def __init__(self, filepath):
        """Initializes the config handler with the file path."""
        self.filepath = filepath
        self.data = {} # Internal dictionary to store config data
    
    @abstractmethod
    def load(self):
        """Load configuration data from the file."""
        pass
    
    @abstractmethod
    def save(self):
        """Save the internal data to the configuration file."""
        pass
    
    def get(self, key, default=None):
        """
        Retrieve a value by key. Supports dotted path notation (e.g., 'section.key').
        Returns the default value if the key is not found.
        """
        try:
            return self._resolve_path(key)
        except (KeyError, IndexError, TypeError):
            return default

    def set(self, key, value):
        """
        Set a value for a given key. Supports dotted path notation.
        Creates intermediate dictionaries/sections if they don't exist.
        """
        self._set_path(key, value)
        
    def _resolve_path(self, key):
        """Internal helper to traverse and return a value from the data structure."""
        parts = key.split('.')
        current = self.data
        
        for part in parts:
            if isinstance(current, dict):
                current = current[part]
            else:
                # Structure break
                raise KeyError(f"Path part '{part}' not found or structure invalid at {key}")
                
        return current

    def _set_path(self, key, value):
        """Internal helper to traverse and set a value in the data structure."""
        parts = key.split('.')
        current = self.data
        
        # Traverse until the second to last part
        for part in parts[:-1]:
            if part not in current or not isinstance(current[part], dict):
                current[part] = {} # Create the section/nested dict if it doesn't exist
            current = current[part]
            
        # Set the final key/value
        current[parts[-1]] = value

# -----------------------------------------------------------
# 2. STANDARD LIBRARY FORMAT-SPECIFIC HANDLERS
# -----------------------------------------------------------

class INIConfig(BaseConfig):
    """Handles INI configuration files using standard library's configparser."""
    
    def load(self):
        config = configparser.ConfigParser()
        if os.path.exists(self.filepath):
            # Read files without raising error if missing
            config.read(self.filepath)
            # Convert configparser object to a standard dict structure
            self.data = {s: dict(config.items(s)) for s in config.sections()}
        else:
            self.data = {}
            
    def save(self):
        config = configparser.ConfigParser()
        
        # Restructure the internal dict for configparser
        for section, items in self.data.items():
            if section != 'DEFAULT':
                config[section] = items
            
        with open(self.filepath, 'w') as configfile:
            config.write(configfile)

class JSONConfig(BaseConfig):
    """Handles JSON configuration files using standard library's json module."""
    
    def load(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r') as f:
                # Handle empty file case
                try:
                    self.data = json.load(f)
                except json.JSONDecodeError:
                    self.data = {}
        else:
            self.data = {}
            
    def save(self):
        with open(self.filepath, 'w') as f:
            # Use indent=4 for human-readable output
            json.dump(self.data, f, indent=4)
            
class XMLConfig(BaseConfig):
    """Handles XML configuration files using standard library's xml.etree.ElementTree.
    Note: This implementation assumes a simple 'root > section > key' structure 
    to map to the internal dictionary format. Complex XML structures are not fully supported.
    """
    
    def load(self):
        self.data = {}
        if os.path.exists(self.filepath):
            try:
                tree = ET.parse(self.filepath)
                root = tree.getroot()
                for section_element in root:
                    section_name = section_element.tag
                    self.data[section_name] = {}
                    for item_element in section_element:
                        key = item_element.tag
                        value = item_element.text
                        self.data[section_name][key] = value
            except ET.ParseError as e:
                print(f"Error parsing XML file {self.filepath}: {e}")
                self.data = {}
        
    def save(self):
        # Create the root element (e.g., <config>)
        root = ET.Element("config") 
        
        for section_name, items in self.data.items():
            section_element = ET.SubElement(root, section_name)
            for key, value in items.items():
                item_element = ET.SubElement(section_element, key)
                item_element.text = str(value)
                
        tree = ET.ElementTree(root)
        # Write to file
        tree.write(self.filepath, encoding='utf-8', xml_declaration=True)

# -----------------------------------------------------------
# 3. CONFIG FACTORY
# -----------------------------------------------------------

def ConfigFactory(filepath):
    """
    Factory function to return the correct ConfigHandler based on file extension.
    Only supports standard library formats: .ini, .json, .xml.
    """
    ext = os.path.splitext(filepath)[1].lower()
    
    if ext == '.ini':
        return INIConfig(filepath)
    elif ext == '.json':
        return JSONConfig(filepath)
    elif ext == '.xml':
        return XMLConfig(filepath)
    else:
        raise ValueError(f"Unsupported configuration file type: {ext}. Must be .ini, .json, or .xml.")

# -----------------------------------------------------------
# 4. USAGE EXAMPLE
# -----------------------------------------------------------

if __name__ == '__main__':
    # --- Example 1: JSON Configuration ---
    print("--- JSON Example ---")
    json_filepath = 'pure_config.json'
    json_config = ConfigFactory(json_filepath)
    
    # Set nested data
    json_config.set('server.host', 'localhost')
    json_config.set('server.port', 8080)
    json_config.set('features.enabled', True)
    
    json_config.save()
    print(f"Saved JSON configuration to {json_filepath}")
    
    # Load and retrieve
    loaded_json = ConfigFactory(json_filepath)
    loaded_json.load()
    is_enabled = loaded_json.get('features.enabled')
    print(f"Retrieved JSON Feature Enabled Status: {is_enabled}")
    
    # --- Example 2: XML Configuration ---
    print("\n--- XML Example ---")
    xml_filepath = 'pure_config.xml'
    xml_config = ConfigFactory(xml_filepath)

    # Set data (maps to <users><max>100</max></users>)
    xml_config.set('users.max', 100)
    xml_config.set('theme.color', '#1E90FF')

    xml_config.save()
    print(f"Saved XML configuration to {xml_filepath}")

    # Load and retrieve
    loaded_xml = ConfigFactory(xml_filepath)
    loaded_xml.load()
    max_users = loaded_xml.get('users.max')
    print(f"Retrieved XML Max Users: {max_users}")
    
    # --- Example 3: General Manipulation (INI) ---
    print("\n--- INI Manipulation Example ---")
    ini_filepath = 'pure_config.ini'
    ini_config = ConfigFactory(ini_filepath)
    ini_config.set('Logging.Level', 'DEBUG')
    ini_config.set('Logging.File', '/var/log/app.log')
    ini_config.save()
    
    # Change value
    ini_config.set('Logging.Level', 'INFO')
    ini_config.save()
    
    loaded_ini = ConfigFactory(ini_filepath)
    loaded_ini.load()
    log_level = loaded_ini.get('Logging.Level')
    print(f"Updated INI Log Level: {log_level}")

    # --- Cleanup ---
    print("\nCleaning up created files...")
    # These lines are commented out, but show how to clean up the files if needed.
    # for f in [json_filepath, xml_filepath, ini_filepath]:
    #     if os.path.exists(f):
    #         os.remove(f)
    print("Cleanup complete.")