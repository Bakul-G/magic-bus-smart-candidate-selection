import os
import json
from speechToText import transcribe_speech
from newllm import analyze_speech
from processWithLLM import process_with_llm

def main():
    # Define the audio file path
    audio_file_path = "C:\\Users\\BGupta\\Desktop\\Test_data_hindi.wav"
    
    # Define output directory
    output_dir = "C:\\Users\\BGupta\\Desktop\\outputs"
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Step 1: Transcribe the speech
    print("Step 1: Transcribing speech...")
    transcription_result = transcribe_speech(
        audio_file_path=audio_file_path,
        output_file=os.path.join(output_dir, "transcription_output.json")
    )
    print("Transcription completed.")

    # Step 2: Analyze speech features
    print("Step 2: Analyzing speech features...")
    speech_analysis_result = analyze_speech(audio_file_path)
    print("Speech analysis completed.")

    # Save speech analysis to JSON file in outputs directory
    speech_analysis_path = os.path.join(output_dir, "speech_analysis_output.json")
    with open(speech_analysis_path, "w") as json_file:
        json.dump(speech_analysis_result, json_file, indent=2)
    print(f"Speech analysis saved to {speech_analysis_path}")

    # Step 3: Process with LLM using both transcription and speech analysis
    print("Step 3: Processing with LLM...")
    llm_result = process_with_llm(
        transcription_json_path=os.path.join(output_dir, "transcription_output.json"),
        speech_analysis_json_path=speech_analysis_path,
        output_file=os.path.join(output_dir, "final_analysis_2.json")
    )
    print("LLM analysis completed.")

    # Print final results
    print("\n=== FINAL RESULTS ===")
    print("Transcription Status Code:", transcription_result["status_code"])
    print("Speech Analysis Summary:", speech_analysis_result)
    print("LLM Analysis:", llm_result["llm_analysis"])

    return {
        "transcription": transcription_result,
        "speech_analysis": speech_analysis_result,
        "llm_analysis": llm_result
    }

if __name__ == "__main__":
    results = main()
    print("\nIntegration completed successfully!")
