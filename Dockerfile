FROM python:3.13.0rc1-alpine3.19
# Update the system
RUN apk update && apk upgrade
WORKDIR /app
# Install the dependencies
COPY python/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
# Create a non-root user
ARG UNAME=ddns_acc
ARG UID=10001
ARG GID=10001
# Create the app user
RUN adduser -D $UNAME -u $UID -g $GID
RUN chown -R $UNAME:$UNAME /app
USER $UNAME
# Copy the app files
COPY python/app/ app/
EXPOSE 8000
# Set the environment variables
ENV LUMIGO_SECRET_MASKING_REGEX_HTTP_REQUEST_HEADERS='["Bearer:\s*[A-Za-z0-9]{64}"]'
# Run the DDNS app
CMD [ "gunicorn", "-b", "0.0.0.0:8000", "--access-logfile", "-", "--error-logfile", "-", "app:create_app()", "-n", "ddns_acc"]