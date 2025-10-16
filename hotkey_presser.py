#!/usr/bin/env python3
"""
Hotkey Presser Module
Automatically press or hold down keys for gaming applications
"""

import threading
import time
try:
    import pynput
    from pynput import keyboard
    from pynput.keyboard import Key, Listener as KeyboardListener
except ImportError:
    print("Warning: pynput not installed. Please install with: pip install pynput")
    pynput = None

class HotkeyPresser:
    def __init__(self):
        self.is_pressing = False
        self.press_thread = None
        self.hotkey_listener = None
        self.stop_pressing_flag = False
        
        # Default settings
        self.target_key = 'f'
        self.press_mode = 'continuous'  # 'continuous' or 'hold'
        self.press_interval = 0.05  # seconds between presses in continuous mode
        self.activation_hotkey = 'F8'
        
    def start_pressing(self, key='f', mode='continuous', interval=0.05, activation_hotkey='F8'):
        """Start pressing/holding the specified key"""
        if not pynput:
            print("Cannot start key pressing: pynput not available")
            return
            
        if self.is_pressing:
            print("Hotkey presser is already running")
            return
            
        # Store settings
        self.target_key = key.lower()
        self.press_mode = mode
        self.press_interval = max(0.001, interval)  # Minimum 1ms
        self.activation_hotkey = activation_hotkey
        self.stop_pressing_flag = False
        
        print(f"Starting hotkey presser - Key: {key}, Mode: {mode}")
        if mode == 'continuous':
            print(f"Interval: {interval}s")
        print(f"Press {activation_hotkey} to toggle")
        
        # Setup hotkey listener
        self.setup_hotkey_listener()
        
        # Start pressing thread
        self.press_thread = threading.Thread(target=self._pressing_worker)
        self.press_thread.daemon = True
        self.press_thread.start()
        
    def setup_hotkey_listener(self):
        """Setup hotkey listener for toggling key pressing"""
        def on_key_press(key):
            try:
                # Check for activation hotkey
                key_str = ''
                if hasattr(key, 'name'):
                    key_str = key.name.upper()
                else:
                    key_str = str(key).replace("'", "").upper()
                    
                if key_str == self.activation_hotkey.upper():
                    if self.is_pressing:
                        self.stop_pressing()
                    else:
                        # If stopped, restart with current settings
                        self.start_pressing(self.target_key, self.press_mode,
                                          self.press_interval, self.activation_hotkey)
            except Exception as e:
                print(f"Hotkey error: {e}")
                
        self.hotkey_listener = KeyboardListener(on_press=on_key_press)
        self.hotkey_listener.start()
        
    def _pressing_worker(self):
        """Worker thread for key pressing/holding"""
        if not pynput:
            return
            
        keyboard_controller = keyboard.Controller()
        self.is_pressing = True
        
        try:
            # Parse target key
            target_key = self._parse_key(self.target_key)
            if not target_key:
                print(f"Invalid key: {self.target_key}")
                return
                
            press_count = 0
            
            if self.press_mode == 'hold':
                # Hold down mode - press once and hold until stopped
                print(f"Holding down key: {self.target_key}")
                keyboard_controller.press(target_key)
                
                # Keep holding until stopped
                while not self.stop_pressing_flag:
                    time.sleep(0.1)  # Check every 100ms
                    
                # Release key when stopping
                keyboard_controller.release(target_key)
                print(f"Released key: {self.target_key}")
                
            else:
                # Continuous press mode - repeatedly press and release
                print(f"Continuously pressing key: {self.target_key}")
                
                while not self.stop_pressing_flag:
                    # Press and release key
                    keyboard_controller.press(target_key)
                    time.sleep(0.001)  # Very short press duration
                    keyboard_controller.release(target_key)
                    
                    press_count += 1
                    
                    # Wait before next press
                    if not self.stop_pressing_flag:
                        time.sleep(self.press_interval)
                        
                print(f"Stopped continuous pressing. Total presses: {press_count}")
                
        except Exception as e:
            print(f"Key pressing error: {e}")
        finally:
            self.is_pressing = False
            if self.hotkey_listener:
                self.hotkey_listener.stop()
            print("Hotkey presser stopped")
            
    def _parse_key(self, key_str):
        """Parse key string to pynput key object"""
        try:
            # Convert to lowercase for consistency
            key_str = key_str.lower().strip()
            
            # Handle special keys
            special_keys = {
                'space': Key.space,
                'enter': Key.enter,
                'tab': Key.tab,
                'shift': Key.shift,
                'ctrl': Key.ctrl,
                'alt': Key.alt,
                'cmd': Key.cmd,
                'up': Key.up,
                'down': Key.down,
                'left': Key.left,
                'right': Key.right,
                'home': Key.home,
                'end': Key.end,
                'page_up': Key.page_up,
                'page_down': Key.page_down,
                'delete': Key.delete,
                'backspace': Key.backspace,
                'insert': Key.insert,
                'esc': Key.esc,
                'escape': Key.esc,
                'caps_lock': Key.caps_lock,
                'num_lock': Key.num_lock,
                'scroll_lock': Key.scroll_lock,
            }
            
            # Function keys
            for i in range(1, 13):
                special_keys[f'f{i}'] = getattr(Key, f'f{i}')
                
            # Check if it's a special key
            if key_str in special_keys:
                return special_keys[key_str]
                
            # Handle single character keys
            if len(key_str) == 1 and key_str.isalnum():
                return key_str
                
            # Handle some common symbols
            symbol_map = {
                ',': ',',
                '.': '.',
                '/': '/',
                ';': ';',
                "'": "'",
                '[': '[',
                ']': ']',
                '\\': '\\',
                '=': '=',
                '-': '-',
                '`': '`',
                '1': '1', '2': '2', '3': '3', '4': '4', '5': '5',
                '6': '6', '7': '7', '8': '8', '9': '9', '0': '0'
            }
            
            if key_str in symbol_map:
                return symbol_map[key_str]
                
            print(f"Warning: Unrecognized key '{key_str}', treating as character")
            return key_str
            
        except Exception as e:
            print(f"Error parsing key '{key_str}': {e}")
            return None
            
    def stop_pressing(self):
        """Stop key pressing/holding"""
        self.stop_pressing_flag = True
        self.is_pressing = False
        
        if self.hotkey_listener:
            self.hotkey_listener.stop()
            
    def press_key_once(self, key, hold_duration=0.01):
        """Press a key once with specified hold duration"""
        if not pynput:
            print("Cannot press key: pynput not available")
            return
            
        try:
            keyboard_controller = keyboard.Controller()
            target_key = self._parse_key(key)
            
            if target_key:
                keyboard_controller.press(target_key)
                time.sleep(hold_duration)
                keyboard_controller.release(target_key)
                print(f"Pressed key: {key}")
            else:
                print(f"Invalid key: {key}")
                
        except Exception as e:
            print(f"Error pressing key '{key}': {e}")
            
    def send_key_sequence(self, keys, interval=0.05):
        """Send a sequence of keys with specified interval between them"""
        if not pynput:
            print("Cannot send key sequence: pynput not available")
            return
            
        try:
            keyboard_controller = keyboard.Controller()
            
            for key in keys:
                target_key = self._parse_key(key)
                if target_key:
                    keyboard_controller.press(target_key)
                    time.sleep(0.01)
                    keyboard_controller.release(target_key)
                    time.sleep(interval)
                else:
                    print(f"Skipping invalid key: {key}")
                    
            print(f"Sent key sequence: {keys}")
            
        except Exception as e:
            print(f"Error sending key sequence: {e}")
            
    def type_text(self, text, typing_speed=0.05):
        """Type text with specified speed"""
        if not pynput:
            print("Cannot type text: pynput not available")
            return
            
        try:
            keyboard_controller = keyboard.Controller()
            
            for char in text:
                keyboard_controller.type(char)
                time.sleep(typing_speed)
                
            print(f"Typed text: {text}")
            
        except Exception as e:
            print(f"Error typing text: {e}")
            
    def set_activation_hotkey(self, hotkey):
        """Change the activation hotkey"""
        self.activation_hotkey = hotkey
        
        # Restart hotkey listener if running
        if self.hotkey_listener:
            self.hotkey_listener.stop()
            self.setup_hotkey_listener()
            
    def get_status(self):
        """Get current status information"""
        return {
            'is_pressing': self.is_pressing,
            'target_key': self.target_key,
            'press_mode': self.press_mode,
            'press_interval': self.press_interval,
            'activation_hotkey': self.activation_hotkey
        }
        
    def cleanup(self):
        """Cleanup resources"""
        self.stop_pressing()
        
        if self.hotkey_listener:
            self.hotkey_listener.stop()
            
        # Wait for thread to finish
        if self.press_thread and self.press_thread.is_alive():
            self.press_thread.join(timeout=1.0)

# Utility functions
def create_key_combo_presser(keys, activation_hotkey='F7'):
    """Create a hotkey presser for key combinations (like Ctrl+C)"""
    # This would be extended to handle key combinations
    pass

def get_supported_keys():
    """Get list of supported key names"""
    return [
        # Letters
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
        'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
        # Numbers
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
        # Function keys
        'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12',
        # Special keys
        'space', 'enter', 'tab', 'shift', 'ctrl', 'alt', 'cmd',
        'up', 'down', 'left', 'right', 'home', 'end', 'page_up', 'page_down',
        'delete', 'backspace', 'insert', 'esc', 'escape',
        'caps_lock', 'num_lock', 'scroll_lock',
        # Symbols
        ',', '.', '/', ';', "'", '[', ']', '\\', '=', '-', '`'
    ]