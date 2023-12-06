FROM python:3.12.0-alpine3.18
WORKDIR /app
# Install the dependencies
COPY python/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
# Create the app user
RUN adduser -D ddns_acc
RUN chown -R ddns_acc:ddns_acc /app
USER ddns_acc
# Copy the app files
COPY python/app/ app/
EXPOSE 8000
# Run the DDNS app
CMD [ "gunicorn", "-b", "0.0.0.0:8000", "--access-logfile", "-", "--error-logfile", "-", "app:create_app()", "-n", "ddns_acc"]