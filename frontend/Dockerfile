# Base image
FROM node:20-bullseye

# Çalışma klasörü
WORKDIR /app

# package.json ve package-lock.json kopyala
COPY package*.json ./

# Bağımlılıkları yükle
RUN npm install

# Proje dosyalarını kopyala
COPY . .

# Development server'ı başlat
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host"]
