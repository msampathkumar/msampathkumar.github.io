from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class ModelPricing:
    input_text: Optional[str] = None
    input_audio: Optional[str] = None
    input_video: Optional[str] = None
    input_image: Optional[str] = None
    output_text: Optional[str] = None
    output_audio: Optional[str] = None
    output_video: Optional[str] = None
    output_image: Optional[str] = None


@dataclass
class ModelContext:
    input_modalities: List[str]
    output_modalities: List[str]
    input_max_tokens: int
    output_max_tokens: int


@dataclass
class SdkInfo:
    lang: str
    url: str
    version: str


@dataclass
class AdkInfo:
    lang: str
    url: str
    version: str


@dataclass
class GeminiModel:
    name: str
    model_name: str
    api_name: str
    model_availability_start_date: str
    model_availability_end_date: str
    knowledge_cutoff: str
    context: ModelContext
    location: List[str]
    model_features: List[str]
    pricing: ModelPricing
    sdks: List[SdkInfo]
    adk: List[AdkInfo]
