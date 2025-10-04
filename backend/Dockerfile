# Use official Python base image
FROM python:3.11-alpine

# Set working directory
WORKDIR /usr/src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies for Postgres and Python packages
RUN apk update && apk add --no-cache \
    gcc \
    g++ \
    libc-dev \
    musl-dev \
    python3-dev \
    libffi-dev \
    postgresql-dev \
    curl \
    icu-data-full


# Copy requirements and install
COPY ./requirements.txt .
# Upgrade pip and install dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install python-dotenv

# Copy project files
COPY . .

# Set entrypoint
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
