/** @type {import('next').NextConfig} */
const removeImports = require('next-remove-imports')();
module.exports = removeImports({
  reactStrictMode: true,
  images: {
    domains: ['*'],
  },
  typescript: {
    // !! WARN !!
    // Dangerously allow production builds to successfully complete even if
    // your project has type errors.
    // !! WARN !!
    ignoreBuildErrors: true,
  }
})

