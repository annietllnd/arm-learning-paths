---
title: Build the executor_runner firmware
weight: 10

### FIXED, DO NOT MODIFY
layout: learningpathall
---
You build the Cortex-M33 `executor_runner` firmware on your host machine, then deploy it to the FRDM i.MX 93 board.

This is the core milestone of the Learning Path.
On i.MX 93, Linux runs on the application cores, but the real-time ML runtime that talks to Ethos-U65 runs as **firmware on Cortex-M33**.
When you can build and boot your own `executor_runner`, you’ve proven that the microcontroller side of the system is under your control and ready to host ML workloads.

The project links against prebuilt ExecuTorch static libraries. You built those libraries earlier as part of the container-based ExecuTorch setup, so this section focuses on pulling the runner project, wiring it up to your SDK and toolchain, and building it.

In architectural terms:

- The application core (Linux) loads the firmware image and manages its lifecycle
- The Cortex-M33 firmware owns model execution and the delegate path into Ethos-U65
- The `.pte` model remains a separate artifact that you update independently

## Set up MCUXpresso for VS Code

Install the [MCUXpresso extension for VS Code](https://marketplace.visualstudio.com/items?itemName=NXPSemiconductors.mcuxpresso).

In VS Code, open **Extensions**, search for “MCUXpresso”, and install the extension published by NXP.

## Install MCUXpresso SDK and Arm toolchain

Use the MCUXpresso Installer to install the SDK and toolchain components.

In VS Code, open the Command Palette and run **MCUXpresso for VS Code: Open MCUXpresso Installer**. Select the following items, then select **Install**:

- **MCUXpresso SDK Developer** (under Software Kits)
- **Arm GNU Toolchain (Latest)** (under Arm components)
- **Standalone Toolchain Add-ons (Latest)** (under Arm components)

![MCUXpresso Installer showing SDK and toolchain selection options#center](mcuxpresso-installer.png "MCUXpresso Installer")

## Clone the executor_runner repository

Clone the ready-to-build executor_runner project:

```bash
git clone https://github.com/fidel-makatia/Executorch_runner_cm33.git
cd Executorch_runner_cm33
```

The repository contains the complete runtime source code and build configuration for Cortex-M33.

## Copy ExecuTorch libraries

Copy the prebuilt ExecuTorch libraries (including the Ethos-U delegate library) out of the Docker container where you built ExecuTorch.

From the `Executorch_runner_cm33` directory, find your ExecuTorch build container:

```bash { output_lines = "2-3" }
docker ps -a
CONTAINER ID   IMAGE                 COMMAND       CREATED        STATUS        PORTS     NAMES
abc123def456   ubuntu-24-container   "/bin/bash"     *              *             *         *
```

Replace `abc123def456` with your actual container ID.

If your ExecuTorch checkout lives in `/root/executorch` inside the container (as in the earlier setup steps), copy the libraries into the runner project:

```bash
docker cp abc123def456:/root/executorch/arm_test/cmake-out/lib/. ./executorch/lib/
```

If you’re not sure where the libraries are in your container, list them first and then adjust the `docker cp` path:

```bash
docker exec -it abc123def456 bash -lc "find /root/executorch -type f -name 'libexecutorch*.a' -o -name 'libexecutorch_delegate_ethos_u.a'"
```

Verify the libraries were copied:

```bash { output_lines = "2-5" }
ls -lh executorch/lib/
-rw-r--r-- 1 user user 2.1M libexecutorch.a
-rw-r--r-- 1 user user 856K libexecutorch_core.a
-rw-r--r-- 1 user user 1.3M libexecutorch_delegate_ethos_u.a
```


## Configure the project for FRDM-MIMX93

Open the project in VS Code:

```bash
code .
```

If the MCUXpresso extension doesn’t automatically pick up the project, import it:

1. Open the Command Palette
2. Run **MCUXpresso for VS Code: Import Project**
3. Select the `Executorch_runner_cm33` folder
4. When prompted, choose **Arm GNU Toolchain**

![Import Project dialog showing project path, repository, and toolchain selection#center](import-project.png "Import Cloned Project folder")

## Set environment variables

Set three environment variables so the build can find your toolchain, your SDK, and the MCUXpresso Python environment.

Do this once for your user account, then restart VS Code so the changes take effect.

### Required variables

| Variable | Description | Example Value |
|----------|-------------|---------------|
| `ARMGCC_DIR` | Path to the Arm GCC toolchain root, i.e. a directory starting with `arm-gnu-toolchain-14.2.rel1*` | 
| `SdkRootDirPath` | Path to the folder that contains the `mcuxsdk/` subdirectory | 
| `MCUX_VENV_PATH` | Path to the MCUXpresso Python venv executables | 

These quick checks catch most path mistakes before you start debugging build errors:

```bash
test -x "$ARMGCC_DIR/bin/arm-none-eabi-gcc" && echo "OK: toolchain" || echo "FAIL: ARMGCC_DIR"
test -d "$SdkRootDirPath/mcuxsdk" && echo "OK: SDK" || echo "FAIL: SdkRootDirPath"
```

## Build the firmware

Build the project from VS Code. In the left sidebar, open **Explorer**, then in the MCUXpresso **Projects** view select the build icon next to `executorch_runner_cm33`.

![VS Code explorer showing project structure with build icon in the Projects tab#center](build-nxp.png "VS Code Projects panel with build icon")

The build output shows the progress:

```output
[build] Scanning dependencies of target executorch_runner_cm33.elf
[build] [ 25%] Building CXX object source/arm_executor_runner.cpp.obj
[build] [ 50%] Building CXX object source/arm_memory_allocator.cpp.obj
[build] [ 75%] Linking CXX executable executorch_runner_cm33.elf
[build] [100%] Built target executorch_runner_cm33.elf
[build] Build finished with exit code 0
```

Verify that the build succeeded:

```bash { output_lines = "2" }
ls -lh debug/executorch_runner_cm33.elf 
-rwxr-xr-x 1 user user 601K executorch_runner_cm33.elf
```

Check the memory usage to ensure it fits in the Cortex-M33:

```bash { output_lines = "2-3" }
$ARMGCC_DIR/bin/arm-none-eabi-size debug/executorch_runner_cm33.elf
   text	   data	    bss	    dec	    hex	filename
  52408	    724	  50472	 103604	  19494	executorch_runner_cm33.elf
```

The total RAM usage (data + bss) is approximately 51KB, well within the 108KB limit.

You now have everything you need to deploy the `.elf` binary on your NXP board.