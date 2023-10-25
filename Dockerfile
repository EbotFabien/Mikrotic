FROM python:slim

RUN useradd mikrotic

WORKDIR /home/mikrotic

COPY req.txt req.txt
RUN python -m venv venv
RUN venv/bin/pip install -r req.txt
RUN venv/bin/pip install gunicorn

COPY app app
COPY migrations migrations
COPY mikrotic.py config.py boot.sh mikro.db ./
RUN chmod +x boot.sh

ENV FLASK_APP mikrotic.py

RUN chown -R mikrotic:mikrotic ./
USER mikrotic

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]