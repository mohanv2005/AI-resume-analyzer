
# master skills database.

SKILLS_DB = {
    "languages": [
        "python", "javascript", "typescript", "java", "c", "c++", "c#",
        "go", "rust", "ruby", "php", "swift", "kotlin", "scala", "r",
        "matlab", "perl", "bash", "shell", "powershell",
        "dart", "elixir", "haskell", "lua"
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
        "postman", "figma", "vim", "vscode", "unity", "blender"
    ],

    "concepts": [
        "rest api", "graphql", "microservices", "ci/cd", "agile", "scrum",
        "oop", "object oriented", "data structures", "algorithms",
        "system design", "api design", "test driven development", "tdd"
    ],

    "frontend": [
        "html", "css", "sass", "scss", "tailwind", "bootstrap",
        "redux", "webpack", "vite", "jquery"
    ],

    "testing": [
        "pytest", "unittest", "jest", "mocha", "cypress", "selenium",
        "junit", "testng"
    ],

    "mobile": [
        "react native", "flutter", "android", "ios", "xamarin"
    ]
}

# Aliases:
# Key = what might appear in a resume
# Value = the canonical skill name in our DB
SKILL_ALIASES = {
    "js":            "javascript",
    "ts":            "typescript",
    "py":            "python",
    "ml":            "machine learning",
    "dl":            "deep learning",
    "cv":            "computer vision",
    "rl":            "reinforcement learning",
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

SKILL_SYNONYMS = {
    "natural language processing": "nlp",
    "artificial intelligence": "ai",
    "continuous integration": "ci/cd",
    "continuous deployment": "ci/cd",
    "continuous integration/continuous deployment": "ci/cd",
    "object oriented programming": "oop",
    "object-oriented programming": "oop",
    "restful api": "rest apis",
    "restful apis": "rest apis",
    "large language model": "llm",
    "large language models": "llm",
}

def get_all_skills() -> set:
    """
    Flattens SKILLS_DB into a single set of all known skills.
    Used for fast lookup during matching.

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
    - Resolve synonyms to canonical form

    Args:
        skill: Raw skill string

    Returns:
        Normalized canonical skill name
    """
    normalized = skill.lower().strip()

    resolved = SKILL_ALIASES.get(normalized, normalized)

    return SKILL_SYNONYMS.get(resolved, resolved)


def get_skill_category(skill: str) -> str:
    """
    Given a skill, returns which category it belongs to.
    Useful for generating category-level feedback.

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