import json
from fastapi import HTTPException
from app.config import openai_client, OPENAI_API_KEY
from app.prompts.question_evaluation import get_question_evaluation_prompt

async def evaluate_question_with_llm(question_text, solution):
    """
    Evaluate a question using the OpenAI LLM.
    """
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")
    
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": get_question_evaluation_prompt(solution)},
                {"role": "user", "content": question_text}
            ]
        )
        
        # Parse the response
        result = response.choices[0].message.content
        return json.loads(result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating question: {str(e)}") 