# import re
# from transformers import pipeline
# from config import SUMMARIZER_MODEL

# _summarizer = None

# def get_summarizer():
#     global _summarizer
#     if _summarizer is None:
#         try:
#             _summarizer = pipeline("summarization", model=SUMMARIZER_MODEL)
#         except:
#             _summarizer = None
#     return _summarizer

# def summarize_text(text, max_length=150, min_length=40):
#     s = get_summarizer()
#     if s is None:
#         # fallback simple first few sentences
#         sentences = re.split(r'(?<=[.!?])\s+', text)
#         return ' '.join(sentences[:5])
    
#     max_chunk = 1000
#     chunks = [text[i:i+max_chunk] for i in range(0, len(text), max_chunk)]
#     summaries = []
#     for chunk in chunks:
#         out = s(chunk, max_length=max_length, min_length=min_length, do_sample=False)
#         summaries.append(out[0]['summary_text'])
#     return ' '.join(summaries)


import re
from transformers import pipeline
from config import SUMMARIZER_MODEL

_summarizer = None

def get_summarizer():
    global _summarizer
    if _summarizer is None:
        try:
            _summarizer = pipeline("summarization", model=SUMMARIZER_MODEL)
        except Exception as e:
            print(f"Summarizer load failed: {e}")
            _summarizer = None
    return _summarizer

def summarize_text(text, max_length=150, min_length=40):
    # Handle empty or very short text safely
    if not text or len(text.strip()) < 50:  
        return text.strip()

    s = get_summarizer()
    if s is None:
        # fallback simple first few sentences
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return ' '.join(sentences[:5])
    
    max_chunk = 1000
    chunks = [text[i:i+max_chunk] for i in range(0, len(text), max_chunk)]
    summaries = []
    for chunk in chunks:
        if len(chunk.strip()) < 50:   # skip tiny chunks
            summaries.append(chunk.strip())
            continue
        try:
            out = s(chunk, max_length=max_length, min_length=min_length, do_sample=False)
            summaries.append(out[0]['summary_text'])
        except Exception as e:
            print(f"Summarization failed for chunk: {e}")
            summaries.append(chunk.strip())
    return ' '.join(summaries)
