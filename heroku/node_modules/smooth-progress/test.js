#!/usr/bin/env node

'use strict'
let progress = require('./index')

let bar = progress(512 * 1024)

let interval = setInterval(function () {
  let chunk = Math.random() * 1024
  bar.tick(chunk)
  if (bar.complete) clearInterval(interval)
}, 5)
