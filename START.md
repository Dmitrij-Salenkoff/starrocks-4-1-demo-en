# Workstation setup and first run

Install Docker with Compose v2.20.0 or newer, VS Code with the Python extension, DataGrip, and uv. Check `docker compose version`, `docker info`, and `uv --version`. As a laptop starting point, allocate 6–8 GB to Docker for the base lab and more for Iceberg or local inference. First use downloads images. Run one lesson at a time because the labs share host ports.

1. Open the repository root in VS Code. Run the commands below. Use **Python: Select Interpreter** and choose Python 3.14 from the project’s `.venv` (on Windows, `.venv/Scripts/python.exe`).
2. In DataGrip select **File → New → Data Source → MySQL**. Use `127.0.0.1`, port `9030`, user `root`, and an empty password for this local instance. Download the driver when prompted and choose **Test Connection**. Select the `sr01` database after setup. The native StarRocks JDBC driver is another supported option.
3. Keep your work in a separate file. Run a selection in a DataGrip query console. Inspect `SELECT current_version();` and `SHOW BACKENDS;`. Expect version 4.1.4 and an alive backend. One frontend and one backend share a container. Tables therefore use replication_num=1. Each operations exercise explains which failure can be demonstrated at this scale.

```sh
uv python install 3.14
uv sync --locked
cd lessons/01
docker compose up -d --wait
uv run --project ../.. python ../../tools/lab.py setup
```

Follow the tasks in the lesson README and implement your answer in DataGrip. Check it before opening the reference. The second command below applies the supplied solution.

```sh
uv run --project ../.. python ../../tools/lab.py check
uv run --project ../.. python ../../tools/lab.py solve
uv run --project ../.. python ../../tools/lab.py check
```

Use `docker compose stop` for a break and `docker compose start` to continue. Stop the previous lab before entering the next directory to free port 9030. The StarRocks data lives inside this container. `docker compose down` removes it and its lesson database. Run up and setup to start again. To remove extra named volumes for this lab too, use `docker compose down -v`. Setup rebuilds exercise objects. All labs use synthetic data on the local machine.

**Troubleshooting.** For a port conflict, inspect `docker ps` and stop the previous lesson. For an unhealthy container inspect `docker compose logs --tail=120 starrocks`, available Docker memory and image pull status. If DataGrip shows no tables after setup, select the schema under Data Source and synchronize. When SQL connects but table creation fails, check the BE Alive flag. FE’s HTTP endpoint is on 8030 and the SQL protocol on 9030.

[StarRocks Docker guide](https://docs.starrocks.io/docs/quick_start/shared-nothing/) · [4.1 release notes](https://docs.starrocks.io/docs/release_notes/release-4.1/) · [DataGrip](https://docs.starrocks.io/docs/integrations/IDE_integrations/DataGrip/) · [uv and Python](https://docs.astral.sh/uv/guides/install-python/)
