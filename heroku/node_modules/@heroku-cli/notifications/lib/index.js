"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const NodeNotifier = require("node-notifier");
const path = require("path");
function notify(notification = {}, callback) {
    if (!notification.force && ['0', 'false'].includes(process.env.HEROKU_NOTIFICATIONS))
        return;
    return NodeNotifier.notify(Object.assign({ title: 'Heroku CLI', icon: path.join(__dirname, '../assets/heroku.png'), appName: 'Microsoft.Windows.ShellExperienceHost_cw5n1h2txyewy!App' }, notification), callback);
}
exports.notify = notify;
