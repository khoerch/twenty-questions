def get_solution_generation_prompt(difficulty: int):
    return f"""
    Generate a solution for a word guessing game. Today the difficulty level is {difficulty}/7.

    Rules:
    1. The solution must be a person, place, or thing.
    2. For difficulty {difficulty}/7, make the solution {'very common and simple' if difficulty <= 2 else 'moderately challenging' if difficulty <= 5 else 'quite difficult but still recognizable'}.
    3. Provide a single hint that gives a clue without making the answer obvious. The hint should be a single sentence that is not too long.
    4. Format your response exactly as follows:
    
    Return your evaluation in JSON format with the following fields:
    - solution: [single word or short phrase]
    - hint: [brief hint in the form of a single sentence]

    IMPORTANT:
    - Your entire response should be the JSON object only, without any additional text or formatting.

    Example output:
    BEGIN JSON
        {{
            "solution": "Eiffel Tower",
            "hint": "This landmark was built for a world exposition."
        }}
    END JSON
    """ 