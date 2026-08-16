# Pinned upstreams

The fork tracks both upstreams as Git submodules. Their exact commits are recorded in `../upstream-pins.json`.

```sh
git submodule update --init --recursive
git -C AppViewLite checkout --detach 75f78e8e098c05f52821e836832205050c0f539e
git -C social-app checkout --detach 1f5c698165c922e707833809902ee959e9824f00
```

Do not move either submodule to a branch head without updating the pin manifest, reviewing the diff, and rerunning the baseline checks.
