# Week 1 · How StarRocks executes a query

Two tables hold the same 131,072 events in 16 tablets each. One filter selects a single tablet in the first layout and all 16 in the second. Predict what changes when the caller supplies only an event_id. Test your prediction in the FE plan and inspect what the BE executed.

- [01 · Where did 15 of the 16 tablets go?](01/README.md) · [Lesson slides (PDF)](01/slides.pdf)
