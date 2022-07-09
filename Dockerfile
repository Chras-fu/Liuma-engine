FROM python:3.8

MAINTAINER "panghu"

COPY browser /liuma/browser

COPY core /liuma/core

COPY requirements.txt /liuma/

COPY tools/ /liuma/tools

COPY lm/ /liuma/lm

COPY startup.py /liuma/

WORKDIR /liuma

RUN pip install -r requirements.txt -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com

CMD ["python", "startup.py"]
