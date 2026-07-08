async function analyzeResume() {
    const fileInput = document.getElementById("resumeFile");
    const jobDescInput = document.getElementById("jobDescription");

    if (!fileInput.files[0]) {
        showError("Please select a PDF file.");
        return;
    }

    if (jobDescInput.value.trim().length < 20) {
        showError("Please enter a complete job description.");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);
    formData.append("job_description", jobDescInput.value);

    showLoading(true);
    hideResults();
    hideError();
    disableButton(true);

    try {
        const response = await fetch("/analyze-resume", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Server error occurred.");
        }

        const data = await response.json();

        displayResults(data);

    } catch (error) {
        showError(error.message);
    } finally {
        showLoading(false);
        disableButton(false);
    }
}


function displayResults(data) {
    const pct = data.match_percentage;
    document.getElementById("matchPercentage").textContent = pct + "%";
    document.getElementById("matchSummary").textContent =
        `${data.total_matched} of ${data.total_job_skills} required skills matched`;

    const bar = document.getElementById("matchProgressBar");
    bar.style.width = pct + "%";
    bar.className = "progress-bar " + getProgressBarColor(pct);

    
    const quality = deriveQuality(pct);
    const badge = document.getElementById("matchQualityBadge");
    badge.textContent = quality.toUpperCase();
    badge.className = "badge fs-6 " + getQualityBadgeColor(quality); 

    if (data.ai_suggestions?.overall_assessment) {
        document.getElementById("overallAssessment").textContent =
            data.ai_suggestions.overall_assessment;
        show("assessmentCard");
    }

    renderSkillBadges("matchedSkills", data.matched_skills, "skill-matched");
    renderSkillBadges("missingSkills", data.missing_skills, "skill-missing");
    renderSkillBadges("extraSkills", data.extra_skills, "skill-extra");

    renderMissingByCategory(data.missing_by_category);

    if (data.ai_suggestions) {
        renderAISuggestions(data.ai_suggestions);
        show("aiSuggestionsCard");
    } else if (data.ai_error) {
        document.getElementById("aiSuggestionsCard").innerHTML =
            `<div class="card-body p-4">
                <h5 class="card-title mb-3">AI Suggestions</h5>
                <div class="alert alert-warning mb-0">
                    AI suggestions unavailable: ${data.ai_error}
                </div>
            </div>`;
        show("aiSuggestionsCard");
    }

    show("resultsSection");

    document.getElementById("resultsSection").scrollIntoView({ behavior: "smooth" });
}


function renderSkillBadges(elementId, skills, cssClass) {
    const container = document.getElementById(elementId);

    if (!skills || skills.length === 0) {
        container.innerHTML = '<span class="text-muted small">None</span>';
        return;
    }

    // Building all badges as one HTML string (faster than appending one by one)
    container.innerHTML = skills
        .map(skill => `<span class="skill-badge ${cssClass}">${skill}</span>`)
        .join("");
}


function renderMissingByCategory(missingByCategory) {
    const container = document.getElementById("missingByCategory");

    if (!missingByCategory || Object.keys(missingByCategory).length === 0) {
        container.innerHTML = '<span class="text-muted small">No category data available.</span>';
        return;
    }

    // Object.entries() gives us [key, value] pairs
    container.innerHTML = Object.entries(missingByCategory)
        .map(([category, skills]) => `
            <div class="category-group">
                <div class="category-label">${category.replace("_", " ")}</div>
                <div>
                    ${skills.map(s => `<span class="skill-badge skill-missing">${s}</span>`).join("")}
                </div>
            </div>
        `)
        .join("");
}


