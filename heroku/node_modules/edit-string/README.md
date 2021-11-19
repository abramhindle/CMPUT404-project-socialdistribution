edit-string
===========

```js
const edit = require('edit-string')

async function run () {
  // open 'foo' in $EDITOR
  let s = await edit('foo')
  console.dir(s)
}
run()
```
