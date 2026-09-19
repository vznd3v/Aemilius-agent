import subprocess


def listfiles(path: str) -> str | None:
    # 1. use the good param 'cwd' 
    result = subprocess.run('ls -pA', shell=True, capture_output=True, text=True, check=True, cwd=path)
    return result.stdout



