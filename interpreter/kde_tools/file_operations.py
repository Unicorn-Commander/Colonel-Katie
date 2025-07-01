

import os
import shutil

def write_file_content(path, content):
    """
    Writes content to a file. Creates the file if it doesn't exist.

    Args:
        path (str): The absolute path to the file.
        content (str): The content to write to the file.
    """
    try:
        with open(path, 'w') as f:
            f.write(content)
    except Exception as e:
        raise Exception(f"Failed to write file {path}: {e}")

def read_file_content(path):
    """
    Reads content from a file.

    Args:
        path (str): The absolute path to the file.

    Returns:
        str: The content of the file.
    """
    try:
        with open(path, 'r') as f:
            return f.read()
    except Exception as e:
        raise Exception(f"Failed to read file {path}: {e}")

def append_file_content(path, content):
    """
    Appends content to a file. Creates the file if it doesn't exist.

    Args:
        path (str): The absolute path to the file.
        content (str): The content to append to the file.
    """
    try:
        with open(path, 'a') as f:
            f.write(content)
    except Exception as e:
        raise Exception(f"Failed to append to file {path}: {e}")

def create_directory(path):
    """
    Creates a new directory.

    Args:
        path (str): The absolute path to the directory to create.
    """
    try:
        os.makedirs(path, exist_ok=True)
    except Exception as e:
        raise Exception(f"Failed to create directory {path}: {e}")

def delete_file(path):
    """
    Deletes a file.

    Args:
        path (str): The absolute path to the file to delete.
    """
    try:
        os.remove(path)
    except Exception as e:
        raise Exception(f"Failed to delete file {path}: {e}")

def delete_directory(path):
    """
    Deletes a directory and all its contents.

    Args:
        path (str): The absolute path to the directory to delete.
    """
    try:
        shutil.rmtree(path)
    except Exception as e:
        raise Exception(f"Failed to delete directory {path}: {e}")

def list_directory_contents(path):
    """
    Lists the contents of a directory.

    Args:
        path (str): The absolute path to the directory.

    Returns:
        list: A list of file and directory names within the specified path.
    """
    try:
        return os.listdir(path)
    except Exception as e:
        raise Exception(f"Failed to list directory contents for {path}: {e}")

def move_item(source_path, destination_path):
    """
    Moves a file or directory from source to destination.

    Args:
        source_path (str): The absolute path of the item to move.
        destination_path (str): The absolute path to the destination.
    """
    try:
        shutil.move(source_path, destination_path)
    except Exception as e:
        raise Exception(f"Failed to move item from {source_path} to {destination_path}: {e}")

def copy_item(source_path, destination_path):
    """
    Copies a file or directory from source to destination.

    Args:
        source_path (str): The absolute path of the item to copy.
        destination_path (str): The absolute path to the destination.
    """
    try:
        if os.path.isfile(source_path):
            shutil.copy2(source_path, destination_path)
        elif os.path.isdir(source_path):
            shutil.copytree(source_path, destination_path)
        else:
            raise Exception(f"Source path {source_path} is neither a file nor a directory.")
    except Exception as e:
        raise Exception(f"Failed to copy item from {source_path} to {destination_path}: {e}")

