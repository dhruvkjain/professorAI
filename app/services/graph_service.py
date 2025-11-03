import json
from pyvis.network import Network


def push_syllabus_to_neo4j(driver, syllabus_data):
    with driver.session() as session:
        
        # create constraints (only once, if not exist)
        session.run("""
            CREATE CONSTRAINT unit_unique IF NOT EXISTS
            FOR (u:Unit) REQUIRE u.title IS UNIQUE;
        """)
        session.run("""
            CREATE CONSTRAINT chapter_unique IF NOT EXISTS
            FOR (c:Chapter) REQUIRE c.title IS UNIQUE;
        """)

        for entry in syllabus_data:
            unit_title = entry["unit_title"]
            unit_number = entry["unit_number"]
            chapter_title = entry["chapter"]
            content = entry.get("content", [])
            competencies = entry.get("competencies", [])
            explanation = entry.get("explanation", "")
            dependencies = entry.get("dependencies", [])
            qa_data = entry.get("qa")
            animation_data = entry.get("animation")

            # convert complex fields to JSON strings
            qa_data = json.dumps(qa_data, ensure_ascii=False) if qa_data else None
            animation_data = json.dumps(animation_data, ensure_ascii=False) if animation_data else None

            # create / merge Unit
            session.run("""
                MERGE (u:Unit {title: $unit_title})
                SET u.number = $unit_number
            """, unit_title=unit_title, unit_number=unit_number)

            # create / merge Chapter
            session.run("""
                MERGE (c:Chapter {title: $chapter_title})
                SET c.content = $content,
                    c.competencies = $competencies,
                    c.explanation = $explanation,
                    c.qa_pairs = $qa_pairs,
                    c.animation_script = $animation_script
            """, chapter_title=chapter_title,
               content=content,
               competencies=competencies,
               explanation=explanation,
               qa_pairs=qa_data,
               animation_script=animation_data)

            # Unit–Chapter relationship
            session.run("""
                MATCH (u:Unit {title: $unit_title}), (c:Chapter {title: $chapter_title})
                MERGE (u)-[:HAS_CHAPTER]->(c)
            """, unit_title=unit_title, chapter_title=chapter_title)

            # Chapter dependencies relationship
            for dep in dependencies:
                session.run("""
                    MATCH (src:Chapter {title: $chapter_title})
                    MATCH (dep:Chapter {title: $dep_title})
                    WHERE src.title <> dep.title
                    MERGE (src)-[:DEPENDS_ON]->(dep)
                """, chapter_title=chapter_title, dep_title=dep)



def visualize_syllabus_graph(driver, output_file="syllabus_graph.html"):
    net = Network(height="750px", width="100%", directed=True)

    with driver.session() as session:
        result = session.run("""
            MATCH (u:Unit)-[:HAS_CHAPTER]->(c:Chapter)
            OPTIONAL MATCH (c)-[:DEPENDS_ON]->(dep:Chapter)
            RETURN u, c, dep
        """)

        for record in result:
            u = record["u"]
            c = record["c"]
            dep = record["dep"]

            net.add_node(u["title"], label=f"Unit: {u['title']}", color="#87CEEB")
            net.add_node(c["title"], label=f"Chapter: {c['title']}", color="#FFD700")
            net.add_edge(u["title"], c["title"], color="#4682B4", title="HAS_CHAPTER")

            if dep:
                net.add_node(dep["title"], label=f"Chapter: {dep['title']}", color="#FFD700")
                net.add_edge(c["title"], dep["title"], color="#FF6347", title="DEPENDS_ON")

    net.show(output_file)
