# Workstation setup for the first lab

Open the [lesson guide](weeks/01/01/README.md) or the [slides](weeks/01/01/slides.pdf) for the first part. When you reach the query trace, use this page to start StarRocks 4.1.4 on your laptop and connect from DataGrip.

## 1. Open the materials

On GitHub choose **Code → Download ZIP** and extract the archive. In VS Code select **File → Open Folder**. Pick the folder containing the file `lab.py` and the directory `weeks`. Run all the commands below from this folder. [Download VS Code](https://code.visualstudio.com/)

## 2. Install the tools

- **Docker with Docker Compose** starts a ready-to-use copy of the database. On macOS and Windows, install Docker Desktop, launch it and wait until it is ready. On Linux you can use Docker Engine with the Compose plugin. [Install Docker](https://docs.docker.com/get-started/get-docker/)
- **uv** installs Python and the packages that run the lesson. [Install uv](https://docs.astral.sh/uv/getting-started/installation/)
- **DataGrip** is the application you will use to view the data and ask questions. Install it and open a project. [Download DataGrip](https://www.jetbrains.com/datagrip/download/)

The first download needs an internet connection. In VS Code choose **Terminal → New Terminal**. A terminal is a window where you can paste commands. Run these one at a time, waiting for the prompt to return after each one.

```sh
docker compose version
uv python install 3.14
uv sync --locked
uv run python lab.py up 01/01
uv run python lab.py setup 01/01
```

The first command checks Docker Compose. The next two install Python 3.14 and the course packages. The `up` command starts the database. Its first download may take a few minutes. The `setup` command fills it with café receipts.

## 3. Connect DataGrip to your database

In **Database Explorer** choose **+ → Data Source → MySQL**. StarRocks understands this connection method. Enter the following settings.

| DataGrip field | Enter |
|---|---|
| Host | `127.0.0.1` means your own computer |
| Port | `9030` |
| User | `root` |
| Password | Leave empty |
| Database | `course` |

If offered, click **Download missing driver files**. Click **Test Connection**, then **OK**. Return to the [lab](weeks/01/01/README.md). Open [architecture.sql](weeks/01/01/architecture.sql) to inspect the version, mode and nodes. In [plan.sql](weeks/01/01/plan.sql), run the statements individually to compare the plan, the sum and the execution profile. [DataGrip connection settings](https://www.jetbrains.com/help/datagrip/mysql.html)

## If something stops you

| What you see | What to do |
|---|---|
| Terminal cannot find `uv` or `docker` | Install the missing tool, close the terminal and open it again. |
| Docker cannot connect | Start Docker, wait until it is ready, then rerun `up`. |
| DataGrip reports “Connection refused” | Wait for `up` to finish. Check the host and port. |
| You cannot see `cafe_sales` | Run `uv run python lab.py setup 01/01`, select database `course` and refresh the list of tables. |
| The day already shows 8 cups | You have already added the extra receipt. Run `setup 01/01` again to restore the example with 6 cups. |

At the end, `uv run python lab.py down 01/01` stops the lab database and removes this lab’s data. Keep any notes you want to save separately.
