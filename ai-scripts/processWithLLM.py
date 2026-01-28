import os
import json
from openai import AzureOpenAI

def process_with_llm(transcription_json_path, speech_analysis_json_path=None, system_prompt_json_path=None, endpoint=None, deployment=None, subscription_key=None, api_version=None, output_file="llm_analysis.json"):
    """
    Process transcription data and speech analysis with Azure OpenAI LLM.
    
    Args:
        transcription_json_path (str): Path to the JSON file containing transcription data
        speech_analysis_json_path (str): Path to the JSON file containing speech analysis data. Optional
        system_prompt_json_path (str): Path to JSON file with system prompt. If None, uses default prompt
        endpoint (str): Azure OpenAI endpoint URL. If None, uses default
        deployment (str): Azure deployment name. If None, uses default
        subscription_key (str): Azure subscription key. If None, uses default
        api_version (str): Azure API version. If None, uses default
        output_file (str): Path to save the output JSON file (default: llm_analysis.json)
    
    Returns:
        dict: Dictionary containing llm_analysis, model, and api_version
    """
    
    # Load transcription data from JSON file
    with open(transcription_json_path, "r") as json_file:
        transcription_data = json.load(json_file)
    
    # Load speech analysis data from JSON file if provided
    speech_analysis_data = None
    if speech_analysis_json_path and os.path.exists(speech_analysis_json_path):
        with open(speech_analysis_json_path, "r") as json_file:
            speech_analysis_data = json.load(json_file)
    
    # Load system prompt from JSON file or use default
    if system_prompt_json_path and os.path.exists(system_prompt_json_path):
        with open(system_prompt_json_path, "r") as json_file:
            prompt_data = json.load(json_file)
            system_prompt = prompt_data.get("system_prompt", get_default_system_prompt())
    else:
        system_prompt = get_default_system_prompt()
    
    # Use provided parameters or defaults
    endpoint = endpoint or ""
    deployment = deployment or "gpt-4.1-mini"
    subscription_key = subscription_key or ""
    api_version = api_version or "2024-12-01-preview"
    
    # Initialize Azure OpenAI client
    client = AzureOpenAI(
        api_version=api_version,
        azure_endpoint=endpoint,
        api_key=subscription_key,
    )
    
    # Prepare the content with both transcription and speech analysis data
    combined_data = {
        "transcription": transcription_data
    }
    if speech_analysis_data:
        combined_data["speech_analysis"] = speech_analysis_data
    
    # Make API call to LLM
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": json.dumps(combined_data),
            }
        ],
        max_completion_tokens=13107,
        temperature=1.0,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        model=deployment
    )
    
    print("LLM Analysis Result:")
    print(response.choices[0].message.content)
    
    # Save the LLM response to a file
    llm_output = {
        "llm_analysis": response.choices[0].message.content,
        "model": deployment,
        "api_version": api_version
    }
    
    with open(output_file, "w") as json_file:
        json.dump(llm_output, json_file, indent=2)
    
    print(f"\nLLM analysis saved to {output_file}")
    
    return llm_output


def get_default_system_prompt():
    """Returns the default system prompt for candidate evaluation with training program likelihood."""
    return """You are an expert AI evaluator for a training program. 
    You are given a transcript of a discussion with a candidate along with their speech analysis metrics. 
    Your task: 
    1) Extract relevant information from the transcript. 
    2) Analyze the speech metrics to assess communication effectiveness and engagement level.
    3) Evaluate the likelihood of the person joining the training program based on ALL factors.
    4) Provide the output strictly in JSON format.
    5) Do not add explanations, markdown, or extra text.
    
    Speech Metrics Interpretation Guide:
    - speech_rate_wpm (words per minute): Higher values indicate faster speech. Range 80-150 is normal. >300 is very fast, <50 is very slow.
    - pause_ratio: Ratio of silence. Higher values indicate more pauses. Range 0.1-0.3 is normal. >0.5 indicates hesitation/uncertainty.
    - pitch_mean_hz: Average pitch in Hertz. Higher values indicate higher pitched voice.
    - pitch_variability: Standard deviation of pitch. Higher values indicate more vocal variety and engagement.
    - energy_variability: Variation in voice energy. Higher values indicate more dynamic speech.
    - spectral_flux: Measure of timbral variation. Higher values indicate more vocal variation.
    - confidence_score: Out of 5. Higher indicates more confident speech patterns.
    - cognitive_load_score: Out of 5. Higher indicates signs of stress or cognitive load.
    
    Output JSON format (return ONLY this JSON, no markdown or extra text):
    {
        "person_name": null,
        "age": null,
        "12th_pass": null,
        "employment_status": null,
        "location": null,
        "phone_number": null,
        "skills": [],
        "willing_to_join_training": null,
        "confidence_level": null,
        "engagement_level": null,
        "communication_quality": null,
        "stress_indicators": null,
        "training_program_likelihood": null,
        "likelihood_percentage": null,
        "key_factors": [],
        "concerns": [],
        "recommendations": null
    }
    
    Field Descriptions:
    - person_name: Candidate's name if mentioned
    - age: Age if mentioned
    - 12th_pass: Yes/No - Whether the candidate has passed 12th grade/secondary education
    - employment_status: Current employment status
    - location: Geographic location if mentioned
    - phone_number: Contact number if mentioned
    - skills: Array of mentioned skills or competencies
    - willing_to_join_training: Yes/No/Maybe based on explicit or implicit statements
    - confidence_level: 1-5 rating based on tone and speech patterns
    - engagement_level: 1-5 rating based on participation and energy
    - communication_quality: 1-5 rating assessing clarity and articulation
    - stress_indicators: None/Low/Medium/High based on pause_ratio, cognitive_load_score, pitch_variability
    - training_program_likelihood: Very Low/Low/Medium/High/Very High
    - likelihood_percentage: 0-100% numerical likelihood of joining
    - key_factors: Array of positive factors supporting training program participation
    - concerns: Array of potential concerns or red flags
    - recommendations: Suggestions for improving their chances or concerns to address
    
    Evaluation Criteria for Training Program Likelihood:
    - High confidence_score (3+) and low cognitive_load_score (<3) = positive indicators
    - Good engagement through pitch_variability (>50) and energy_variability (>0.02) = positive
    - Moderate speech_rate and pause_ratio = positive
    - Clear willingness mentioned in transcript = strong positive
    - Relevant skills and education = positive
    - Expressed motivations and goals = positive
    - High stress indicators or hesitation patterns = concerns
    - Vague or unclear responses = concerns
    
    Rules:
    1) If information is missing, set value to null
    2) Use only data from the transcript and speech metrics provided
    3) Be concise but thorough in analysis
    4) Return JSON only, no markdown formatting
    5) Likelihood percentage should reflect overall assessment integrating all factors"""


if __name__ == "__main__":
    # Example usage with only transcription
    result = process_with_llm(
        transcription_json_path="output.json"
    )
    
    # Example usage with both transcription and speech analysis
    # result = process_with_llm(
    #     transcription_json_path="output.json",
    #     speech_analysis_json_path="speech_analysis.json"
    # )

