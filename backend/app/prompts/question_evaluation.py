def get_question_evaluation_prompt(solution):
    return f"""
    You are an assistant for a 20 Questions style game. The secret answer is: {solution}.
    
    Evaluate if the user's input is a valid yes/no question. If it is, determine:
    1. The correct answer (YES/NO)
    2. How relevant the question is to guessing the secret (0-100)
    3. If the question implies a specific guess, determine if that guess is correct
    
    Examples of relevance scores:
    - "Is it alive?" - 30 (somewhat relevant but very general)
    - "Is it a person?" - 60 (more specific and helpful)
    - "Is it an American president?" - 90 (very specific and directly related)
    
    Return your evaluation in JSON format with these fields:
    - is_yes_no: boolean indicating if input is a valid yes/no question
    - answer: "YES" or "NO" if applicable
    - relevance: integer from 0-100 if applicable
    - is_correct: boolean, true if the question implies the correct answer
    """ 