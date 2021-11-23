'use strict'

function progress (opts) {
  const chalk = require('chalk')
  const throttle = require('./throttle')
  const ansi = require('ansi-escapes')
  const partials = ['▏', '▎', '▍', '▌', '▋', '▊', '▉'].map((p) => chalk.blue(p))

  if (typeof (opts) === 'number') {
    opts = {total: opts}
  }
  let stderr = process.stderr
  let bar = {
    total: opts.total,
    width: opts.width || 25,
    tmpl: opts.tmpl || ':bar :percent :eta',
    cur: 0,
    percent: 0,
    complete: false,
    start: new Date(),
    tokens: {}
  }

  let termWidth = () => stderr.getWindowSize()[0]
  let pad = (num) => num < 10 ? '0' + num.toString() : num.toString()
  stderr.write(ansi.cursorHide)

  function line () {
    let line = bar.tmpl
    .replace(':bar', renderBar())
    .replace(':percent', pad(Math.round(bar.percent * 100)) + '%')
    .replace(':eta', eta())
    if (bar.tokens) {
      for (let token of Object.keys(bar.tokens)) {
        line = line.replace(':' + token, bar.tokens[token])
      }
    }
    // add blank characters to the end of the line
    // so we don't have to clear it causing a flicker
    line = line + ' '.repeat(Math.max(termWidth() - chalk.stripColor(line).length, 0))
    return line
  }

  function renderBar () {
    let output = ''
    let ticks = bar.percent * bar.width - 1
    if (ticks < 0) ticks = 0
    let filled = Math.floor(ticks)
    let open = bar.width - filled - 1
    output += chalk.blue('█').repeat(filled)
    output += partials[Math.floor((ticks - filled) * partials.length)]
    output += ' '.repeat(open) + ' '
    return output
  }

  function eta () {
    let elapsed = new Date() - bar.start
    let eta = Math.abs(((bar.percent === 100) ? 0 : elapsed * (bar.total / bar.cur - 1)) / 1000)
    let hours = Math.floor(eta / 3600)
    let minutes = Math.floor((eta - (hours * 3600)) / 60)
    let seconds = Math.round(eta - (hours * 3600) - (minutes * 60))
    if (hours) {
      return `${pad(hours)}:${pad(minutes)}:${pad(seconds)}`
    } else {
      return `${pad(minutes)}:${pad(seconds)}`
    }
  }

  function render () {
    if (!stderr.isTTY) return
    if (bar.complete) return
    stderr.write(line())
    stderr.cursorTo(0)
  }
  let throttledRender = throttle(render, 16)

  function done () {
    render()
    bar.complete = true
    stderr.write('\n')
    stderr.write(ansi.cursorShow)
  }

  bar.tick = function (inc, tokens) {
    bar.tokens = tokens
    bar.cur += inc
    bar.percent = parseFloat(bar.cur) / bar.total
    if (bar.percent > 1) bar.percent = 1
    if (bar.percent < 0) bar.percent = 0

    throttledRender()

    if (bar.cur >= bar.total) done()
  }

  return bar
}

module.exports = progress
