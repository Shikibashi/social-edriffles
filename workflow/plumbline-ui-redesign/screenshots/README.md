# Screenshot evidence

Screenshots in this directory are generated evidence, not design specifications.

## Baseline

- `current-live-desktop.png`: captured from the live `plumblines.uk` page on 2026-09-02 using the Codex in-app browser.
- `current-live-mobile.png`: attempted narrow capture from the same connector. The connector's viewport override did not change the actual runtime viewport, so this file is not proof of a 390x844 render.

The baseline must be retained for comparison. Future captures should record URL, revision, date/time, actual `innerWidth`/`innerHeight`, device pixel ratio, color mode, and authentication state in the corresponding iteration critique.

## Required target captures

The implementation phase must obtain actual renders at approximately:

- 1440x900;
- 1280x720;
- 1024x768;
- 390x844;
- dark mode;
- grayscale.

If the browser connector cannot honor a viewport request, use a supported browser/runtime or a local screenshot harness and record the limitation rather than relabeling a desktop capture as mobile.
