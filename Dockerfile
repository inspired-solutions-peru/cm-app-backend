# 1. Imagen base de Python
FROM python:3.10-slim

# 2. Variables de entorno para Python
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# 3. Directorio de trabajo
WORKDIR /app

# 4. Instalamos dependencias del sistema necesarias para Django
RUN apt-get update \
    && apt-get install -y \
       build-essential \
       default-libmysqlclient-dev \
       pkg-config \
       libjpeg-dev \
       zlib1g-dev \
       locales \
       curl \
    && apt-get clean

# 5. Copiamos e instalamos dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copiamos el resto del código
COPY . .

# 7. Creamos directorio para archivos estáticos (collectstatic)
RUN mkdir -p /app/staticfiles

# 8. Comando por defecto para producción
# Realiza migraciones, collectstatic y levanta Gunicorn
CMD bash -c "\
    python manage.py migrate && \
    python manage.py collectstatic --noinput && \
    gunicorn backend_project.wsgi:application --bind 0.0.0.0:8000 --workers 3 \
"
