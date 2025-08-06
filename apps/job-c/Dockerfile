FROM python-base

# Install numpy>=2.3.0 for strings.slice functionality
RUN pip install "numpy>=2.3.0" pandas

# Copy application code
COPY apps/job-c/app.py .


# Copy static data
COPY static_data/ /app/static_data/

# Set PYTHONPATH and data path
ENV PYTHONPATH=/app/lib:$PYTHONPATH
ENV DATA_PATH=/app/static_data/enron_emails_1702.csv

# Run the job
CMD [".local/bin/python", "app.py"]