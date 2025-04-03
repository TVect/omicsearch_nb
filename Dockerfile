FROM condaforge/mambaforge:4.9.2-5

RUN pip install \
    flask==3.0.3 \
    pandas==2.0.3 \
    flask_sqlalchemy==3.1.1 \
    flask_marshmallow==1.2.1 \
    Flask-Migrate==4.0.7 \
    flask-session==0.8.0 \
    gunicorn==23.0.0 \
    marshmallow-sqlalchemy==1.1.0 \
    -i https://pypi.tuna.tsinghua.edu.cn/simple && \
    rm -r /root/.cache

COPY . /opt/omicsearch_nb

WORKDIR /opt/omicsearch_nb

EXPOSE 10080

CMD ["bash", "bin/run.sh"]
