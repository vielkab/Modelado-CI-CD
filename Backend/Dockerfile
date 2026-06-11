# 1. Usamos una imagen oficial de Python ligera como base
FROM python:3.10-slim

# 2. Creamos y nos movemos a la carpeta de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiamos los requerimientos desde la carpeta Backend hacia el contenedor
COPY requirements.txt .

# 4. Instalamos las dependencias dentro del contenedor sin guardar caché (para ahorrar espacio)
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiamos TODO el contenido de tu carpeta Backend local dentro del contenedor
COPY . .

# 6. Le avisamos al contenedor que el tráfico entrará por el puerto 8080 (el estándar de Cloud Run)
EXPOSE 8080

# 7. Comando definitivo para arrancar la API con Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]