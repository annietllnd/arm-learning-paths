---
additional_search_terms:
- Kubernetes
- k8s
- deploy
- containers
- ci/cd


layout: installtoolsall
minutes_to_complete: 15
author: Jason Andrews
multi_install: false
multitool_install_part: false
official_docs: https://kubernetes.io/docs/reference/kubectl
test_images:
- ubuntu:latest
test_link: null
test_maintenance: true
title: Kubectl
tool_install: true
weight: 1
---

The Kubernetes command-line tool, [kubectl](https://kubernetes.io/docs/reference/kubectl/kubectl/), allows you to run commands against Kubernetes clusters.

`kubectl` is available for Windows, macOS, Linux and supports the Arm architecture.

## What should I consider before installing kubectl for Ubuntu on Arm?

[General installation information](https://kubernetes.io/docs/tasks/tools/) is available which covers all supported operating systems, but it doesn't talk about Arm.

This article provides a quick solution to install `kubectl` for Ubuntu on Arm.

Confirm you are using an Arm machine by running:
```bash
uname -m
```

The output should be:
```output
aarch64
```

If you see a different result, you are not using an Arm computer running 64-bit Linux.

## How do I download and Install kubectl for Ubuntu on Arm?

The easiest way to install `kubectl` for Ubuntu on Arm is to use curl and copy the executable to a common location.

To install curl, for example on ubuntu:

```bash { target="ubuntu:latest" }
sudo apt install -y curl
```

Download and install the latest version of `kubctl`. There is just 1 executable to copy to the desired location.

```bash { target="ubuntu:latest" }
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/arm64/kubectl"
```

If you have sudo or root access, install the executable in a common location for all users.

```bash { target="ubuntu:latest" }
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```
If you do not have sudo or root permission, add executable permission and add the location to the `$PATH` environment variable.

```console
chmod +x kubectl
export PATH=$PATH:$HOME
```

Confirm the executable is available and get the version of the client:

```bash { target="ubuntu:latest" }
kubectl version -o json --client
```

You are ready to use the Kubernetes command-line tool, `kubectl`