ARG PYTHON_VERSION

FROM python:$PYTHON_VERSION

WORKDIR /app

COPY main.py .
RUN pip install jupytext
RUN pip install python-frontmatter
RUN pip install python-slugify

ENTRYPOINT ["python", "/app/main.py"]