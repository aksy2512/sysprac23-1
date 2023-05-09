FROM alpine:latest
# FROM alpine:3.14.2 
# wkhtmltopdf is only available in versions 3.14 and below but they cause issues with other dependencies

# Below 2 lines can be commented when not using proxy
ENV HTTP_PROXY "http://gateway.iitmandi.ac.in:8080"
ENV HTTPS_PROXY "http://gateway.iitmandi.ac.in:8080"

RUN apk add build-base
RUN apk add ffmpeg libreoffice-common poppler-utils
RUN apk add --update py3-pip
RUN apk add python3-dev py3-numpy py3-pandas
# RUN apk add wkhtmltopdf xvfb ttf-dejavu ttf-droid ttf-freefont ttf-liberation;
WORKDIR /app/

RUN mkdir -p uploads/ converted/ instance/
COPY API/* ./API/
COPY static/* ./static/
COPY templates/* ./templates/
COPY *.py ./
COPY requirements.txt ./
RUN pip install --no-cache-dir -r ./requirements.txt

# No need unless proxy needs to be removed for some reasons
# ENV HTTP_PROXY ""
# ENV HTTPS_PROXY ""

EXPOSE 5000
CMD ["python3","app.py"]
