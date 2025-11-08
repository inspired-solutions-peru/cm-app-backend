# 1. Imagen base de Python
FROM python:3.10-slim

# 2. Variables de entorno para Python
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# 3. Directorio de trabajo
WORKDIR /app

# 4. Instalamos dependencias del sistema operativo
# (Esto previene errores comunes al instalar mysqlclient)
RUN apt-get update \
    && apt-get install -y build-essential default-libmysqlclient-dev pkg-config \
    && apt-get clean

# 5. Instalamos dependencias de Python
# (Copiamos solo requirements primero para usar la caché de Docker)
COPY requirements.txt .
RUN pip install -r requirements.txt

# 6. Copiamos el resto del código
COPY . .