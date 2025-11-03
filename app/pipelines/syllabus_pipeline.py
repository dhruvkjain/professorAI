from datetime import datetime
import json, os, dspy
from app.config.config import DEEP_INFRA_API_KEY, DEEP_INFRA_API_URL
from app.services.pdf_service import extract_syllabus_text
from app.services.llm_service import SyllabusExtractor, ChapterDependencyFinder, QAGenerator, ScriptGenerator
from app.services.graph_service import push_syllabus_to_neo4j, visualize_syllabus_graph
from app.config.neo4j_config import get_driver
from app.models.syllabus_models import SyllabusItem

def process_syllabus_pipeline(subject: str, pdf_filepath: str):
    # configuration of qwen in dspy
    qwen_lm = dspy.LM(
        model="Qwen/Qwen3-32B",
        api_key=DEEP_INFRA_API_KEY,
        base_url=DEEP_INFRA_API_URL,
    )
    dspy.configure(lm=qwen_lm)

    print(f"[Pipeline] Running syllabus pipeline for {subject}...")

    with dspy.context(lm=qwen_lm):
        # syllabus extraction
        text = extract_syllabus_text(pdf_filepath)
        extractor = SyllabusExtractor()
        syllabus_items: list[SyllabusItem] = extractor(text)
        # print(syllabus_items[:2])

        # dependencies
        dep_finder = ChapterDependencyFinder()
        chapters = [i.chapter for i in syllabus_items]
        for item in syllabus_items:
            item.dependencies = dep_finder(item.chapter, chapters)
        # print(syllabus_items[:2])

        # QA
        qa_generator = QAGenerator()
        for item in syllabus_items:
            item.qa = qa_generator(item)
        # print(syllabus_items[:2])

        # video scripts
        script_generator = ScriptGenerator()
        for item in syllabus_items:
            item.animation = script_generator(subject, item)
        # print(syllabus_items[:2])

    # convert to JSON for both file storage and neo4j
    json_syllabus = [i.model_dump() for i in syllabus_items]
    
    # save syllabus JSON
    os.makedirs("test_doc", exist_ok=True)
    syllabus_file = f"./test_doc/syllabus_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(syllabus_file, "w", encoding="utf-8") as f:
        json.dump(json_syllabus, f, ensure_ascii=False, indent=4)

    # neo4j visualization
    try:
        driver = get_driver()
        push_syllabus_to_neo4j(driver, json_syllabus)
        visualize_syllabus_graph(driver)
        driver.close()
        print("[Pipeline] Neo4j graph updated and visualized")
    except Exception as e:
        print(f"[Pipeline] Neo4j step failed: {e}")

    print(f"Pipeline complete. Syllabus saved at {syllabus_file}")
    return {"file": syllabus_file, "data": json_syllabus}
