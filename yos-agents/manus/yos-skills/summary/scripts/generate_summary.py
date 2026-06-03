#!/usr/bin/env python
# -*- coding: utf-8 -*-

import google.generativeai as genai
import os
import sys
import json

def get_transcript_from_stdin():
    """Reads conversation transcript from stdin."""
    return sys.stdin.read()

def generate_summary(transcript):
    """Generates a structured summary using the Gemini API."""
    try:
        api_key = os.environ["GEMINI_API_KEY"]
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set.")
        genai.configure(api_key=api_key)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = f"""Tu es un architecte cognitif expert. Analyse la conversation suivante et extrais les informations clés dans un format JSON structuré. Sois extrâmement précis et synthétique.

    **TRANSCRIPT:**
    {transcript}

    **FORMAT JSON ATTENDU (en français):**
    {{
      "main_topic": "Le sujet principal unique de la conversation.",
      "key_points": [
        "Une liste de 3 à 5 points clés abordés."
      ],
      "initial_question": "La question ou le problème initial qui a lancé la conversation.",
      "thought_process": {{
        "starting_point": "L'état initial ou l'idée de départ.",
        "exploration": [
          "Une liste des pistes, idées ou solutions qui ont été explorées."
        ],
        "conclusion_reached": "Le point de convergence ou la conclusion finale de la discussion."
      }},
      "key_decisions": [
        "Une liste des décisions claires qui ont été prises."
      ],
      "action_items": [
        "Une liste des prochaines étapes ou actions, avec le responsable si mentionné."
      ],
      "final_conclusions": "Un résumé de l'état final de la réflexion et des conclusions."
    }}
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error calling Gemini API: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    """Main function to run the script."""
    transcript_content = get_transcript_from_stdin()
    if not transcript_content:
        print("Error: Transcript from stdin is empty.", file=sys.stderr)
        sys.exit(1)

    summary_json_str = generate_summary(transcript_content)

    # Clean the output to ensure it is valid JSON
    if '```json' in summary_json_str:
        summary_json_str = summary_json_str.split('```json')[1].split('```')[0].strip()
    
    try:
        # Validate JSON
        json.loads(summary_json_str)
        print(summary_json_str)
    except json.JSONDecodeError as e:
        print(f"Error: Failed to decode JSON from model output.\n{e}", file=sys.stderr)
        print(f"Raw output:\n{summary_json_str}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
