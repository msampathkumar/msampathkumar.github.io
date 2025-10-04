from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class ModelPricing:
    input_text: Optional[float] = None
    input_audio: Optional[float] = None
    input_video: Optional[float] = None
    input_image: Optional[float] = None
    output_text: Optional[float] = None
    output_audio: Optional[float] = None
    output_video: Optional[float] = None
    output_image: Optional[float] = None


@dataclass
class ModelContext:
    input_modalities: List[str]
    output_modalities: List[str]
    input_max_tokens: int
    output_max_tokens: int


@dataclass
class GeminiModel:
    name: str
    model_name: str
    api_name: str
    model_availability: str
    knowledge_cutoff: str
    context: ModelContext
    location: List[str]
    model_features: List[str]
    pricing: ModelPricing
    sdks: Dict[str, str]
    adk: Dict[str, str]
