# -----------------------------
# 1) Build React Native Web
# -----------------------------
FROM node:20-alpine AS builder

WORKDIR /app

# Copier le code
COPY package.json package-lock.json ./
RUN npm ci

COPY . .

# Build web Expo
RUN npx expo export --platform web

# -----------------------------
# 2) Serveur NGINX
# -----------------------------
FROM nginx:1.25-alpine

# Suppression des templates par défaut
RUN rm -rf /usr/share/nginx/html/*

# Copier les assets web
COPY --from=builder /app/dist /usr/share/nginx/html

# Copier la configuration Nginx personnalisée
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
