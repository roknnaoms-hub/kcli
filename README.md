# KCLI 한국사이버리터러시 홈페이지

`cicd 강의`의 Git → CI → CD 흐름, Spring Boot `demo`, 별도 제공된 KCLI 회사소개·로고·IQCS 지정서·ISO 42001 교육자료를 활용해 만든 홈페이지 시안입니다. 운영 기본안은 별도 서버가 필요 없는 **GitHub Pages + GitHub Actions**입니다.

## 빠른 미리보기

```powershell
python -m http.server 8000 --directory src/main/resources/static
```

브라우저에서 `http://localhost:8000`을 엽니다.

## 검증

```powershell
python scripts/validate_site.py
```

검증은 필수 파일, HTML 내부 자산 경로, GitHub 프로젝트 Pages에서 깨질 수 있는 루트 절대 경로를 확인합니다.

## 배포

1. 이 폴더를 GitHub 공개 저장소의 `main` 브랜치에 올립니다.
2. 저장소 `Settings → Pages → Build and deployment → Source`를 `GitHub Actions`로 지정합니다.
3. `main`에 push하면 `.github/workflows/pages.yml`이 검증 후 자동 배포합니다.

상세 비교, 비용, 보안 및 운영 절차는 [docs/CICD-REVIEW.md](docs/CICD-REVIEW.md)를 참고하세요.

## 주요 경로

- `src/main/resources/static/`: 실제 GitHub Pages 배포 대상
- `.github/workflows/pages.yml`: Jenkins 없는 CI/CD 파이프라인
- `scripts/validate_site.py`: 의존성 없는 정적 사이트 검사
- `src/main/java/`: 강의용 Spring Boot 확장 코드이며 Pages에서는 실행하지 않음

> 기관 기본정보와 교육실적은 제공 자료를 기준으로 반영했습니다. 공개 전 IQCS 지정 유효 상태, 개인정보처리방침, 이미지·로고 게시 권한과 최신 연락처를 기관이 최종 확인해야 합니다.
