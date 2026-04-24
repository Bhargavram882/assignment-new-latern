from fastapi import FastAPI
from datetime import datetime

app = FastAPI()


@app.get("/")
def root():
    return {"status": "running"}


def is_relevant(current, prior):
    curr_desc = current.get("study_description", "").upper()
    prior_desc = prior.get("study_description", "").upper()

    if curr_desc == prior_desc:
        return True

    if "BRAIN" in curr_desc and ("BRAIN" in prior_desc or "HEAD" in prior_desc):
        return True

    curr_mod = curr_desc.split()[0] if curr_desc else ""
    prior_mod = prior_desc.split()[0] if prior_desc else ""

    if curr_mod == prior_mod:
        return True
    try:
        d1 = datetime.fromisoformat(current.get("study_date"))
        d2 = datetime.fromisoformat(prior.get("study_date"))

        if abs((d1 - d2).days) < 700:
            return True
    except:
        pass

    return False


@app.post("/predict")
def predict(request: dict):
    predictions = []

    cases = request.get("cases", [])

    for case in cases:
        case_id = case.get("case_id")
        current = case.get("current_study", {})
        priors = case.get("prior_studies", [])

        for prior in priors:
            pred = is_relevant(current, prior)

            predictions.append({
                "case_id": case_id,
                "study_id": prior.get("study_id"),
                "predicted_is_relevant": pred
            })

    return {"predictions": predictions}
