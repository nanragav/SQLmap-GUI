#!/usr/bin/env python3
"""
Direct Detection Test
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.sqlmap_wrapper import SqlmapWrapper

def test_detection_methods():
    """Test detection methods directly"""
    print("=" * 50)
    print("Direct Detection Method Test")
    print("=" * 50)
    
    wrapper = SqlmapWrapper()
    
    # Test Python detection directly
    print("1. Testing Python detection method...")
    try:
        wrapper._check_python_availability()
        print(f"Python available: {wrapper.python_available}")
        if wrapper.python_available:
            print(f"Python command: {wrapper.python_cmd}")
        else:
            print("No Python detected")
    except Exception as e:
        print(f"Python detection error: {e}")
        import traceback
        traceback.print_exc()
    
    # Test SQLmap detection directly
    print("\n2. Testing SQLmap detection method...")
    try:
        wrapper._check_sqlmap_availability()
        print(f"SQLmap available: {wrapper.sqlmap_available}")
        if wrapper.sqlmap_available:
            print(f"SQLmap path: {wrapper.sqlmap_path}")
        else:
            print("No SQLmap detected")
    except Exception as e:
        print(f"SQLmap detection error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_detection_methods()