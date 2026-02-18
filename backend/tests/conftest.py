"""Pytest configuration and shared fixtures"""
import sys
import os
import pytest

# Add backend root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
