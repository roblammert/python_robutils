import hashlib
import secrets
import string
import math

# --- Custom Exceptions ---

class InvalidCredentialsError(Exception):
    """Custom exception raised for incorrect hash format or parsing failure."""
    pass

# --- Configuration Constants ---

# Define the currently recommended schema version.
CURRENT_SCHEMA_VERSION = "v1.1" 

# Centralized history of hashing configurations. 
# ONLY ADD new versions/iteration counts; NEVER change or remove old ones.
HASH_CONFIG_HISTORY = {
    # v1.0: Initial strong configuration
    "v1.0": 50000,   
    # v1.1: Increased iteration count for future-proofing (current recommendation)
    "v1.1": 100000, 
    # v1.2: Example of a future planned upgrade
    # "v1.2": 150000, 
}

# The currently required iteration count is derived from the history dictionary
try:
    CURRENT_ITERATIONS = HASH_CONFIG_HISTORY[CURRENT_SCHEMA_VERSION]
except KeyError:
    raise RuntimeError(f"CURRENT_SCHEMA_VERSION '{CURRENT_SCHEMA_VERSION}' not defined in HASH_CONFIG_HISTORY.")

SALT_LENGTH = 16  # Bytes

# Character Sets for Password Generation
_LOWERCASE = string.ascii_lowercase
_UPPERCASE = string.ascii_uppercase
_DIGITS = string.digits
# Define a safe, commonly-allowed subset of special characters
_SPECIAL = "!@#$%^&*()_+-=[]{}|;:,.<>?" 

def _generate_salt(length: int = SALT_LENGTH) -> bytes:
    """
    Generates a cryptographically secure random salt.
    """
    return secrets.token_bytes(length)

# --- Core Hashing and Verification ---

def hash_password(password: str) -> str:
    """
    Hashes a plaintext password using PBKDF2-HMAC-SHA256 with the CURRENT configuration.
    
    The output format is a self-describing string:
    'SCHEMA_VERSION:ITERATIONS:salt_hex:hash_hex'
    
    Args:
        password: The plaintext password string.
        
    Returns:
        A string containing the version, iteration count, salt, and hash for storage.
    """
    # 1. Generate Salt
    salt = _generate_salt()
    
    # 2. Derive Key (Hash) using CURRENT ITERATIONS
    password_bytes = password.encode('utf-8')
    derived_key = hashlib.pbkdf2_hmac(
        'sha256',
        password_bytes,
        salt,
        CURRENT_ITERATIONS, # Use the latest iteration count
        dklen=32
    )
    
    # 3. Format for Storage
    salt_hex = salt.hex()
    hash_hex = derived_key.hex()
    
    # Store all config details with the hash
    return f"{CURRENT_SCHEMA_VERSION}:{CURRENT_ITERATIONS}:{salt_hex}:{hash_hex}"

def verify_password(password: str, stored_credentials: str) -> tuple[bool, str | None]:
    """
    Verifies a plaintext password against stored credentials and checks if re-hashing is needed.
    
    The function uses the version and iteration count embedded in the stored_credentials
    to perform the correct comparison.
    
    Args:
        password: The plaintext password entered by the user.
        stored_credentials: The credential string retrieved from the database.
        
    Returns:
        A tuple (is_valid: bool, new_hash_string_if_rehash_needed: str | None).
        If the hash is valid but outdated, the new hash string is returned.
    """
    try:
        # 1. Parse Stored Credentials
        parts = stored_credentials.split(':')
        
        if len(parts) != 4:
            raise InvalidCredentialsError("Stored hash does not match the expected format (vX.X:ITERS:salt:hash).")

        version, stored_iterations_str, salt_hex, stored_hash_hex = parts

        # Check if the stored version is outdated
        needs_rehash = (version != CURRENT_SCHEMA_VERSION)

        stored_iterations = int(stored_iterations_str)
        salt = bytes.fromhex(salt_hex)
        
    except (ValueError, TypeError, KeyError) as e:
        # Catch errors from int() conversion or fromhex()
        raise InvalidCredentialsError(f"Error parsing stored credentials: {e}")

    # 2. Re-hash the provided password using the STORED iteration count
    password_bytes = password.encode('utf-8')
    derived_key = hashlib.pbkdf2_hmac(
        'sha256',
        password_bytes,
        salt,
        stored_iterations, # IMPORTANT: Must use the stored iteration count!
        dklen=32
    )
    
    # 3. Compare the new hash with the stored hash using constant-time comparison
    is_match = secrets.compare_digest(derived_key.hex(), stored_hash_hex)
    
    if is_match:
        # 4. Handle Re-hashing
        if needs_rehash:
            # Password is correct, but needs to be re-hashed with the current settings
            new_hash = hash_password(password)
            return (True, new_hash)
        else:
            return (True, None) # Valid, no re-hash needed
    else:
        return (False, None) # Invalid password

# --- Password Generation Functions ---

