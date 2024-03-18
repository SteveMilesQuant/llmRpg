FROM python:3.10-alpine

WORKDIR /stories-api
COPY ./requirements.txt ./requirements.txt
RUN python3 -m pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY ./*.py ./

RUN addgroup app && adduser -S -G app app
USER app

EXPOSE 3000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]