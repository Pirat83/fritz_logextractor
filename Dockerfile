# Build .whl in a separate build container
FROM python:3.14.8-alpine@sha256:f6a589d43c42b9e7f7dc67a12d37132491f362859a5d750607710cc56da3bc72 AS build
WORKDIR /app

RUN pip install --upgrade pip build

COPY README.md pyproject.toml /app/
COPY fritzlogextractor /app/fritzlogextractor

RUN python -m build --wheel

# Build the actual runner
FROM python:3.14.8-alpine@sha256:f6a589d43c42b9e7f7dc67a12d37132491f362859a5d750607710cc56da3bc72

LABEL Name=fritz_logextractor
ENV PIP_NO_CACHE_DIR="true"

WORKDIR /app

COPY --from=build /app/dist/*.whl /

RUN pip install /fritz_logextractor-*.whl && \
    rm /fritz_logextractor-*.whl && \
    mkdir -p /etc/fritz /var/lib/fritzlogextractor

VOLUME ["/var/lib/fritzlogextractor"]

ENTRYPOINT ["python", "-m", "fritzlogextractor"]
