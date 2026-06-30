SKILLS_DB = {
    "languages": [
        "python", "javascript", "typescript", "java", "c", "c++", "c#",
        "go", "rust", "ruby", "php", "swift", "kotlin", "scala", "r",
        "matlab", "perl", "bash", "shell", "powershell"
    ],

    "web_frameworks": [
        "fastapi", "flask", "django", "express", "react", "angular", "vue",
        "nextjs", "nuxtjs", "svelte", "spring", "rails", "laravel",
        "asp.net", "nodejs", "node.js"
    ],

    "databases": [
        "sql", "mysql", "postgresql", "sqlite", "mongodb", "redis",
        "elasticsearch", "cassandra", "dynamodb", "firebase",
        "oracle", "mssql", "mariadb"
    ],

    "cloud": [
        "aws", "azure", "gcp", "google cloud", "heroku", "render",
        "digitalocean", "vercel", "netlify", "cloudflare"
    ],

    "devops": [
        "docker", "kubernetes", "k8s", "jenkins", "github actions",
        "gitlab ci", "terraform", "ansible", "nginx", "linux"
    ],

    "ai_ml": [
        "machine learning", "deep learning", "nlp", "natural language processing",
        "computer vision", "tensorflow", "pytorch", "keras", "scikit-learn",
        "pandas", "numpy", "matplotlib", "reinforcement learning",
        "transformers", "llm", "openai", "langchain"
    ],

    "tools": [
        "git", "github", "gitlab", "bitbucket", "jira", "confluence",
        "postman", "figma", "linux", "vim", "vscode", "unity", "blender"
    ],

    "concepts": [
        "rest api", "graphql", "microservices", "ci/cd", "agile", "scrum",
        "oop", "object oriented", "data structures", "algorithms",
        "system design", "api design", "test driven development", "tdd"
    ]
}


SKILL_ALIASES = {
    "js":            "javascript",
    "ts":            "typescript",
    "py":            "python",
    "ml":            "machine learning",
    "dl":            "deep learning",
    "k8s":           "kubernetes",
    "gcp":           "google cloud",
    "postgres":      "postgresql",
    "mongo":         "mongodb",
    "node":          "nodejs",
    "react.js":      "react",
    "vue.js":        "vue",
    "next.js":       "nextjs",
    "sklearn":       "scikit-learn",
    "tf":            "tensorflow",
    "c sharp":       "c#",
    "golang":        "go",
}

def get_all_skills():
    """
    Flattens SKILLS_DB into a single set of all known skills.

    Returns:
        A set of all skill strings (lowercase)
    """

    all_skills = set()
    for category, skill_list in SKILLS_DB.items():
        all_skills.update(skill_list)

    all_skills.update(SKILL_ALIASES.keys())

    return all_skills

def normalize_skill(skill: str) -> str:
    """
    Normalizes a skill string:
    - Lowercase
    - Strip whitespace
    - Resolve aliases

    Args:
        skill: Raw skill string

    Returns:
        Normalized canonical skill name
    """
    normalized = skill.lower().strip()

    return SKILL_ALIASES.get(normalized, normalized)

def get_skill_category(skill: str) -> str:
    """
    Given a skill, returns which category it belongs to.

    Args:
        skill: Normalized skill string

    Returns:
        Category name or "other" if not found
    """
    normalized = normalize_skill(skill)

    for category, skill_list in SKILLS_DB.items():
        if normalized in skill_list:
            return category

    return "other"
