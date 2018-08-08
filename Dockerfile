FROM alpine:latest
MAINTAINER w8ay.w8ay@qq.com
# install requirements
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories

RUN set -x \
    && apk update \
    && apk add bash \
    && apk add python3 \
    && apk add redis \
    && apk add mongodb \
    && apk add mongodb-tools

# install w11scan
RUN mkdir -p /opt/w11scan
COPY . /opt/w11scan

RUN set -x \
    && pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r /opt/w11scan/requirements.txt

RUN set -x \
    && chmod a+x /opt/w11scan/dockerconf/start.sh

WORKDIR /opt/w11scan

ENTRYPOINT ["/opt/w11scan/dockerconf/start.sh"]

EXPOSE 8000

CMD ["/usr/bin/tail", "-f", "/dev/null"]