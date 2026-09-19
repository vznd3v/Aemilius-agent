import subprocess


def _listfiles(path: str) -> str | None:
    result = subprocess.run('ls -pA', shell=True, capture_output=True, text=True, check=True, cwd=path)
    return result.stdout


listfiles = {
    "type": "function",
    "function": {
        "name": "listfiles",
        "description": "List files and directories in a given path (ls -pA).",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Directory path to list."}
            },
            "required": ["path"],
        },
    },
    "call": _listfiles,
}