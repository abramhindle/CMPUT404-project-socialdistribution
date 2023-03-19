# ARG NEXT_PUBLIC_SUPABASE_URL=${NEXT_PUBLIC_SUPABASE_URL}
# ARG NEXT_PUBLIC_SUPABASE_ANON_KEY=${NEXT_PUBLIC_SUPABASE_ANON_KEY}

FROM node:16-alpine AS deps
RUN apk add --no-cache libc6-compat
RUN echo ${NEXT_PUBLIC_SUPABASE_URL}
RUN echo *******************************************************************

WORKDIR /app
COPY package.json ./
COPY yarn.lock  ./

RUN yarn install --frozen-lockfile

FROM node:16-alpine AS builder
RUN echo ${NEXT_PUBLIC_SUPABASE_URL}
RUN echo *******************************************************************
ENV NODE_ENV=production
WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules

COPY . .
RUN yarn build
 
# Production image, copy all the files and run next
FROM node:16-alpine AS runner
RUN echo ${NEXT_PUBLIC_SUPABASE_URL}
RUN echo *******************************************************************
# ARG NEXT_PUBLIC_SUPABASE_URL
# ARG NEXT_PUBLIC_SUPABASE_ANON_KEY
# ENV NEXT_PUBLIC_SUPABASE_URL=$NEXT_PUBLIC_SUPABASE_URL
# ENV NEXT_PUBLIC_SUPABASE_ANON_KEY=$NEXT_PUBLIC_SUPABASE_ANON_KEY
WORKDIR /app
COPY --from=builder /app/public ./public
# Automatically leverage output traces to reduce image size
# https://nextjs.org/docs/advanced-features/output-file-tracing
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/next.config.js ./next.config.js
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

EXPOSE 3000
CMD ["yarn", "start"]