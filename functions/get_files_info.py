import os

def get_file_metadata(target_path: str, contents: list[str]) -> list[str]:
    content_metadata = []
    for content in contents:
        try:
            file_size = os.path.getsize(f"{target_path}/{content}")
        except Exception as e:
            file_size = "Error: failed to get file size"
        try:
            is_dir = "True" if os.path.isdir(f"{target_path}/{content}") else "False"
        except:
            is_dir = "Error: failed to check for directory"
        content_metadata.append(f"\t- {content}: file_size={file_size} bytes, is_dir={is_dir}")
    return content_metadata

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}
def get_files_info(working_directory: str, directory: str = "working_dir") -> str:
    try:
        if directory == "working_dir":
            directory = working_directory
        working_dir_abs = os.path.abspath(working_directory)
        combined_path = os.path.join(working_dir_abs, directory)
        target_dir = os.path.normpath(combined_path)
        if os.path.commonpath([working_dir_abs, target_dir]) != working_dir_abs:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if os.path.isdir(target_dir) == False:
            return f"Error \"{directory}\" is not a directory"
        else:
            contents = os.listdir(target_dir)
            content_metadata = get_file_metadata(target_dir, contents)
            content_metadata_joined = "\n".join(content_metadata)
            return f"Result for \'{directory}\' directory: \n" + content_metadata_joined

    except Exception as e:
        return e