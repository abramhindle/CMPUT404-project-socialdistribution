# ARG NEXT_PUBLIC_SUPABASE_URL=${NEXT_PUBLIC_SUPABASE_URL}
# ARG NEXT_PUBLIC_SUPABASE_ANON_KEY=${NEXT_PUBLIC_SUPABASE_ANON_KEY}

FROM node:16-alpine AS deps
RUN apk add --no-cache libc6-compat
# ARG NEXT_PUBLIC_SUPABASE_URL
# ARG NEXT_PUBLIC_SUPABASE_ANON_KEY
# ENV NEXT_PUBLIC_SUPABASE_URL=$NEXT_PUBLIC_SUPABASE_URL
# ENV NEXT_PUBLIC_SUPABASE_ANON_KEY=$NEXT_PUBLIC_SUPABASE_ANON_KEY

WORKDIR /app
COPY package.json ./
COPY yarn.lock  ./

RUN yarn install --frozen-lockfile

FROM node:16-alpine AS builder
# ARG NEXT_PUBLIC_SUPABASE_URL
# ARG NEXT_PUBLIC_SUPABASE_ANON_KEY
# ENV NEXT_PUBLIC_SUPABASE_URL=$NEXT_PUBLIC_SUPABASE_URL
# ENV NEXT_PUBLIC_SUPABASE_ANON_KEY=$NEXT_PUBLIC_SUPABASE_ANON_KEY
ENV NODE_ENV=production
WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules

COPY . .
RUN yarn build
 
# Production image, copy all the files and run next
FROM node:16-alpine AS runner
# ARG NEXT_PUBLIC_SUPABASE_URL
# ARG NEXT_PUBLIC_SUPABASE_ANON_KEY
ENV NEXT_PUBLIC_SUPABASE_URL=https://ryfotblenvmtqnedsulf.supabase.co/
ENV NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ5Zm90YmxlbnZtdHFuZWRzdWxmIiwicm9sZSI6ImFub24iLCJpYXQiOjE2Nzc4MTI2NDcsImV4cCI6MTk5MzM4ODY0N30.HCwMSFmA5shFft6o7W7X64ddzGcP2ptjYck-d7sWNAM
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