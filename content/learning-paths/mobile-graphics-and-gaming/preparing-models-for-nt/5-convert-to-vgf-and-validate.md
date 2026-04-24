---
title: Convert to VGF and run validation
weight: 6

### FIXED, DO NOT MODIFY
layout: learningpathall
---

## Why VGF?

`.vgf` is the deployable format used by Arm neural technology with the ML extensions for Vulkan. In this section, you generate `.vgf` artifacts from TOSA and from the ExecuTorch VGF backend, then run a quick validation pass.

## Path A: Convert TOSA to VGF with `model_converter`

```python
import pathlib
import subprocess

tosa_path = pathlib.Path("./tosa-dump/output_tag0_TOSA-1.0+FP.tosa")
vgf_path = pathlib.Path("./executorch-model/model.vgf")

vgf_path.parent.mkdir(parents=True, exist_ok=True)

subprocess.run(
    [
        "model_converter",
        "--input",
        str(tosa_path),
        "--output",
        str(vgf_path),
    ],
    check=True,
)

print("Wrote:", vgf_path.resolve())
```

## Path B: Lower directly with the ExecuTorch VGF backend

```python
import os

from executorch.backends.arm.vgf import VgfCompileSpec, VgfPartitioner
from executorch.exir import (
    EdgeCompileConfig,
    ExecutorchBackendConfig,
    to_edge_transform_and_lower,
)
from executorch.extension.export_util.utils import save_pte_program

os.makedirs("executorch-model", exist_ok=True)

compile_spec = VgfCompileSpec()
compile_spec.dump_intermediate_artifacts_to("executorch-model")
partitioner = VgfPartitioner(compile_spec)

edge_pm = to_edge_transform_and_lower(
    exported_model,
    partitioner=[partitioner],
    compile_config=EdgeCompileConfig(_check_ir_validity=False),
)

et_pm = edge_pm.to_executorch(
    config=ExecutorchBackendConfig(extract_delegate_segments=False)
)

pte_path = os.path.abspath("as-vgf.pte")
save_pte_program(et_pm, pte_path)
print("Wrote:", pte_path)
```

After this step, re-open Model Explorer and compare `.tosa`, `.vgf`, and `.pte` artifacts.

## Optional: Build and run VKML runtime validation

From `repo/executorch` root, build the runner:

```bash
source ./examples/arm/arm-scratch/setup_path.sh
cd ./examples/arm

cmake \
  -DCMAKE_INSTALL_PREFIX=cmake-out \
  -DCMAKE_BUILD_TYPE=Debug \
  -DEXECUTORCH_BUILD_EXTENSION_DATA_LOADER=ON \
  -DEXECUTORCH_BUILD_EXTENSION_MODULE=ON \
  -DEXECUTORCH_BUILD_EXTENSION_NAMED_DATA_MAP=ON \
  -DEXECUTORCH_BUILD_EXTENSION_FLAT_TENSOR=ON \
  -DEXECUTORCH_BUILD_EXTENSION_TENSOR=ON \
  -DEXECUTORCH_BUILD_KERNELS_QUANTIZED=ON \
  -DEXECUTORCH_BUILD_XNNPACK=OFF \
  -DEXECUTORCH_BUILD_VULKAN=ON \
  -DEXECUTORCH_BUILD_VGF=ON \
  -DEXECUTORCH_ENABLE_LOGGING=ON \
  -DPYTHON_EXECUTABLE=python \
  -B../../cmake-out-vkml ../..

cmake --build ../../cmake-out-vkml --target executor_runner
```

Run the generated `.pte`:

```python
import os
import subprocess

cwd_dir = os.getcwd()
script_dir = os.path.join(cwd_dir, "repo", "executorch", "backends", "arm", "scripts")
et_dir = os.path.join(cwd_dir, "repo", "executorch")

args = f"--model={pte_path}"
subprocess.run(
    os.path.join(script_dir, "run_vkml.sh") + " " + args,
    shell=True,
    cwd=et_dir,
    check=True,
)
```

For an input tensor of ones, `x + y = 2`, so the expected output is close to `sigmoid(2) = 0.880797`.
