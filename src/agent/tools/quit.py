class QuitRequested(Exception):
    pass


def _quit_impl():
    raise QuitRequested()


quit = {
    "type": "function",
    "function": {
        "name": "quit",
        "description": "Terminate the current agent session. Call this when the user asks to quit, exit, leave, close the session, or stop the agent.",
        "parameters": {"type": "object", "properties": {}},
    },
    "call": _quit_impl,
}