import re

skills = [
    "Python",
    "Java",
    "C++",
    "JavaScript",
    "SQL",
    "HTML",
    "CSS",
    "React",
    "Node.js",
    "Django",
    "Flask",
    "Ruby",
    "PHP",
    "Swift",
    "Kotlin",
    "R",
    "MATLAB",
    "Scala",
    "Go",
    "TypeScript",
    "PostgreSQL",
    "MongoDB",
    "Redis",
    "AWS",
    "REST API",
    "Machine Learning",
    "Deep Learning",
    "Data Analysis",
    "Data Visualization",
    "Natural Language Processing",
    "TensorFlow",
    "PyTorch",
    "Pandas",
    "NumPy",
    "Power BI",
    "Tableau",
    "Docker",
    "Kubernetes",
    "Git"
]

def extract_skills(text):
    found_skills = []

    text = text.lower()

    for skill in skills:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, text):
            found_skills.append(skill)

    return found_skills
