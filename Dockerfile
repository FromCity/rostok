FROM astral/uv:python3.12-bookworm
WORKDIR /app
COPY requirements.txt .
RUN uv venv /app/.venv
ENV PATH="/app/.venv/bin:${PATH}"
RUN uv pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uv", "run", "fastapi", "dev"]