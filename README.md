# Demo lab · StarRocks 4.1

Two tables hold the same 131,072 events in 16 tablets each. One filter selects a single tablet in the first layout and all 16 in the second. Predict what changes when the caller supplies only an event_id. Test your prediction in the FE plan and inspect what the BE executed.

**Tools:** StarRocks 4.1.4 · Docker Compose · Python 3.14 · uv · VS Code · DataGrip.

[Workstation setup](START.md) · [Demo lesson slides (PDF)](weeks/01/01/slides.pdf)

## Take the demo lab

[Where did 15 of the 16 tablets go?](weeks/01/01/README.md)

After installing the tools, run these commands in the repository root. Open a DataGrip console as described in the setup guide and complete the lab exercises.

```sh
uv sync --locked
uv run python lab.py up 01/01
uv run python lab.py setup 01/01
uv run python lab.py run 01/01
uv run python weeks/01/01/run.py --profile
uv run python lab.py check 01/01
uv run python lab.py down 01/01
```

The twelve-week course continues into Stream Load, Kafka, CBO plans, pipeline profiles, MV refresh, Iceberg scans, workload routing and vector search.
