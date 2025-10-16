#!/usr/bin/env python3
"""
Auto Clicker Module
Automated mouse clicking with customizable settings
"""

import threading
import time
import random
try:
    import pynput
    from pynput import mouse, keyboard
    from pynput.mouse import Button, Listener as MouseListener
    from pynput.keyboard import Key, Listener as KeyboardListener
except ImportError:
    print("Warning: pynput not installed. Please install with: pip install pynput")
    pynput = None

class AutoClicker:
    def __init__(self):
        self.is_clicking = False
        self.click_thread = None
        self.hotkey_listener = None
        self.stop_clicking_flag = False
        
        # Default settings
        self.click_interval = 0.1  # seconds
        self.random_offset = False
        self.random_offset_ms = 0.04  # 40ms default
        self.mouse_button = 'left'
        self.click_type = 'single'
        self.repeat_times = 0  # 0 means unlimited
        self.hotkey = 'F6'
        
        # Click position (None means current cursor position)
        self.click_position = None
        
    def start_clicking(self, interval=0.1, random_offset=False, random_offset_val=0.04,
                      mouse_button='left', click_type='single', repeat_times=0, 
                      hotkey='F6', position=None):
        """Start auto clicking with specified settings"""
        if not pynput:
            print("Cannot start clicking: pynput not available")
            return
            
        if self.is_clicking:
            print("Auto clicker is already running")
            return
            
        # Store settings
        self.click_interval = max(0.001, interval)  # Minimum 1ms
        self.random_offset = random_offset
        self.random_offset_ms = random_offset_val
        self.mouse_button = mouse_button
        self.click_type = click_type
        self.repeat_times = repeat_times
        self.hotkey = hotkey
        self.click_position = position
        self.stop_clicking_flag = False
        
        print(f"Starting auto clicker - Interval: {interval}s, Button: {mouse_button}, Type: {click_type}")
        print(f"Press {hotkey} to stop")
        
        # Setup hotkey listener
        self.setup_hotkey_listener()
        
        # Start clicking thread
        self.click_thread = threading.Thread(target=self._clicking_worker)
        self.click_thread.daemon = True
        self.click_thread.start()
        
    def setup_hotkey_listener(self):
        """Setup hotkey listener for toggling clicking"""
        def on_key_press(key):
            try:
                # Check for hotkey
                key_str = ''
                if hasattr(key, 'name'):
                    key_str = key.name.upper()
                else:
                    key_str = str(key).replace("'", "").upper()
                    
                if key_str == self.hotkey.upper():
                    if self.is_clicking:
                        self.stop_clicking()
                    else:
                        # If stopped, restart with current settings
                        self.start_clicking(self.click_interval, self.random_offset,
                                          self.random_offset_ms, self.mouse_button,
                                          self.click_type, self.repeat_times, self.hotkey)
            except Exception as e:
                print(f"Hotkey error: {e}")
                
        self.hotkey_listener = KeyboardListener(on_press=on_key_press)
        self.hotkey_listener.start()
        
    def _clicking_worker(self):
        """Worker thread for clicking"""
        if not pynput:
            return
            
        mouse_controller = mouse.Controller()
        self.is_clicking = True
        
        # Map button strings to pynput buttons
        button_map = {
            'left': Button.left,
            'right': Button.right,
            'middle': Button.middle
        }
        
        button = button_map.get(self.mouse_button.lower(), Button.left)
        
        try:
            click_count = 0
            
            while not self.stop_clicking_flag:
                # Check if we've reached the repeat limit
                if self.repeat_times > 0 and click_count >= self.repeat_times:
                    break
                    
                # Set click position if specified
                if self.click_position:
                    mouse_controller.position = self.click_position
                    
                # Perform click
                if self.click_type.lower() == 'double':
                    mouse_controller.click(button, 2)
                else:
                    mouse_controller.click(button, 1)
                    
                click_count += 1
                
                # Calculate delay
                delay = self.click_interval
                if self.random_offset and self.random_offset_ms > 0:
                    # Add random offset
                    offset = random.uniform(-self.random_offset_ms, self.random_offset_ms)
                    delay = max(0.001, delay + offset)
                    
                # Wait before next click
                if not self.stop_clicking_flag:
                    time.sleep(delay)
                    
        except Exception as e:
            print(f"Clicking error: {e}")
        finally:
            self.is_clicking = False
            if self.hotkey_listener:
                self.hotkey_listener.stop()
            print(f"Auto clicking stopped. Total clicks: {click_count}")
            
    def stop_clicking(self):
        """Stop auto clicking"""
        self.stop_clicking_flag = True
        self.is_clicking = False
        
        if self.hotkey_listener:
            self.hotkey_listener.stop()
            
    def set_click_position(self, x=None, y=None):
        """Set specific click position. None means use current cursor position"""
        if x is not None and y is not None:
            self.click_position = (x, y)
        else:
            self.click_position = None
            
    def get_current_position(self):
        """Get current mouse position"""
        if not pynput:
            return None
            
        try:
            mouse_controller = mouse.Controller()
            return mouse_controller.position
        except:
            return None
            
    def click_at_position(self, x, y, button='left', click_type='single', count=1):
        """Perform a single click or series of clicks at specific position"""
        if not pynput:
            print("Cannot click: pynput not available")
            return
            
        try:
            mouse_controller = mouse.Controller()
            
            # Map button string to pynput button
            button_map = {
                'left': Button.left,
                'right': Button.right,
                'middle': Button.middle
            }
            
            btn = button_map.get(button.lower(), Button.left)
            
            # Move to position
            mouse_controller.position = (x, y)
            time.sleep(0.01)  # Small delay to ensure position is set
            
            # Perform clicks
            for _ in range(count):
                if click_type.lower() == 'double':
                    mouse_controller.click(btn, 2)
                else:
                    mouse_controller.click(btn, 1)
                    
                if count > 1:
                    time.sleep(0.05)  # Small delay between multiple clicks
                    
        except Exception as e:
            print(f"Error clicking at position ({x}, {y}): {e}")
            
    def set_hotkey(self, hotkey):
        """Change the hotkey for toggling clicking"""
        self.hotkey = hotkey
        
        # Restart hotkey listener if running
        if self.hotkey_listener:
            self.hotkey_listener.stop()
            self.setup_hotkey_listener()
            
    def get_status(self):
        """Get current status information"""
        return {
            'is_clicking': self.is_clicking,
            'interval': self.click_interval,
            'button': self.mouse_button,
            'click_type': self.click_type,
            'repeat_times': self.repeat_times,
            'hotkey': self.hotkey,
            'position': self.click_position
        }
        
    def cleanup(self):
        """Cleanup resources"""
        self.stop_clicking()
        
        if self.hotkey_listener:
            self.hotkey_listener.stop()
            
        # Wait for thread to finish
        if self.click_thread and self.click_thread.is_alive():
            self.click_thread.join(timeout=1.0)

# Utility functions
def calculate_interval_from_cps(clicks_per_second):
    """Calculate interval from clicks per second"""
    if clicks_per_second <= 0:
        return 1.0
    return 1.0 / clicks_per_second

def calculate_cps_from_interval(interval):
    """Calculate clicks per second from interval"""
    if interval <= 0:
        return 0
    return 1.0 / interval

def format_interval(hours=0, minutes=0, seconds=0, milliseconds=0):
    """Format time components into total seconds"""
    total_seconds = hours * 3600 + minutes * 60 + seconds + milliseconds / 1000.0
    return max(0.001, total_seconds)  # Minimum 1ms