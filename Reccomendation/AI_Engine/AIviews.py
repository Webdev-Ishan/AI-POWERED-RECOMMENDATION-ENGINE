from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import google.generativeai as genai
from decouple import config
import json



@csrf_exempt
@login_required
@require_POST
def AI_view(request):
    # Load the book-crossing dataset (Note: 'book-crossing' is not a built-in dataset)
    try:
        body = json.loads(request.body.decode("utf-8"))
        prompt = body.get("prompt")

        if not prompt:
            return JsonResponse({'error': 'Prompt is required'}, status=400)
        
        api_key = config("GEMINI_API_KEY")
        genai.configure(api_key=api_key)

        system_instruction = """
        You are a highly intelligent and context-aware Movie Recommendation Assistant.
        
        Your job is to recommend highly relevant movies based on the user’s prompt. 
        You understand user moods, genres, actors, directors, languages, and even abstract prompts like "movies that make you cry" or "like Interstellar but more philosophical."
        You analyze not only the text but also the intent behind the prompt.
        
        Your task:
        1. Understand the user's request deeply. Parse emotions, tone, genre preferences, language, and themes.
        2. Provide exactly 3 to 7 movie recommendations.
        3. For each movie, include:
           - Title
           - Release year
           - A short plot summary (2–3 sentences)
           - Why it matches the user’s request
        4. Be concise and provide explanations for your recommendations.
        """
        full_prompt = f"{system_instruction}\nUser prompt: {prompt}"
        model = genai.GenerativeModel("gemini-1.5-flash")  # or "gemini-1.5-flash", etc.

        response = model.generate_content(full_prompt)

        return JsonResponse({'recommendation': response.text}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

