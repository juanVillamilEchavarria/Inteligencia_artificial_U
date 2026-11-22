FROM python:3.14-slim

ARG USER=app
ARG UID=1000
WORKDIR /app

# Las dependencias se instalan como root para que queden en el entorno global
# de la imagen y no en el directorio personal del usuario sin privilegios.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN useradd -u $UID -m $USER
COPY --chown=$UID:$UID . .
RUN chown -R $UID:$UID /app

USER $USER

CMD ["sleep", "infinity"]
