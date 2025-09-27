from ml.feedback import FeedbackTracker

def test_positive_feedback_boosts_priority():
    fb = FeedbackTracker()
    score_before = fb.score("Yoga")
    fb.record("Yoga", accepted=True)
    score_after = fb.score("Yoga")
    assert score_after > score_before
