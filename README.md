# ComfyUI-ImageCompare Node

A simple custom node for [ComfyUI](https://github.com/comfyanonymous/ComfyUI) that allows you to compare two images (or batches of images) side-by-side within the UI.

This node is useful for visually inspecting differences or similarities between images generated at different steps of a workflow, or comparing outputs from different models or prompts.

## Acknowledgements

Much of the foundational code for handling image saving and previews was adapted from the excellent [rgthree-comfy](https://github.com/rgthree/rgthree-comfy) custom nodes by rgthree. Their work provided a great starting point for the UI display logic.

## Features

* Displays two input images (A and B) next to each other.
* Supports single images and batches.
* Integrates directly into the ComfyUI interface.

## Installation

1. Navigate to your ComfyUI `custom_nodes` directory:

    ```bash
    cd ComfyUI/custom_nodes/
    ```

2. Clone this repository:

    ```bash
    git clone https://github.com/rakki194/ComfyUI-ImageCompare.git
    ```

3. Restart ComfyUI.

Alternatively, you can download the `.py` files (and any `web` directory files if applicable) and place them inside a folder named `ComfyUI-ImageCompare` within your `custom_nodes` directory.

## Usage

1. Add the "Image Compare (🐺)" node to your workflow (you can find it under the "ComfyUI-ImageCompare" category or by searching).
2. Connect an image output to the `image_a` input.
3. Connect another image output to the `image_b` input.
4. Queue your prompt. When the workflow reaches the Image Compare node, the images will be displayed side-by-side in the node's interface.

*Note: This node saves temporary preview images similar to the built-in PreviewImage/SaveImage nodes to display them in the UI.*

## Contributing

Contributions are welcome! Please feel free to open an issue or submit a pull request.

## License

MIT License (See LICENSE.md)
Copyright (c) 2025 Balazs Horvath
