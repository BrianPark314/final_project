FROM python:3.11

# 
WORKDIR /code

# opencv dependancy
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./ /code/

# 
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "80"]