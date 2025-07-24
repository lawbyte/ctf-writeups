#!/usr/bin/env python3

def reverse_transform_pass_char(transformed_value, position):
    """
    Reverse the password character transformation based on position.
    
    Original transform logic from IDA analysis:
    - position % 4 == 0: (char - 48) + 10
    - position % 4 == 1: (char - 48) * 2  
    - position % 4 == 2: (char - 48) ^ 7
    - position % 4 == 3: (char - 48) + 20
    """
    pos_mod = position % 4
    
    if pos_mod == 0:
        # Original: (char - 48) + 10 = transformed_value
        # So: char - 48 = transformed_value - 10
        original_value = transformed_value - 10
    elif pos_mod == 1:
        # Original: (char - 48) * 2 = transformed_value
        # So: char - 48 = transformed_value / 2
        if transformed_value % 2 != 0:
            return None  # Invalid - must be even
        original_value = transformed_value // 2
    elif pos_mod == 2:
        # Original: (char - 48) ^ 7 = transformed_value
        # So: char - 48 = transformed_value ^ 7 (XOR is self-inverse)
        original_value = transformed_value ^ 7
    elif pos_mod == 3:
        # Original: (char - 48) + 20 = transformed_value
        # So: char - 48 = transformed_value - 20
        original_value = transformed_value - 20
    
    # Convert back to ASCII character
    ascii_value = original_value + 48
    if 32 <= ascii_value <= 126:  # Printable ASCII range
        return chr(ascii_value)
    else:
        return None  # Invalid character

def reverse_transform_user_char(transformed_value, position):
    """
    Reverse the username character transformation based on position.
    
    Original transform logic:
    - position is odd (position & 1 != 0): char + 10
    - position is even: char ^ 5
    """
    if position & 1 != 0:  # Odd position
        # Original: char + 10 = transformed_value
        # So: char = transformed_value - 10
        original_char = transformed_value - 10
    else:  # Even position
        # Original: char ^ 5 = transformed_value
        # So: char = transformed_value ^ 5 (XOR is self-inverse)
        original_char = transformed_value ^ 5
    
    # Check if it's a valid ASCII printable character
    if 32 <= original_char <= 126:
        return chr(original_char)
    else:
        return None  # Invalid character

def solve_username():
    """Solve for the username using the secret_data values."""
    
    # The secret_data values from IDA (8 bytes)
    secret_data = [0x4C, 0x5E, 0x43, 0x4F, 0x56, 0x5E, 0x37, 0x3F]
    
    username = ""
    
    print("=== Solving Username ===")
    print("Pos | Secret | Odd/Even | Operation    | Calculated | Char")
    print("-" * 60)
    
    for i in range(8):
        secret_value = secret_data[i]
        is_odd = (i & 1) != 0
        
        if is_odd:
            operation = "subtract 10"
            calculated = secret_value - 10
        else:
            operation = "XOR with 5"
            calculated = secret_value ^ 5
        
        char = reverse_transform_user_char(secret_value, i)
        
        print(f"{i:3} | 0x{secret_value:02X}  | {'Odd' if is_odd else 'Even':8} |"
              f" {operation:12} | {calculated:10} | {char if char else 'FAIL'}")
        
        if char is None:
            print(f"ERROR: Could not reverse position {i} with value "
                  f"0x{secret_value:02X}")
            return None
        
        username += char
    
    return username

def solve_password():
    """Solve for the password using the pass_matrix values."""
    
    # The pass_matrix values from IDA
    pass_matrix = [
        0x2E, 0x84, 0x4E, 0x43, 0x48, 0x00, 0x43, 0x43, 0x4E, 0x3E, 0x28,
        0x4A, 0x49, 0x84, 0x30, 0x17, 0x4E, 0x5E, 0x4E, 0x14, 0x4F, 0x84,
        0x28, 0x39, 0x4D, 0x6A, 0x45, 0x52, 0x0E, 0x7A, 0x32, 0x43, 0x4A,
        0x62, 0x02, 0x19, 0x51, 0x7E, 0x45, 0x48
    ]
    
    password = ""
    
    print("Solving password with ASCII characters...")
    print("Position | Matrix Value | Pos%4 | Original Value | ASCII | Character")
    print("-" * 75)
    
    for i in range(40):
        matrix_value = pass_matrix[i]
        pos_mod = i % 4
        
        char = reverse_transform_pass_char(matrix_value, i)
        
        if char is None:
            print(f"ERROR: Could not reverse position {i} with value 0x{matrix_value:02X}")
            return None
        
        original_value = ord(char) - 48
        print(f"{i:8} | 0x{matrix_value:08X} | {pos_mod:5} | {original_value:13} | {ord(char):5} | '{char}'")
        
        password += char
    
    return password

def transform_pass_char_forward(char, position):
    """Forward transformation for verification."""
    pos_mod = position % 4
    original_value = ord(char) - 48
    
    if pos_mod == 0:
        return original_value + 10
    elif pos_mod == 1:
        return original_value * 2
    elif pos_mod == 2:
        return original_value ^ 7
    elif pos_mod == 3:
        return original_value + 20

def main():
    print("=== Login Binary Password Solver ===")
    print()
    
    password = solve_password()
    username = solve_username()
    
    print(f"Username: {username}")
    print(f"Password: {password}")

if __name__ == "__main__":
    main() 
