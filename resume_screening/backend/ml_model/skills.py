import re


# Canonical skills with common spellings seen in real resumes. Keeping aliases
# here makes the detector useful even when candidates use shorthand or dots.
SKILL_ALIASES = {
    "Python": ["python", "python3"],
    "Java": ["java"],
    "C++": ["c++", "cpp", "c plus plus"],
    "JavaScript": ["javascript", "js", "ecmascript"],
    "SQL": ["sql", "mysql", "sqlite", "mssql"],
    "HTML": ["html", "html5"],
    "CSS": ["css", "css3", "tailwind"],
    "React": ["react", "reactjs", "react.js"],
    "Node.js": ["node", "nodejs", "node.js"],
    "Django": ["django"],
    "Flask": ["flask"],
    "Ruby": ["ruby", "ruby on rails", "rails"],
    "PHP": ["php"],
    "Swift": ["swift"],
    "Kotlin": ["kotlin"],
    "R": ["r programming", "r language"],
    "MATLAB": ["matlab"],
    "Scala": ["scala"],
    "Go": ["golang", "go language"],
    "TypeScript": ["typescript", "ts"],
    "PostgreSQL": ["postgresql", "postgres", "psql"],
    "MongoDB": ["mongodb", "mongo db", "mongo"],
    "Redis": ["redis"],
    "AWS": ["aws", "amazon web services"],
    "REST API": ["rest api", "restful", "rest api's", "rest apis"],
    "Machine Learning": ["machine learning", "ml model", "ml"],
    "Deep Learning": ["deep learning", "neural network", "neural networks"],
    "Data Analysis": ["data analysis", "data analytics", "data analyst"],
    "Data Visualization": ["data visualization", "data visualisation", "visualization"],
    "Natural Language Processing": ["natural language processing", "nlp"],
    "TensorFlow": ["tensorflow", "tensor flow"],
    "PyTorch": ["pytorch", "py torch"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy", "num py"],
    "Power BI": ["power bi", "powerbi"],
    "Tableau": ["tableau"],
    "Docker": ["docker", "containerization", "containerisation"],
    "Kubernetes": ["kubernetes", "k8s"],
    "Git": ["git", "github", "gitlab", "bitbucket"],
}

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
    """Return recognised skills, including common aliases and resume spellings."""
    normalized_text = re.sub(r"\s+", " ", text.casefold())
    found_skills = []

    for skill, aliases in SKILL_ALIASES.items():
        for alias in aliases:
            pattern = rf"(?<!\w){re.escape(alias.casefold())}(?!\w)"
            if re.search(pattern, normalized_text):
                found_skills.append(skill)
                break

    return found_skills
