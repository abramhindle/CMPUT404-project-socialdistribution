'use strict'
var exec = require('./lib/exec')
var ssh = require('./lib/ssh')

exports.createSocksProxy = exec.createSocksProxy
exports.checkStatus = exec.checkStatus
exports.initFeature = exec.initFeature
exports.updateClientKey = exec.updateClientKey

exports.socksv5 = ssh.socksv5
exports.connect = ssh.connect
exports.ssh = ssh.ssh
exports.scp = ssh.scp
exports.buildCommand = ssh.buildCommand
