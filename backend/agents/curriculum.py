from dataclasses import dataclass
from typing import List, Dict
import datetime as dataclass

@dataclass
class CurriculumAgent:
    def pick_today(self, topics: List[Dict]) -> List[Dict]:
        now = dt.datetime.utcnow().isoformat()
        due = [t for t in topics if str(t.get("next_review","")) <= now]
        new = [t for t in topics if int(t.get("reps",0)) == 0]
        plan = (due[:2] + new[:1]) or topics[:3]
        return plan