FROM python:3.9

WORKDIR /app

# Install pandoc
RUN apt-get update && apt-get install -y pandoc

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install python-dotenv

COPY . .

# Copy the .env file
COPY .env .env

# Create the resumes directory
RUN mkdir -p /app/resumes

# Run the OpenAI migration tool
RUN openai migrate

# Use the development server with hot reloading
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
