from dataclasses import dataclass
from typing import Dict, List
from crewai import Agent, Task, Crew
from .historian import HistorianAgent
from .quiz import QuizAgent
from .coach import CoachAgent
from .curriculum import CurriculumAgent 
from ..db import list_topics

@dataclass
class StudyCrew:
    def __post_init__(self):
        self.historian = HistorianAgent()
        self.quiz = QuizAgent()
        self.coach = CoachAgent()
        self.curriculum = CurriculumAgent()
        
        self.planner_agent = Agent(role="curriculum_planner", goal="Pick topics for today's study session",)
        self.quiz_agent = Agent(role="Quiz Master", goal="Draft quizzes")
        self.coach_agent = Agent(role="Coach", goal="Grade answers")

    def plan_today(self) -> List[Dict]:
        return self.curriculum.pick_today(list_topics())

    def start_quiz(self, topic: Dict) -> Dict:
        return self.quiz.generate(topic)

    def submit_answer(self, topic_id: str, question: List[Dict], answer:List[str]) -> Dict:
        results = self.coach.evaluate(questions,answers)
        self.historian.persist(topic_id, float(results.get("score",0)), results.get("feedback",""))
        return results

    def crew_demo(self, topic: Dict) -> str:
        t1 = Task(description=f"List subskills for topic {topic['name']}", agent=self.planner_agent)
        t2 = Task(description=f"Create 3 questions for topic {topic['name']}", agent=self.quiz_agent, context=[t1])
        t3 = Task(description=f"Define brief grading criteria", agent=self.coach_agent, context=[t2])
        crew = Crew(agents=[self.planner_agent, self.quiz_agent, self.coach_agent], tasks=[t1, t2, t3])
        return str(crew.kickoff())