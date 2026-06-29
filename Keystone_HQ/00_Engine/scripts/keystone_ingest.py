#!/usr/bin/env python3
"""
Keystone Database Automation, Ingestion, and Antigravity Boot-Sync System.
Designed for local execution alongside Spark SQL pipelines and anyquery environments.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Any, List

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("[Pipeline Error] The 'google-genai' package is missing. Please run 'pip install google-genai'.")
    sys.exit(1)


class LocalKeystoneEngine:
    def __init__(self, db_path: str):
        self.db_path = Path(db_path)
        self.in_memory_registry = {}
        if not self.db_path.exists() and self.db_path.suffix == ".keystone":
            self.db_path.touch()
            print(f" Initialized new database file at: {self.db_path}")

    def put_item(self, partition_key: str, sort_key: str, payload: Dict[str, Any], vector: List[float]) -> bool:
        record_id = f"{partition_key}#{sort_key}"
        self.in_memory_registry[record_id] = {
            "pk": partition_key,
            "sk": sort_key,
            "payload": payload,
            "vector": vector
        }
        return True

    def scan_all_records(self) -> List[Dict[str, Any]]:
        return list(self.in_memory_registry.values())


def generate_semantic_vector(text_block: str) -> List[float]:
    if not text_block.strip():
        return [0.0] * 768

    try:
        client = genai.Client()
        response = client.models.embed_content(
            model="text-embedding-004",
            contents=text_block
        )
        return response.embeddings.values
    except Exception as exc:
        print(f" Embedded computation failed: {exc}. Utilizing a standard zero-vector.")
        return [0.0] * 768


def parse_spark_jsonl_export(file_path: Path, db: LocalKeystoneEngine) -> List[Dict[str, Any]]:
    ingested_records = []
    if not file_path.exists():
        raise FileNotFoundError(f"Spark export file not found at: {file_path}")

    # Load Lexicon dictionary for automated text normalization
    lexicon = {}
    lexicon_path = Path(r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\Audiobook\04_Companion_Docs\lexicon.json")
    if lexicon_path.exists():
        try:
            with open(lexicon_path, "r", encoding="utf-8") as lex_f:
                lexicon = json.load(lex_f)
            print(f"[Normalization Hook] Loaded {len(lexicon)} terms from lexicon.json.")
        except Exception as lex_ex:
            print(f"[Normalization Hook Warning] Failed to read lexicon.json: {lex_ex}")

    with open(file_path, "r", encoding="utf-8") as file:
        for idx, line in enumerate(file, 1):
            line_content = line.strip()
            if not line_content:
                continue

            try:
                raw_object = json.loads(line_content)
                
                message_id = raw_object.get("id") or f"spark_msg_{idx}"
                thread_id = raw_object.get("threadId") or "thread_root"
                sender = raw_object.get("from") or "anonymous@domain.com"
                subject = raw_object.get("subject") or "No Subject"
                body_text = raw_object.get("body") or raw_object.get("snippet") or ""
                date_stamp = raw_object.get("date") or "0"

                # Apply Lexicon Spelling Normalization Hook automatically
                normalized_body = body_text
                for key, val in lexicon.items():
                    normalized_body = normalized_body.replace(key, val)

                vector_embedding = generate_semantic_vector(normalized_body)

                payload_data = {
                    "SenderAddress": sender,
                    "SubjectLine": subject,
                    "SanitizedBody": normalized_body,
                    "UnixEpoch": date_stamp
                }

                db.put_item(
                    partition_key=f"EMAIL#{message_id}",
                    sort_key=f"THREAD#{thread_id}",
                    payload=payload_data,
                    vector=vector_embedding
                )

                ingested_records.append({
                    "id": message_id,
                    "thread_id": thread_id,
                    "sender": sender,
                    "subject": subject,
                    "body": normalized_body,
                    "timestamp": date_stamp
                })

            except json.JSONDecodeError as decode_error:
                print(f"[Line {idx}] Skipping malformed JSON line: {decode_error}")
                continue

    return ingested_records


def generate_agent_boot_assets(records: List[Dict[str, Any]], target_workspace: Path):
    rules_directory = target_workspace / ".agents" / "rules"
    rules_directory.mkdir(parents=True, exist_ok=True)
    
    memory_file = rules_directory / "project-context.md"
    markdown_buffer = []

    for item in records:
        markdown_buffer.append(f"### Record Identification: {item['id']}")
        markdown_buffer.append(f"- **Origin Entity:** {item['sender']}")
        markdown_buffer.append(f"- **Header:** {item['subject']}")
        markdown_buffer.append(f"- **Epoch Time:** {item['timestamp']}")
        markdown_buffer.append(f"- **Text Body:**\n  {item['body']}\n")
        markdown_buffer.append("---\n")

    with open(memory_file, "w", encoding="utf-8") as mem_out:
        mem_out.write("\n".join(markdown_buffer))

    config_dir = Path(os.path.expanduser("~/.config/antigravity"))
    config_dir.mkdir(parents=True, exist_ok=True)
    toml_config_path = config_dir / "config.toml"

    base_toml_payload = (
        '# Antigravity CLI Custom Configuration\n'
        'model = "antigravity-preview-05-2026"\n'
        'name = "The Hand"\n\n'
        '[boot]\n'
        'sync_mode = "filesystem-native"\n'
        'rules_path = ".agents/rules/project-context.md"\n'
        'validate_toml_drift = false\n'
    )
    
    with open(toml_config_path, "w", encoding="utf-8") as toml_out:
        toml_out.write(base_toml_payload)

    agents_instruction_path = target_workspace / "AGENTS.md"
    agents_content = (
        "# Persona Assignment: The Hand\n\n"
        "## Core Supervisor Instructions\n"
        "You are 'The Hand', a specialized managed cognitive agent.\n"
        "Upon boot, do not attempt to establish remote network handshakes or scan raw databases.\n"
        "Instead, instantly read '.agents/rules/project-context.md' and load the cached email memory.\n\n"
        "## CRITICAL SOVEREIGN BOOTSTRAP RULE\n"
        "Upon initialization, you MUST immediately read the Master Blackboard file at:\n"
        "c:/Users/Curtis/New folder/construction-website/Keystone_HQ/00_Master_Brain/Master_Docs/STATE_OF_THE_EMPIRE.md\n"
        "to synchronize with our current brand identity, active task lists, and exact project state before taking any actions.\n"
    )
    with open(agents_instruction_path, "w", encoding="utf-8") as agents_out:
        agents_out.write(agents_content)

    print(f" Local files, TOML settings, and AGENTS.md written to: {target_workspace}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Synchronize Spark JSON Lines with local Keystone Vector DB.")
    parser.add_argument("--spark-source", required=True, help="Path to Spark's exported newline-delimited JSON Lines.")
    parser.add_argument("--database", default="mydb.keystone", help="Target Keystone database file path.")
    parser.add_argument("--workspace", default=".", help="Root directory of the Antigravity workspace.")

    parsed_args = parser.parse_args()
    
    local_db = LocalKeystoneEngine(parsed_args.database)
    workspace_root = Path(parsed_args.workspace)

    try:
        print("[Pipeline] Executing database ingestion...")
        data_records = parse_spark_jsonl_export(Path(parsed_args.spark_source), local_db)
        
        print("[Pipeline] Writing boot assets and initializing configuration structures...")
        generate_agent_boot_assets(data_records, workspace_root)
        
        print("[Pipeline] Pipeline execution finished with zero errors.")
    except Exception as error_exception:
        print(f"[Critical Failure] Automation pipeline aborted: {error_exception}")
        sys.exit(1)
