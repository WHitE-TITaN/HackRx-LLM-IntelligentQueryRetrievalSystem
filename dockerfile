FROM gradle:8.5-jdk17 AS builder

# Copy source and build
COPY . /app
WORKDIR /app

# Build WAR
RUN gradle clean build

# Use Tomcat to run WAR
FROM tomcat:9.0-jdk17

# Remove default webapps
RUN rm -rf /usr/local/tomcat/webapps/*

# Copy WAR from builder image
COPY --from=builder /app/build/libs/*.war /usr/local/tomcat/webapps/ROOT.war

EXPOSE 8080
CMD ["catalina.sh", "run"]
