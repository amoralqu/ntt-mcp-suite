from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from ntt_jadx_mcp.tools.health import health_check
from ntt_jadx_mcp.tools import class_tools, search_tools, resource_tools, refactor_tools, debug_tools, xrefs_tools


def register_all(mcp: FastMCP) -> None:
    # Health
    mcp.tool()(health_check)

    # Class tools
    mcp.tool()(class_tools.fetch_current_class)
    mcp.tool()(class_tools.get_selected_text)
    mcp.tool()(class_tools.get_class_source)
    mcp.tool()(class_tools.get_all_classes)
    mcp.tool()(class_tools.get_methods_of_class)
    mcp.tool()(class_tools.get_fields_of_class)
    mcp.tool()(class_tools.get_smali_of_class)
    mcp.tool()(class_tools.get_main_application_classes_names)
    mcp.tool()(class_tools.get_main_application_classes_code)
    mcp.tool()(class_tools.get_main_activity_class)

    # Search tools
    mcp.tool()(search_tools.get_method_by_name)
    mcp.tool()(search_tools.search_method_by_name)
    mcp.tool()(search_tools.search_classes_by_keyword)

    # Resource tools
    mcp.tool()(resource_tools.get_android_manifest)
    mcp.tool()(resource_tools.get_strings)
    mcp.tool()(resource_tools.get_all_resource_file_names)
    mcp.tool()(resource_tools.get_resource_file)

    # Refactor tools
    mcp.tool()(refactor_tools.rename_class)
    mcp.tool()(refactor_tools.rename_method)
    mcp.tool()(refactor_tools.rename_field)
    mcp.tool()(refactor_tools.rename_package)
    mcp.tool()(refactor_tools.rename_variable)

    # Debug tools
    mcp.tool()(debug_tools.debug_get_stack_frames)
    mcp.tool()(debug_tools.debug_get_threads)
    mcp.tool()(debug_tools.debug_get_variables)

    # Xrefs tools
    mcp.tool()(xrefs_tools.get_xrefs_to_class)
    mcp.tool()(xrefs_tools.get_xrefs_to_method)
    mcp.tool()(xrefs_tools.get_xrefs_to_field)
