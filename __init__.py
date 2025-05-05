"""
Custom node for comparing two images.
"""

from .image_compare_node import KDS_ImageCompare

NODE_CLASS_MAPPINGS = {
    KDS_ImageCompare.NAME: KDS_ImageCompare,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    KDS_ImageCompare.NAME: "Image Compare (🐺)",
}

WEB_DIRECTORY = "./web"
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]

print("\033[34mKDS Nodes: \033[92mLoaded\033[0m")
