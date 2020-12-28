import sys
from pathlib import Path
import shutil
# from distutils.dir_util import copy_tree


def exists(path: Path) -> Path:
    if not path.exists():
        raise FileNotFoundError(f"Error: {path} does not exist")
    return path


def erase(dir_to_remove: Path):
    """Remove directory"""
    try:
        if dir_to_remove.exists():
            shutil.rmtree(str(dir_to_remove))
            return f"Removed: {dir_to_remove}"
        return f"Doesn't exist: {dir_to_remove}"
    except OSError as e:
        print(
            f"""
        Removal failed: {dir_to_remove}
        Are you inside that directory, or using a file inside it?
        """
        )
        print(e)
        sys.exit(1)
