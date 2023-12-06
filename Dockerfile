FROM python:3.12.0-alpine3.18
WORKDIR /app
# Install the dependencies
COPY python/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Copy the app files
COPY python/app/ app/
EXPOSE 80 
# Run the DDNS app
CMD [ "gunicorn", "-b", "0.0.0.0:80", "app:create_app()", "-n", "ddns_acc"]