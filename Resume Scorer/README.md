# 🧠 JobRight-Style Resume Scoring System

An intelligent resume scoring system that uses NLP and semantic similarity to match resumes against job descriptions.

## Features

- **Semantic Similarity**: Uses sentence transformers to compute deep semantic matching between resume and job description
- **Keyword Extraction**: Automatically extracts important keywords from job descriptions using spaCy NLP
- **Keyword Coverage**: Calculates what percentage of job keywords appear in the resume
- **Weighted Scoring**: Combines semantic similarity (65%) and keyword coverage (35%) for a final score out of 10

## Installation

### 1. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 2. Download spaCy language model

```bash
python -m spacy download en_core_web_sm
```

## Usage

### Basic Usage

Run the example:

```bash
python resume_scorer.py
```

### Using in Your Own Code

```python
from resume_scorer import score_resume

# Your resume text
resume_text = """
Experienced data analyst skilled in Python, SQL, ETL pipelines,
machine learning, cloud systems, and dashboard creation.
"""

# Job description text
job_text = """
Looking for a data analyst knowledgeable in SQL, Python,
ETL, data modeling, cloud tools, and business dashboards.
"""

# Score the resume
results = score_resume(resume_text, job_text)

print(f"Final Score: {results['final_score']}/10")
print(f"Semantic Similarity: {results['similarity']:.4f}")
print(f"Keyword Coverage: {results['coverage']:.4f}")
print(f"Matched Keywords: {results['matched_keywords']}")
```

## How It Works

1. **Keyword Extraction**: Extracts nouns, proper nouns, noun phrases, and verbs from the job description
2. **Text Embedding**: Converts both resume and job description into dense vector representations using `all-MiniLM-L6-v2` model
3. **Similarity Calculation**: Computes cosine similarity between the two embeddings
4. **Keyword Matching**: Checks how many extracted keywords appear in the resume
5. **Final Scoring**: Combines similarity (65%) + keyword coverage (35%) and scales to 0-10

## Output

The `score_resume()` function returns a dictionary with:

- `similarity`: Semantic similarity score (0-1)
- `coverage`: Keyword coverage score (0-1)
- `matched_keywords`: List of job keywords found in resume
- `raw_keywords`: All keywords extracted from job description
- `final_score`: Combined final score (0-10)

## Requirements

- Python 3.7+
- sentence-transformers
- spacy
- numpy

## License

MIT
