import base64

def encode_base64(input_string: str) -> str:
    """
    Encodes the given string into Base64.

    Args:
        input_string (str): The string to encode.

    Returns:
        str: The Base64 encoded string.
    """
    # Convert the input string to bytes
    input_bytes = input_string.encode("utf-8")
    # Encode the bytes to Base64
    base64_bytes = base64.b64encode(input_bytes)
    # Convert the Base64 bytes back to a string
    base64_string = base64_bytes.decode("utf-8")
    return base64_string

def decode_base64(base64_string: str) -> str:
    """
    Decodes a Base64 encoded string.

    Args:
        base64_string (str): The Base64 encoded string to decode.

    Returns:
        str: The decoded string.
    """
    try:
        # Convert the Base64 string to bytes
        base64_bytes = base64_string.encode("utf-8")
        # Decode the Base64 bytes
        decoded_bytes = base64.b64decode(base64_bytes)
        # Convert the bytes back to a string
        decoded_string = decoded_bytes.decode("utf-8")
        return decoded_string
    except Exception as e:
        return f"Error decoding Base64 string: {e}"
    
if __name__ == "__main__":
    raw_str = "Hello World"
    encoded_str = encode_base64(raw_str)
    print(encoded_str)
    decoded_str = decode_base64(encoded_str)
    print(decoded_str)