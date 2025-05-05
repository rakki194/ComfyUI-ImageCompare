"""
Custom node for comparing two images.
"""

from .image_compare_node import ComfyUIImageCompare

NODE_CLASS_MAPPINGS = {
    ComfyUIImageCompare.NAME: ComfyUIImageCompare,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    ComfyUIImageCompare.NAME: ComfyUIImageCompare.NAME,
}

WEB_DIRECTORY = "./web"
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]

print("\033[34mComfyUI-ImageCompare Nodes: \033[92mLoaded\033[0m")
