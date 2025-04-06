import json
import os
from typing import Any, Dict, Optional, Union

class Config:
    """
    A class to handle configuration management from config.json.
    Provides methods to get parameters and check if required parameters exist.
    """
    _instance = None
    _config_data = None
    
    def __new__(cls):
        """Singleton pattern to ensure only one instance of Config exists."""
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance
    
    def _load_config(self):
        """Load configuration from config.json file."""
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        try:
            with open(config_path, 'r') as f:
                self._config_data = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found at {config_path}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON format in configuration file at {config_path}")
    
    def get_param(self, key: str, required: bool = False, default: Any = None) -> Any:
        """
        Get a parameter from the configuration.
        
        Args:
            key: The parameter key to retrieve
            required: If True, raises ValueError when the parameter is not found
            default: Default value to return if parameter is not found and not required
            
        Returns:
            The parameter value or default if not found and not required
            
        Raises:
            ValueError: If the parameter is required but not found
        """
        if key in self._config_data:
            return self._config_data[key]
        
        if required:
            raise ValueError(f"Required parameter '{key}' not found in configuration file")
        
        return default
    
    def get_all_params(self) -> Dict[str, Any]:
        """
        Get all parameters from the configuration.
        
        Returns:
            Dict: A copy of all configuration parameters
        """
        return self._config_data.copy() if self._config_data else {}


# Create a singleton instance for easy import
config = Config()


def get_param(key: str, required: bool = False, default: Any = None) -> Any:
    """
    Convenience function to get a parameter from the configuration.
    
    Args:
        key: The parameter key to retrieve
        required: If True, raises ValueError when the parameter is not found
        default: Default value to return if parameter is not found and not required
        
    Returns:
        The parameter value or default if not found and not required
        
    Raises:
        ValueError: If the parameter is required but not found
    """
    return config.get_param(key, required, default)


def get_all_params() -> Dict[str, Any]:
    """
    Convenience function to get all parameters from the configuration.
    
    Returns:
        Dict: A copy of all configuration parameters
    """
    return config.get_all_params()