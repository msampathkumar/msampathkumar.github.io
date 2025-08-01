"""
Configuration file for the Gemini AI Chatbot.
"""

import os

# UI configuration
HEADER = "🤖 Gemini AI Chatbot"
DESCRIPTION = """
Welcome to the Gemini AI Chatbot! 

This interactive chatbot is powered by Google's latest **Gemini-2.5 Flash Lite** model. 

Feel free to ask anything! It can answer your questions, provide information, and even help you with creative tasks. 

Read more about the Gemini family of models [here](https://deepmind.google/technologies/gemini/).
"""
SIDEBAR_TITLE = "Chatbot Settings"
SIDEBAR_DESCRIPTION = """
Use the settings below to customize the chatbot's behavior.
"""

# LLM configuration
_UNIQUE_SUFFIX = "-COOKBOOK-WITH-CLOUD-GEMINI-DEMO-APP"
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
MODEL_NAME = "gemini-2.5-flash-lite"
LOCATION = "global"
SYSTEM_INSTRUCTION = [
    "You're a helpful Gemini AI Chatbot.",
    "Answer user's questions and use simple and clear language.",
    "When possible, reply to user's question with a single sentence or a few sentences.",
    "Free to use emojis.",
    "Be open and friendly. Don't be afraid to ask questions or clarify things.",
]

# Cache configuration
CACHE_NAME = "EXAMPLE-CACHE" + _UNIQUE_SUFFIX
CACHE_TTL_SECONDS = 30 * 60  # 30 minutes
CACHE_FILE = ".cache"
CACHE_OBJECTS_LIST = [
    "gs://cloud-samples-data/generative-ai/pdf/2312.11805v3.pdf",
    "gs://cloud-samples-data/generative-ai/pdf/2403.05530.pdf",
]

# RAG configuration
LOCATION_RAG = "us-central1"
RAG_DATASET_FOLDER = "rag_dataset"
RAG_CORPUS_NAME_FILE = ".rag"
RAG_CORPUS_DISPLAY_NAME = "Example-RAG-Corpus" + _UNIQUE_SUFFIX
