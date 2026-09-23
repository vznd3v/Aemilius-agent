from pathlib import Path


def _read_file(path: str) -> str:
    """
    Reads the content of a file and returns it as a string.

    Args:
        file_path (str): The path to the file to be read. 
    
    Returns:
        str: The content of the file.
    """
    return Path(path).read_text()
 # Example usage, replace with the actual file path you want to read.



read_file = {
    "type": "function",
        "function": {
            "name": "readfile",
            "description": "Read and return the complete content of a file at the given path.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path to the file to read."}
                },
                "required": ["path"],
            },
        },
        "call": _read_file,
}