---
title: Create a reference model
weight: 3

### FIXED, DO NOT MODIFY
layout: learningpathall
---

## Why start with a small model?

Before using a production NSS model, it helps to validate the toolchain with a small graph that is easy to inspect.

This page uses a minimal `AddSigmoid` model so you can focus on the conversion flow:
- PyTorch export
- TOSA extraction
- VGF conversion
- runtime validation

This is the same workflow pattern used in other NX learning paths, including [Quantize neural upscaling models with ExecuTorch](/learning-paths/mobile-graphics-and-gaming/quantize-neural-upscaling-models/).

## Create and export the model

Run the following in a notebook cell:

```python
import torch


class AddSigmoid(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.sigmoid = torch.nn.Sigmoid()

    def forward(self, x: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
        return self.sigmoid(x + y)


example_inputs = (torch.ones(1, 1, 1, 1), torch.ones(1, 1, 1, 1))

model = AddSigmoid().eval()
exported_model = torch.export.export(model, example_inputs)
graph_module = exported_model.module(check_guards=False)

_ = graph_module.print_readable()
```

The printed graph confirms the model was exported correctly and is ready for backend lowering.
