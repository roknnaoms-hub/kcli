# 한국사이버리터러시저널 KCLI

GitHub Pages 배포용 정적 사이트입니다.

- 배포 저장소: `roknnaoms-hub/kcli`
- 배포 URL: `https://roknnaoms-hub.github.io/kcli/`
- 기사 URL 목록: `data/article-urls.md`
- 기사 데이터 원문: `data/daily-articles.json`

## 업데이트 방법

1. `data/article-urls.md`에 기사 URL을 한 줄에 하나씩 수정합니다.
2. 변경 파일을 `main` 브랜치에 커밋/푸시합니다.
3. `.github/workflows/daily-articles.yml`이 URL 목록 기준으로 `index.html`과 `data/daily-articles.json`을 자동 갱신합니다.
4. `.github/workflows/pages.yml`이 GitHub Pages로 자동 배포합니다.

GitHub Pages 설정은 Repository Settings > Pages에서 Source를 `GitHub Actions`로 지정합니다.

저장소가 공개 상태이고 Pages 설정이 완료되면 `https://roknnaoms-hub.github.io/kcli/`에서 확인할 수 있습니다.
