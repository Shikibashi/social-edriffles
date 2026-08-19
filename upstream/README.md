# Pinned upstreams

The fork tracks the client and first-party PDS as Git submodules. Their upstream
provenance commits and reviewed local feature checkout commits are recorded in
`../upstream-pins.json`.

```sh
git submodule update --init --recursive
git -C social-app checkout --detach e1a5455eefe7357f73e98ea95874e4a4fed4bf4b
git -C atproto-pds checkout --detach 39612da7bdeac12e9abed1762e9844c85e61d70d
```

Do not move either submodule to a branch head without updating the pin manifest, reviewing the diff, and rerunning the baseline checks. Retired AppViewLite/FishyFlip checkouts are not submodules and must not be reintroduced as runtime dependencies without a new approved architecture review.
