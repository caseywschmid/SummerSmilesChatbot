from pathlib import Path
import logging
from services.logger import configure_logging

log = configure_logging(__name__, log_level=logging.DEBUG)


def load_system_message() -> str:
    """
    Load the system message content from the markdown file.

    Returns:
        str: The system message content from summer_smiles_system_prompt.md

    Raises:
        FileNotFoundError: If the markdown file is not found
        IOError: If there's an error reading the file
    """
    log.debug("Loading system message from markdown file.")
    current_dir = Path(__file__).parent

    md_file_path = current_dir / "summer_smiles_system_prompt.md"

    try:
        with open(md_file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"System prompt file not found: {md_file_path}")
    except IOError as e:
        raise IOError(f"Error reading system prompt file: {e}")


SYSTEM_MESSAGE = load_system_message()
