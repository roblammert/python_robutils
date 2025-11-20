import hashlib
import hmac
import os
from typing import Union, List, Optional
from pathlib import Path

# --- Configuration and Utility ---

class HashTools:
    """
    A comprehensive utility class for hashing and HMAC generation, supporting 
    strings, bytes, and files. All methods are static as they do not rely 
    on class instance state.
    """
    @staticmethod
    def get_algorithms() -> List[str]:
        """Returns a sorted list of all available hashing algorithms in the environment."""
        return sorted(hashlib.algorithms_available)

    @staticmethod
    def is_supported(algorithm: str) -> bool:
        """Checks if a specific algorithm is supported."""
        return algorithm.lower() in hashlib.algorithms_available

    @staticmethod
    def _get_hasher(
        algorithm: str, 
        key: Optional[bytes],
        digest_length: Optional[int]
    ) -> Union['hashlib._Hash', 'hmac.HMAC']:
        """
        Internal function to initialize the hasher, using HMAC if a key is provided.
        Handles special initialization for variable-output-size algorithms (BLAKE2).
        
        :param algorithm: The hashing algorithm (e.g., 'sha256').
        :param key: Optional byte key for HMAC.
        :param digest_length: Optional desired output length (used for BLAKE2).
        :return: An initialized hash or HMAC object.
        :raises ValueError: If the algorithm is unsupported.
        """
        algo_lower = algorithm.lower()

        if not HashTools.is_supported(algo_lower):
            raise ValueError(
                f"Unsupported algorithm '{algorithm}'. "
                f"Supported algorithms include: {', '.join(HashTools.get_algorithms()[:10])}..."
            )
        
        kwargs = {}
        
        # BLAKE2 (blake2b, blake2s) requires the size to be passed as 'digest_size' 
        # during initialization for both standard hash and HMAC.
        if algo_lower.startswith("blake2") and digest_length is not None:
            kwargs['digest_size'] = digest_length
            
        if key is not None:
            # Key provided: Initialize as an HMAC object
            # Note: hmac.new must be passed the digestmod *object* for BLAKE2 with kwargs
            if 'digest_size' in kwargs:
                # Initialize the base hash object with parameters first
                base_hash_obj = hashlib.new(algo_lower, **kwargs)
                return hmac.new(key, digestmod=lambda: base_hash_obj)
            else:
                return hmac.new(key, digestmod=algo_lower)
        else:
            # No key: Initialize as a standard hash object
            return hashlib.new(algo_lower, **kwargs)

    @staticmethod
    def calculate_digest(
        data_source: Union[str, bytes, os.PathLike],
        algorithm: str = 'sha256',
        key: Optional[Union[str, bytes]] = None,
        encoding: str = 'utf-8',
        chunk_size: int = 4096,
        digest_length: Optional[int] = None
    ) -> str:
        """
        Calculates the hash digest for text, raw bytes, or a file path.
        If a 'key' is provided, it calculates the HMAC (Hash-based Message 
        Authentication Code) instead of a standard hash.

        The optional 'digest_length' parameter is used for variable-output-length 
        algorithms (SHAKE128, SHAKE256, BLAKE2b, BLAKE2s).

        :param data_source: The data to hash (string, bytes, or file path).
        :param algorithm: The hashing algorithm (e.g., 'md5', 'sha256').
        :param key: Optional secret key (string or bytes) for HMAC calculation.
        :param encoding: Encoding to use if data_source is a string.
        :param chunk_size: Chunk size (in bytes) for file processing (ignored for strings/bytes).
        :param digest_length: The desired output length in bytes (for SHAKE/BLAKE2 only).
        :return: The hexadecimal hash digest string.
        :raises TypeError: If input data type is invalid.
        :raises FileNotFoundError: If the file path is invalid.
        :raises ValueError: If the algorithm is unsupported.
        """
        
        # 1. Prepare the Key (if provided)
        if isinstance(key, str):
            key_bytes = key.encode(encoding)
        elif isinstance(key, bytes) or key is None:
            key_bytes = key
        else:
            raise TypeError("Key must be a string or bytes.")

        # 2. Initialize Hasher (Standard Hash or HMAC, includes BLAKE2 size setup)
        try:
            hasher = HashTools._get_hasher(algorithm, key_bytes, digest_length)
        except ValueError:
            raise
        
        # 3. Process Input
        if isinstance(data_source, (str, bytes)):
            if isinstance(data_source, str):
                data_bytes = data_source.encode(encoding)
            else:
                data_bytes = data_source
            hasher.update(data_bytes)
            
        elif isinstance(data_source, os.PathLike) or (isinstance(data_source, str) and Path(data_source).is_file()):
            filepath = Path(data_source)
            if not filepath.is_file():
                raise FileNotFoundError(f"File not found: {filepath}")

            with open(filepath, 'rb') as f:
                while chunk := f.read(chunk_size):
                    hasher.update(chunk)
        else:
            raise TypeError(
                "Input 'data_source' must be a string, byte sequence, or a valid file path."
            )

        # 4. Return the Digest
        algo_lower = algorithm.lower()
        
        # SHAKE algorithms require the length to be specified when calling hexdigest()
        if algo_lower.startswith('shake') and digest_length is not None:
            return hasher.hexdigest(digest_length)
        else:
            # Standard hexdigest for fixed-length algorithms or BLAKE2 (where length was set during initialization)
            return hasher.hexdigest()


