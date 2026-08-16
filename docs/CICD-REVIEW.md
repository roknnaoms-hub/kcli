# KCLI 홈페이지 CI/CD 검토 및 권고안

## 1. 결론

현재 범위가 기관 소개, 교육 안내, 연구·콘텐츠 소개인 **정보 제공형 홈페이지**이므로 `GitHub Pages + GitHub Actions`가 최적입니다.

- AWS EC2, RDS, Docker, Jenkins 서버가 필요 없습니다.
- 공개 저장소를 사용하면 GitHub Free에서 Pages를 운영할 수 있습니다.
- `main` push만으로 검사와 배포가 끝납니다.
- 별도 서버 패치, SSH 키, 방화벽, DB 백업을 관리하지 않습니다.
- 기본 `github.io` 주소와 HTTPS를 제공하며, 보유한 도메인도 연결할 수 있습니다.

Spring Boot/JPA 코드는 강의 학습 및 향후 동적 기능 확장용으로 보존하되, 현재 Pages 운영에는 포함하지 않습니다.

## 2. 강의안 대비 변경점

강의안의 목표인 `git push → 자동 검증 → 자동 배포`는 그대로 유지합니다. 실행 주체만 단순화합니다.

| 구간 | 강의안 | 최종 권고안 |
|---|---|---|
| 소스 관리 | GitHub | GitHub |
| CI 실행 | Jenkins EC2 | GitHub-hosted Actions runner |
| 빌드/검사 | Maven, Jenkins Pipeline | 정적 자산 경로 검사 |
| 배포 산출물 | JAR + Docker image | HTML + CSS + JavaScript |
| 운영 위치 | AWS EC2 | GitHub Pages |
| 데이터베이스 | AWS RDS MySQL | 사용하지 않음 |
| 운영 인증 | Jenkins SSH 개인 키 | GitHub 기본 `GITHUB_TOKEN`과 Pages OIDC |
| 서버 관리 | Jenkins/EC2/Docker 패치 필요 | 없음 |

강의안도 CI/CD의 본질은 Jenkins가 아니라 “작게, 자주, 자동으로 검증하고 배포하는 구조”라고 설명합니다. 이번 구성은 그 원칙에 맞습니다.

## 3. 대안 비교

| 방안 | 예상 고정비 | 동적 기능 | 운영 난이도 | 보안 부담 | 적합도 |
|---|---:|---|---|---|---|
| GitHub Pages, branch 직접 배포 | 거의 0원 | 불가 | 매우 낮음 | 낮음 | 보통 |
| **GitHub Actions → GitHub Pages** | **거의 0원** | **불가** | **낮음** | **낮음** | **최적** |
| GitHub Actions → AWS EC2/RDS | EC2·RDS·트래픽 비용 | 가능 | 중간 | IAM·서버·DB 관리 | 동적 기능 필요 시 |
| Jenkins → AWS EC2/RDS | Jenkins용 EC2까지 추가 | 가능 | 높음 | Jenkins·SSH·플러그인 관리 | 교육 외 비권장 |

branch 직접 배포보다 Actions 방식을 권장하는 이유는 PR과 push마다 동일한 검사를 수행하고, 성공한 산출물만 배포하며, 배포 이력이 GitHub Environments에 남기 때문입니다.

## 4. GitHub Pages 사용 시 알아야 할 점

### 적합한 기능

- 기관 소개, 사업·교육과정 안내
- 공지·자료·보고서 링크
- 정적 검색 또는 외부 콘텐츠 연결
- 보유 도메인 연결 및 HTTPS

### 제공하지 않는 기능

- Java/Spring Boot, PHP, Node.js 같은 서버 실행
- MySQL 등 데이터베이스 직접 연결
- 회원가입, 관리자 로그인, 결제
- 비밀번호·민감정보를 받는 폼

교육 신청이 필요하면 초기에는 검증된 외부 폼을 링크하고, 개인정보 처리방침과 수집 동의를 별도로 마련하는 방법이 경제적입니다. 신청·회원·결제·관리자 기능이 실제 요구사항으로 확정된 뒤에만 별도 백엔드를 도입하는 것이 좋습니다.

### 공식 한도 요약

- 공개 저장소의 GitHub Pages는 GitHub Free에서 사용 가능
- 게시 사이트 및 소스 저장소 권장 크기 1GB
- 월 소프트 대역폭 한도 100GB
- 배포 작업 제한 시간 10분
- Pages 사이트는 저장소가 비공개여도 인터넷에 공개될 수 있으므로 민감정보 저장 금지
- 전자상거래나 SaaS를 위한 무료 호스팅 용도로는 사용할 수 없음

KCLI와 같은 비거래성 기관 안내 사이트는 기술적으로 잘 맞지만, 향후 결제·민감 거래 기능을 붙일 때는 다른 호스팅으로 분리해야 합니다.

## 5. 구현된 파이프라인

`.github/workflows/pages.yml`은 다음 순서로 실행됩니다.

```text
Pull Request ──> HTML·CSS·JS 경로 검사 ──> 결과만 보고, 배포 안 함
main push   ──> HTML·CSS·JS 경로 검사 ──> Pages artifact ──> GitHub Pages
```

주요 통제는 다음과 같습니다.

