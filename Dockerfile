FROM python:3.12

WORKDIR /CommerceAPI

COPY ./requirements.txt /CommerceAPI/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /CommerceAPI/requirements.txt

COPY ./app /CommerceAPI/app

COPY ./alembic /CommerceAPI/alembic

COPY ./alembic.ini /CommerceAPI/alembic.ini

CMD ["uvicorn", "app.main:app","--host", "0.0.0.0","--port","80"]
