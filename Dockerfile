FROM python:3
WORKDIR /app
COPY ./extractor ./extractor
CMD [ "python", "-m", "extractor" ]