- workflow 기본 권한은 `contents: read`로 제한
- 배포 job에만 `pages: write`, `id-token: write` 부여
- PR에서는 배포 job 실행 금지
- 같은 브랜치의 이전 배포는 취소해 오래된 버전의 역전 배포 방지
- Actions를 이동하는 major tag 대신 확인된 불변 버전 태그로 지정
- Dependabot이 Actions 버전을 매월 점검
- 상대 경로만 사용해 `계정.github.io/저장소명/`에서도 CSS와 JS가 정상 로드

## 6. 최초 배포 절차

### 6.1 GitHub 저장소 준비

`demo` 폴더에서 아래 절차를 수행합니다. 원격 주소는 새로 만든 저장소 주소로 바꿉니다.

```powershell
git init -b main
git add .
git commit -m "Build KCLI website with GitHub Pages CI/CD"
git remote add origin https://github.com/OWNER/REPOSITORY.git
git push -u origin main
```

### 6.2 Pages 활성화

1. GitHub 저장소의 `Settings`를 엽니다.
2. `Pages`를 선택합니다.
3. `Build and deployment`의 Source를 `GitHub Actions`로 설정합니다.
4. `Actions` 탭에서 `KCLI Pages CI/CD` 성공을 확인합니다.
5. 배포 job의 URL로 접속합니다.

저장소 이름이 `OWNER.github.io`이면 루트 사이트가 되고, 다른 이름이면 `https://OWNER.github.io/REPOSITORY/`에 게시됩니다.

### 6.3 권장 저장소 정책

- `main` 직접 push를 제한하고 Pull Request 1회 이상 검토
- `Validate site` 성공을 필수 상태 검사로 지정
- 관리자도 규칙 적용
- 2단계 인증 사용
- GitHub secret scanning 및 push protection 활성화

## 7. 사용자 도메인 연결

도메인 구입 비용은 별도지만 서버 비용은 생기지 않습니다.

1. GitHub 계정 또는 조직에서 도메인을 먼저 검증합니다.
2. 저장소 `Settings → Pages → Custom domain`에 도메인을 등록합니다.
3. DNS 제공자에서 GitHub 안내에 따라 `A/AAAA` 또는 `CNAME` 레코드를 설정합니다.
4. `Enforce HTTPS`를 켭니다.

와일드카드 DNS는 도메인 탈취 위험이 있어 사용하지 않는 편이 좋습니다.

## 8. 보안 조치

원본 `application-prod.properties`에 RDS 주소, 사용자명, 비밀번호가 평문으로 있었습니다. 현재 파일은 `DB_URL`, `DB_USERNAME`, `DB_PASSWORD` 환경변수만 읽도록 바꿨습니다.

이 값이 실제 시스템에서 사용됐거나 GitHub에 한 번이라도 올라간 적이 있다면 파일 삭제만으로 충분하지 않습니다.

1. RDS 비밀번호를 즉시 교체합니다.
2. 불필요한 DB 계정과 공개 네트워크 접근을 제거합니다.
3. Git 기록에 포함됐다면 유출된 값으로 간주합니다.
4. 필요 시 `git filter-repo`로 이력을 정리하되, 비밀번호 교체를 먼저 합니다.

현재 Pages workflow는 `src/main/resources/static`만 배포하지만, 공개 저장소의 나머지 소스도 누구나 읽을 수 있으므로 어떤 파일에도 비밀값을 커밋하면 안 됩니다.

## 9. 언제 AWS로 전환할 것인가

다음 중 하나가 확정될 때만 동적 호스팅을 검토합니다.

- 자체 신청서 저장과 관리자 처리 화면
- 사용자 계정과 권한 관리
- 결제 또는 민감정보 처리
- 외부 API를 숨겨 호출해야 하는 기능
- 서버에서 생성하는 개인화 콘텐츠

그때도 Jenkins 서버를 추가하지 않고 `GitHub Actions + OIDC`로 AWS에 단기 자격증명을 발급받아 배포하는 방식을 권장합니다. 기존 EC2를 유지한다면 `ECR + Systems Manager`, 신규 구축이라면 관리형 컨테이너 또는 서버리스 서비스를 요구량에 맞춰 비교합니다.

## 10. KCLI 자료 반영 및 공개 전 확인

다음 제공 자료를 홈페이지에 반영했습니다.

- `KCLI 회사소개 v0.2.pptx`: 기관명, 설립일, 대표, 주소, 핵심사업
- `KCL연구원 로고.png`: 기관 소개 및 지정서 영역 로고
- `ISO42001 교육포스터.jpg`: 교육 목적·대상·과정 구성
- `ISO42001 1회교육 성과.jpg`: 2026년 5월 제1회 교육 운영 결과
- `ISO42001 교육수료증-예시.jpg`: 수료증 예시
- `IQCS 한국사이버리터러시연구원 지정서.pdf`: 지정 범위와 등록번호 KRT0184

공개 전에는 아래 항목을 기관이 최종 확인해야 합니다.

- IQCS 지정서의 현재 유효·갱신 상태와 표시 허용 범위
- 공식 로고와 교육 이미지의 웹 게시 권한
- 전화, 이메일, 도메인 및 사업장 주소의 최신성
- 교육 신청 시 개인정보 처리방침과 수집 동의 절차
- 수료증 예시의 마스킹·공개 범위
- 사용자 도메인 `k-cli.kr`의 DNS 변경 권한

지정서의 유효일과 갱신일 표기가 혼재하므로 홈페이지는 현재 유효성을 단정하지 않고, 제공 문서의 발급일과 등록번호만 표시했습니다.
