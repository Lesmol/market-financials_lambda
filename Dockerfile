FROM public.ecr.aws/lambda/python:3.14

# COPY the requirements.txt file to the Lambda task root
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Use --no-cache-dir to keep the image size smaller by removing temporary cache files
RUN pip install --no-cache-dir -r requirements.txt

# COPY function code
COPY app.py ${LAMBDA_TASK_ROOT}

# SET CMD to handler
CMD [ "app.handler" ]
