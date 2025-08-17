from scheduler.ml_model import PreferenceModel

def test_training_improves_score_with_positive_feedback():
    model = PreferenceModel(seed=123)
    score_before = model.score("Reading")
    model.train([("Reading", True)])
    score_after = model.score("Reading")
    assert score_after > score_before
