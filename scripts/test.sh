#!/usr/bin/env bash
set -euo pipefail

tests=$(cd "$(dirname "$0")/../lessons/testing" && pwd)
workdir=$(mktemp -d)
redis_id=
worker_pid=
cleanup() {
  if [[ -n "$worker_pid" ]]; then
    kill "$worker_pid" 2>/dev/null || true
    wait "$worker_pid" || true
  fi
  if [[ -n "$redis_id" ]]; then docker rm -fv "$redis_id" >/dev/null; fi
  rm -rf "$workdir"
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

redis_id=$(docker run -d -p 127.0.0.1::6379 redis:7-alpine)
address=$(docker port "$redis_id" 6379/tcp)
export CELERY_BROKER_URL="redis://$address/0"
export CELERY_RESULT_BACKEND="redis://$address/1"
export PYTHONPATH="$tests${PYTHONPATH:+:$PYTHONPATH}"

cd "$workdir"
python -m celery -A tasks worker --pool=solo --loglevel=INFO &
worker_pid=$!
python -m pytest -q "$tests"
