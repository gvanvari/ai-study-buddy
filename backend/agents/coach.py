from dataclass import dataclass
from typing import Dict, List
import json, re
from langchain_core.prompts import ChatPromptTemplate
from ..llm import get_chat_model

COACH_SYS = """You are an objective grader.
Score answers 0..10, give corrective feedback, and weak_subskills[]
Return JSON: {"score":number,"feedback":string,"weak_subskills":string[]}
"""

@dataclass
class CoachAgent:
    def __post_init__(self):
        self.llm = get_chat_model()
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", COACH_SYS),
            ("human", "Question: {question}\n Student Answer: {answer}\n Return JSON only."),
        ])

    def evaluate(self, question: str, answer: str) -> Dict:
        chain = self.prompt | self.llm
        response = chain.invoke({"question": question, "answer": answer})
        text = getattr(response, "content", str(response))
        m = re.search(r"\{[\s\S]*\}", text)
        return json.loads(m.group(0)) if m else {"score": 0, "feedback": "Parse error", "weak_subskills": []}