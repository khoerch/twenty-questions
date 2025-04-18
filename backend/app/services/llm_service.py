import json
import logging
from fastapi import HTTPException
from langfuse import Langfuse
# Replace openai with langfuse.openai for integrated tracing in Langfuse
# import openai
from langfuse.openai import openai
from app.core.config import OPENAI_API_KEY
from app.prompts.question_evaluation import get_question_evaluation_prompt
from app.prompts.solution_generation import get_solution_generation_prompt
from app.core.cache import ttl_cache

logger = logging.getLogger(__name__)

langfuse = Langfuse()


class LLMService:
    def __init__(self):
        self.llm = openai.OpenAI(api_key=OPENAI_API_KEY)

    async def invoke_llm(self, messages: list[dict]):
        try:
            response = self.llm.chat.completions.create(
                model="gpt-3.5-turbo",
                response_format={"type": "json_object"},
                messages=messages
            )
            
            result = response.choices[0].message.content
            return json.loads(result)
            
        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=500, detail=f"Error evaluating question: {str(e)}")

    @ttl_cache(namespace="question_evaluations", maxsize=100, ttl_seconds=86400)
    async def evaluate_question(self, question_text, solution):
        """
        Evaluate a question using the OpenAI LLM.
        """
        messages = [
                    {"role": "system", "content": get_question_evaluation_prompt(solution)},
                    {"role": "user", "content": question_text}
                ]
        return await self.invoke_llm(messages)

    async def generate_solution(self, difficulty: int):
        """Generate a solution and hint using the LLM service."""
        messages = [
            {"role": "system", "content": get_solution_generation_prompt(difficulty)}
        ]
        response = await self.invoke_llm(messages)
        logger.info(f"Generated solution: {response}")
        return response
