import cohere
import os
from dotenv import load_dotenv

load_dotenv()


API_KEY = os.getenv("COHERE_API_KEY")

if not API_KEY:

    try:
        from config import COHERE_API_KEY  
        API_KEY = COHERE_API_KEY
    except:
        raise ValueError("""
        ERROR: Cohere API key not configured.
        
        You MUST:
        1. Create a .env file with COHERE_API_KEY=your_key
        2. OR create config.py with COHERE_API_KEY='your_key'
        
        Get your key from: https://dashboard.cohere.com/api-keys
        """)

try:
    co = cohere.Client(API_KEY)
except Exception as e:
    raise RuntimeError(f"Failed to initialize Cohere: {str(e)}")

def get_medical_response(user_input):
    """Get AI medical response"""
    try:
        if not user_input.strip():
            return "Please describe your symptoms."
        
        response = co.generate(
            model='command',
            prompt=f"""As a medical AI, analyze these symptoms:
            {user_input}
            
            Provide:
            1. Possible conditions (2-3 most likely)
            2. Recommended actions (home/doctor/emergency)
            3. Clear disclaimer
            
            Use bullet points and be concise.""",
            max_tokens=1024,
            temperature=0.7
        )
        return response.generations[0].text
        
    except Exception as e:
        return f"Error: {str(e)}"