def generate_strong_password(
    length: int = 16, 
    use_uppercase: bool = True, 
    use_lowercase: bool = True, 
    use_digits: bool = True, 
    use_special: bool = True
) -> str:
    """
    Generates a cryptographically secure, high-entropy random password.

    The password is guaranteed to contain at least one character from every 
    selected character set.

    Args:
        length: The desired length of the password (min 8).
        use_...: Booleans to control which character sets are included.

    Returns:
        The generated strong password string.
    """
    if length < 8:
        length = 8
        
    # Build character pool and required characters
    required_chars = []
    char_pool = []
    
    if use_lowercase:
        required_chars.append(secrets.choice(_LOWERCASE))
        char_pool.append(_LOWERCASE)
    if use_uppercase:
        required_chars.append(secrets.choice(_UPPERCASE))
        char_pool.append(_UPPERCASE)
    if use_digits:
        required_chars.append(secrets.choice(_DIGITS))
        char_pool.append(_DIGITS)
    if use_special:
        required_chars.append(secrets.choice(_SPECIAL))
        char_pool.append(_SPECIAL)

    if not char_pool:
        raise ValueError("Must enable at least one character set for generation.")
        
    full_pool = "".join(char_pool)
    
    # Fill the rest of the password length randomly
    remaining_length = length - len(required_chars)
    if remaining_length < 0:
        # Handle case where required components are longer than length (shouldn't happen with min 8)
        remaining_length = 0 
        
    random_fill = [secrets.choice(full_pool) for _ in range(remaining_length)]
    
    # Combine all characters and shuffle to randomize positions
    password_list = required_chars + random_fill
    secrets.SystemRandom().shuffle(password_list) 
    
    return "".join(password_list)

def generate_pin(length: int = 6) -> str:
    """
    Generates a cryptographically secure, numeric PIN.
    
    Args:
        length: The desired length of the PIN (default 6, min 4).
        
    Returns:
        The generated PIN string.
    """
    if length < 4:
        length = 4
    
    return "".join(secrets.choice(_DIGITS) for _ in range(length))

# --- Password Quality Functions ---

def calculate_entropy(password: str) -> float:
    """
    Calculates the Shannon entropy (in bits) of a password.
    
    Entropy = L * log2(N)
    Where L is password length, and N is the size of the character space used.
    
    Returns:
        The entropy value in bits (float).
    """
    # Determine the size of the character space (N) by checking which sets are present.
    char_space_size = 0
    if any(c in _LOWERCASE for c in password):
        char_space_size += len(_LOWERCASE)
    if any(c in _UPPERCASE for c in password):
        char_space_size += len(_UPPERCASE)
    if any(c in _DIGITS for c in password):
        char_space_size += len(_DIGITS)
    if any(c in _SPECIAL for c in password):
        char_space_size += len(_SPECIAL)
        
    if char_space_size == 0:
        return 0.0

    length = len(password)
    
    return length * math.log2(char_space_size)


def is_strong_password(password: str, min_length: int = 12) -> dict:
    """
    Checks if a password meets basic strength requirements.

    Args:
        password: The plaintext password string.
        min_length: The minimum required length.

    Returns:
        A dictionary of requirements and their fulfillment status.
    """
    results = {
        'length': len(password) >= min_length,
        'uppercase': any(c.isupper() for c in password),
        'lowercase': any(c.islower() for c in password),
        'digit': any(c.isdigit() for c in password),
        'special_char': any(not c.isalnum() for c in password)
    }
    results['overall'] = all(results.values())
    return results

# --- Example Usage ---

if __name__ == '__main__':
    print("--- ADVANCED Secure Password Manager Demo (Multi-Version Support) ---")
    
    # Note: For this demo, we access the configuration constants directly to simulate old data.
    
    # A. SIMULATE OLD DATA (v1.0)
    
    print("Generated Password: "+generate_strong_password())
    
    test_password = "UserPassword123!"
    
    # 1. Temporarily calculate an "old" hash using v1.0 settings
    OLD_ITERATIONS = HASH_CONFIG_HISTORY["v1.0"] 
    OLD_VERSION = "v1.0"
    
    old_salt = _generate_salt()
    old_derived_key = hashlib.pbkdf2_hmac(
        'sha256',
        test_password.encode('utf-8'),
        old_salt,
        OLD_ITERATIONS,
        dklen=32
    )
    old_stored_hash = f"{OLD_VERSION}:{OLD_ITERATIONS}:{old_salt.hex()}:{old_derived_key.hex()}"
    print(f"\n[DEMO SETUP] Stored Hash (OLD SCHEMA {OLD_VERSION}, {OLD_ITERATIONS} iter):")
    print(f"  {old_stored_hash[:30]}...{old_stored_hash[-30:]}")
    
    # 2. Verify and Trigger Re-hash
    print(f"\n[STEP 1] Attempting to verify old hash against current schema (v{CURRENT_SCHEMA_VERSION})...")
    try:
        is_match, new_hash = verify_password(test_password, old_stored_hash)
        
        if is_match and new_hash:
            print(f"✅ Verification Successful (Password is correct).")
            print(f"   ⚠️ Re-hash Needed! Hash schema {OLD_VERSION} is outdated.")
            print(f"   New hash generated with v{CURRENT_SCHEMA_VERSION} ({CURRENT_ITERATIONS} iterations):")
            print(f"   New Hash (Current v{CURRENT_SCHEMA_VERSION}): {new_hash[:30]}...")
            
            # Action: Application should now UPDATE the database with 'new_hash'
            current_stored_hash = new_hash
        elif is_match:
            print(f"✅ Verification Successful (Hash is up-to-date).")
            current_stored_hash = old_stored_hash
        else:
            print("❌ Verification Failed (Incorrect password).")
            current_stored_hash = None

        # 3. Verify Up-to-Date Hash (no re-hash needed this time)
        if current_stored_hash:
            print("\n[STEP 2] Verifying NEW, up-to-date hash (should require no re-hash)...")
            is_match_new, rehash_check = verify_password(test_password, current_stored_hash)
            
            print(f"Result: Match={is_match_new}, Rehash Check={rehash_check}")
            if is_match_new and rehash_check is None:
                print("✅ Verification Successful. Hash is fully up-to-date.")
                
    except InvalidCredentialsError as e:
        print(f"❌ Critical Error: {e}")