#!/usr/bin/env python3
"""
AutoMation Suite Launcher
Simple launcher with dependency checking and error handling
"""

import sys
import subprocess
import os

def check_python_version():
    """Check if Python version is adequate"""
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher is required.")
        print(f"Current version: {sys.version}")
        return False
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import tkinter
        print("✓ tkinter found")
    except ImportError:
        print("✗ tkinter not found - please install Python with tkinter support")
        return False
    
    try:
        import pynput
        print("✓ pynput found")
    except ImportError:
        print("✗ pynput not found")
        print("Installing pynput...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pynput"])
            print("✓ pynput installed successfully")
            import pynput
        except subprocess.CalledProcessError:
            print("✗ Failed to install pynput")
            print("Please run: pip install pynput")
            return False
        except ImportError:
            print("✗ pynput installation failed")
            return False
    
    return True

def run_application():
    """Run the main application"""
    try:
        from main import AutoMationSuite
        
        print("\n🤖 Starting AutoMation Suite...")
        print("Press Ctrl+C in terminal to force quit if needed\n")
        
        app = AutoMationSuite()
        try:
            app.run()
        finally:
            app.cleanup()
            
    except KeyboardInterrupt:
        print("\n🛑 Application interrupted by user")
    except ImportError as e:
        print(f"\n✗ Import error: {e}")
        print("Make sure all files are in the same directory")
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        print("Please check the GitHub issues page for help")

def main():
    """Main launcher function"""
    print("=" * 50)
    print("🤖 AutoMation Suite Launcher")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        input("Press Enter to exit...")
        return
    
    print(f"✓ Python {sys.version.split()[0]} detected")
    
    # Check dependencies
    print("\nChecking dependencies...")
    if not check_dependencies():
        print("\n✗ Dependency check failed")
        print("Please install missing dependencies and try again")
        input("Press Enter to exit...")
        return
    
    print("✓ All dependencies found")
    
    # Check if main files exist
    required_files = ['main.py', 'macro_recorder.py', 'auto_clicker.py', 'hotkey_presser.py']
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"\n✗ Missing required files: {', '.join(missing_files)}")
        print("Please make sure all files are downloaded from the repository")
        input("Press Enter to exit...")
        return
    
    print("✓ All required files found")
    
    # Run the application
    run_application()
    
    print("\n👋 Thanks for using AutoMation Suite!")

if __name__ == "__main__":
    main()