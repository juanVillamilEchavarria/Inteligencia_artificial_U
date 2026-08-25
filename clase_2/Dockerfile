FROM python:3.10-slim

ARG USER=app
ARG UID=1000
WORKDIR /app

RUN useradd -u $UID -m $USER


COPY --chown=$UID:$UID . .
RUN chown -R $UID:$UID /app

USER $USER
RUN pip install -r requirements.txt



CMD ["sleep", "infinity"]