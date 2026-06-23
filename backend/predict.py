import random

classes = [
    "Healthy Tomato",
    "Tomato Early Blight",
    "Tomato Late Blight",
    "Apple Scab",
    "Healthy Apple",
    "Corn Rust",
    "Healthy Corn"
]


def predict_disease(image_path):
    """
    Dummy prediction until real AI model is added.
    """

    disease = random.choice(classes)

    confidence = round(random.uniform(90, 99), 2)

    return {
        "status": True,
        "disease": disease,
        "confidence": confidence,
        "message": "Demo prediction (AI model not installed)"
    }