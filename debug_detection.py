#!/usr/bin/env python3
"""
Debug Cross-Platform Detection
"""

import sys
import os
import subprocess
import platform
import glob

def debug_python_detection():
    """Debug Python detection step by step"""
    print("=" * 50)
    print("Debug Python Detection")
    print("=" * 50)
    
    system = platform.system().lower()
    print(f"Platform: {system}")
    
    # Test basic commands
    python_commands = ['python.exe', 'python3.exe', 'python', 'python3']
    
    for cmd in python_commands:
        try:
            result = subprocess.run([cmd, '--version'], 
                                  capture_output=True, text=True, timeout=3)
            print(f"{cmd}: returncode={result.returncode}")
            if result.returncode == 0:
                version = result.stdout.strip() or result.stderr.strip()
                print(f"  Version: {version}")
            else:
                print(f"  Error: {result.stderr.strip()}")
        except FileNotFoundError:
            print(f"{cmd}: FileNotFoundError")
        except subprocess.TimeoutExpired:
            print(f"{cmd}: TimeoutExpired")
        except Exception as e:
            print(f"{cmd}: Exception - {e}")
    
    # Test current Python executable
    print(f"\nCurrent Python executable: {sys.executable}")
    try:
        result = subprocess.run([sys.executable, '--version'], 
                              capture_output=True, text=True, timeout=3)
        print(f"Current executable test: returncode={result.returncode}")
        if result.returncode == 0:
            version = result.stdout.strip() or result.stderr.strip()
            print(f"  Version: {version}")
    except Exception as e:
        print(f"Current executable test failed: {e}")

def debug_sqlmap_detection():
    """Debug SQLmap detection"""
    print("\n" + "=" * 50)
    print("Debug SQLmap Detection")
    print("=" * 50)
    
    # Test basic sqlmap commands
    sqlmap_commands = ['sqlmap', 'sqlmap.exe', 'python -m sqlmap']
    
    for cmd in sqlmap_commands:
        try:
            if ' ' in cmd:
                cmd_parts = cmd.split()
            else:
                cmd_parts = [cmd]
            
            result = subprocess.run(cmd_parts + ['--version'], 
                                  input='', capture_output=True, text=True, timeout=10)
            print(f"{cmd}: returncode={result.returncode}")
            if result.stdout:
                print(f"  Stdout: {result.stdout.strip()[:100]}...")
            if result.stderr:
                print(f"  Stderr: {result.stderr.strip()[:100]}...")
        except FileNotFoundError:
            print(f"{cmd}: FileNotFoundError")
        except subprocess.TimeoutExpired:
            print(f"{cmd}: TimeoutExpired")
        except Exception as e:
            print(f"{cmd}: Exception - {e}")

if __name__ == '__main__':
    debug_python_detection()
    debug_sqlmap_detection()