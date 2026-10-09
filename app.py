"""
Multimodal Studio Hub: project skeleton
Run with:  pip install streamlit  then  streamlit run app.py

File layout (top to bottom):
  1. Page configuration
  2. Theme and CSS
  3. Placeholder data
  4. Reusable UI components
  5. Page functions (one per sidebar section)
  6. Router and sidebar (main)
"""

import html

import streamlit as st

# ---------------------------------------------------------------------------
# 1. PAGE CONFIGURATION
# Must be the first Streamlit call in the script.
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Multimodal Studio Hub",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# 2. THEME AND CSS
# Palette: ink navy (#16213E), cool paper (#F5F7FA), rule gray (#D9E0E7).
# Each modality has its own color; cards use it as a left border so the
# medium of a resource is readable at a glance.
# ---------------------------------------------------------------------------
MODALITY_COLORS = {
    "Written": "#324A5F",
    "Visual": "#1F7A8C",
    "Audio": "#A8620F",
    "Video": "#8A3B5E",
    "Interactive": "#3F7D4E",
}

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,500;6..72,700&family=IBM+Plex+Sans:wght@400;500;600&display=swap');

/* Page background and body text */
.stApp { background: #F5F7FA; }
.block-container { max-width: 1100px; padding-top: 2rem; }
[data-testid="stMarkdownContainer"] { font-family: 'IBM Plex Sans', system-ui, sans-serif; }

/* Headings use a serif face for an academic feel */
h1, h2, h3, h4, h5 { font-family: 'Newsreader', Georgia, serif !important; color: #16213E; letter-spacing: -0.01em; }

/* Sidebar: dark ink background with light text */
[data-testid="stSidebar"] { background: #16213E; }
[data-testid="stSidebar"] p, [data-testid="stSidebar"] label, [data-testid="stSidebar"] span { color: #D6DEE8; }
.brand { font-family: 'Newsreader', Georgia, serif; font-size: 1.6rem; font-weight: 700; color: #FFFFFF; line-height: 1.15; }
.tagline { color: #AEBBCB; font-size: .9rem; margin: .4rem 0 1.2rem; }

/* Home hero banner and modality strip */
.hero { background: #16213E; border-radius: 6px; padding: 2rem 2.25rem 1.5rem; margin-bottom: 1.25rem; }
.hero-title { font-family: 'Newsreader', Georgia, serif; font-size: 2.3rem; line-height: 1.15; color: #FFFFFF; margin-bottom: .6rem; }
.hero p { color: #C9D3DF; max-width: 62ch; line-height: 1.55; margin: 0; }
.strip { display: flex; gap: 4px; margin-top: 1.4rem; flex-wrap: wrap; }
.strip div { flex: 1 1 110px; padding: .6rem .8rem; color: #FFFFFF; font-size: .9rem; border-radius: 3px; }
.strip b { display: block; font-family: 'Newsreader', Georgia, serif; font-size: 1.6rem; }

/* Content cards */
.card { background: #FFFFFF; border: 1px solid #D9E0E7; border-left: 6px solid var(--accent, #1F7A8C); border-radius: 4px; padding: 1rem 1.25rem; margin-bottom: .75rem; }
.card-title { font-family: 'Newsreader', Georgia, serif; font-size: 1.2rem; font-weight: 700; color: #16213E; margin-bottom: .2rem; }
.card .meta { font-size: .85rem; color: #5B6877; margin-bottom: .5rem; }
.card p { color: #3A4756; line-height: 1.55; margin: 0 0 .6rem; }
.pill { display: inline-block; background: #E8EEF3; color: #2B3A4B; border-radius: 999px; padding: 2px 10px; font-size: .78rem; margin: 0 6px 4px 0; }

/* Rubric table */
.table-wrap { overflow-x: auto; }
table.rubric { border-collapse: collapse; width: 100%; font-size: .9rem; }
table.rubric th { background: #16213E; color: #FFFFFF; text-align: left; padding: .6rem .75rem; font-weight: 600; }
table.rubric td { border: 1px solid #D9E0E7; padding: .6rem .75rem; vertical-align: top; color: #3A4756; background: #FFFFFF; }
table.rubric td.crit { font-weight: 600; color: #16213E; background: #EEF2F6; }
</style>
"""

# ---------------------------------------------------------------------------
# 3. PLACEHOLDER DATA
# Plain Python structures. Replace with CSV, a database, or an API later.
# ---------------------------------------------------------------------------
COURSES = ["Composition I", "Intro to Communication", "Public Speaking"]

RESOURCES = [
    {"title": "Choosing a medium for your argument", "format": "Guide", "modality": "Written",
     "course": "Composition I", "summary": "Helps students match a claim and audience to a genre and medium before drafting.",
     "tags": ["argument", "audience", "genre"]},
    {"title": "Podcast episode planning template", "format": "Template", "modality": "Audio",
     "course": "Public Speaking", "summary": "A one-page planner for segment order, scripting, and sound cues.",
     "tags": ["podcast", "scripting", "planning"]},
    {"title": "Infographic design checklist", "format": "Checklist", "modality": "Visual",
     "course": "Intro to Communication", "summary": "Covers hierarchy, color contrast, data labeling, and source notes.",
     "tags": ["infographic", "design", "data"]},
    {"title": "Storyboarding a two-minute video essay", "format": "Guide", "modality": "Video",
     "course": "Composition I", "summary": "Walks through shot lists, voiceover timing, and revision checkpoints.",
     "tags": ["video", "storyboard", "revision"]},
    {"title": "Citing images, audio, and AI tools", "format": "Reference", "modality": "Written",
     "course": "All courses", "summary": "Sample citations and disclosure statements for multimodal work.",
     "tags": ["citation", "AI policy", "attribution"]},
    {"title": "Writing alt text and captions", "format": "Guide", "modality": "Visual",
     "course": "All courses", "summary": "Short practice set for making images and video accessible.",
     "tags": ["accessibility", "alt text", "captions"]},
    {"title": "Interactive timeline starter", "format": "Tool", "modality": "Interactive",
     "course": "Intro to Communication", "summary": "A no-code timeline students can adapt for a research story.",
     "tags": ["timeline", "web", "storytelling"]},
]

EXEMPLARS = [
    {"title": "Campus Food Access: Photo Essay", "modality": "Visual", "course": "Composition I",
     "assignment": "Visual argument", "summary": "Eight images and captions that build one claim about food access.",
     "commentary": "Strong sequencing: each caption adds evidence rather than describing the image."},
    {"title": "Sleep and Study: A Three-Part Podcast", "modality": "Audio", "course": "Intro to Communication",
     "assignment": "Audio narrative", "summary": "Interviews and narration explaining how sleep affects exam performance.",
     "commentary": "Notice how music cues mark transitions and keep the audience oriented."},
    {"title": "Why Libraries Still Matter: Video Essay", "modality": "Video", "course": "Composition I",
     "assignment": "Video essay", "summary": "A two-minute essay combining archival images, voiceover, and on-screen text.",
     "commentary": "The opening thirty seconds state the claim clearly; sources appear on screen."},
    {"title": "Transit Funding Brief with Data Visuals", "modality": "Written", "course": "Intro to Communication",
     "assignment": "Policy brief", "summary": "A two-page brief that pairs short paragraphs with three annotated charts.",
     "commentary": "Charts are introduced in the text before they appear, so readers know what to look for."},
]

LESSON_PLANS = [
    {"title": "From Essay to Podcast: Translating an Argument", "course": "Composition I", "duration": "75 minutes",
     "objectives": ["Identify what changes when an argument moves from page to audio", "Draft a 60-second script from an essay paragraph"],
     "timeline": [("10 min", "Warm-up: listen to a short audio argument"), ("20 min", "Compare print and audio versions of one claim"),
                  ("30 min", "Script a 60-second segment in pairs"), ("15 min", "Read aloud and give peer feedback")],
     "materials": ["Sample audio clip", "Script template", "Peer feedback form"]},
    {"title": "Designing for Audience: Infographic Workshop", "course": "Intro to Communication", "duration": "50 minutes",
     "objectives": ["Choose a visual hierarchy for a specific audience", "Revise a draft using a design checklist"],
     "timeline": [("10 min", "Review two contrasting infographics"), ("25 min", "Sketch and build a draft"), ("15 min", "Gallery walk with checklist")],
     "materials": ["Infographic design checklist", "Sticky notes", "Shared slide template"]},
    {"title": "Responsible AI Use in Multimodal Projects", "course": "All courses", "duration": "50 minutes",
     "objectives": ["Explain the course AI policy in their own words", "Write a disclosure statement for a project"],
     "timeline": [("10 min", "Discuss scenarios: allowed, allowed with disclosure, not allowed"), ("25 min", "Annotate a sample project"), ("15 min", "Draft a disclosure statement")],
     "materials": ["Course AI policy", "Scenario cards"]},
]

LEVELS = ["Exemplary (4)", "Proficient (3)", "Developing (2)", "Beginning (1)"]
RUBRICS = {
    "Podcast episode": {
        "use": "Use for audio projects of three to five minutes.",
        "criteria": [
            ("Purpose and audience", ["Purpose is clear and shapes every segment.", "Purpose is clear in most segments.", "Purpose appears but shifts.", "Purpose is unclear."]),
            ("Script and structure", ["Opening, development, and close are polished.", "Structure is clear with minor lapses.", "Structure is uneven.", "Structure is hard to follow."]),
            ("Audio quality", ["Clean recording; sound choices add meaning.", "Clean recording; some sound choices.", "Noticeable noise or uneven levels.", "Audio interferes with understanding."]),
            ("Sources and attribution", ["All sources and tools are credited.", "Most sources are credited.", "Some credits are missing.", "Sources are not credited."]),
        ],
    },
    "Infographic": {
        "use": "Use for single-page visual arguments.",
        "criteria": [
            ("Claim and evidence", ["Claim is clear; evidence is accurate and relevant.", "Claim is clear; evidence is mostly relevant.", "Claim or evidence is vague.", "No clear claim."]),
            ("Visual hierarchy", ["Eye path is deliberate and easy to follow.", "Hierarchy is mostly clear.", "Hierarchy is inconsistent.", "Layout is cluttered."]),
            ("Accessibility", ["High contrast, alt text, readable type.", "Most accessibility needs met.", "Some needs met.", "Accessibility not addressed."]),
            ("Sources and attribution", ["All sources are credited on the page.", "Most sources are credited.", "Some credits are missing.", "Sources are not credited."]),
        ],
    },
}

# ---------------------------------------------------------------------------
# 4. REUSABLE UI COMPONENTS
# Small helpers so every page draws cards the same way.
# ---------------------------------------------------------------------------
def esc(text):
    """Escape text before placing it inside HTML."""
    return html.escape(str(text))


def render_card(title, body, modality=None, meta=None, tags=None):
    """Draw one content card. The left border color encodes the modality."""
    accent = MODALITY_COLORS.get(modality, "#1F7A8C")
    parts = [f'<div class="card" style="--accent:{accent}">', f'<div class="card-title">{esc(title)}</div>']
    if meta:
        parts.append(f'<div class="meta">{esc(meta)}</div>')
    parts.append(f"<p>{esc(body)}</p>")
    if tags:
        parts.append("".join(f'<span class="pill">{esc(t)}</span>' for t in tags))
    parts.append("</div>")
    st.markdown("".join(parts), unsafe_allow_html=True)


def card_grid(items, render_fn, columns=2):
    """Lay items out in a grid, filling columns left to right."""
    cols = st.columns(columns)
    for i, item in enumerate(items):
        with cols[i % columns]:
            render_fn(item)


def render_resource(r):
    render_card(r["title"], r["summary"], r["modality"], f'{r["format"]} for {r["course"]}', [r["modality"]] + r["tags"])


def render_exemplar(e):
    render_card(e["title"], e["summary"], e["modality"], f'{e["assignment"]} in {e["course"]}', [e["modality"]])
    with st.expander("Instructor commentary"):
        st.write(e["commentary"])


def page_header(title, blurb):
    """Standard page title and one-line description."""
    st.title(title)
    st.write(blurb)


def go_to(page):
    """Button callback: switch the sidebar selection to another page."""
    st.session_state["nav"] = page


# ---------------------------------------------------------------------------
# 5. PAGE FUNCTIONS
# ---------------------------------------------------------------------------
def page_home():
    # Hero banner with a strip counting items in each modality
    counts = {m: sum(x["modality"] == m for x in RESOURCES + EXEMPLARS) for m in MODALITY_COLORS}
    strip = "".join(f'<div style="background:{c}"><b>{counts[m]}</b>{m}</div>' for m, c in MODALITY_COLORS.items())
    st.markdown(
        '<div class="hero"><div class="hero-title">Teach and learn through writing, image, sound, and video.</div>'
        "<p>Find resources, study student work, plan class sessions, and grade with shared rubrics. "
        "The strip below shows how many resources and exemplars the hub holds in each modality.</p>"
        f'<div class="strip">{strip}</div></div>',
        unsafe_allow_html=True,
    )

    # Quick-start cards: each button jumps to a section
    st.subheader("Start here")
    links = [
        ("Search Resources", "Find a resource", "Search guides, templates, and tools by keyword, modality, or course."),
        ("Browse Exemplars", "See student work", "Study sample projects with instructor commentary."),
        ("Lesson Plans", "Plan a session", "Open ready-to-adapt plans with timelines and materials."),
        ("Rubrics", "Choose a rubric", "Compare criteria and performance levels for common projects."),
    ]
    cols = st.columns(2)
    for i, (page, heading, text) in enumerate(links):
        with cols[i % 2]:
            with st.container(border=True):
                st.markdown(f"##### {heading}")
                st.write(text)
                st.button(f"Open {page}", key=f"go_{page}", on_click=go_to, args=(page,))

    # Recently added resources
    st.subheader("Recently added")
    card_grid(RESOURCES[:3], render_resource, columns=3)


def page_search():
    page_header("Search resources", "Find guides, templates, and tools for multimodal projects.")

    # Search bar and filters inside a bordered container
    with st.container(border=True):
        query = st.text_input("Search by keyword", placeholder="Try: podcast, alt text, storyboard")
        c1, c2 = st.columns(2)
        modality = c1.selectbox("Modality", ["All"] + list(MODALITY_COLORS))
        course = c2.selectbox("Course", ["All"] + COURSES)

    # Apply keyword and filter matching (resources marked "All courses" always match a course)
    def matches(r):
        haystack = " ".join([r["title"], r["summary"]] + r["tags"]).lower()
        return (
            query.lower() in haystack
            and (modality == "All" or r["modality"] == modality)
            and (course == "All" or r["course"] in (course, "All courses"))
        )

    results = [r for r in RESOURCES if matches(r)]
    st.caption(f"{len(results)} resources found")
    if results:
        card_grid(results, render_resource)
    else:
        st.info("No resources match. Clear a filter or try a broader keyword.")


def page_exemplars():
    page_header("Browse exemplars", "Sample student projects (placeholders) with notes on what makes them work.")
    with st.container(border=True):
        c1, c2 = st.columns(2)
        modality = c1.selectbox("Modality", ["All"] + list(MODALITY_COLORS), key="ex_mod")
        course = c2.selectbox("Course", ["All"] + COURSES, key="ex_course")
    shown = [e for e in EXEMPLARS if (modality == "All" or e["modality"] == modality) and (course == "All" or e["course"] == course)]
    if shown:
        card_grid(shown, render_exemplar)
    else:
        st.info("No exemplars match these filters yet. Try another modality or course.")


def page_lessons():
    page_header("Lesson plans", "Adaptable plans with objectives, a timeline, and materials.")
    for i, plan in enumerate(LESSON_PLANS):
        # One expandable container per plan; the first starts open
        with st.expander(f'{plan["title"]} ({plan["duration"]})', expanded=(i == 0)):
            st.caption(f'Course: {plan["course"]}')
            left, right = st.columns(2)
            with left:
                st.markdown("**Objectives**")
                for obj in plan["objectives"]:
                    st.markdown(f"- {obj}")
                st.markdown("**Materials**")
                for item in plan["materials"]:
                    st.markdown(f"- {item}")
            with right:
                st.markdown("**Timeline**")
                for minutes, activity in plan["timeline"]:
                    st.markdown(f"- **{minutes}:** {activity}")


def page_rubrics():
    page_header("Rubrics", "Choose a rubric to see its criteria across four performance levels.")
    name = st.selectbox("Project type", list(RUBRICS))
    rubric = RUBRICS[name]

    # Build the criteria-by-level table as HTML so it matches the theme
    head = "<tr><th>Criterion</th>" + "".join(f"<th>{esc(level)}</th>" for level in LEVELS) + "</tr>"
    rows = "".join(
        f'<tr><td class="crit">{esc(crit)}</td>' + "".join(f"<td>{esc(d)}</td>" for d in descs) + "</tr>"
        for crit, descs in rubric["criteria"]
    )
    with st.container(border=True):
        st.markdown(f"##### {name}")
        st.write(rubric["use"])
        st.markdown(f'<div class="table-wrap"><table class="rubric">{head}{rows}</table></div>', unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# 6. ROUTER AND SIDEBAR
# The sidebar radio stores the current page in st.session_state["nav"];
# PAGES maps each label to the function that draws it.
# ---------------------------------------------------------------------------
PAGES = {
    "Home": page_home,
    "Search Resources": page_search,
    "Browse Exemplars": page_exemplars,
    "Lesson Plans": page_lessons,
    "Rubrics": page_rubrics,
}


def main():
    st.markdown(CSS, unsafe_allow_html=True)
    st.session_state.setdefault("nav", "Home")

    with st.sidebar:
        st.markdown(
            '<div class="brand">Multimodal Studio Hub</div>'
            '<div class="tagline">Resources for teaching and learning beyond the written word</div>',
            unsafe_allow_html=True,
        )
        st.radio("Navigate", list(PAGES), key="nav", label_visibility="collapsed")
        st.caption("All content is placeholder data. Replace it in Section 3 of app.py.")

    PAGES[st.session_state["nav"]]()


if __name__ == "__main__":
    main()
