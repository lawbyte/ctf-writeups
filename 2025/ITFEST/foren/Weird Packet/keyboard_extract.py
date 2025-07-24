#!/usr/bin/env python3
import subprocess

# USB HID keyboard mapping
usb_hid_map = {
    0x04: 'a', 0x05: 'b', 0x06: 'c', 0x07: 'd', 0x08: 'e', 0x09: 'f',
    0x0a: 'g', 0x0b: 'h', 0x0c: 'i', 0x0d: 'j', 0x0e: 'k', 0x0f: 'l',
    0x10: 'm', 0x11: 'n', 0x12: 'o', 0x13: 'p', 0x14: 'q', 0x15: 'r',
    0x16: 's', 0x17: 't', 0x18: 'u', 0x19: 'v', 0x1a: 'w', 0x1b: 'x',
    0x1c: 'y', 0x1d: 'z', 0x1e: '1', 0x1f: '2', 0x20: '3', 0x21: '4',
    0x22: '5', 0x23: '6', 0x24: '7', 0x25: '8', 0x26: '9', 0x27: '0',
    0x28: '\n', 0x2a: '[BACKSPACE]', 0x2c: ' ', 0x2d: '-', 0x2e: '=',
    0x2f: '[', 0x30: ']', 0x33: ';', 0x34: "'", 0x36: ',', 0x37: '.', 0x38: '/'
}

# Shift characters
shift_map = {
    '1': '!', '2': '@', '3': '#', '4': '$', '5': '%', '6': '^', '7': '&',
    '8': '*', '9': '(', '0': ')', '-': '_', '=': '+', '[': '{', ']': '}',
    ';': ':', "'": '"', ',': '<', '.': '>', '/': '?'
}

def extract_keyboard():
    # Extract keyboard USB data
    cmd = ['tshark', '-r', 'chall.pcap', '-Y', 'usb.src == "1.1.2" and usb.transfer_type == 0x01', '-T', 'fields', '-e', 'usb.capdata']
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return result.stdout.strip().split('\n')

def parse_keyboard(data_lines):
    message = ""
    shift_pressed = False
    prev_keycode = 0
    
    for line in data_lines:
        if not line.strip():
            continue
            
        try:
            data = bytes.fromhex(line.strip())
            if len(data) != 8:
                continue
                
            modifier = data[0]
            keycode = data[2]
            
            shift_pressed = bool(modifier & 0x02) or bool(modifier & 0x20)
            
            if keycode != 0 and keycode != prev_keycode:
                if keycode in usb_hid_map:
                    char = usb_hid_map[keycode]
                    
                    if keycode == 0x2a:  # Backspace
                        if message:
                            message = message[:-1]
                        continue
                    
                    if char.isalpha():
                        if shift_pressed:
                            char = char.upper()
                    elif shift_pressed and char in shift_map:
                        char = shift_map[char]
                    
                    message += char
            
            prev_keycode = keycode
            
        except ValueError:
            continue
    
    return message

if __name__ == "__main__":
    print("Extracting keyboard message...")
    
    keyboard_data = extract_keyboard()
    message = parse_keyboard(keyboard_data)
    
    print("\nCLEAN MESSAGE:")
    print("=" * 50)
    print(message)
    print("=" * 50)
    
    # Save to file
    with open('clean_message.txt', 'w') as f:
        f.write(message)
    print(f"\nSaved to clean_message.txt") 
