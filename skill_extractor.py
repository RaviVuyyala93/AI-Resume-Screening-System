import re


SKILLS_DATABASE = [
    "python",
    "java",
    "c++",
    "sql",
    "mysql",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "nlp",
    "tensorflow",
    "keras",
    "pandas",
    "numpy",
    "scikit-learn",
    "fastapi",
    "flask",
    "django",
    "html",
    "css",
    "javascript",
    "react",
    "git",
    "github",
    "rest api",
    "spring boot",
    "docker",
    "power bi",
    "tableau",
    "excel"
]


def extract_skills(text):

    found_skills = []

    text = text.lower()

    for skill in SKILLS_DATABASE:

        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text):

            found_skills.append(skill)

    return found_skills