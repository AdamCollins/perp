FROM python:3.7

RUN mkdir src
WORKDIR src

RUN apt-get update
RUN apt-get install -y nginx

COPY api /src
COPY dist /dist
COPY ./docker-entrypoint.sh /
COPY .git /

COPY etc/nginx/sites-available/perp /etc/nginx/sites-available/perp
RUN ln -s /etc/nginx/sites-available/perp /etc/nginx/sites-enabled
RUN rm /etc/nginx/sites-enabled/default
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

RUN pip install -r requirements.txt
RUN pip install -e .

ENTRYPOINT ["/docker-entrypoint.sh"]
