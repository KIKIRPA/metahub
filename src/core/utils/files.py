import os
from distutils import extension

import core



# translates file extensions to mdi icons
file_types = {
    "pdf": "file-pdf-box",

    "docx": "file-word",
    "doc": "file-word",
    "odt": "file-word",
    "rdf": "file-word",

    "xlsx": "file-excel",
    "xls": "file-excel",
    "ods": "file-excel",

    "pptx": "file-powerpoint",
    "ppt": "file-powerpoint",
    "odp": "file-powerpoint",

    "csv": "file-delimited",

    "txt": "file-lines",
    "text": "file-lines",
    "ascii": "file-lines",

    "jpg": "file-image",
    "jpeg": "file-image",
    "tiff": "file-image",
    "tif": "file-image",
    "png": "file-image",
    "bmp": "file-image",

    "mpg": "file-video",
    "mpeg": "file-video",
    "avi": "file-video",
    "mp4": "file-video",

    "zip": "folder-zip",
    "gz": "folder-zip",
    "bz2": "folder-zip",
    "rar": "folder-zip"
}


class DirectoryNotFoundError(Exception):
    """
    Exception raised when the requested directory was not found
    """
    pass


class DirectoryNotReadableError(Exception):
    """
    Exception raised when the requested directory cannot be read
    """
    pass


def construct_file_prop(base_path, file):
    # file type based on extension
    extension = os.path.splitext(file)[1].lower().lstrip(".")

    if extension in file_types:
        file_type = file_types[extension]
    else:
        file_type = "file"
    
    return {
        "name": file,
        "path": os.path.join(base_path, file),
        "type": file_type,
    }



def read_path(path, base_path = None):
    """
    Read a directory path and return its contents as a dict
    """
    repo_path = core.settings.files_base_path
    full_path = os.path.join(repo_path, path)

    if base_path is None: 
        base_path = "/"
        if not os.path.isdir(full_path):
            raise DirectoryNotFoundError
        if not os.access(full_path, os.R_OK):
            raise DirectoryNotReadableError

    for root, dirs, files in os.walk(full_path):
        if base_path == "/":
            tree = []
            tree.extend([read_path(os.path.join(root, d), os.path.join(base_path, d)) for d in dirs])
            tree.extend([construct_file_prop(base_path, f) for f in files])
            return tree
        else: 
            tree = {
                "name": os.path.basename(base_path),
                "path": base_path,
                "type": "folder", 
                "children": []
            }
            tree["children"].extend([read_path(os.path.join(root, d), os.path.join(base_path, d)) for d in dirs])
            tree["children"].extend([construct_file_prop(base_path, f) for f in files])
            return tree