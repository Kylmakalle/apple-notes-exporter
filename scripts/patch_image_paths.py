#!/usr/bin/env python3
import os
import argparse


def replace_file_paths(directory):
    valid_extensions = (
        ".md",
        ".html",
    )

    for root, dirs, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in valid_extensions):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                new_content = content.replace('src="file:///', 'src="./')
                new_content = new_content.replace("](file:///", "](")

                if new_content != content:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"Updated {file_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Replace file:/// with ./ in .md and .html files."
    )
    parser.add_argument(
        "directory", help="Directory to recursivelly scan for markdown and HTML files."
    )
    args = parser.parse_args()

    replace_file_paths(args.directory)


if __name__ == "__main__":
    main()
