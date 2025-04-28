import sys
import argparse
import pathlib
import subprocess
import re
import yaml
import os


def find_markdown_files(base_dir):
    return list(pathlib.Path(base_dir).rglob("*.md"))


def extract_code_blocks_with_metadata(md_path):
    blocks = []
    current_block = []
    inside = False
    metadata = {}

    code_block_pattern = re.compile(r"^```(?:([a-zA-Z0-9_+-]+))?(?:\s*\{([^}]*)\})?\s*$")

    with open(md_path) as f:
        for line in f:
            match = code_block_pattern.match(line.strip())

            if match:
                if not inside:
                    inside = True
                    current_block = []
                    lang = match.group(1)
                    raw_meta = match.group(2)
                    metadata = {"lang": lang} if lang else {}
                    if raw_meta:
                        for part in raw_meta.split(','):
                            k, _, v = part.partition('=')
                            metadata[k.strip()] = v.strip().strip('"')
                else:
                    blocks.append(("\n".join(current_block), metadata))
                    inside = False
                continue

            if inside:
                current_block.append(line.rstrip())

    return blocks


def run_code_block(code):
    try:
        result = subprocess.run(
            code,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            executable="/bin/bash",
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.output


def check_maintenance_flag(md_path):
    with open(md_path) as f:
        for line in f:
            if "maintenance: false" in line:
                return "off"
    return "on"

def extract_weight(md_path):
    with open(md_path) as f:
        for line in f:
            if line.strip().startswith("weight:"):
                try:
                    return int(line.split(":", 1)[1].strip())
                except ValueError:
                    break
    return float("inf")  # Files without weight go to the end

import yaml

def extract_front_matter_flags(md_path):
    with open(md_path) as f:
        lines = []
        in_front_matter = False
        for line in f:
            if line.strip() == "---":
                if in_front_matter:
                    break
                else:
                    in_front_matter = True
                    continue
            if in_front_matter:
                lines.append(line)

    front_matter = yaml.safe_load("".join(lines))
    test_images = front_matter.get("test_images", ["ubuntu-latest"])
    maintenance = "off" if not front_matter.get("test_maintenance", True) else "on"
    return test_images, maintenance

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", help="A single .md file or a directory containing .md files with weights")
    parser.add_argument("--debug", action="store_true", help="Show full output of all commands")
    parser.add_argument("--target", help="Only run tests matching this GitHub Actions target (e.g., ubuntu-latest)")

    args = parser.parse_args()

    failures = []
    maintenance_status = "on"
    created_files = []

    total_blocks = 0
    passed_blocks = 0
    failed_blocks = 0

    input_path = pathlib.Path(args.path)

    if input_path.is_file():
        md_files = [input_path]
        test_images, maintenance_status = extract_front_matter_flags(input_path)

    elif input_path.is_dir():
        index_path = input_path / "_index.md"
        test_images, maintenance_status = extract_front_matter_flags(index_path)

        md_files = list(input_path.glob("*.md"))
        md_files.sort(key=extract_weight)
    else:
        print(f"❌ Invalid path: {args.path}. Must be a .md file or directory.")
        sys.exit(1)

    for md_file in md_files:
        file_status = check_maintenance_flag(md_file)
        if file_status == "off":
            maintenance_status = "off"
            print(f"🚫 Skipping {md_file}: maintenance is off")
            continue

        print(f"🔍 Testing: {md_file}")
        blocks = extract_code_blocks_with_metadata(md_file)
        print(f"Extracted {len(blocks)} blocks from {md_file}")

        for i, (block, meta) in enumerate(blocks):
            total_blocks += 1

            lang = meta.get("lang", "bash")
            file_name = meta.get("file_name")

            if lang not in {"bash", "sh"} and not file_name:
                print(f"⏭️ Skipping non-executable block {i+1} (lang='{lang}')")
                continue
            print(f"--- Running block {i+1} ---")
            print(f"{block}")

            if args.target:
                current_target = args.target
            else:
                current_target = test_images[0]  # Default to the first image listed

            block_target = meta.get("target", current_target)

            if block_target != current_target:
                print(f"⏭️ Skipping block for target '{block_target}' (runner is '{current_target}')")
                continue

            pre_cmds = meta.get("pre_cmd")
            env_source = meta.get("env_source")
            file_name = meta.get("file_name")
            cwd = meta.get("cwd")

            if file_name:
                temp_file_name = pathlib.Path(file_name)
                try:
                    with open(temp_file_name, "w") as f:
                        f.write(block)
                    created_files.append(temp_file_name)
                    print(f"📄 Created file: {temp_file_name}")
                except Exception as e:
                    print(f"❌ Failed to write {temp_file_name}: {e}")
                    failures.append((md_file, i+1))
                    failed_blocks += 1
                    continue
                passed_blocks += 1  # writing file counts as success
                continue

            full_cmd = ""
            if env_source:
                full_cmd += f"source {env_source} && "
            if pre_cmds:
                full_cmd += f"{pre_cmds} && "
            if cwd:
                full_cmd += f"cd {cwd} && "
            full_cmd += block

            ok, output = run_code_block(full_cmd)

            if ok:
                passed_blocks += 1
                if args.debug:
                    print(output)
            else:
                failed_blocks += 1
                print(output)
                print(f"❌ Test failed in {md_file}, block {i+1}")
                failures.append((md_file, i+1))

    print("\n📊 Test Summary:")
    print(f"✅ Passed: {passed_blocks}")
    print(f"❌ Failed: {failed_blocks}")
    print(f"🧪 Total:  {total_blocks}")

    for file in created_files:
        try:
            os.remove(file)
            print(f"🧹 Removed file: {file}")
        except Exception as e:
            print(f"Could not remove {file}: {e}")

    if maintenance_status == "off":
        print("::set-output name=maintenance::off")
    else:
        print("::set-output name=maintenance::on")

    if failures:
        print("::error::Tests failed in test suite")
        sys.exit(1)
    else:
        print("✅ All tests passed")


if __name__ == "__main__":
    main()