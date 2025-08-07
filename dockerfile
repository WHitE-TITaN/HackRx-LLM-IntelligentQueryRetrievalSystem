# Stage 1: Build the WAR file
FROM gradle:7.6-jdk17 AS builder
WORKDIR /app
COPY . .
RUN gradle clean war

# Stage 2: Deploy to Tomcat
FROM tomcat:9.0
COPY --from=builder /app/build/libs/*.war /usr/local/tomcat/webapps/ROOT.war
EXPOSE 8080
