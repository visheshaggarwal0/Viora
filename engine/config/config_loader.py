import os
import json
from dotenv import load_dotenv

load_dotenv()

DEFAULT_CONFIG = {
    "router_provider": "ollama",
    "reasoning_provider": "groq",
    "extractor_provider": "groq",
    "router_model": "gemma3:1b",
    "reasoning_model": "llama3.1",
    "extractor_model": "llama-3.3-70b-versatile",
    "temperature": 0.0,
    "chroma_db_path": "data/chroma_db",
    "browser_profile_path": "data/browser_profile_selenium",
    "max_steps": 15
}

class Config:
    def __init__(self, config_path: str = "config/settings.json"):
        self.config_path = config_path
        self._config_data = {}
        self.load()

    def load(self):
        """Loads configuration from JSON and parses environment overrides."""
        # 1. Start with defaults
        self._config_data = DEFAULT_CONFIG.copy()

        # 2. Try loading from settings.json
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    file_data = json.load(f)
                    for key, val in file_data.items():
                        if key in self._config_data:
                            # Keep types consistent (float/int/str)
                            expected_type = type(self._config_data[key])
                            try:
                                self._config_data[key] = expected_type(val)
                            except (ValueError, TypeError):
                                self._config_data[key] = val
            except Exception as e:
                print(f"[Config Loader Warning] Failed to load {self.config_path}: {e}")

        # 3. Environment overrides (for backwards compatibility & flexibility)
        env_mappings = {
            "VIORA_ROUTER_PROVIDER": "router_provider",
            "VIORA_REASONING_PROVIDER": "reasoning_provider",
            "VIORA_EXTRACTOR_PROVIDER": "extractor_provider",
            "VIORA_ROUTER_MODEL": "router_model",
            "VIORA_REASONING_MODEL": "reasoning_model",
            "VIORA_EXTRACTOR_MODEL": "extractor_model",
            "VIORA_CHROMA_DB_PATH": "chroma_db_path",
            "VIORA_BROWSER_PROFILE_PATH": "browser_profile_path",
            "VIORA_MAX_STEPS": "max_steps",
            "VIORA_TEMPERATURE": "temperature"
        }

        # Legacy fallback logic support
        # In case VIORA_MODEL_PROVIDER is set in .env, map it to reasoning_provider
        legacy_provider = os.getenv("VIORA_MODEL_PROVIDER")
        if legacy_provider:
            self._config_data["reasoning_provider"] = legacy_provider.lower()

        for env_var, config_key in env_mappings.items():
            val = os.getenv(env_var)
            if val is not None:
                expected_type = type(self._config_data[config_key])
                try:
                    if expected_type == bool:
                        self._config_data[config_key] = val.lower() in ("true", "1", "yes")
                    elif expected_type == float:
                        self._config_data[config_key] = float(val)
                    elif expected_type == int:
                        self._config_data[config_key] = int(val)
                    else:
                        self._config_data[config_key] = val
                except (ValueError, TypeError):
                    self._config_data[config_key] = val

    def get(self, key: str, default=None):
        return self._config_data.get(key, default)

    @property
    def router_provider(self) -> str:
        return self.get("router_provider")

    @property
    def reasoning_provider(self) -> str:
        return self.get("reasoning_provider")

    @property
    def extractor_provider(self) -> str:
        return self.get("extractor_provider")

    @property
    def router_model(self) -> str:
        return self.get("router_model")

    @property
    def reasoning_model(self) -> str:
        return self.get("reasoning_model")

    @property
    def extractor_model(self) -> str:
        return self.get("extractor_model")

    @property
    def temperature(self) -> float:
        return self.get("temperature")

    @property
    def chroma_db_path(self) -> str:
        return self.get("chroma_db_path")

    @property
    def browser_profile_path(self) -> str:
        return self.get("browser_profile_path")

    @property
    def max_steps(self) -> int:
        return self.get("max_steps")

    def __repr__(self) -> str:
        return json.dumps(self._config_data, indent=2)

# Global configuration instance
config = Config()
