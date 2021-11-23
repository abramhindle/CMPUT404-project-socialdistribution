@heroku-cli/notifications
=========================

display notifications in Heroku CLI commands. Based on [node-notifier](https://github.com/mikaelbr/node-notifier).

[![Version](https://img.shields.io/npm/v/@heroku-cli/notifications.svg)](https://npmjs.org/package/@heroku-cli/notifications)
[![CircleCI](https://circleci.com/gh/heroku/heroku-cli-notifications/tree/master.svg?style=shield)](https://circleci.com/gh/heroku/heroku-cli-notifications/tree/master)
[![Appveyor CI](https://ci.appveyor.com/api/projects/status/github/heroku/heroku-cli-notifications?branch=master&svg=true)](https://ci.appveyor.com/project/heroku/heroku-cli-notifications/branch/master)
[![Codecov](https://codecov.io/gh/heroku/heroku-cli-notifications/branch/master/graph/badge.svg)](https://codecov.io/gh/heroku/heroku-cli-notifications)
[![Downloads/week](https://img.shields.io/npm/dw/@heroku-cli/notifications.svg)](https://npmjs.org/package/@heroku-cli/notifications)
[![License](https://img.shields.io/npm/l/@heroku-cli/notifications.svg)](https://github.com/heroku/heroku-cli-notifications/blob/master/package.json)
[![Greenkeeper badge](https://badges.greenkeeper.io/heroku/heroku-cli-notifications.svg)](https://greenkeeper.io/)

<!-- toc -->

# Usage

If `HEROKU_NOTIFICATIONS=0|false` then this will not be displayed.

```typescript
import {notify} from '@heroku-cli/notifications'
notify({
  title: 'notification title',
  message: 'notification message',
})
```

See the [node-notifier](https://github.com/mikaelbr/node-notifier) docs for more information.
