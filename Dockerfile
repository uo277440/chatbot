# Usar una imagen oficial de Python como imagen base
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Instalar dependencias de sistema necesarias
RUN apt-get update && apt-get install -y libpq-dev gcc

# Copiar los requerimientos de Python
COPY requirements.txt .

# Instalar las dependencias de Python
RUN pip install -r requirements.txt

# Copiar el resto del código de la aplicación
COPY . .


# Exponer el puerto que usa Django
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
