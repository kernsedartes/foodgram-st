#!/bin/bash
set -e

host="$1"
shift
cmd="$@"

echo "⏳ Waiting for Postgres at $host..."

until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$host" -U "$POSTGRES_USER" -c '\q' >/dev/null 2>&1; do
  echo "Postgres is unavailable - sleeping"
  sleep 1
done

echo "✅ Postgres is up - executing command"
exec $cmd