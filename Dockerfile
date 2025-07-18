# Pinned digest for python:3.11-slim to ensure reproducible builds
FROM python@sha256:0df0b6c8ee6285ef3a0655e768f8b51006979cd13e341fa9a316bed36b1cfc7d

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN pip install --no-cache-dir -e .

ENTRYPOINT ["brookside-cli"]
CMD ["start"]
