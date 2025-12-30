# 1. Use an official Python image
FROM python:3.9-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy your project files into the container
COPY . /app

# 4. Install the necessary libraries
RUN pip install --no-cache-dir -r requirements.txt

# 5. Keep the container running (or you could set it to run a specific script)
CMD ["python", "anomalies.py"]