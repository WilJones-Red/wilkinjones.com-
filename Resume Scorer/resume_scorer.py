# Install dependencies:
# pip install sentence-transformers spacy
# python -m spacy download en_core_web_sm

# Import libraries

import spacy
import numpy as np
from sentence_transformers import SentenceTransformer


# Load models

word_wizard = spacy.load("en_core_web_sm")
text_ninja = SentenceTransformer("all-MiniLM-L6-v2")w

# Custom stop words to exclude from keyword extraction
JUNK_WORDS = {
    # personal pronouns
    "i", "me", "my", "mine", "myself",
    "we", "us", "our", "ours", "ourselves",
    "you", "your", "yours", "yourself", "yourselves",
    "he", "him", "his", "himself",
    "she", "her", "hers", "herself",
    "they", "them", "their", "theirs", "themselves",

    # demonstratives
    "that", "this", "these", "those", "here", "there",

    # weak verbs / helpers
    "am", "is", "are", "was", "were", "be", "been", "being",
    "do", "does", "did", "doing",
    "have", "has", "had", "having",
    "make", "makes", "made",
    "get", "gets", "got", "getting",
    "give", "gives", "gave", "giving",
    "feel", "feels", "felt",

    # intent/emotional verbs
    "love", "like", "want", "need", "hope", "wish", "think", "believe",

    # modal verbs
    "can", "could", "should", "would", "may", "might", "must", "shall", "will",

    # conjunctions
    "and", "or", "but", "nor", "yet", "so", "for",
    "if", "then", "else", "because", "while", "although",

    # determiners & quantifiers
    "a", "an", "the", "some", "any", "each", "every",
    "either", "neither", "both", "few", "many", "much",
    "more", "most",

    # prepositions
    "in", "on", "at", "by", "for", "from", "to", "with", "without",
    "over", "under", "into", "onto", "through", "across", "against",
    "about", "during", "before", "after",

    # conversational fluff
    "just", "really", "very", "pretty", "quite", 
    "basically", "actually", "literally",
    "maybe", "perhaps", "probably",
    "again", "still", "even", "often", "sometimes",

    # generic nouns
    "thing", "things", "stuff",
    "something", "anything", "everything", "nothing",

    # resume generic fluff / buzzwords
    "team", "player", "teamplayer", "hardworking", "selfstarter",
    "gogetter", "fastlearner", "detailoriented", "detail-oriented",
    "resultsdriven", "results-driven", "multitasker", "multitasking",
    "proactive", "dedicated", "motivated", "driven", "passionate",
    "reliable", "dependable", "responsible", "adaptable",
    "peopleperson", "people-person", "organized", "creative",
    "innovative", "professional", "enthusiastic",

    # vague corporate filler
    "collaborative", "crossfunctional", "cross-functional",
    "strategic", "dynamic", "synergy", "empower", "empowered",
    "mission-driven", "missiondriven", "value-added", "valueadded",
    "cuttingedge", "cutting-edge",

    # nothing statements
    "workwell", "work well", "workswell", "works well",
    "problem solver", "problemsolver",
    "team oriented", "teamoriented",
    "strong communicator", "excellent communication skills",
    "communication skills", "leadership skills",
    "critical thinker", "criticalthinking",
    "quick learner", "quicklearner"
}



# Keyword extraction

def extract_keywords(text):
    """
    Extracts keywords from job description using spaCy noun chunks
    + nouns + proper nouns + verbs, excluding stop words and pronouns.
    """

    parsed_doc = word_wizard(text)
    cool_words = set()

    # Add noun phrases
    for chunk in parsed_doc.noun_chunks:
        phrase = chunk.text.lower().strip()
        if phrase not in JUNK_WORDS:
            cool_words.add(phrase)

    # Add single tokens (nouns/verbs/etc), excluding stop words and pronouns
    for token in parsed_doc:
        word = token.text.lower().strip()
        if (token.pos_ in ["NOUN", "PROPN", "VERB"] and 
            not token.is_stop and 
            token.pos_ != "PRON" and
            word not in JUNK_WORDS):
            cool_words.add(word)

    # Filter out tiny junk words
    cool_words = {kw for kw in cool_words if len(kw) > 2}

    return list(cool_words)


# Embedding function

def embed(text):
    """Embeds text using SentenceTransformers (normalized)."""
    return text_ninja.encode(text, normalize_embeddings=True)


# Cosine similarity

def cosine_sim(vector_a, vector_b):
    """
    Computes cosine similarity between two normalized embeddings.
    Dot = cosine because vectors are normalized.
    """
    return float(np.dot(vector_a, vector_b))


# Keyword coverage score

def keyword_coverage(resume_text, job_keywords):
    """
    Checks how many job keywords appear in the resume.
    Returns:
        (coverage_score, matched_keywords)
    """
    resume_lowercased = resume_text.lower()
    word_matches = [keyword for keyword in job_keywords if keyword in resume_lowercased]

    if len(job_keywords) == 0:
        return 0, []

    match_ratio = len(word_matches) / len(job_keywords)
    return match_ratio, word_matches


# Final score (weighted combo)

def final_score(similarity, coverage):
    """
    Combines semantic similarity + keyword coverage into a score.
    Scale is returned on 0 to 10.
    """
    blended_score = (0.65 * similarity) + (0.35 * coverage)
    return round(blended_score * 10, 2)


# Full scoring function

def score_resume(resume_text, job_text):
    """
    Main function: takes raw resume + job description,
    computes:
      - extracted keywords
      - embeddings
      - similarity
      - keyword coverage
      - final score
    """
    # Extract keywords
    job_buzzwords = extract_keywords(job_text)

    # Embeddings
    job_vector = embed(job_text)
    resume_vector = embed(resume_text)

    # Similarity score
    semantic_match = cosine_sim(job_vector, resume_vector)

    # Keyword coverage
    keyword_match, winning_words = keyword_coverage(resume_text, job_buzzwords)

    # Final score
    total_score = final_score(semantic_match, keyword_match)

    return {
        "similarity": semantic_match,
        "coverage": keyword_match,
        "matched_keywords": winning_words,
        "raw_keywords": job_buzzwords,
        "final_score": total_score
    }


# Example usage

if __name__ == "__main__":

    my_resume = """
    Experienced data analyst skilled in Python, SQL, ETL pipelines,
    machine learning, cloud systems, and dashboard creation.
    """

    dream_job = """
    Looking for a data analyst knowledgeable in SQL, Python,
    ETL, data modeling, cloud tools, and business dashboards.
    """

    results = score_resume(my_resume, dream_job)

    print("\n===== SCORING RESULTS =====")
    print(f"Semantic Similarity: {results['similarity']:.4f}")
    print(f"Keyword Coverage:    {results['coverage']:.4f}")
    print(f"Matched Keywords:     {results['matched_keywords']}")
    print(f"Final Score (0 to 10):   {results['final_score']}")
    print("===========================\n")
