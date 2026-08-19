# Pinned upstreams

The fork tracks the client and first-party PDS as Git submodules. Their exact
commits are recorded in `../upstream-pins.json`.

```sh
git submodule update --init --recursive
git -C social-app checkout --detach 1f5c698165c922e707833809902ee959e9824f00
git -C atproto-pds checkout --detach 760fb12a080c87cdfd0dae42ae833bad8bc20886
```

Do not move either submodule to a branch head without updating the pin manifest, reviewing the diff, and rerunning the baseline checks. Retired AppViewLite/FishyFlip checkouts are not submodules and must not be reintroduced as runtime dependencies without a new approved architecture review.
