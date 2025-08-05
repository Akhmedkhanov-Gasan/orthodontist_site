# ---------- build stage ----------
FROM node:18 AS builder
WORKDIR /app

ARG NEXT_PUBLIC_API_URL
ARG NEXT_PUBLIC_RECAPTCHA_SITE_KEY

COPY package*.json ./
RUN npm ci --legacy-peer-deps

COPY . .

ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_RECAPTCHA_SITE_KEY=$NEXT_PUBLIC_RECAPTCHA_SITE_KEY

RUN npm run build        # «next build»

# ---------- runtime stage ----------
FROM node:18-slim
WORKDIR /app

COPY --from=builder /app/.next          .next
COPY --from=builder /app/public         public
COPY --from=builder /app/package*.json  ./

RUN npm ci --omit=dev --legacy-peer-deps

ENV NODE_ENV=production
EXPOSE 3000
CMD ["npm", "run", "start"]
