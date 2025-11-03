# ProfessorAI

ProfessorAI is an intelligent, modular AI assistant designed to provide generate structured learning content.
It integrates `LLMs, Neo4j graph databases, and visualization tools like Manim` to create an interactive learning experience.

## Tech Stack
- Backend: FastAPI
- AI/LLM: DSPy Framework with OpenAI and Qwen models(or compatible LLM)
- Database: Neo4j Graph Database
- Visualization: Manim
- PDF Generation: pdfplumber
- Language: Python 3.9+

## 🚀 Features
- Knowledge Graph Integration (Neo4j) — Connects and manages academic knowledge in graph form for contextual responses.
- LLM-Powered Intelligence — Uses large language models to generate natural explanations and summaries.
- Dynamic Visualization (Manim) — Automatically generates animated explanations and visual content from code.
- PDF Generation — Create and export structured learning materials or lecture summaries.
- Extensible Pipelines — Modular pipelines for syllabus generation, animation, and more.
- REST API Architecture — FastAPI routers for scalable interaction between backend modules.

## Project Structure
```shell
├── app
│   ├── api
│   │   └── routers
│   │       ├── manim.py
│   │       └── syllabus.py
│   ├── config
│   │   ├── config.py
│   │   └── neo4j_config.py
│   ├── main.py
│   ├── models
│   │   ├── manim_models.py
│   │   └── syllabus_models.py
│   ├── pipelines
│   │   ├── manim_pipeline.py
│   │   └── syllabus_pipeline.py
│   ├── services
│   │   ├── graph_service.py
│   │   ├── llm_service.py
│   │   ├── manim_services.py
│   │   └── pdf_service.py
│   └── utils
│       ├── code_parser.py
│       ├── job_status.py
│       ├── json_parser.py
│       └── list_parser.py
├── .gitignore
├── README.md
├── requirements.txt
└── run.py
```

## Folder Overview
- `app/api/routers/`	FastAPI route definitions for syllabus and Manim endpoints
- `app/config/`	Application and Neo4j configuration files
- `app/models/`	Pydantic data models defining request/response schemas
- `app/pipelines/`	Logic pipelines for generating syllabi and animations
- `app/services/`	Core service layer for LLMs, Neo4j, Manim, and PDF generation
- `app/utils/`	Utility functions for parsing, status tracking, and data formatting
- `run.py`	Entry point to launch the FastAPI application
- `requirements.txt`	List of all Python dependencies

## ⚙️ Installation & Setup

- Clone the repository
```shell
git clone https://github.com/dhruvkjain/professorAI.git
cd professorAI
```

- Create and activate a virtual environment (recommended)
```shell
python3 -m venv venv
source venv/bin/activate   # (on Windows: venv\Scripts\activate)
```

- Install dependencies
```shell
pip install -r requirements.txt
```

- Configure environment variables
  Set up your .env file or export environment variables for:
  - LLM API keys (e.g., OpenAI)
  - Neo4j credentials (URI, user, password)


- Run the application
```shell
python run.py
```

Access the API
  Visit:
```shell
http://localhost:8000/docs
```
  to interact with the FastAPI Swagger UI.

## Core Components
1. LLM Service (llm_service.py)
Interfaces with a large language model (e.g., OpenAI GPT) to generate educational text, explanations, and structured outputs.

2. Graph Service (graph_service.py)
Handles Neo4j connections and graph queries to organize and retrieve domain knowledge.

3. Manim Services (manim_services.py, manim_pipeline.py)
Generates dynamic visualizations and educational animations using Manim.

4. PDF Service (pdf_service.py)
Converts structured syllabus or generated content into PDFs for sharing or archiving.

5. Syllabus Pipelines (syllabus_pipeline.py)
Combines LLM output, graph data, and parsing utilities to auto-generate syllabus outlines or study plans.

