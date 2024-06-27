# Usar una imagen oficial de Node.js
FROM node:16

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar los archivos package.json y package-lock.json
COPY package*.json ./

# Instalar las dependencias del proyecto
RUN npm install

# Copiar todos los archivos del proyecto al contenedor
COPY . .

# Exponer el puerto que la aplicación usará
EXPOSE 3000

# Comando para ejecutar la aplicación
CMD ["npm", "start"]



