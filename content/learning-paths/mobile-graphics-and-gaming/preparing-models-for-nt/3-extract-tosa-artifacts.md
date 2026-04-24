---
title: Extract TOSA artifacts
weight: 4

### FIXED, DO NOT MODIFY
layout: learningpathall
---

## Why extract TOSA?

TOSA is the stable intermediate representation (IR) between PyTorch export and backend-specific artifacts such as `.vgf`.

Extracting TOSA helps you:
- Check operator lowering before backend compilation
- Confirm tensor layout and shape flow
- Compare behavior when different backends produce different results

This is especially useful when you debug export issues before deployment to NX-enabled pipelines.

## Dump TOSA for the exported model

Run this cell after creating `exported_model` in the previous section:

```python
from pathlib import Path

from executorch.backends.arm.tosa import TosaSpecification
from executorch.backends.arm.tosa.compile_spec import TosaCompileSpec
from executorch.backends.arm.util._factory import create_partitioner
from executorch.exir import EdgeCompileConfig, to_edge_transform_and_lower

BASE_DUMP = Path("tosa-dump")


def dump_tosa(ep, profile_str: str, label: str):
    BASE_DUMP.mkdir(parents=True, exist_ok=True)

    tosa_spec = TosaSpecification.create_from_string(profile_str)
    compile_spec = TosaCompileSpec(tosa_spec)
    compile_spec.dump_intermediate_artifacts_to(str(BASE_DUMP))

    partitioner = create_partitioner(compile_spec)

    _ = to_edge_transform_and_lower(
        ep,
        partitioner=[partitioner],
        compile_config=EdgeCompileConfig(_check_ir_validity=False),
    )

    tosa_files = list(BASE_DUMP.rglob("*.tosa"))
    print(f"\\n{label}")
    print(f"  Profile: {profile_str}")
    print(f"  Dump dir: {BASE_DUMP.resolve()}")
    print(f"  Total .tosa files so far: {len(tosa_files)}")


# FP profile used in this tutorial
# For INT flows, see the quantization LP.
dump_tosa(exported_model, "TOSA-1.0+FP", "AddSigmoidModel (float)")
```

You should now have one or more `.tosa` files under `tosa-dump/` for inspection.

In the next section, you open these files in Model Explorer.
