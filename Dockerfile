# Stage 1: Base build stage
FROM python:3.13-slim AS builder

# Create the app directory
RUN mkdir /app

# Set the working directory
WORKDIR /app

# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Upgrade pip and install dependencies
RUN pip install --upgrade pip setuptools

# Copy the requirements file first (better caching)
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Production stage
FROM python:3.13-slim

RUN useradd -m -r appuser && \
   mkdir /app && \
   chown -R appuser /app

# Copy the Python dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Set the working directory
WORKDIR /app

# Copy application code
COPY --chown=appuser:appuser . .

# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Switch to non-root user
USER appuser

# Expose the application port
EXPOSE 8080

COPY --chown=appuser:appuser start.sh .
RUN chmod +x start.sh
CMD ["/bin/bash", "-c", "sh ./start.sh"]

# Start the application using Gunicorn (by the moment run it in development mode)
#CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "3", "--reload", "agendadosDjango.wsgi:application"]
#CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "agendadosDjango.asgi:application"]
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]