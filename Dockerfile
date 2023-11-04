FROM python:3.8

WORKDIR /

COPY . /

ARG TOKEN
ENV TOKEN=$TOKEN

ARG scicord_token
ENV scicord_token=$scicord_token

ARG ytKey
ENV ytKey=$ytKey

ARG client_id
ENV client_id=$client_id

ARG client_secret
ENV client_secret=$client_secret

ARG user_agent
ENV user_agent=$user_agent

ARG token
ENV token=$token

ARG tenorkey
ENV tenorkey=$tenorkey

ARG serverapikey
ENV serverapikey=$serverapikey

ARG nsbtoken
ENV nsbtoken=$nsbtoken

ARG spotipyid
ENV spotipyid=$spotipyid

ARG spotipytoken
ENV spotipytoken=$spotipytoken

ARG musixmatchkey
ENV musixmatchkey=$musixmatchkey

ARG dev_id
ENV dev_id=$dev_id

ARG cfkey
ENV cfkey=$cfkey

ARG cfsecret
ENV cfsecret=$cfsecret

ARG fillerApi
ENV fillerApi=$fillerApi

ARG mongo
ENV mongo=$mongo

ARG spotipyredirecturi
ENV spotipyredirecturi=$spotipyredirecturi

ARG redis_host
ENV redis_host=$redis_host

ARG redis_pass
ENV redis_pass=$redis_pass

ARG redis_port
ENV redis_port=$redis_port

RUN apt-get update && \
    apt clean && \
    pip install -Ur requirements.txt

CMD ["python", "main.py"]
