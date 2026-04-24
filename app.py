from fastapi import FastAPI

from datetime import datetime

def is_relevant(current, prior):
    curr_desc = current["study_description"].upper()
    prior_desc = prior["study_description"].upper()

    # Rule 1: exact match
    if curr_desc == prior_desc:
        return True

    # Rule 2: same body part
    if "BRAIN" in curr_desc and ("BRAIN" in prior_desc or "HEAD" in prior_desc):
        return True

    # Rule 3: same modality
    if curr_desc.split()[0] == prior_desc.split()[0]:
        return True

    # Rule 4: recent study (within ~2 years)
    try:
        d1 = datetime.fromisoformat(current["study_date"])
        d2 = datetime.fromisoformat(prior["study_date"])
        if abs((d1 - d2).days) < 700:
            return True
    except:
        pass

    return False


@app.post("/predict")
def predict(request: dict):
    predictions = []

    for case in request["cases"]:
        current = case["current_study"]

        for prior in case["prior_studies"]:
            pred = is_relevant(current, prior)

            predictions.append({
                "case_id": case["case_id"],
                "study_id": prior["study_id"],
                "predicted_is_relevant": pred
            })

    return {"predictions": predictions}