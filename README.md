# Color Tree 🌳

`color-tree` is a lightweight Python package and CLI tool that displays directory structures as visual tree diagrams with colored formatting, precise file/folder size indicators, and safe symlink handling.

## Features

- 🎨 **Colored Output**: Visually distinguishes folders, files, tree branches, and sizes using `colorama`.
- 📊 **Directory Sizes**: Calculates total size for directories recursively.
- ⚡ **Optimized Performance**: Built using `os.scandir` for fast directory traversal.
- 🔒 **Symlink Safe**: Handles symbolic links safely without falling into infinite recursion loops.

## Installation

```bash
pip install git+https://github.com/Abdullah-dev394/color-tree.git
