# Use a base image with Tomcat 9, which supports the javax.servlet API
FROM tomcat:9.0-jdk17

# Remove default apps
RUN rm -rf /usr/local/tomcat/webapps/*

# Copy your newly built WAR file to the webapps directory
# The `*` here is safe now because you know the WAR file exists.
COPY build/libs/*.war /usr/local/tomcat/webapps/ROOT.war

EXPOSE 8080

CMD ["catalina.sh", "run"]