from fastapi import APIRouter, Depends, Request
from transformers import pipeline

router = APIRouter()

# Dependency to provide the emotion detection pipeline
def get_emotion_pipeline(request: Request):
    return request.app.state.emotion_pipeline

@router.post("/detect-emotion")
async def detect_emotion(text: str, emotion_pipeline=Depends(get_emotion_pipeline)):
    """
    Detect the emotion in the given text using a pre-trained NLP model.
    """
    results = emotion_pipeline(text, return_all_scores=True)  # Get scores for all emotions
    return {"text": text, "emotions": results[0]}  # Return all emotions with their scores

@router.post("/answer-question")
async def answer_question(question: str, context: str, qa_pipeline=Depends(lambda request: request.app.state.qa_pipeline)):
    """
    Answer a question based on the provided context using a pre-trained NLP model.
    """
    result = qa_pipeline(question=question, context=context)
    return {"question": question, "context": context, "answer": result["answer"], "score": result["score"]}