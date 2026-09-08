#!/bin/zsh
cd "$(dirname "$0")/web" || exit 1
isec_node_bin="$HOME/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin"
if [ -x "$isec_node_bin/node" ]; then export PATH="$isec_node_bin:$PATH"; fi
if ! command -v node >/dev/null; then
  echo 'Install Node.js 24 LTS, then run this launcher again.'
  read -r '?Press Return to close.'
  exit 1
fi
if [ ! -d node_modules ]; then npm install || exit 1; fi
npm run dev
