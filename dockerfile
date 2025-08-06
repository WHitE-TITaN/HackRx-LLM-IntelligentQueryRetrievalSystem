# Use official Tomcat base image
FROM tomcat:10.1-jdk21-temurin

# Set working directory
WORKDIR /usr/local/tomcat

# Remove default webapps (optional but cleaner)
RUN rm -rf webapps/*

# Copy your WAR file into Tomcat webapps directory
COPY build/libs/*.war webapps/ROOT.war

# Expose the port (Railway will use its own)
EXPOSE 8080
