from neo4j import GraphDatabase
from app.config.config import NEO4J_URI, NEO4J_USER, NEO4J_PASS

def get_driver():
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))
    driver.verify_connectivity()
    return driver
