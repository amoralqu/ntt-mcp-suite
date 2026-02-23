"""
NTT JADX MCP - Cross-Reference Analysis Tools

This module provides MCP tools for finding cross-references (xrefs) to classes,
methods, and fields in decompiled Android applications.

Adapted for: ntt-jadx-mcp
"""

from ntt_jadx_mcp.tools.client import get_from_jadx
from ntt_jadx_mcp.tools.pagination import PaginationUtils


async def get_xrefs_to_class(class_name: str, offset: int = 0, count: int = 20) -> dict:
    """
    Find all references to a class (including constructor calls).

    Args:
        class_name: Fully qualified class name
        offset: Starting index for pagination (default: 0)
        count: Number of references to return (default: 20)

    Returns:
        dict: Paginated list of locations where the class is referenced

    MCP Tool: get_xrefs_to_class
    Description: Finds code locations that instantiate or reference a class.
    """
    return await PaginationUtils.get_paginated_data(
        endpoint="xrefs-to-class",
        offset=offset,
        count=count,
        additional_params={"class_name": class_name},
        data_extractor=lambda parsed: parsed.get("references", []),
        fetch_function=get_from_jadx,
    )


async def get_xrefs_to_method(class_name: str, method_name: str, offset: int = 0, count: int = 20) -> dict:
    """
    Find all references to a method (includes overrides).

    Args:
        class_name: Fully qualified class name containing the method
        method_name: Method name (can include signature)
        offset: Starting index for pagination (default: 0)
        count: Number of references to return (default: 20)

    Returns:
        dict: Paginated list of locations where the method is called

    MCP Tool: get_xrefs_to_method
    Description: Tracks invocations of a specific method across the APK.
    """
    return await PaginationUtils.get_paginated_data(
        endpoint="xrefs-to-method",
        offset=offset,
        count=count,
        additional_params={"class_name": class_name, "method_name": method_name},
        data_extractor=lambda parsed: parsed.get("references", []),
        fetch_function=get_from_jadx,
    )


async def get_xrefs_to_field(class_name: str, field_name: str, offset: int = 0, count: int = 20) -> dict:
    """
    Find all references to a field.

    Args:
        class_name: Fully qualified class name containing the field
        field_name: Field/variable name
        offset: Starting index for pagination (default: 0)
        count: Number of references to return (default: 20)

    Returns:
        dict: Paginated list of locations where the field is accessed

    MCP Tool: get_xrefs_to_field
    Description: Identifies all read/write operations on a class field.
    """
    return await PaginationUtils.get_paginated_data(
        endpoint="xrefs-to-field",
        offset=offset,
        count=count,
        additional_params={"class_name": class_name, "field_name": field_name},
        data_extractor=lambda parsed: parsed.get("references", []),
        fetch_function=get_from_jadx,
    )
