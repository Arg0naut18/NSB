FROM python:3.8

WORKDIR /

COPY . /

RUN sudo apt-get update && \
    sudo apt-get install foo bar baz foo-dev foo-dbg && \
    pip install -Ur requirements.txt

CMD ["python", "main.py"]
