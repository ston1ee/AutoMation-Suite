# AutoMation Suite 🤖

A comprehensive automation tool featuring macro recording/playback, auto clicking, and hotkey pressing functionality. Perfect for productivity tasks, gaming, and repetitive automation needs.

## ✨ Features

### 🎯 Macro Recorder & Player
- **Record** mouse movements, clicks, and keyboard inputs
- **Customizable hotkeys** for recording and playback
- **Variable playback speed** (0.1x to 5.0x)
- **Repeat options** - play once, multiple times, or unlimited
- **Save/load macros** for future use

### 🖱️ Auto Clicker
- **Precise timing control** - set intervals in hours, minutes, seconds, and milliseconds
- **Random offset** - add randomness to avoid detection
- **Multiple mouse buttons** - left, right, middle click support
- **Click types** - single or double clicks
- **Repeat modes** - limited or unlimited clicking
- **Hotkey toggle** - F6 to start/stop (customizable)

### ⌨️ Hotkey Presser
- **Continuous pressing** - repeatedly press keys at set intervals
- **Hold mode** - keep keys pressed down continuously
- **Gaming optimized** - perfect for games requiring held keys
- **Customizable keys** - support for all keyboard keys
- **Activation hotkey** - F8 to toggle (customizable)

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Step 1: Clone the Repository
```bash
git clone https://github.com/ston1ee/AutoMation-Suite.git
cd AutoMation-Suite
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
python main.py
```

## 🎮 Usage

### Macro Recorder
1. **Set hotkeys** for recording (default F9) and playback (default F10)
2. **Click "Start Recording"** or press F9
3. **Perform actions** you want to record
4. **Press F9 again** to stop recording
5. **Configure playback settings** (speed, repeat times)
6. **Click "Play Macro"** or press F10 to replay

### Auto Clicker
1. **Set click interval** using hours, minutes, seconds, milliseconds
2. **Choose mouse button** (Left, Right, Middle)
3. **Select click type** (Single, Double)
4. **Configure repeat options** (limited times or unlimited)
5. **Optional: Enable random offset** for more natural clicking
6. **Press F6** to start/stop clicking

### Hotkey Presser
1. **Enter the key** you want to press (e.g., 'f', 'space', 'ctrl')
2. **Choose mode**:
   - **Continuous**: Repeatedly press and release the key
   - **Hold**: Keep the key pressed down
3. **Set press interval** (for continuous mode)
4. **Press F8** to start/stop

## ⚙️ Configuration

### Supported Keys
The hotkey presser supports:
- **Letters**: a-z
- **Numbers**: 0-9
- **Function keys**: F1-F12
- **Special keys**: space, enter, tab, shift, ctrl, alt, arrows, etc.
- **Symbols**: Most keyboard symbols

### Default Hotkeys
- **Macro Record/Stop**: F9
- **Macro Playback**: F10
- **Auto Clicker Toggle**: F6
- **Hotkey Presser Toggle**: F8

*All hotkeys are customizable through the interface*

## 🛡️ Safety Features

- **Emergency stop** hotkeys for all functions
- **Minimum interval limits** to prevent system overload
- **Thread-safe implementation** for stable operation
- **Graceful cleanup** on application exit

## 📋 System Requirements

- **OS**: Windows, macOS, Linux
- **Python**: 3.7+
- **RAM**: 50MB minimum
- **Permissions**: May require accessibility permissions on macOS/Linux

## 🔧 Troubleshooting

### Common Issues

**"pynput not installed" error:**
```bash
pip install pynput
```

**Permission denied on macOS:**
1. Go to System Preferences → Security & Privacy → Privacy
2. Add Terminal/Python to "Accessibility" and "Input Monitoring"

**Linux accessibility issues:**
```bash
# Install additional dependencies if needed
sudo apt-get install python3-tk python3-dev
```

**Application not responding:**
- Use the designated hotkeys to stop current operations
- Close and restart the application

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is designed for legitimate automation and productivity purposes. Users are responsible for ensuring their use complies with:
- Software terms of service
- Local laws and regulations
- Ethical guidelines

The developers are not responsible for any misuse of this software.

## 🆘 Support

If you encounter issues or have questions:
1. Check the troubleshooting section above
2. Search existing [GitHub Issues](https://github.com/ston1ee/AutoMation-Suite/issues)
3. Create a new issue with detailed information

## 🔄 Version History

### v1.0.0 (Current)
- Initial release
- Macro recording and playback
- Auto clicker functionality
- Hotkey presser for gaming
- Cross-platform support
- Tabbed GUI interface

---

**Made with ❤️ for automation enthusiasts**