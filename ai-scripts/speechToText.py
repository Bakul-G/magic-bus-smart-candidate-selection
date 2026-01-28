import requests
import json
import numpy as np

def transcribe_speech(audio_file_path, service_region="centralindia", subscription_key=None, output_file="output.json"):
    """
    Transcribe audio file using Azure Speech to Text API and save the result to a JSON file.
    
    Args:
        audio_file_path (str): Path to the audio file to transcribe
        service_region (str): Azure service region (default: centralindia)
        subscription_key (str): Azure subscription key. If None, uses hardcoded key from environment
        output_file (str): Path to save the output JSON file (default: output.json)
    
    Returns:
        dict: Dictionary containing status_code and response from the API
    """
    
    # Use provided subscription key or default
    if subscription_key is None:
        subscription_key = ""
    
    # API endpoint
    url = f"https://{service_region}.api.cognitive.microsoft.com/speechtotext/transcriptions:transcribe?api-version=2025-10-15"
    
    # Headers
    headers = {
        "Ocp-Apim-Subscription-Key": subscription_key
    }
    
    # Definition as a dictionary
    definition = {
        "locales": [],
        "diarization": {
            "maxSpeakers": 4,
            "enabled": True
        }
    }
    
    # Prepare the multipart form data
    with open(audio_file_path, "rb") as audio_file:
        files = {
            "audio": audio_file,
            "definition": (None, json.dumps(definition))
        }
        
        # Make the POST request
        response = requests.post(url, headers=headers, files=files)
    
    # Store the response in a JSON file
    output = {
        "status_code": response.status_code,
        "response": response.json()
    }
    
    with open(output_file, "w") as json_file:
        json.dump(output, json_file, indent=2)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print(f"Output saved to {output_file}")
    
    return output


if __name__ == "__main__":
    # Example usage
    audio_path = "C:\\Users\\BGupta\\Desktop\\InterviewHackathon.wav"
    result = transcribe_speech(audio_path)
