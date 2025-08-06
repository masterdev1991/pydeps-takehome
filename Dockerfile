# Base Python container image for all Verse Python apps
FROM python:3.11.9-slim-bookworm

RUN addgroup --gid 1001 verse
RUN adduser  --uid 1001 --ingroup verse verse
USER verse:verse

WORKDIR /app

# Copy project files
COPY --chown=verse:verse pyproject.toml pyproject.toml
COPY --chown=verse:verse README.md README.md
COPY --chown=verse:verse lib/ lib/
COPY --chown=verse:verse apps/ apps/
COPY --chown=verse:verse static_data/ static_data/
COPY --chown=verse:verse scripts/ scripts/ 

# Set up Python environment
ENV PYTHONPATH=lib/
ENV VIRTUAL_ENV=.local
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies
RUN pip install --upgrade pip 

# Install project in editable mode (this will read pyproject.toml correctly)
RUN pip install -e .

# Clean up
RUN rm pyproject.toml
