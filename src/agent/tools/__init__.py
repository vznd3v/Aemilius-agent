from .listfiles import listfiles
from .quit import QuitRequested, quit
from .readfiles import read_file
from .where import where

__all__ = [
    "TOOLS",
    "QuitRequested",
    "execute_tool",
    "get_tools",
    "listfiles",
    "quit",
    "to_schemas",
]

TOOLS = [listfiles, quit, read_file, where]


def get_tools():
    return TOOLS


def to_schemas(tools=None):
    return [
        {key: value for key, value in tool.items() if key != "call"}
        for tool in (tools or TOOLS)
    ]


def execute_tool(tools, name, arguments):
    for tool in tools:
        if tool["function"]["name"] == name:
            return str(tool["call"](**arguments))
    raise KeyError(f"Unknown tool: {name}")