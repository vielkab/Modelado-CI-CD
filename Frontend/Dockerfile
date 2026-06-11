# 1. Imagen base 
FROM nginx:alpine

# 2. Limpiar cualquier archivo por defecto de Nginx
RUN rm -rf /usr/share/nginx/html/*

# 3. Modificación para cambiar el puerto de escucha a 8080 (Obligatorio para Cloud Run)
RUN sed -i 's/listen[: ]*80;/listen 8080;/g' /etc/nginx/conf.d/default.conf

# 4. Copiar SOLO el contenido de tu carpeta Frontend a la ruta de Nginx
COPY . /usr/share/nginx/html/

# 5. Puerto a usar
EXPOSE 8080

# 6. Comando para arrancar el servidor web Nginx
CMD ["nginx", "-g", "daemon off;"]