# --- Example Usage (Test/Demo) ---

if __name__ == '__main__':
    print("\n--- HashTools.py Comprehensive Demo Starting ---")
    
    text_data = "This is a secret message that needs integrity verification."
    file_name = "demo_file.dat"
    secret_key = b'my_super_secret_key_123'
    
    # Demonstrate the new HashTools class
    print(f"\n--- Available Algorithms ---")
    algos = HashTools.get_algorithms()
    print(f"Total supported: {len(algos)}")
    print(f"First 5 algorithms: {', '.join(algos[:5])}")

    # --- Setup Dummy File ---
    try:
        # Create a 4.8 KB file
        with open(file_name, 'wb') as f:
            f.write(b'Binary file contents ' * 100) 
        print(f"\n[SETUP] Created dummy file '{file_name}'.")
        
        # --- Demo 1: Standard Hashing (String) ---
        print("\n--- 1. Standard Hashing (Fixed Length) ---")
        sha256_text = HashTools.calculate_digest(text_data, algorithm='sha256')
        md5_text = HashTools.calculate_digest(text_data, algorithm='md5')
        print(f"Input:  '{text_data[:30]}...'")
        print(f"SHA256 (32 bytes): {sha256_text}")
        print(f"MD5 (16 bytes):    {md5_text}")

        # --- Demo 2: Variable Length Hashing (SHAKE & BLAKE2) ---
        print("\n--- 2. Variable Length Hashing (SHAKE & BLAKE2) ---")
        
        # SHAKE 256, output size 10 bytes (20 hex chars)
        shake_digest = HashTools.calculate_digest(text_data, algorithm='shake_256', digest_length=10)
        print(f"SHAKE256 (Length=10): {shake_digest} (Length: {len(shake_digest) // 2} bytes)")
        
        # BLAKE2b, output size 16 bytes (32 hex chars), keyed for extra measure
        blake2b_digest = HashTools.calculate_digest(text_data, algorithm='blake2b', digest_length=16, key=secret_key)
        print(f"HMAC-BLAKE2b (Length=16): {blake2b_digest} (Length: {len(blake2b_digest) // 2} bytes)")
        
        # --- Demo 3: HMAC Hashing (Keyed String) ---
        print("\n--- 3. HMAC Hashing (Keyed Text) ---")
        hmac_digest = HashTools.calculate_digest(text_data, algorithm='sha256', key=secret_key)
        print(f"Input: Text with Key: '{secret_key.decode()}'")
        print(f"HMAC-SHA256: {hmac_digest}")
        
        # Verification check: changing the key changes the HMAC
        wrong_key = b'a_different_key'
        hmac_wrong_key = HashTools.calculate_digest(text_data, algorithm='sha256', key=wrong_key)
        print(f"HMAC-SHA256 (Wrong Key): {hmac_wrong_key}")
        print(f"Match Check (Same Hash): {hmac_digest == hmac_wrong_key} (Should be False)")

        # --- Demo 4: HMAC Hashing (Keyed File) ---
        print("\n--- 4. HMAC Hashing (Keyed File) ---")
        hmac_file_digest = HashTools.calculate_digest(file_name, algorithm='sha512', key=secret_key)
        print(f"Input: File '{file_name}' with Key: '{secret_key.decode()}'")
        print(f"HMAC-SHA512: {hmac_file_digest}")

        # --- Demo 5: Error Handling ---
        print("\n--- 5. Error Handling Demo ---")
        try:
            HashTools.calculate_digest(text_data, algorithm='unsupported_algo')
        except ValueError as e:
            print(f"Caught expected error: {e}")


    except Exception as e:
        print(f"A critical error occurred during the demo: {e}")
    finally:
        # --- Cleanup ---
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"[CLEANUP] Removed dummy file '{file_name}'.")

    print("\n--- HashTools.py Comprehensive Demo Finished ---")