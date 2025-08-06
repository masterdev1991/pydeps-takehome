FROM python-base

# Install ML dependencies
RUN pip install scikit-learn pandas numpy

# Copy application code
COPY apps/job-a/app.py .

# Copy static data
COPY static_data/ /app/static_data/

# Set PYTHONPATH and data path
ENV PYTHONPATH=/app/lib:$PYTHONPATH
ENV DATA_PATH=/app/static_data/LD2011_2014.csv

# Run the job
CMD [".local/bin/python", "app.py"]