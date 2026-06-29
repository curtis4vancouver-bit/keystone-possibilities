import sqlite3
import os
import time
from neo4j import GraphDatabase

DB_PATH = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Engine\memory\graph_history.db"
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "keystonesovereign"

def main():
    if not os.path.exists(DB_PATH):
        print(f"SQLite DB not found at {DB_PATH}")
        return
        
    print("Connecting to SQLite...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Retrieve all entities
    cursor.execute("SELECT name, type FROM entities")
    entities = cursor.fetchall()
    print(f"Found {len(entities)} entities in SQLite.")
    
    # Retrieve all relationships
    cursor.execute("""
        SELECT e1.name, e1.type, r.relation, e2.name, e2.type
        FROM relationships r
        JOIN entities e1 ON r.source_id = e1.id
        JOIN entities e2 ON r.target_id = e2.id
    """)
    relationships = cursor.fetchall()
    print(f"Found {len(relationships)} relationships in SQLite.")
    conn.close()
    
    # Connect to Neo4j with retry loop (waiting for database startup)
    print("Connecting to Neo4j...")
    driver = None
    max_retries = 10
    for attempt in range(1, max_retries + 1):
        try:
            driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
            # Test query to verify bolt capability
            with driver.session() as session:
                session.run("RETURN 1")
            print("Connected to Neo4j successfully!")
            break
        except Exception as e:
            if attempt == max_retries:
                print(f"Failed to connect to Neo4j after {max_retries} attempts: {e}")
                return
            print(f"Neo4j not ready yet (attempt {attempt}/{max_retries}), retrying in 5s...")
            time.sleep(5)
            
    try:
        with driver.session() as session:
            # Clear existing data in Neo4j
            print("Clearing existing data in Neo4j...")
            session.run("MATCH (n) DETACH DELETE n")
            
            # Import entities
            print("Importing entities...")
            for name, etype in entities:
                session.run(
                    "MERGE (e:Entity {name: $name}) SET e.type = $type",
                    name=name, type=etype
                )
                
            # Import relationships
            print("Importing relationships...")
            for s_name, s_type, relation, t_name, t_type in relationships:
                # Sanitize relation name for Cypher relationship type label
                rel_type = relation.strip().replace(" ", "_").upper()
                if not rel_type:
                    rel_type = "RELATED_TO"
                session.run(f"""
                    MATCH (s:Entity {{name: $s_name}})
                    MATCH (t:Entity {{name: $t_name}})
                    MERGE (s)-[r:{rel_type}]->(t)
                    SET r.relation = $relation
                """, s_name=s_name, t_name=t_name, relation=relation)
                print(f"  [Neo4j Edge]: ({s_name}:{s_type}) -[:{rel_type}]-> ({t_name}:{t_type})")
                
        driver.close()
        print("Migration completed successfully!")
    except Exception as e:
        print(f"Neo4j migration failed: {e}")

if __name__ == "__main__":
    main()
