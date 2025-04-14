import os
import shutil
from fastapi import UploadFile
import uuid

async def save_file(upload_file: UploadFile, destination: str) -> str:
    """
    Save an uploaded file to the specified destination
    
    Args:
        upload_file: The uploaded file
        destination: The destination path (can include subdirectories)
        
    Returns:
        The full path to the saved file
    """
    # Ensure base directory exists
    base_dir = os.path.join("data", os.path.dirname(destination))
    os.makedirs(base_dir, exist_ok=True)
    
    # Generate the full file path
    file_path = os.path.join("data", destination)
    
    # Save the file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    
    return file_path

def read_file(file_path: str) -> str:
    """
    Read a file and return its contents
    
    Args:
        file_path: The path to the file
        
    Returns:
        The file contents as a string
    """
    with open(file_path, "r") as f:
        return f.read()

def update_resume_tools(resume_path: str):
    """
    Update the resume tools to use the specified resume file
    
    Args:
        resume_path: The path to the resume file
    """
    from crewai_tools import FileReadTool, MDXSearchTool
    
    # Create new tools with the updated resume path
    read_resume = FileReadTool(file_path=resume_path)
    semantic_search_resume = MDXSearchTool(mdx=resume_path)
    
    return read_resume, semantic_search_resume