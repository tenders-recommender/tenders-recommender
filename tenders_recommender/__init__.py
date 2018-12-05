from pathlib import Path

MAIN_MODULE_PATH: Path = Path(__file__).parent
REPOSITORY_PATH: Path = MAIN_MODULE_PATH.parent
RESOURCES_PATH: Path = (REPOSITORY_PATH / 'resources').resolve()
