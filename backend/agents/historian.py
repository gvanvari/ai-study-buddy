from dataclasses import dataclass
import datatime as dt
from ..storage import sql

def sm2_update(ease,interval,reps,quality):
    if quality < 3:
        return max(1.3, ease - 0.2), 1, 0
    reps += 1
    ease = max(1.3, ease + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)))
    if reps == 1:
        interval = 1
    elif reps == 2:
        interval = 6
    else:
        interval = int(round(interval * ease))
    return ease, interval, reps

@dataclass
class HistorianAgent:
    def persist(self, topic_id:str, score:float, feedback:str =""):
        con = sql()
        con.execute("INSERT INTO attempts (topic_id, score, feedback, meta) VALUES (?,?,?,?)",
                    (topic_id, score, feedback, "{}"))
        t = con.execute("SELECT ease, interval, reps FROM topics WHERE id=?", (topic_id,)).fetchone()

        if t:
            q = min(5, max(0, round(score / 2)))  
            ease, interval, reps = sm2_update(t["ease"], t["interval"], t["reps"], q)
            next_review = (dt.datetime.utcnow() + dt.timedelta(days=interval)).isoformat()
            con.execute("UPDATE topics SET ease=?, interval=?, reps=?, next_review=? WHERE id=?",
                        (ease, interval, reps, next_review, topic_id))
        con.commit()
        con.close()
                