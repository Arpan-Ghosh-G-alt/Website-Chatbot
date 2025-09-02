# config.py
import os
from pathlib import Path
from typing import Optional

KEY_FILENAME = "openrouter_api.key"  # local fallback file (project root)
ENV_VAR = "OPENROUTER_API_KEY"

def load_api_key() -> Optional[str]:
    """
    Load OpenRouter API key.
    Priority:
      1) environment variable OPENROUTER_API_KEY
      2) local file openrouter_api.key (single line with the key)
      3) .env file with OPENROUTER_API_KEY=...
    Returns None if not found.
    """
    # 1) environment variable
    key = os.getenv(ENV_VAR)
    if key:
        return key.strip()

    root = Path(__file__).parent

    # 2) local key file
    key_file = root / KEY_FILENAME
    if key_file.exists():
        text = key_file.read_text(encoding="utf-8").strip()
        if text:
            return text

    # 3) simple .env parsing
    env_path = root / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith(f"{ENV_VAR}="):
                _, val = line.split("=", 1)
                return val.strip().strip('"').strip("'")

    return None
