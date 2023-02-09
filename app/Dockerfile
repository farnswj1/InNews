FROM python:3.9-slim-bullseye

# set environment variables
ENV PYTHONUNBUFFERED 1

# expose port(s)
EXPOSE 8501

# set directory
WORKDIR /opt/app

# add application and install dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . ./

# run the program
CMD ["streamlit", "run", "App.py", "--server.address=0.0.0.0"]