function renderAISuggestions(suggestions) {
    const adviceContainer = document.getElementById("missingSkillsAdvice");
    if (suggestions.missing_skills_advice?.length > 0) {
        adviceContainer.innerHTML = suggestions.missing_skills_advice
            .map(item => `
                <div class="advice-card ${item.priority}">
                    <div class="d-flex justify-content-between align-items-start mb-1">
                        <strong>${item.skill}</strong>
                        <span class="badge ${item.priority === 'critical' ? 'bg-danger' : 'bg-warning text-dark'}">
                            ${item.priority === 'critical' ? 'Critical' : 'Nice to Have'}
                        </span>
                    </div>
                    <div class="small">${item.advice}</div>
                </div>
            `)
            .join("");
    } else {
        adviceContainer.innerHTML = '<span class="text-muted small">No advice available.</span>';
    }

    const improvementsList = document.getElementById("resumeImprovements");
    if (suggestions.resume_improvements?.length > 0) {
        improvementsList.innerHTML = suggestions.resume_improvements
            .map(item => `<li class="mb-2">${item}</li>`)
            .join("");
    } else {
        improvementsList.innerHTML = '<li class="text-muted">No improvements suggested.</li>';
    }

    const atsContainer = document.getElementById("atsKeywords");
    if (suggestions.ats_keywords?.length > 0) {
        atsContainer.innerHTML = suggestions.ats_keywords
            .map(kw => `<span class="skill-badge skill-ats">${kw}</span>`)
            .join("");
    } else {
        atsContainer.innerHTML = '<span class="text-muted small">No keywords suggested.</span>';
    }

    const projectsContainer = document.getElementById("recommendedProjects");
    if (suggestions.recommended_projects?.length > 0) {
        projectsContainer.innerHTML = suggestions.recommended_projects
            .map(project => `
                <div class="project-card">
                    <strong>${project.title}</strong>
                    <p class="text-muted small mt-1 mb-2">${project.description}</p>
                    <div>
                        ${(project.skills_covered || []).map(s =>
                            `<span class="skill-badge skill-extra">${s}</span>`
                        ).join("")}
                    </div>
                </div>
            `)
            .join("");
    } else {
        projectsContainer.innerHTML = '<span class="text-muted small">No projects suggested.</span>';
    }
}


function showLoading(visible) {
    safeToggle("loadingSection", visible);
}

function showError(message) {
    const el = document.getElementById("errorMessage");
    if (el) el.textContent = message;
    safeToggle("errorSection", true);
}

function hideError() {
    safeToggle("errorSection", false);
}

function hideResults() {
    safeToggle("resultsSection", false);
}

function disableButton(disabled) {
    const btn = document.getElementById("analyzeBtn");
    btn.disabled = disabled;
    btn.textContent = disabled ? "Analyzing..." : "Analyze Resume";
}

function show(elementId) {
    safeToggle(elementId, true);
}

function getProgressBarColor(pct) {
    if (pct >= 70) return "bg-success";
    if (pct >= 40) return "bg-warning";
    return "bg-danger";
}

function getQualityBadgeColor(quality) {
    const map = {
        "strong": "bg-success",
        "moderate": "bg-warning text-dark",
        "weak": "bg-danger"
    };
    return map[quality.toLowerCase()] || "bg-secondary";
}

function deriveQuality(pct) {
    if (pct >= 70) return "strong";
    if (pct >= 40) return "moderate";
    return "weak";
}

/**
 * Safely sets innerHTML on an element.
 * If the element doesn't exist, logs a warning instead of crashing.
 *
 * @param {string} elementId - The ID of the target element
 * @param {string} html - The HTML content to set
 */
function safeSetHTML(elementId, html) {
    const el = document.getElementById(elementId);
    if (el) {
        el.innerHTML = html;
    } else {
        console.warn(`safeSetHTML: element with id "${elementId}" not found in DOM`);
    }
}

/**
 * Safely shows or hides an element by toggling the d-none class.
 * If the element doesn't exist, logs a warning instead of crashing.
 *
 * @param {string} elementId - The ID of the target element
 * @param {boolean} visible - true to show, false to hide
 */
function safeToggle(elementId, visible) {
    const el = document.getElementById(elementId);
    if (el) {
        visible ? el.classList.remove("d-none") : el.classList.add("d-none");
    } else {
        console.warn(`safeToggle: element with id "${elementId}" not found in DOM`);
    }
}