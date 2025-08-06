FROM python-base

# Install FastAPI dependencies
RUN pip install fastapi uvicorn

# Copy application code
COPY app.py .

# Expose port
EXPOSE 8080

# Set PYTHONPATH
ENV PYTHONPATH=/app/lib:$PYTHONPATH

# Run the application
# CMD ["python", "app.py"]
CMD [".local/bin/python", "app.py"]