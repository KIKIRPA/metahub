from distutils import extension
import os

import core

# translates file extensions to fontawesome icons (version 6.1.1)
file_types = {
    "pdf": "file-pdf",

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

    "csv": "file-csv",

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

    "zip": "file-zipper",
    "gz": "file-zipper",
    "bz2": "file-zipper",
    "rar": "file-zipper"
}


def construct_file_prop(root, file):
    # file type based on extension
    extension = os.path.splitext(file)[1].lower()
    if file_types.has_key(extension):
        file_type = file_types[extension]
    else:
        file_type = "file"
    
    return {
        "name": file,
        "path": os.path.join(root, file),
        "type": file_type,
    }



def read_path(path, base_path = None):
    """
    Read a directory path and return its contents as a dict
    """
    repo_path = core.settings.files_base_path
    full_path = os.path.join(repo_path, path)

    if base_path is None: 
        base_path = os.path.basename(full_path)

    for root, dirs, files in os.walk(path):
        tree = {
            "name": os.path.basename(root),
            "path": root,
            "type": "folder", 
            "children": []
        }
        tree["children"].extend([read_path(os.path.join(root, d), os.path.join(base_path, d)) for d in dirs])
        tree["children"].extend([construct_file_prop(root, f) for f in files])
        return tree