"""
This module defines the ChatSettings class, which manages configuration settings for a chat session.

This class allows for loading, saving, and customizing chat settings, including the model name, 
location, system instructions, and cache objects. Settings are persisted to a JSON file to 
maintain configuration across sessions.
"""

import json
import os
from dataclasses import dataclass, field, asdict
from typing import List

import settings

@dataclass
class ChatSettings:
    """
    Manages chat configuration settings, persisting them to a JSON file.

    Attributes:
        chat_session_name (str): The name of the chat session.
        model_name (str): The name of the language model.
        location (str): The location of the model.
        system_instruction (List[str]): A list of system instructions for the model.
        cache_objects_list (List[str]): A list of objects to be cached.
        config_file (str): The path to the configuration file.
    """
    chat_session_name: str = "default"
    model_name: str = settings.MODEL_NAME
    location: str = settings.LOCATION
    system_instruction: List[str] = field(default_factory=lambda: settings.SYSTEM_INSTRUCTION)
    cache_objects_list: List[str] = field(default_factory=lambda: settings.CACHE_OBJECTS_LIST)
    config_file: str = ".chat_settings.json"

    def __post_init__(self):
        """Loads settings from the config file after the object is created."""
        self.load()

    def to_dict(self):
        """
        Converts the ChatSettings object to a dictionary.

        Returns:
            dict: A dictionary representation of the ChatSettings object.
        """
        return asdict(self)

    def save(self):
        """Saves the current settings to the config file."""
        with open(self.config_file, 'w') as f:
            json.dump(self.to_dict(), f, indent=4)

    def load(self):
        """Loads settings from the config file if it exists."""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                config_data = json.load(f)
                for key, value in config_data.items():
                    if hasattr(self, key):
                        setattr(self, key, value)

    def load_session(self, session_name: str):
        """
        Loads a specific chat session's settings.

        Args:
            session_name (str): The name of the session to load.
        """
        self.chat_session_name = session_name
        self.config_file = f".chat_settings_{session_name}.json"
        self.load()
