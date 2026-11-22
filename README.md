# Isaac Ewuoso_ Multimodalstudiohub

The Multimodal Hub Studio is a website and resource hub, featuring a wealth of resources and information for college instructors who wish to design and implement multimodal projects in English communication courses and for students who wish to view model exemplar projects. The website is a "making space"  not a static resource list where users can browse real student work, get teaching materials, and examine multimodal assignment step-by-step, learn more about multimodal projects design, including summative and formative assessment of these projects.


# Multimodal Studio Hub

A Streamlit app that helps college instructors and students find resources,
browse exemplars, plan lessons, and use rubrics for multimodal projects.

**Live app:** https://multimodalsh.streamlit.app

## Features of the current website prototype:
- Search resources by keyword and genre
- Browse student exemplars with instructor commentary
- Lesson plans with objectives, timelines, and materials
- Rubrics for common multimodal projects
- Project space for refining multimodal projects ideas
- Multimoodal Tutor Buddy to assist students in refining multimodal project ideas

## Implementation
- Python & Streamlit: Web interface and application logic.
- Groq API (openai/gpt-oss-20b): LLM-generated feedback for the Multimodal Tutor Buddy.

## Run locally
    pip install -r requirements.txt
    streamlit run main.py

## Project structure
- `main.py`: the Streamlit app
- `docs/`: architecture outline and interface layout

## Status
Presence of a few placeholder contents. Real resources are currently being added.
