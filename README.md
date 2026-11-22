# Demo lab · StarRocks 4.1

Find the extra $12 in the report. Then investigate two cutoffs that both show $23 while the underlying payments change. Reconcile the event log to an independent statement and prove which rows can be published.

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

The twelve-week course takes you from OLAP architecture, Stream Load, Kafka and Iceberg to a payments mart, late data experiments, a snapshot-to-CDC handoff and a release decision for an analytical AI service.
