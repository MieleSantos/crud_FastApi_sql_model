FROM python:3.10-slim

RUN apt-get update

# Installing poetry
RUN pip install poetry
ENV PATH="/root/.local/bin:$PATH" 
ENV PYTHONUNBUFFERED=1 

# Enabling environment and transfering files
WORKDIR /app
COPY ./poetry.lock ./pyproject.toml ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev
COPY . ./