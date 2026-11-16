"""Typed provider boundary. Only Wan HF currently generates clips."""
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

@dataclass(frozen=True)
class ShotRequest:
    scene_id: int
    image_path: Path
    prompt: str
    duration_seconds: float
    seed: int

@dataclass(frozen=True)
class ShotResult:
    scene_id: int
    provider: str
    model: str
    output: Path
    duration_seconds: float

class VideoProvider(Protocol):
    name: str
    def generate(self, request: ShotRequest) -> ShotResult: ...

def available_providers():
    return {
        "wan_hf": {"implemented": True, "requires": "ZeroGPU quota"},
        "comfyui_wan": {"implemented": False, "requires": "GPU and ComfyUI server"},
        "comfyui_ltx": {"implemented": False, "requires": "GPU and ComfyUI server"},
        "minimax_h3": {"implemented": False, "requires": "API credentials and approved billing"},
    }
