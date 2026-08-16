"""Dependency-free checks for the static GitHub Pages bundle."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

SITE = Path(__file__).resolve().parents[1] / "src" / "main" / "resources" / "static"
HTML_FILES = (SITE / "index.html", SITE / "404.html")


class AssetParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.assets: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        attribute = "href" if tag in {"a", "link"} else "src" if tag in {"script", "img"} else None
        if attribute and values.get(attribute):
            self.assets.append((tag, values[attribute] or ""))


def local_path(document: Path, reference: str) -> Path | None:
    parsed = urlparse(reference)
    if parsed.scheme or parsed.netloc or reference.startswith(("#", "mailto:", "tel:")):
        return None
    if reference.startswith("/"):
        raise AssertionError(f"GitHub project Pages에서 깨지는 절대 경로: {document.name} -> {reference}")
    return (document.parent / unquote(parsed.path)).resolve()


def main() -> None:
    required = [*HTML_FILES, SITE / "css" / "styles.css", SITE / "js" / "app.js", SITE / ".nojekyll"]
    missing = [str(path.relative_to(SITE)) for path in required if not path.exists()]
    assert not missing, f"필수 파일 누락: {', '.join(missing)}"

    for document in HTML_FILES:
        parser = AssetParser()
        parser.feed(document.read_text(encoding="utf-8"))
        for tag, reference in parser.assets:
            target = local_path(document, reference)
            if target is not None:
                assert target.exists(), f"깨진 {tag} 경로: {document.name} -> {reference}"
                assert SITE in target.parents or target == SITE, f"사이트 폴더 밖 경로: {reference}"

    index = HTML_FILES[0].read_text(encoding="utf-8")
    assert '<html lang="ko">' in index, "한국어 lang 속성이 필요합니다."
    assert "<title>" in index and "KCLI" in index, "KCLI 문서 제목이 필요합니다."
    print(f"OK: {SITE} 정적 사이트와 내부 자산 경로를 검증했습니다.")


if __name__ == "__main__":
    main()
