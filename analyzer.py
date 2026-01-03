"""
Tiny adapter so existing `app.py` can `from analyzer import ...` while
keeping the main implementation in `core_analyzer.py`.

This avoids renaming files and keeps the original implementation intact.
"""
from core_analyzer import get_app_details, analyze_permissions, get_ai_context_analysis

__all__ = ["get_app_details", "analyze_permissions", "get_ai_context_analysis"]
