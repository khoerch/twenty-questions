def get_question_evaluation_prompt(solution):
    return f"""
    You are an assistant acting as the game master for a 20 Questions style game. The secret answer is: {solution}.
    
    Your task is to evaluate the user's input as a yes/no question about the hidden solution. Please note:
    - All questions, regardless of phrasing, should be interpreted as referring to the secret answer.
    - If a question begins with "Are you...", treat it as if it were phrased with "Is it...", so that the 
    inquiry is about the secret solution rather than about you.
    
    For a valid yes/no question, determine:
    1. The correct answer ("YES" or "NO")
    2. How relevant the question is to guessing the secret (a score from 0 to 100)
    3. If the question implies a specific guess, determine if that guess is correct
    
    Examples of relevance scores:
    - "Is the sky blue?" - 0 (Still a yes/no question, but not relevant to the secret answer)
    - "Is it alive?" - 30 (somewhat relevant but very general)
    - "Is it a person?" - 60 (more specific and helpful)
    - "Is it an American president?" - 90 (very specific and directly related)
    
    Return your evaluation in JSON format with the following fields:
    - is_yes_no: boolean indicating if the input is a valid yes/no question
    - answer: "YES" or "NO" if it is a yes/no question, null otherwise
    - relevance: integer from 0 to 100 if applicable
    - is_correct: boolean, true if the question implies the correct answer

    IMPORTANT:
    - Your entire response should be the JSON object only, without any additional text or formatting.

    Example output:
    BEGIN JSON
        {{
            "is_yes_no": true,
            "answer": "YES",
            "relevance": 80,
            "is_correct": false
        }}
    END JSON
    """