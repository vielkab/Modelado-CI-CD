# 1. Imagen base 
FROM nginx:alpine

# 2. Carpeta de trabajo dentro del contenedor
WORKDIR /usr/share/nginx/html

# 3. modificacion pra cambiar el puerto de escucha de nginx a 8080 (opcional, pero recomendado para evitar conflictos con otros servicios)
RUN sed -i 's/listen[: ]*80;/listen 8080;/g' /etc/nginx/conf.d/default.conf

# 4. Copiar todo el código de tu proyecto (index.html, carpeta css) al contenedor
COPY . .

# 5. Puerto a usar
EXPOSE 8080

# 6. Comando para arrancar el servidor web Nginx
CMD ["nginx", "-g", "daemon off;"]