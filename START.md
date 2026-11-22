# Workstation and first connection

Bring working knowledge of SQL, Python and the terminal. The experiments supply the statements. In the demo you will measure how many tablets the FE selects across two identical datasets and test how routing changes for an event_id lookup. Open the repository root in VS Code and run commands there.

## Install and start

Install Docker Desktop or Docker Engine with Compose v2, uv, VS Code with the Python extension, and DataGrip. The first run downloads container images, Python packages and the JDBC driver. As a starting budget allow Docker 4 vCPUs, 8 GB RAM and 12 GB free disk. Increase Docker memory for the Kafka or Iceberg lab if you observe an OOM kill. [Docker](https://docs.docker.com/get-started/get-docker/) · [uv](https://docs.astral.sh/uv/getting-started/installation/) · [VS Code](https://code.visualstudio.com/) · [DataGrip](https://www.jetbrains.com/datagrip/)

```sh
docker compose version
docker info
uv python install 3.14
uv sync --locked
uv run python --version
uv run python lab.py list
uv run python lab.py up 01/01
uv run python lab.py setup 01/01
```

In VS Code run **Python: Select Interpreter** and choose the repository's `.venv`. The lockfile pins the host packages. Each Compose file pins the runtime image. The 4.1.4 image is published for ARM64 (including Apple Silicon) and AMD64. [Image tags](https://hub.docker.com/r/starrocks/allin1-ubuntu/tags) · [uv lock and sync](https://docs.astral.sh/uv/concepts/projects/sync/)

## Connect DataGrip

Choose **File → New → Data Source → MySQL**. Set Host to `127.0.0.1`, Port to `9030`, User to `root`, Password to empty and Database to `course`. Click **Download missing driver files**, then **Test Connection**. Name the connection “StarRocks · local course.” Open its query console and run the statements below. Use `current_version()` to identify the StarRocks binary. [DataGrip driver](https://www.jetbrains.com/help/datagrip/mysql.html) · [current_version](https://docs.starrocks.io/docs/sql-reference/sql-functions/utility-functions/current_version/)

```sql
USE course;
SELECT current_version(), @@run_mode, DATABASE();
SHOW FRONTENDS;
SHOW BACKENDS;
```

Expect a 4.1.4 build, shared_nothing mode, database course and a live backend. Each lab reuses the same host ports. Reconnect the DataGrip console after changing labs.

## Run an experiment

1. Read `weeks/WW/LL/README.md` and write down a prediction before executing the query.
2. Run `up` to start the lesson's Compose project. Run `setup` to recreate the example tables. Run `uv run python lab.py run 01/01` to test three predicates, then `uv run python weeks/01/01/run.py --profile` to profile the two scans.
3. Open `explore.sql`, attach it to the course data source, select a statement and execute it with Cmd+Enter or Ctrl+Enter. To replay the entire walkthrough use `uv run python lab.py explore 01/01`.
4. Save the FE plan, the relevant BE profile counters and an explanation of any discrepancy separately. `uv run python lab.py check 01/01` verifies a specific data invariant. Use the lesson's acceptance criteria to evaluate your remaining evidence and reasoning.
5. Run `uv run python lab.py down 01/01` to remove that project's containers and volumes. Export work you want to keep before tearing down the stand.

## Diagnose a surprising result

| Symptom | Next observation |
|---|---|
| Port in use | Inspect `docker ps`. Stop the previous lab with its own `down` command. Only stop unrelated software after identifying it. |
| DataGrip connects but table creation fails | Inspect `SHOW BACKENDS` and its Alive field. A responsive FE can precede a ready BE. The lab runner waits for both. |
| Table or database missing | Run the selected lesson's setup. Reconnect the DataGrip session and refresh the schema. |
| Container fails to start | Run `uv run python lab.py status 01/01` and `uv run python lab.py logs 01/01`. For an OOM kill raise the Docker memory limit. Run setup after restarting. |
| Contract returns FAIL | Open `check.sql`, run its subqueries and find the first mismatched key. Save a minimal example before resetting the fixture. |
| DDL reports `backends without enough disk space` | Inspect free space in Docker Desktop and `SHOW BACKENDS`. A live BE can decline new tablets when its disk watermark is reached. Increase the Docker disk allocation or reclaim space before repeating setup. |

All sample credentials belong to disposable local services. The passwordless database is exposed only on loopback. Use the repository's synthetic records throughout.
