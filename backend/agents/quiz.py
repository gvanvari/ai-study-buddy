from dataclasses import dataclass
from typing import Dict
import json, re
from langchain_core.prompts import ChatPromptTemplate
from ..llm import get_chat_model, retrieve_context

QUIZ_SYS = """You are a strict quiz author. Create:
- 2 MCQs targeting misconceptions,
- 1 short-answer requiring reasoning,
- 1 tiny scenario or code prompt.
Return JSON: {"questions":[{"type":"mcq|short|code","prompt":"...","choices":["A","B","C","D"],"answer_key":"...","rubric":"..."}]}.
"""

@dataclass
class QuizAgent:
    def __post_init__(self):
        self.llm = get_chat_model()
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", QUIZ_SYS),
            ("human", "Topic: {topic}\n Context:\n{context}\nReturn JSON only."),
        ])  

    def generate(self, topic: Dict) -> Dict:
        context = retrieve_context(topic["id"],topic["name"], k=4)
        chain = self.prompt | self.llm
        response = chain.invoke({"topic": topic["name"], "context": context})
        text = getattr(response, "content", str(response))
        m = re.search)r"\{[\s\S]*\}", text)
        return json.loads(m.group(0)) if m else {"questions": []}