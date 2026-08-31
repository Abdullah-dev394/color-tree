import os
from colorama import init, Fore, Style

init(autoreset=True)


class PathError(Exception):
    pass


def format_size(size_in_bytes: int) -> str:
    """Converts bytes into a human-readable format (KB, MB, GB, etc.)."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_in_bytes < 1024.0:
            return f"{size_in_bytes:.1f} {unit}"
        size_in_bytes /= 1024.0
    return f"{size_in_bytes:.1f} PB"


def get_dir_size(dir_path: str) -> int:
    """Calculates total size of a directory safely skipping symlinks."""
    total_size = 0
    try:
        with os.scandir(dir_path) as entries:
            for entry in entries:
                try:
                    if entry.is_file(follow_symlinks=False):
                        total_size += entry.stat(follow_symlinks=False).st_size
                    elif entry.is_dir(follow_symlinks=False):
                        total_size += get_dir_size(entry.path)
                except (PermissionError, OSError):
                    continue
    except (PermissionError, OSError):
        pass
    return total_size


def print_colored_prefix(prefix: str, branch_color: str) -> str:
    return prefix.replace("│", f"{branch_color}│{Style.RESET_ALL}")


def get_path_tree(path: str, colorful: bool = True, prefix: str = "") -> None:
    if not os.path.exists(path):
        raise PathError(f"The specified path does not exist: {path}")

    # Color configurations
    if colorful:
        base_folder_color = Fore.LIGHTYELLOW_EX
        folder_color = Fore.LIGHTCYAN_EX
        file_color = Fore.LIGHTGREEN_EX
        branch_color = Fore.LIGHTRED_EX
        size_color = Fore.LIGHTBLACK_EX
    else:
        base_folder_color = folder_color = file_color = branch_color = size_color = ""

    abs_path = os.path.abspath(path)

    # Print root folder (only on top-level call)
    if prefix == "":
        base_name = os.path.basename(abs_path) or abs_path
        total_root_size = format_size(get_dir_size(abs_path))
        print(f"{base_folder_color}{base_name}/{Style.RESET_ALL} {size_color}[{total_root_size}]{Style.RESET_ALL}")

    try:
        with os.scandir(abs_path) as entries:
            items = sorted(list(entries), key=lambda e: e.name)
    except (PermissionError, OSError):
        return

    count = len(items)
    for index, entry in enumerate(items):
        is_last = (index == count - 1)
        connector_char = "└── " if is_last else "├── "
        connector = f"{branch_color}{connector_char}{Style.RESET_ALL}"
        
        formatted_prefix = print_colored_prefix(prefix, branch_color)

        is_symlink = entry.is_symlink()
        is_directory = entry.is_dir(follow_symlinks=False) and not is_symlink

        if is_directory:
            dir_size = format_size(get_dir_size(entry.path))
            print(f"{formatted_prefix}{connector}{folder_color}{entry.name}/{Style.RESET_ALL} {size_color}[{dir_size}]{Style.RESET_ALL}")

            new_prefix = prefix + ("    " if is_last else "│   ")
            get_path_tree(entry.path, colorful=colorful, prefix=new_prefix)
        else:
            try:
                file_size = entry.stat(follow_symlinks=False).st_size
                formatted_size = f" ({format_size(file_size)})"
            except OSError:
                formatted_size = ""

            name_display = f"{entry.name} -> [Symlink]" if is_symlink else entry.name

            print(f"{formatted_prefix}{connector}{file_color}{name_display}{Style.RESET_ALL}{size_color}{formatted_size}{Style.RESET_ALL}")


if __name__ == "__main__":
    get_path_tree(".", colorful=True)