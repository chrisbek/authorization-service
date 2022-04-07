#!/bin/bash
set -euo pipefail

arg=$@
re="[\s\S]*(create|migrate|preview)[\s\S]*$"
if [[ $arg =~ $re ]]; then
  usage=${BASH_REMATCH[1]};
else
  echo "Usage: migrations {argument}, where argument={create|migrate|preview}"
  return
fi

if [[ $usage = "create" ]]
then
  echo "================================ Creating migration ================================="
  current_date=`date +"%Y-%m-%d"`
  alembic revision --autogenerate -m $current_date
  echo "====================================================================================="
elif [[ $usage = "migrate" ]]
then
  echo "======================== Executing all migrations until head ========================"
  alembic upgrade head
elif [[ $usage = "preview" ]]
then
  echo "================================= Creating preview =================================="
  generated_revision=$(alembic revision --autogenerate | tail -n1 | cut -d' ' -f4)
  echo "====================================================================================="
  cat "${generated_revision}"
  echo "====================================================================================="
  rm -rf "${generated_revision}"
fi