##
## Elasticsearch
##

FROM iron/java:1.8


ENV LANG C.UTF-8

##
## Add some things that help in development
##
RUN apk update && apk add vim curl bash

##
## install gosu for entrypoint function
## (https://github.com/tianon/gosu)
ENV GOSU_VERSION 1.7
RUN wget -O  /usr/local/bin/gosu "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-amd64" && \
    wget -O  /usr/local/bin/gosu.asc "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-amd64.asc"  && \
    chmod +x /usr/local/bin/gosu

##
## download and install  elasticsearch
##
ENV ELASTICSEARCH_VERSION 2.0.2
RUN wget https://download.elastic.co/elasticsearch/release/org/elasticsearch/distribution/tar/elasticsearch/${ELASTICSEARCH_VERSION}/elasticsearch-${ELASTICSEARCH_VERSION}.tar.gz -O  /usr/share/elasticsearch.tar.gz

RUN tar -zxvf /usr/share/elasticsearch.tar.gz && \
    mv /elasticsearch-${ELASTICSEARCH_VERSION} /usr/share/elasticsearch && \
    rm /usr/share/elasticsearch.tar.gz

WORKDIR /usr/share/elasticsearch

ENV PATH /usr/share/elasticsearch/bin:$PATH

##
## install browser plugin
##  
##  This allows you to have browser read and search access 
##  to the elasticsearch instance at URL
##   http://192.168.99.101:9200/_plugin/head/
##  (assuming your hostname is 192.168.99.101 and you used port 9200 
##   
RUN /usr/share/elasticsearch/bin/plugin install mobz/elasticsearch-head

##
## configurations for elasticsearch
##
## user to run elasticsearch:
RUN adduser -D -h /usr/share/elasticsearch  elasticsearch
## log, plugin directories
RUN mkdir -p /usr/share/elasticsearch/logs && \
    mkdir -p /usr/share/elasticsearch/plugins
COPY config /usr/share/elasticsearch/

## mounted volume for elasticsearch data 
VOLUME /usr/share/elasticsearch/data
COPY docker-entrypoint.sh /
RUN chmod -R g+w /usr/share/elasticsearch/data/  && \
    chown -R elasticsearch:elasticsearch /usr/share/elasticsearch && \
    chmod u+x /docker-entrypoint.sh

## 
## Hack to allow elasticsearch user to write to mounted volumes:
## (this shouldn't be needed on a linux machine??)
## (https://github.com/docker-library/elasticsearch/issues/27)
## RUN usermod -u 1000 elasticsearch


##
## Add some things that help in development
##
RUN printf 'PS1="\u@elastic:$ "\n'        >> /root/.bashrc  && \
    printf 'alias ls="ls --color=auto"\n' >> /root/.bashrc  && \
    printf "syntax on\n"     >> /root/.vimrc  && \
    printf ":set hlsearch\n" >> /root/.vimrc  && \
    printf ":set ruler\n"    >> /root/.vimrc  && \
    echo '-w "\n"'       >> /root/.curlrc

EXPOSE 9200 9300
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["elasticsearch"]



