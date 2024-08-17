# llmRpg

RPG on the web using LLM for dialog and quests.

<code>export $(grep -v '^#' .env | xargs)</code>
<code>mysqldump --host $DB_HOST --port $DB_PORT --result-file=./backups/llmrpg-db-$(date +%Y-%m-%d).sql $DB_SCHEMA_NAME</code> (uses ~/.my.cnf)
