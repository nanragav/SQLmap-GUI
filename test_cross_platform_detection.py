#!/usr/bin/env python3
"""
Cross-Platform Detection Test Script
Test the enhanced SQLmap and Python detection capabilities
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.sqlmap_wrapper import SqlmapWrapper

def test_cross_platform_detection():
    """Test the cross-platform detection capabilities"""
    print("=" * 60)
    print("Cross-Platform Detection Test")
    print("=" * 60)
    
    # Test with default configuration
    print("\n1. Testing with default sqlmap path...")
    wrapper = SqlmapWrapper()
    
    print(f"Python available: {wrapper.python_available}")
    if wrapper.python_available:
        print(f"Python command: {wrapper.python_cmd}")
    
    print(f"SQLmap available: {wrapper.sqlmap_available}")
    if wrapper.sqlmap_available:
        print(f"SQLmap path: {wrapper.sqlmap_path}")
    
    # Test with common installation paths
    print("\n2. Testing with common installation paths...")
    
    import platform
    system = platform.system().lower()
    
    test_paths = []
    if system == 'windows':
        test_paths = [
            'sqlmap',
            'sqlmap.exe', 
            'C:\\Python311\\Scripts\\sqlmap.exe',
            'C:\\tools\\sqlmap\\sqlmap.py'
        ]
    elif system == 'darwin':
        test_paths = [
            'sqlmap',
            '/usr/local/bin/sqlmap',
            '/opt/homebrew/bin/sqlmap',
            '~/sqlmap/sqlmap.py'
        ]
    else:  # Linux
        test_paths = [
            'sqlmap',
            '/usr/bin/sqlmap',
            '/usr/local/bin/sqlmap',
            '~/sqlmap/sqlmap.py'
        ]
    
    for path in test_paths:
        print(f"\nTesting path: {path}")
        test_wrapper = SqlmapWrapper(sqlmap_path=path)
        print(f"  Python: {'✓' if test_wrapper.python_available else '✗'}")
        print(f"  SQLmap: {'✓' if test_wrapper.sqlmap_available else '✗'}")
        if test_wrapper.sqlmap_available:
            print(f"  Final path: {test_wrapper.sqlmap_path}")
    
    print("\n" + "=" * 60)
    print("Detection Test Complete")
    print("=" * 60)

if __name__ == '__main__':
    test_cross_platform_detection()