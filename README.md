# Backend Súper-App (Travel & Delivery)

Este es el backend centralizado para la Súper-App, construido con Django, Django Rest Framework y MySQL, todo gestionado con Docker.

---

## 🚀 Stack de Tecnología

* **Backend:** Django
* **API:** Django Rest Framework (DRF)
* **Base de Datos:** MySQL 8.0
* **Admin de DB:** phpMyAdmin
* **Contenedores:** Docker & Docker Compose

---

## 🛠️ Cómo Levantar el Entorno (Instalación)

Este proyecto está 100% dockerizado, por lo que no necesitas instalar Python o MySQL en tu máquina.

**Requisitos:** Tener Docker Desktop instalado.

### 1. Clonar el Repositorio

```bash
git clone [URL_DE_TU_REPOSITORIO_AQUI]
cd Backend_Travel
```

### 2. Crear el Archivo de Entorno

Este proyecto necesita un archivo `.env` para guardar las contraseñas y secretos.

1.  Copia la plantilla de ejemplo:
    ```bash
    cp .env.example .env
    ```
    *(En Windows, puedes copiar y pegar el archivo `.env.example` y renombrarlo a `.env`)*

2.  Abre el archivo `.env` y rellena las variables (ej. `DJANGO_SECRET_KEY` y `MYSQL_ROOT_PASSWORD`).

### 3. Levantar los Contenedores

Este comando construirá la imagen de Django y levantará los 3 servicios (Django, MySQL, phpMyAdmin).

```bash
docker-compose up --build -d
```

### 4. Crear la Base de Datos (Migraciones)

Una vez que los contenedores estén corriendo, dile a Django que cree todas las tablas en la base de datos MySQL:

```bash
docker-compose exec web python manage.py migrate
```

### 5. Crear un Super-Usuario

Finalmente, crea tu cuenta de administrador para acceder al panel:

```bash
docker-compose exec web python manage.py createsuperuser
```
*(Sigue los pasos: usuario, email y contraseña)*

---

## 🌐 Puertos y Accesos

¡Todo listo! Ya puedes acceder a los servicios:

* **API de Django (Admin):** `http://localhost:8086/admin/`
* **phpMyAdmin (Base de Datos):** `http://localhost:8087/`
    * **Usuario:** `root`
    * **Contraseña:** (La que pusiste en tu `.env`)