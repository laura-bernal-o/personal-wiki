#!/bin/zsh
# Offline demonstration. Turn Wi-Fi OFF first, then run:
#   script -q evidence/offline/terminal-recording.txt zsh scripts/offline_demo.sh
# Everything below talks only to Ollama on 127.0.0.1.
set -u
cd "$(dirname "$0")/.."
WIKI=.venv/bin/wiki
OUT=evidence/offline
mkdir -p $OUT/ask

step() { print -r -- $'\n\e[36m$ '"${(q-)@}"$'\e[0m'; "$@"; }
wait_note() { print -r -- $'\e[33m⏳ '"$1"$'\e[0m'; }

print "=== OFFLINE DEMO $(date '+%Y-%m-%d %H:%M:%S') ==="
print -r -- "--- proof of no internet ---"
step networksetup -getairportpower en0
step curl -sS -m 5 -o /dev/null -w "%{http_code}\n" https://www.google.com || print "(curl failed: internet unreachable ✔)"
step ping -c 1 -t 2 1.1.1.1 || print "(ping failed: internet unreachable ✔)"

print -r -- $'\n'"--- device + runtime ---"
step sysctl -n machdep.cpu.brand_string
step ollama --version
step ollama list

print -r -- $'\n'"--- restart the CLI + local model ---"
step ollama stop gemma4:e4b
step $WIKI --help

print -r -- $'\n'"--- ingest a new local source (held back until now) ---"
wait_note "Gemma is reading the new document and writing wiki pages. This prints NOTHING for 4-6 minutes. Do not type anything, just wait."
step /usr/bin/time -l $WIKI ingest "staging/Class 5 - Personal Wiki Brief.md"
step $WIKI ingest vault/raw          # second run: every source unchanged -> no duplicates
step $WIKI check
step ollama ps

print -r -- $'\n'"--- search mode (no model answer) ---"
step $WIKI search "learning rate" --scope raw -k 3 --save $OUT/search-learning-rate.md

print -r -- $'\n'"--- the four ask-mode tests ---"
wait_note "Running the 4 test questions: about 1 minute each, with pauses. Do not type anything."
step $WIKI eval --out $OUT/ask

print -r -- $'\n'"--- ask ignores chat: claim only made in chat ---"
step $WIKI ask "What was my favorite ghost in the Pac-Man project?" --save $OUT/ask-chat-claim.md

print -r -- $'\n'"--- chat mode checks ---"
wait_note "Chat checks: 5 messages to Wren plus 1 ask, about 5 minutes. Do not type anything."
step .venv/bin/python scripts/mode_checks.py --out $OUT/mode-checks.md

print -r -- $'\n'"=== END OFFLINE DEMO $(date '+%H:%M:%S') ==="
