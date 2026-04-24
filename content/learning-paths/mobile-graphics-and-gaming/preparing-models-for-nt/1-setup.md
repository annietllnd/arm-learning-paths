---
title: Set up your environment
weight: 2

### FIXED, DO NOT MODIFY
layout: learningpathall
---

## Overview

In this section, you set up the environment used across this Learning Path and prepare a notebook workflow for running each code cell in sequence.

{{% notice Note %}}
The workflow in this Learning Path mirrors notebook-first guidance used in [Model Gym](/learning-paths/mobile-graphics-and-gaming/model-training-gym/), so using Jupyter makes it easier to reproduce each stage.
{{% /notice %}}

## OS and tooling requirements

Use one of the following:
- Linux
- macOS with Apple Silicon

Install and verify Python 3.10+:

```bash
python3 --version
```

## Create a Python virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
```

## Install Jupyter

Install Jupyter Lab so you can run the tutorial in notebook form:

```bash
pip install jupyterlab
```

## Clone and install ExecuTorch

```bash
git clone https://github.com/pytorch/executorch.git repo/executorch
cd repo/executorch
./install_executorch.sh
```

## Install Arm backend dependencies

From the root of `repo/executorch`, run:

```bash
./examples/arm/setup.sh \
  --i-agree-to-the-contained-eula \
  --disable-ethos-u-deps \
  --enable-mlsdk-deps
```

Source the generated path script in the same shell session:

```bash
source ./examples/arm/arm-scratch/setup_path.sh
```

Verify key tools are available:

```bash
command -v model-converter || command -v model_converter
command -v model-explorer
```

## Launch Jupyter Lab

From the `preparing-models-for-nt` directory, launch Jupyter Lab:

```bash
jupyter lab
```

Open the notebook:

```output
prepare-models-for-nt.ipynb
```

You are now ready to create and export your first test model.
