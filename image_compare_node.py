import folder_paths
from PIL import Image, ImageOps, ImageSequence
from PIL.PngImagePlugin import PngInfo
import numpy as np
import json
import os
import random
import sys
import torch
import hashlib  # Added for potential future IS_CHANGED
import node_helpers  # Added for save_images dependencies if any missed

# Check if metadata saving is disabled
# We need a way to check this. Since args isn't directly available,
# we might default to True or try a placeholder check.
# For now, let's assume metadata is enabled unless specifically disabled elsewhere.
# A more robust solution might involve accessing comfy.options or similar.
# args = type('obj', (object,), {'disable_metadata': False})() # Removed mock object

# MAX_RESOLUTION moved here if needed by copied methods, otherwise remove
# from comfy import MAX_RESOLUTION # Avoid comfy import if possible
MAX_RESOLUTION = 8192  # Placeholder if needed


# Note: Removed inheritance from PreviewImage
class KDS_ImageCompare:
    def __init__(self):
        # Mimic PreviewImage initialization for save_images context
        self.output_dir = folder_paths.get_temp_directory()
        self.type = "temp"
        self.prefix_append = "_temp_" + "".join(
            random.choice("abcdefghijklmnopqrstupvxyz") for x in range(5)
        )
        self.compress_level = 1  # Preview uses lower compression

    NAME = "Image Compare (kds)"  # Directly define name
    CATEGORY = "kds"  # Directly define category
    FUNCTION = "compare_images"
    RETURN_TYPES = ()
    OUTPUT_NODE = True

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "image_a": ("IMAGE",),
                "image_b": ("IMAGE",),
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
        }

    # Copied and adapted from SaveImage/PreviewImage in nodes.py
    # Make sure all dependencies like 'folder_paths', 'Image', 'PngInfo', 'np', 'json', 'os', 'args' are available
    def save_images(
        self, images, filename_prefix="ComfyUI", prompt=None, extra_pnginfo=None
    ):
        filename_prefix += self.prefix_append
        full_output_folder, filename, counter, subfolder, filename_prefix = (
            folder_paths.get_save_image_path(
                filename_prefix, self.output_dir, images[0].shape[1], images[0].shape[0]
            )
        )
        results = list()
        for batch_number, image in enumerate(images):
            # Ensure image is on CPU before converting to numpy
            if image.device != torch.device("cpu"):
                image = image.cpu()

            i = 255.0 * image.numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            metadata = None
            # Assume metadata is enabled unless globally disabled (which we can't easily check here)
            # If it *is* disabled globally, this will save metadata anyway, which is acceptable.
            # Check if prompt or extra_pnginfo is provided before creating PngInfo object
            if prompt is not None or extra_pnginfo is not None:
                metadata = PngInfo()
                if prompt is not None:
                    metadata.add_text("prompt", json.dumps(prompt))
                if extra_pnginfo is not None:
                    for x in extra_pnginfo:
                        metadata.add_text(x, json.dumps(extra_pnginfo[x]))

            # Preserve batch number if filename contains placeholder, otherwise use counter
            if "%batch_num%" in filename:
                filename_with_batch_num = filename.replace(
                    "%batch_num%", str(batch_number)
                )
                file = f"{filename_with_batch_num}_{counter:05}_.png"
            else:
                file = f"{filename}_{counter:05}_.png"

            img.save(
                os.path.join(full_output_folder, file),
                pnginfo=metadata,
                compress_level=self.compress_level,
            )
            results.append(
                {"filename": file, "subfolder": subfolder, "type": self.type}
            )
            counter += 1

        return {"ui": {"images": results}}

    # The main function for this node
    def compare_images(
        self,
        image_a=None,
        image_b=None,
        # filename_prefix="kds.compare.", # Use default from save_images or keep custom?
        prompt=None,
        extra_pnginfo=None,
    ):
        print("[KDS ImageCompare Node] Entering compare_images")  # DEBUG
        # Use the node's filename prefix logic
        filename_prefix = "kds.compare."

        result = {"ui": {"a_images": [], "b_images": []}}
        try:
            if image_a is not None and len(image_a) > 0:
                print(
                    f"[KDS ImageCompare Node] Processing image_a (shape: {image_a.shape})"
                )  # DEBUG
                # Call the copied save_images method
                saved_a = self.save_images(
                    image_a, filename_prefix, prompt, extra_pnginfo
                )
                print(
                    f"[KDS ImageCompare Node] Result from save_images (A): {saved_a}"
                )  # DEBUG
                if saved_a and "ui" in saved_a and "images" in saved_a["ui"]:
                    result["ui"]["a_images"] = saved_a["ui"]["images"]
                else:
                    print(
                        "[KDS ImageCompare Node] WARNING: Unexpected format from save_images (A)"
                    )  # DEBUG

            if image_b is not None and len(image_b) > 0:
                print(
                    f"[KDS ImageCompare Node] Processing image_b (shape: {image_b.shape})"
                )  # DEBUG
                # Call the copied save_images method
                saved_b = self.save_images(
                    image_b, filename_prefix, prompt, extra_pnginfo
                )
                print(
                    f"[KDS ImageCompare Node] Result from save_images (B): {saved_b}"
                )  # DEBUG
                if saved_b and "ui" in saved_b and "images" in saved_b["ui"]:
                    result["ui"]["b_images"] = saved_b["ui"]["images"]
                else:
                    print(
                        "[KDS ImageCompare Node] WARNING: Unexpected format from save_images (B)"
                    )  # DEBUG
        except Exception as e:
            print(
                f"[KDS ImageCompare Node] ERROR during compare_images: {e}",
                file=sys.stderr,
            )  # DEBUG
            import traceback

            traceback.print_exc()
            # Optionally re-raise or return an error structure?
            # For now, just return the potentially empty result

        # Ensure the output format matches what the JS expects
        # The JS now expects { ui: { a_images: [...], b_images: [...] } }
        print(f"[KDS ImageCompare Node] Returning result: {result}")  # DEBUG
        return result

    # Optional: Add IS_CHANGED if needed, e.g., based on input images?
    # @classmethod
    # def IS_CHANGED(cls, image_a, image_b, **kwargs):
    #     # Simple change detection: if either input image changes, the node changes.
    #     # This might require hashing the image tensors or using a simpler proxy.
    #     # For now, returning a random value forces execution.
    #     return float("nan") # Always re-run
