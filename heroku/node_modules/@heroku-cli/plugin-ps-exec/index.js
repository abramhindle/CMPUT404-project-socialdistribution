'use strict';
exports.topic = {
  name: 'ps'
};

exports.commands = [
  require('./commands/ssh.js')('ps', 'exec'),
  require('./commands/socks.js')('ps', 'socks'),
  require('./commands/port.js')('ps', 'forward'),
  require('./commands/copy.js')('ps', 'copy')
];
