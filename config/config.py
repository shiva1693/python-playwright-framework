import os
import json

def load_settings(filename="settings.json"):
    """Loads settings from a JSON file and swaps any 'env.' values with matching environment variables."""
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        data = json.load(f)

    # Replace any value that starts with "env." with its environment variable value
    for key, value in data.items():
        if isinstance(value, str) and value.startswith("env."):
            env_var = value[4:]
            data[key] = os.getenv(env_var, "")  # fallback to "" if not found
    return data

settings = load_settings()

BASE_URL = settings.get("base_url")
USERNAME = settings.get("username")
PASSWORD = settings.get("password")
YOLO11_URL = settings.get("yolo11_url")
MODEL_EXPORT_URL = settings.get("model_export_url")