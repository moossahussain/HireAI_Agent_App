# CrewAI Job Application Assistant

A containerized application that uses AI agents to analyze job postings, tailor resumes, and prepare for interviews.

## Features

- Analyze job postings to extract key requirements
- Match your resume against job requirements
- Generate tailored resumes for specific job applications
- Create interview preparation materials

## Quick Start

### Prerequisites

- Docker and Docker Compose
- OpenAI API key
- Serper API key (for web searches)

### Setup

1. Clone this repository:
   ```
   git clone <repository-url>
   cd crewai-job-app
   ```

2. Create a `.env` file with your API keys:
   ```
   cp .env.example .env
   ```
   Then edit the `.env` file to add your API keys.

3. Build and start the container:
   ```
   docker-compose up -d
   ```

4. The API will be available at `http://localhost:8000`

## API Endpoints

### Health Check
```
GET /
```
Returns a welcome message to confirm the API is running.

### Upload Resume
```
POST /api/upload-resume
```
Upload a resume file (Markdown format preferred).

### Analyze Job
```
POST /api/analyze-job
```
Start the job analysis process with a job posting URL and optional GitHub profile.

### Get Results
```
GET /api/results/{session_id}
```
Retrieve the results of a job analysis session.

## Example Usage

1. Upload your resume:
   ```
   curl -X POST -H "X-API-Key: your_api_key" -F "file=@your_resume.md" http://localhost:8000/api/upload-resume
   ```

2. Analyze a job posting:
   ```
   curl -X POST -H "Content-Type: application/json" -H "X-API-Key: your_api_key" \
     -d '{"job_posting_url": "https://example.com/job-posting", "github_url": "https://github.com/yourusername", "personal_writeup": "Your personal summary"}' \
     http://localhost:8000/api/analyze-job
   ```

3. Get results:
   ```
   curl -H "X-API-Key: your_api_key" http://localhost:8000/api/results/your_session_id
   ```

## Development

To run in development mode with hot-reloading:
```
docker-compose up
```

## Next Steps

This is a minimal viable product. Future improvements:
- Implement match scoring percentage
- Add job recommendation features
- Create a database for storing resumes and results