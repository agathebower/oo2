FROM python:3
RUN pip install flask
RUN pip install requests
RUN pip install sentry-sdk==0.10.2
#CMD ["flask", "run", "--host=0.0.0.0", "--port=80"]
