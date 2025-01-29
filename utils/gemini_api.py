import aiohttp
import os
import mimetypes
from typing import Tuple
from PIL import Image
from google.generativeai import configure, GenerativeModel
from google.generativeai.types import GenerationConfig

# Configure Gemini
configure(api_key=os.getenv("GEMINI_API_KEY"))

async def ask_gemini(query: str) -> Tuple[str, bool]:
    """
    Get response from Gemini Pro text model
    Returns (response, success)
    """
    model = GenerativeModel('gemini-pro')
    try:
        response = await model.generate_content_async(
            query,
            generation_config=GenerationConfig(
                temperature=0.7,
                max_output_tokens=2000
            )
        )
        return response.text, True
    except Exception as e:
        return f"Error: {str(e)}", False

async def analyze_file(file_path: str) -> Tuple[str, bool]:
    """
    Analyze files using Gemini Pro Vision
    Returns (description, success)
    """
    try:
        # Determine file type
        mime_type, _ = mimetypes.guess_type(file_path)
        
        if mime_type.startswith('image/'):
            img = Image.open(file_path)
            model = GenerativeModel('gemini-pro-vision')
            response = await model.generate_content_async(
                ["Analyze this image and describe its content in detail. Include any text found.", img]
            )
            return response.text, True
            
        elif mime_type == 'application/pdf':
            # PDF handling (requires text extraction first)
            return "PDF analysis requires text extraction first", False
            
        else:
            return "Unsupported file format", False

    except Exception as e:
        return f"Analysis error: {str(e)}", False