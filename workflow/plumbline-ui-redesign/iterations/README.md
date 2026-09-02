# Iteration evidence

Each implementation iteration gets its own directory, for example:

```text
iterations/01-ledger-slice/
  desktop-wide.png
  desktop-standard.png
  narrow.png
  dark.png
  grayscale.png
  critique.md
```

`critique.md` must record:

- what improved;
- what regressed;
- what still looks generic;
- what still wastes space;
- what violates the H1–H8 hypotheses or `docs/design/PLUMBLINE_DESIGN.md`;
- what changed in the next iteration;
- actual viewport and browser/auth state;
- whether the adversarial “Bluesky with an editorial/retro stylesheet” test passed.

Do not mark an iteration complete from typecheck/build alone.
