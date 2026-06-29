import os
from pathlib import Path
from core.state_store import StateStore
from core.skill_generator import SkillGenerator
from core.conversation_compressor import ConversationCompressor
from core.memory_manager import MemoryManager
from core.self_knowledge import SelfKnowledgeManager
from core.self_healer import SelfHealer

# Resolve root workspace directory
ROOT_DIR = Path(__file__).resolve().parent.parent
DB_DIR = ROOT_DIR / "memory"
DB_PATH = DB_DIR / "state.db"
SKILLS_DIR = ROOT_DIR / ".agents" / "skills"
CORRECTION_JOURNAL_PATH = ROOT_DIR / ".learnings" / "correction_journal.json"

# Global Singletons
state_store = None
skill_generator = None
conversation_compressor = None
memory_manager = None
self_knowledge_manager = None
self_healer = None

def init_brain_transplant(qdrant_url: str = "http://localhost:6333", model_client = None):
    """
    Initializes and wires the entire self-learning brain transplant.
    Creates state database, compiles triggers, and syncs history.
    """
    global state_store, skill_generator, conversation_compressor, memory_manager, self_knowledge_manager, self_healer
    
    print("[BrainInit] Wiring Hermes -> Antigravity Brain Transplant core components...")
    
    # Ensure memory directories exist
    DB_DIR.mkdir(parents=True, exist_ok=True)
    
    # 1. State Store (SQLite DB)
    state_store = StateStore(str(DB_PATH))
    
    # 2. Auto-Skill Generator
    try:
        from core.skill_generator import SkillGenerator
        skill_generator = SkillGenerator(str(SKILLS_DIR))
    except ImportError:
        # Compatibility fallback if import name mismatches
        import sys
        sys.path.append(str(ROOT_DIR))
        from core.skill_generator import SkillGenerator
        skill_generator = SkillGenerator(str(SKILLS_DIR))

    # 3. Conversation Compressor
    conversation_compressor = ConversationCompressor(state_store, model_client=model_client)
    
    # 4. Memory Context Manager
    memory_manager = MemoryManager(state_store, qdrant_url=qdrant_url)
    
    # 5. Self Knowledge Manager & Sync Journal
    self_knowledge_manager = SelfKnowledgeManager(state_store)
    if CORRECTION_JOURNAL_PATH.exists():
        self_knowledge_manager.sync_journal_to_db(str(CORRECTION_JOURNAL_PATH))
        
    # 6. Self Healer
    self_healer = SelfHealer(state_store, conversation_compressor)
    
    print("[BrainInit] Core initialization complete. Active state saved to state.db.")
    
    return {
        "state_store": state_store,
        "skill_generator": skill_generator,
        "conversation_compressor": conversation_compressor,
        "memory_manager": memory_manager,
        "self_knowledge_manager": self_knowledge_manager,
        "self_healer": self_healer
    }
