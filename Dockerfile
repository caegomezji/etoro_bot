# FROM ultrafunk/undetected-chromedriver:3.20-chrome-lateinstall
FROM python:3.10

RUN apt update && apt install -y chromium #=120.0.6099.224-1~deb12u1
#=120.0.6099.129-1~deb12u1
RUN pip install -U pip
 
RUN pip install \
    selenium==4.16.0 \
    undetected-chromedriver==3.5.4 \
    fastapi \
    uvicorn

RUN mkdir -p /usr/app

WORKDIR /usr/app

COPY ./ /usr/app

#ENTRYPOINT ["python3"   , "-m" , "etoro_bot.etoro_bot"]

#ENTRYPOINT ["/bin/bash"]

ENTRYPOINT ["uvicorn" , "etoro_bot.main:app"]
