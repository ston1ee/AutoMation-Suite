#!/usr/bin/env python3
"""
AutoMation Suite - Comprehensive Automation Tool
Features: Macro Recording/Playback, Auto Clicker, Auto Hotkey Presser
"""

import tkinter as tk
from tkinter import ttk
import threading
import time
import json
from datetime import datetime

# Import our modules
from macro_recorder import MacroRecorder
from auto_clicker import AutoClicker
from hotkey_presser import HotkeyPresser

class AutoMationSuite:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AutoMation Suite v1.0")
        self.root.geometry("500x400")
        self.root.resizable(True, True)
        
        # Set app icon and style
        self.root.configure(bg='#f0f0f0')
        
        # Initialize modules
        self.macro_recorder = MacroRecorder()
        self.auto_clicker = AutoClicker()
        self.hotkey_presser = HotkeyPresser()
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the main user interface with tabs"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.macro_frame = ttk.Frame(self.notebook)
        self.clicker_frame = ttk.Frame(self.notebook)
        self.hotkey_frame = ttk.Frame(self.notebook)
        
        self.notebook.add(self.macro_frame, text="Macro Recorder")
        self.notebook.add(self.clicker_frame, text="Auto Clicker")
        self.notebook.add(self.hotkey_frame, text="Hotkey Presser")
        
        # Setup each tab
        self.setup_macro_tab()
        self.setup_clicker_tab()
        self.setup_hotkey_tab()
        
        # Add status bar
        self.status_bar = tk.Label(self.root, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def setup_macro_tab(self):
        """Setup macro recording tab"""
        # Title
        title = tk.Label(self.macro_frame, text="Macro Recorder & Player", font=('Arial', 14, 'bold'))
        title.pack(pady=10)
        
        # Record settings frame
        record_frame = tk.LabelFrame(self.macro_frame, text="Recording Settings", padx=10, pady=10)
        record_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(record_frame, text="Record Hotkey:").grid(row=0, column=0, sticky='w')
        self.macro_record_key = tk.Entry(record_frame, width=10)
        self.macro_record_key.insert(0, "F9")
        self.macro_record_key.grid(row=0, column=1, padx=5)
        
        tk.Label(record_frame, text="Playback Hotkey:").grid(row=1, column=0, sticky='w')
        self.macro_playback_key = tk.Entry(record_frame, width=10)
        self.macro_playback_key.insert(0, "F10")
        self.macro_playback_key.grid(row=1, column=1, padx=5)
        
        # Playback settings frame
        playback_frame = tk.LabelFrame(self.macro_frame, text="Playback Settings", padx=10, pady=10)
        playback_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(playback_frame, text="Playback Speed:").grid(row=0, column=0, sticky='w')
        self.macro_speed = tk.Scale(playback_frame, from_=0.1, to=5.0, resolution=0.1, orient='horizontal')
        self.macro_speed.set(1.0)
        self.macro_speed.grid(row=0, column=1, padx=5)
        
        tk.Label(playback_frame, text="Repeat Times:").grid(row=1, column=0, sticky='w')
        self.macro_repeat = tk.Entry(playback_frame, width=10)
        self.macro_repeat.insert(0, "1")
        self.macro_repeat.grid(row=1, column=1, padx=5)
        
        self.macro_unlimited = tk.BooleanVar()
        tk.Checkbutton(playback_frame, text="Unlimited (until stopped)", variable=self.macro_unlimited).grid(row=1, column=2, padx=5)
        
        # Control buttons
        button_frame = tk.Frame(self.macro_frame)
        button_frame.pack(pady=20)
        
        self.macro_record_btn = tk.Button(button_frame, text="Start Recording", command=self.toggle_macro_recording, bg='#4CAF50', fg='white')
        self.macro_record_btn.pack(side='left', padx=5)
        
        self.macro_play_btn = tk.Button(button_frame, text="Play Macro", command=self.play_macro, bg='#2196F3', fg='white')
        self.macro_play_btn.pack(side='left', padx=5)
        
        self.macro_stop_btn = tk.Button(button_frame, text="Stop", command=self.stop_macro, bg='#f44336', fg='white')
        self.macro_stop_btn.pack(side='left', padx=5)
        
        # Status
        self.macro_status = tk.Label(self.macro_frame, text="Status: Ready", fg='green')
        self.macro_status.pack(pady=5)
        
    def setup_clicker_tab(self):
        """Setup auto clicker tab"""
        # Title
        title = tk.Label(self.clicker_frame, text="Auto Clicker", font=('Arial', 14, 'bold'))
        title.pack(pady=10)
        
        # Click interval frame
        interval_frame = tk.LabelFrame(self.clicker_frame, text="Click Interval", padx=10, pady=10)
        interval_frame.pack(fill='x', padx=10, pady=5)
        
        # Time inputs
        time_frame = tk.Frame(interval_frame)
        time_frame.pack()
        
        tk.Label(time_frame, text="Hours:").grid(row=0, column=0)
        self.click_hours = tk.Spinbox(time_frame, from_=0, to=23, width=5, value=0)
        self.click_hours.grid(row=0, column=1, padx=2)
        
        tk.Label(time_frame, text="Minutes:").grid(row=0, column=2)
        self.click_mins = tk.Spinbox(time_frame, from_=0, to=59, width=5, value=0)
        self.click_mins.grid(row=0, column=3, padx=2)
        
        tk.Label(time_frame, text="Seconds:").grid(row=0, column=4)
        self.click_secs = tk.Spinbox(time_frame, from_=0, to=59, width=5, value=0)
        self.click_secs.grid(row=0, column=5, padx=2)
        
        tk.Label(time_frame, text="Milliseconds:").grid(row=0, column=6)
        self.click_ms = tk.Spinbox(time_frame, from_=1, to=999, width=5, value=100)
        self.click_ms.grid(row=0, column=7, padx=2)
        
        # Random offset
        self.random_offset = tk.BooleanVar()
        random_frame = tk.Frame(interval_frame)
        random_frame.pack(pady=5)
        tk.Checkbutton(random_frame, text="Random offset ±", variable=self.random_offset).pack(side='left')
        self.random_ms = tk.Entry(random_frame, width=8)
        self.random_ms.insert(0, "40")
        self.random_ms.pack(side='left', padx=2)
        tk.Label(random_frame, text="milliseconds").pack(side='left')
        
        # Click options frame
        options_frame = tk.LabelFrame(self.clicker_frame, text="Click Options", padx=10, pady=10)
        options_frame.pack(fill='x', padx=10, pady=5)
        
        # Mouse button
        tk.Label(options_frame, text="Mouse Button:").grid(row=0, column=0, sticky='w')
        self.mouse_button = ttk.Combobox(options_frame, values=["Left", "Right", "Middle"], width=10)
        self.mouse_button.set("Left")
        self.mouse_button.grid(row=0, column=1, padx=5)
        
        # Click type
        tk.Label(options_frame, text="Click Type:").grid(row=1, column=0, sticky='w')
        self.click_type = ttk.Combobox(options_frame, values=["Single", "Double"], width=10)
        self.click_type.set("Single")
        self.click_type.grid(row=1, column=1, padx=5)
        
        # Repeat options frame
        repeat_frame = tk.LabelFrame(self.clicker_frame, text="Click Repeat", padx=10, pady=10)
        repeat_frame.pack(fill='x', padx=10, pady=5)
        
        self.click_repeat_type = tk.StringVar(value="unlimited")
        tk.Radiobutton(repeat_frame, text="Repeat", variable=self.click_repeat_type, value="limited").grid(row=0, column=0, sticky='w')
        self.click_repeat_times = tk.Entry(repeat_frame, width=8)
        self.click_repeat_times.insert(0, "1")
        self.click_repeat_times.grid(row=0, column=1, padx=5)
        tk.Label(repeat_frame, text="times").grid(row=0, column=2)
        
        tk.Radiobutton(repeat_frame, text="Repeat until stopped", variable=self.click_repeat_type, value="unlimited").grid(row=1, column=0, columnspan=3, sticky='w')
        
        # Control buttons
        button_frame = tk.Frame(self.clicker_frame)
        button_frame.pack(pady=20)
        
        self.clicker_start_btn = tk.Button(button_frame, text="Start (F6)", command=self.toggle_auto_clicker, bg='#4CAF50', fg='white')
        self.clicker_start_btn.pack(side='left', padx=5)
        
        self.clicker_stop_btn = tk.Button(button_frame, text="Stop (F6)", command=self.stop_auto_clicker, bg='#f44336', fg='white')
        self.clicker_stop_btn.pack(side='left', padx=5)
        
        # Status
        self.clicker_status = tk.Label(self.clicker_frame, text="Status: Stopped", fg='red')
        self.clicker_status.pack(pady=5)
        
    def setup_hotkey_tab(self):
        """Setup hotkey presser tab"""
        # Title
        title = tk.Label(self.hotkey_frame, text="Auto Hotkey Presser", font=('Arial', 14, 'bold'))
        title.pack(pady=10)
        
        # Key settings frame
        key_frame = tk.LabelFrame(self.hotkey_frame, text="Key Settings", padx=10, pady=10)
        key_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(key_frame, text="Key to Press:").grid(row=0, column=0, sticky='w')
        self.hotkey_key = tk.Entry(key_frame, width=10)
        self.hotkey_key.insert(0, "f")
        self.hotkey_key.grid(row=0, column=1, padx=5)
        
        tk.Label(key_frame, text="Activation Hotkey:").grid(row=1, column=0, sticky='w')
        self.hotkey_activation = tk.Entry(key_frame, width=10)
        self.hotkey_activation.insert(0, "F8")
        self.hotkey_activation.grid(row=1, column=1, padx=5)
        
        # Mode settings frame
        mode_frame = tk.LabelFrame(self.hotkey_frame, text="Press Mode", padx=10, pady=10)
        mode_frame.pack(fill='x', padx=10, pady=5)
        
        self.hotkey_mode = tk.StringVar(value="continuous")
        tk.Radiobutton(mode_frame, text="Continuous Press (Press repeatedly)", variable=self.hotkey_mode, value="continuous").pack(anchor='w')
        tk.Radiobutton(mode_frame, text="Hold Down (Keep key pressed)", variable=self.hotkey_mode, value="hold").pack(anchor='w')
        
        # Speed settings for continuous mode
        speed_frame = tk.LabelFrame(self.hotkey_frame, text="Speed Settings (Continuous Mode)", padx=10, pady=10)
        speed_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(speed_frame, text="Press Interval (ms):").grid(row=0, column=0, sticky='w')
        self.hotkey_interval = tk.Scale(speed_frame, from_=1, to=1000, orient='horizontal')
        self.hotkey_interval.set(50)
        self.hotkey_interval.grid(row=0, column=1, padx=5)
        
        # Control buttons
        button_frame = tk.Frame(self.hotkey_frame)
        button_frame.pack(pady=20)
        
        self.hotkey_start_btn = tk.Button(button_frame, text="Start", command=self.toggle_hotkey_presser, bg='#4CAF50', fg='white')
        self.hotkey_start_btn.pack(side='left', padx=5)
        
        self.hotkey_stop_btn = tk.Button(button_frame, text="Stop", command=self.stop_hotkey_presser, bg='#f44336', fg='white')
        self.hotkey_stop_btn.pack(side='left', padx=5)
        
        # Status
        self.hotkey_status = tk.Label(self.hotkey_frame, text="Status: Stopped", fg='red')
        self.hotkey_status.pack(pady=5)
        
    # Macro functions
    def toggle_macro_recording(self):
        if self.macro_recorder.is_recording:
            self.macro_recorder.stop_recording()
            self.macro_record_btn.config(text="Start Recording")
            self.macro_status.config(text="Status: Recording stopped")
        else:
            record_key = self.macro_record_key.get()
            self.macro_recorder.start_recording(record_key)
            self.macro_record_btn.config(text="Stop Recording")
            self.macro_status.config(text="Status: Recording...")
            
    def play_macro(self):
        if self.macro_recorder.recorded_actions:
            speed = self.macro_speed.get()
            unlimited = self.macro_unlimited.get()
            times = 0 if unlimited else int(self.macro_repeat.get() or "1")
            playback_key = self.macro_playback_key.get()
            
            self.macro_recorder.play_macro(speed, times, playback_key)
            self.macro_status.config(text="Status: Playing macro...")
        else:
            self.macro_status.config(text="Status: No macro recorded")
            
    def stop_macro(self):
        self.macro_recorder.stop_playback()
        self.macro_status.config(text="Status: Stopped")
        
    # Auto clicker functions
    def toggle_auto_clicker(self):
        if not self.auto_clicker.is_clicking:
            # Get interval
            hours = int(self.click_hours.get())
            mins = int(self.click_mins.get())
            secs = int(self.click_secs.get())
            ms = int(self.click_ms.get())
            interval = hours * 3600 + mins * 60 + secs + ms / 1000.0
            
            # Get other settings
            random_offset = self.random_offset.get()
            random_ms_val = int(self.random_ms.get() or "0")
            mouse_btn = self.mouse_button.get().lower()
            click_type_val = self.click_type.get().lower()
            
            # Get repeat settings
            unlimited = self.click_repeat_type.get() == "unlimited"
            times = 0 if unlimited else int(self.click_repeat_times.get() or "1")
            
            self.auto_clicker.start_clicking(interval, random_offset, random_ms_val/1000.0, 
                                           mouse_btn, click_type_val, times)
            self.clicker_start_btn.config(text="Stop (F6)")
            self.clicker_status.config(text="Status: Clicking...", fg='green')
        else:
            self.stop_auto_clicker()
            
    def stop_auto_clicker(self):
        self.auto_clicker.stop_clicking()
        self.clicker_start_btn.config(text="Start (F6)")
        self.clicker_status.config(text="Status: Stopped", fg='red')
        
    # Hotkey presser functions
    def toggle_hotkey_presser(self):
        if not self.hotkey_presser.is_pressing:
            key = self.hotkey_key.get()
            mode = self.hotkey_mode.get()
            interval = self.hotkey_interval.get() / 1000.0
            activation_key = self.hotkey_activation.get()
            
            self.hotkey_presser.start_pressing(key, mode, interval, activation_key)
            self.hotkey_start_btn.config(text="Stop")
            self.hotkey_status.config(text="Status: Active", fg='green')
        else:
            self.stop_hotkey_presser()
            
    def stop_hotkey_presser(self):
        self.hotkey_presser.stop_pressing()
        self.hotkey_start_btn.config(text="Start")
        self.hotkey_status.config(text="Status: Stopped", fg='red')
        
    def run(self):
        """Start the application"""
        self.root.mainloop()
        
    def cleanup(self):
        """Cleanup when closing"""
        self.macro_recorder.cleanup()
        self.auto_clicker.cleanup()
        self.hotkey_presser.cleanup()

if __name__ == "__main__":
    app = AutoMationSuite()
    try:
        app.run()
    finally:
        app.cleanup()