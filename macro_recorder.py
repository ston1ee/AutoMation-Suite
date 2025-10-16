#!/usr/bin/env python3
"""
Macro Recorder Module
Records and plays back user input sequences
"""

import threading
import time
import json
from datetime import datetime
try:
    import pynput
    from pynput import mouse, keyboard
    from pynput.mouse import Button, Listener as MouseListener
    from pynput.keyboard import Key, Listener as KeyboardListener
except ImportError:
    print("Warning: pynput not installed. Please install with: pip install pynput")
    pynput = None

class MacroRecorder:
    def __init__(self):
        self.recorded_actions = []
        self.is_recording = False
        self.is_playing = False
        self.start_time = None
        self.record_hotkey = 'F9'
        self.playback_hotkey = 'F10'
        
        # Listeners
        self.mouse_listener = None
        self.keyboard_listener = None
        self.hotkey_listener = None
        
        # Threading
        self.record_thread = None
        self.playback_thread = None
        self.stop_playback_flag = False
        
    def start_recording(self, record_hotkey='F9'):
        """Start recording user actions"""
        if not pynput:
            print("Cannot start recording: pynput not available")
            return
            
        self.record_hotkey = record_hotkey
        self.recorded_actions = []
        self.is_recording = True
        self.start_time = time.time()
        
        print(f"Started recording. Press {record_hotkey} to stop.")
        
        # Start listeners
        self.mouse_listener = MouseListener(
            on_move=self.on_mouse_move,
            on_click=self.on_mouse_click,
            on_scroll=self.on_mouse_scroll
        )
        
        self.keyboard_listener = KeyboardListener(
            on_press=self.on_key_press,
            on_release=self.on_key_release
        )
        
        self.mouse_listener.start()
        self.keyboard_listener.start()
        
    def stop_recording(self):
        """Stop recording user actions"""
        self.is_recording = False
        
        if self.mouse_listener:
            self.mouse_listener.stop()
        if self.keyboard_listener:
            self.keyboard_listener.stop()
            
        print(f"Recording stopped. Recorded {len(self.recorded_actions)} actions.")
        
    def on_mouse_move(self, x, y):
        """Record mouse movement"""
        if self.is_recording:
            timestamp = time.time() - self.start_time
            self.recorded_actions.append({
                'type': 'mouse_move',
                'timestamp': timestamp,
                'x': x,
                'y': y
            })
            
    def on_mouse_click(self, x, y, button, pressed):
        """Record mouse clicks"""
        if self.is_recording:
            timestamp = time.time() - self.start_time
            self.recorded_actions.append({
                'type': 'mouse_click',
                'timestamp': timestamp,
                'x': x,
                'y': y,
                'button': str(button),
                'pressed': pressed
            })
            
    def on_mouse_scroll(self, x, y, dx, dy):
        """Record mouse scroll"""
        if self.is_recording:
            timestamp = time.time() - self.start_time
            self.recorded_actions.append({
                'type': 'mouse_scroll',
                'timestamp': timestamp,
                'x': x,
                'y': y,
                'dx': dx,
                'dy': dy
            })
            
    def on_key_press(self, key):
        """Record key press"""
        if self.is_recording:
            # Check for stop recording hotkey
            try:
                if hasattr(key, 'name') and key.name.upper() == self.record_hotkey.upper():
                    self.stop_recording()
                    return
                elif str(key).replace("'", "").upper() == self.record_hotkey.upper():
                    self.stop_recording()
                    return
            except:
                pass
                
            timestamp = time.time() - self.start_time
            key_str = str(key).replace("'", "")
            self.recorded_actions.append({
                'type': 'key_press',
                'timestamp': timestamp,
                'key': key_str
            })
            
    def on_key_release(self, key):
        """Record key release"""
        if self.is_recording:
            timestamp = time.time() - self.start_time
            key_str = str(key).replace("'", "")
            self.recorded_actions.append({
                'type': 'key_release',
                'timestamp': timestamp,
                'key': key_str
            })
            
    def play_macro(self, speed=1.0, repeat_times=1, playback_hotkey='F10'):
        """Play back recorded macro"""
        if not pynput:
            print("Cannot play macro: pynput not available")
            return
            
        if not self.recorded_actions:
            print("No macro recorded to play")
            return
            
        self.playback_hotkey = playback_hotkey
        self.stop_playback_flag = False
        
        # Start hotkey listener for stopping playback
        self.setup_playback_hotkey_listener()
        
        # Start playback in separate thread
        self.playback_thread = threading.Thread(
            target=self._playback_worker,
            args=(speed, repeat_times)
        )
        self.playback_thread.daemon = True
        self.playback_thread.start()
        
    def setup_playback_hotkey_listener(self):
        """Setup hotkey listener for stopping playback"""
        def on_hotkey_press(key):
            try:
                if hasattr(key, 'name') and key.name.upper() == self.playback_hotkey.upper():
                    self.stop_playback()
                elif str(key).replace("'", "").upper() == self.playback_hotkey.upper():
                    self.stop_playback()
            except:
                pass
                
        self.hotkey_listener = KeyboardListener(on_press=on_hotkey_press)
        self.hotkey_listener.start()
        
    def _playback_worker(self, speed, repeat_times):
        """Worker thread for macro playback"""
        if not pynput:
            return
            
        mouse_controller = mouse.Controller()
        keyboard_controller = keyboard.Controller()
        
        self.is_playing = True
        
        try:
            current_repeat = 0
            while (repeat_times == 0 or current_repeat < repeat_times) and not self.stop_playback_flag:
                last_timestamp = 0
                
                for action in self.recorded_actions:
                    if self.stop_playback_flag:
                        break
                        
                    # Calculate delay
                    delay = (action['timestamp'] - last_timestamp) / speed
                    if delay > 0:
                        time.sleep(delay)
                        
                    # Execute action
                    self._execute_action(action, mouse_controller, keyboard_controller)
                    last_timestamp = action['timestamp']
                    
                if repeat_times > 0:
                    current_repeat += 1
                    
        except Exception as e:
            print(f"Error during playback: {e}")
        finally:
            self.is_playing = False
            if self.hotkey_listener:
                self.hotkey_listener.stop()
                
    def _execute_action(self, action, mouse_controller, keyboard_controller):
        """Execute a single recorded action"""
        try:
            if action['type'] == 'mouse_move':
                mouse_controller.position = (action['x'], action['y'])
                
            elif action['type'] == 'mouse_click':
                button_map = {
                    'Button.left': Button.left,
                    'Button.right': Button.right,
                    'Button.middle': Button.middle
                }
                
                button = button_map.get(action['button'], Button.left)
                
                if action['pressed']:
                    mouse_controller.press(button)
                else:
                    mouse_controller.release(button)
                    
            elif action['type'] == 'mouse_scroll':
                mouse_controller.scroll(action['dx'], action['dy'])
                
            elif action['type'] == 'key_press':
                key = self._parse_key(action['key'])
                if key:
                    keyboard_controller.press(key)
                    
            elif action['type'] == 'key_release':
                key = self._parse_key(action['key'])
                if key:
                    keyboard_controller.release(key)
                    
        except Exception as e:
            print(f"Error executing action {action['type']}: {e}")
            
    def _parse_key(self, key_str):
        """Parse key string to pynput key object"""
        try:
            # Handle special keys
            if key_str.startswith('Key.'):
                key_name = key_str.replace('Key.', '')
                return getattr(Key, key_name, None)
            else:
                # Regular character key
                return key_str
        except:
            return None
            
    def stop_playback(self):
        """Stop macro playback"""
        self.stop_playback_flag = True
        self.is_playing = False
        
        if self.hotkey_listener:
            self.hotkey_listener.stop()
            
        print("Macro playback stopped")
        
    def save_macro(self, filename):
        """Save recorded macro to file"""
        try:
            with open(filename, 'w') as f:
                json.dump({
                    'recorded_actions': self.recorded_actions,
                    'created': datetime.now().isoformat()
                }, f, indent=2)
            print(f"Macro saved to {filename}")
        except Exception as e:
            print(f"Error saving macro: {e}")
            
    def load_macro(self, filename):
        """Load macro from file"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                self.recorded_actions = data.get('recorded_actions', [])
            print(f"Macro loaded from {filename}")
        except Exception as e:
            print(f"Error loading macro: {e}")
            
    def cleanup(self):
        """Cleanup resources"""
        self.stop_recording()
        self.stop_playback()
        
        if self.mouse_listener:
            self.mouse_listener.stop()
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        if self.hotkey_listener:
            self.hotkey_listener.stop()