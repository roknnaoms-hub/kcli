FROM eclipse-temurin:17-jdk

# JAR 파일이 저장될 작업 디렉토리 설정
WORKDIR /app

# Maven 빌드 후 생성된 JAR 파일을 컨테이너 /app에 app.jar로 복사
COPY app.jar app.jar

# 실행 포트 지정
EXPOSE 8081

# 컨테이너 실행 시 JAR 실행
ENTRYPOINT ["java", "-jar", "app.jar"]