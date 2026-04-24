---
title: Prepare models for neural graphics with Arm neural technology
description: Learn how to export a PyTorch model through ExecuTorch, inspect TOSA IR, generate VGF artifacts, and validate outputs for neural graphics workflows.

minutes_to_complete: 45

who_is_this_for: This is an advanced topic for developers who want to understand and debug the model preparation flow used by Arm neural technology in neural graphics pipelines.

learning_objectives:
    - Build and export a simple PyTorch model for ExecuTorch
    - Inspect TOSA intermediate representation to validate operator lowering
    - Convert model artifacts to `.vgf` and compare export paths
    - Visualize model structure using Model Explorer

prerequisites:
    - Basic PyTorch and Python experience
    - A Linux machine or macOS machine with Apple Silicon
    - Python 3.10+ <3.14, and Git installed

author: Joshua Marshall-Law

### Tags
skilllevels: Advanced
subjects: ML
armips:
    - Mali
tools_software_languages:
    - ExecuTorch
    - PyTorch
    - Model Explorer
    - Jupyter Notebook
    - Vulkan
    - TOSA
    - NX
operatingsystems:
    - Linux
    - macOS

further_reading:
    - resource:
        title: Fine-tune neural graphics models using Model Gym
        link: /learning-paths/mobile-graphics-and-gaming/model-training-gym/
        type: learningpath
    - resource:
        title: Quantize neural upscaling models with ExecuTorch
        link: /learning-paths/mobile-graphics-and-gaming/quantize-neural-upscaling-models/
        type: learningpath
    - resource:
        title: Enable neural graphics using ML Extensions for Vulkan
        link: /learning-paths/mobile-graphics-and-gaming/vulkan-ml-sample/
        type: learningpath
    - resource:
        title: Enable Neural Super Sampling in Unreal Engine with ML Extensions
        link: /learning-paths/mobile-graphics-and-gaming/nss-unreal/
        type: learningpath
    - resource:
        title: Neural Graphics Development Kit
        link: https://developer.arm.com/mobile-graphics-and-gaming/neural-graphics
        type: website
    - resource:
        title: VGF library (GitHub)
        link: https://github.com/arm/ai-ml-sdk-vgf-library
        type: code

### FIXED, DO NOT MODIFY
# ================================================================================
weight: 1                       # _index.md always has weight of 1 to order correctly
layout: "learningpathall"       # All files under learning paths have this same wrapper
learning_path_main_page: "yes"  # This should be surfaced when looking for related content. Only set for _index.md of learning path content.
---
