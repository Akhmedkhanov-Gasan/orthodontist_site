FROM node:18

WORKDIR /app

# -------------------------------------------------
ARG NEXT_PUBLIC_API_URL
# -------------------------------------------------

COPY package.json package-lock.json ./
RUN npm ci --legacy-peer-deps

COPY . .

# -------------------------------------------------
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
# -------------------------------------------------


RUN npm run build

EXPOSE 3000
CMD ["npm", "run", "start"]