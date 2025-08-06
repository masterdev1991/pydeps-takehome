FROM python-base

# Install FastAPI and data processing dependencies
RUN uv pip install fastapi uvicorn

# Copy application code
COPY app.py .

# Copy static data
COPY ../../static_data/ /app/static_data/

# Expose port
EXPOSE 8080

# Set PYTHONPATH and data path
ENV PYTHONPATH=/app/lib:$PYTHONPATH
ENV DATA_PATH=/app/static_data/LD2011_2014.csv

# Run the application
CMD ["python", "app.py"]