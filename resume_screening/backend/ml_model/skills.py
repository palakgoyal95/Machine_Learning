skills =[
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
    "postgreSQL",
    "MongoDB",
    "Redis",
    "AWS",
    "Restful APIs",
    "Machine Learning",
    "Deep Learning",
    "Data Analysis",
    "Data Visualization",
    "Natural Language Processing",
    "tensorFlow",
    "PyTorch",
    "pandas",
    "NumPy",
    "powerBI",
    "Tableau",
    "docker",
    "Kubernetes",
    "Git"
]

def extract_skills(text):

    found_skills = []

    text = text.lower()

    for skill in skills:

        if skill.lower() in text:

            found_skills.append(skill)

    return found_skills