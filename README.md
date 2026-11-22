# Demo lab · StarRocks 4.1

One purchase was delivered twice. Why did the report rise from $33 to $45, and which row proves it? Reconstruct the incident in a real StarRocks database and test your hypothesis.

**Tools:** StarRocks 4.1.4 · Docker Compose · Python 3.14 · uv · VS Code · DataGrip.

[Workstation setup](START.md) · [Demo lesson slides (PDF)](weeks/01/01/slides.pdf)

## Take the demo lab

[Why does the report show $45 instead of $33?](weeks/01/01/README.md)

After installing the tools, run these commands in the repository root. Open a DataGrip console as described in the setup guide and complete the lab exercises.

```sh
uv sync --locked
uv run python lab.py up 01/01
uv run python lab.py setup 01/01
uv run python lab.py explore 01/01
uv run python lab.py check 01/01
```

The ten-week syllabus covers OLAP architecture, table models, Stream Load and Kafka, CDC and backfills, analytical SQL, query profiles and materialized views, Iceberg, operations, AI and a capstone.
