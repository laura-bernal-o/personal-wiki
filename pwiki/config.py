"""All tunable settings in one place. Paths are relative to the repo root."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# --- Vault (open vault/ in Obsidian) -------------------------------------
VAULT = ROOT / "vault"
RAW_DIR = VAULT / "raw"          # unchanged originals = evidence
WIKI_DIR = VAULT / "wiki"        # generated + reviewed notes
INDEX_MD = VAULT / "index.md"
SOURCES_MD = VAULT / "Sources.md"
WIKI_FOLDERS = ["Courses", "Projects", "Concepts"]

# --- Machine files (outside the vault) -----------------------------------
DATA = ROOT / "data"
SOURCES_JSON = DATA / "sources.json"      # source catalog: id -> original path, hash
NOTE_MAP_JSON = DATA / "note_map.json"    # source id -> note titles it produced
INDEX_DIR = DATA / "index"                # chunks.jsonl + embeddings.npy
PROMPTS = ROOT / "prompts"
EVIDENCE = ROOT / "evidence"
DRAFTS = ROOT / "outputs" / "drafts"
EVALS = ROOT / "evals" / "questions.json"

# --- Model (local Ollama is the only runtime) ----------------------------
OLLAMA_URL = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
CHAT_MODEL = os.environ.get("WIKI_MODEL", "gemma4:e4b")
EMBED_MODEL = os.environ.get("WIKI_EMBED_MODEL", "embeddinggemma")
NUM_CTX = 8192          # context window we ask Ollama to allocate
REQUEST_TIMEOUT = 600   # seconds; first call includes model load

# --- Chunking / retrieval ------------------------------------------------
CHUNK_WORDS = 220       # target passage size
CHUNK_OVERLAP = 40      # words shared between consecutive passages
TOP_K = 8               # passages sent to Gemma in ask mode (~1,800 words)
RRF_K = 60              # reciprocal-rank-fusion constant
EXPAND_TOP = 3          # ask: extend the best 3 passages through the rest of their section
MAX_PER_SOURCE = 3      # at most this many of the top-k passages from one file
# Ask-mode gate: if no passage reaches this cosine similarity AND no BM25 hit
# exists, skip the model and report insufficient evidence directly.
MIN_COSINE = 0.30

# --- Chat ----------------------------------------------------------------
HISTORY_MESSAGES = 12   # rolling window of user/assistant messages kept
