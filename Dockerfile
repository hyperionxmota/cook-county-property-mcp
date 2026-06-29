FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY server.py ./
ENV API_BASE_URL=https://api.ingest0r.com
# stdio MCP server; Glama starts it and sends initialize/tools/list to introspect.
CMD ["python", "server.py"]
