"""Regression checks for the client-side age-assurance removal.

The ATProto age-assurance lexicons remain available for wire compatibility,
but this fork's client must not prefetch, gate, redirect, or present that
feature. Ordinary birthdate/account metadata is intentionally out of scope.
"""

from collections.abc import Iterator
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLIENT_SRC = ROOT / "upstream" / "social-app" / "src"
BSKYWEB_SERVER = (
    ROOT / "upstream" / "social-app" / "bskyweb" / "cmd" / "bskyweb" / "server.go"
)
BSKYWEB_MAIN = (
    ROOT / "upstream" / "social-app" / "bskyweb" / "cmd" / "bskyweb" / "main.go"
)


def _runtime_sources() -> Iterator[Path]:
    for path in CLIENT_SRC.rglob("*"):
        if path.suffix not in {".ts", ".tsx", ".js", ".jsx"}:
            continue
        relative_parts = path.relative_to(CLIENT_SRC).parts
        if "__tests__" in relative_parts or "__mocks__" in relative_parts:
            continue
        if ".test." in path.name or ".spec." in path.name:
            continue
        if "locale" in relative_parts:
            continue
        # Generated Lexicon TypeScript is protocol compatibility code, not
        # client product wiring. The standard age-assurance definitions stay
        # available for interoperable parsing while no runtime imports them.
        if "lexicons" in relative_parts:
            continue
        yield path


def test_client_age_assurance_feature_directories_are_removed():
    assert not (CLIENT_SRC / "ageAssurance").exists()
    assert not (CLIENT_SRC / "components" / "ageAssurance").exists()


def test_client_runtime_has_no_age_assurance_import_or_gate():
    forbidden = (
        "AgeAssurance",
        "ageAssurance",
        "age-assurance",
        "AgeRestricted",
        "NoAccessScreen",
        "RedirectOverlay",
    )
    offenders: list[str] = []
    for path in _runtime_sources():
        text = path.read_text(encoding="utf-8")
        if any(token in text for token in forbidden):
            offenders.append(str(path.relative_to(ROOT)))

    assert offenders == [], "age-assurance runtime references remain: " + ", ".join(
        offenders
    )


def test_web_shell_does_not_expose_age_geolocation_service():
    server = BSKYWEB_SERVER.read_text(encoding="utf-8")
    main = BSKYWEB_MAIN.read_text(encoding="utf-8")
    assert 'e.GET("/ipcc"' not in server
    assert "WebIpCC" not in server
    assert 'Name:    "ipcc-host"' not in main
