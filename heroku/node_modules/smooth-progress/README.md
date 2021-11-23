pixel-by-pixel progress bar

![demo](https://raw.github.com/dickeyxxx/smooth-progress/master/demo.gif)

Usage
-----

```js
'use strict';
let https    = require('https');
let progress = require('smooth-progress');

https.get('https://raw.githubusercontent.com/dickeyxxx/smooth-progress/master/demo.gif', function (rsp) {
  let bar = progress({
    tmpl: 'Downloading... :bar :percent :eta',
    width: 25,
    total: parseInt(rsp.headers['content-length']),
  });
  rsp.on('data', (chunk) => bar.tick(chunk.length));
});
```
