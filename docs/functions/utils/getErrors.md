# $getErrors

Returns a semicolon-separated list of all non-fatal errors that occurred during rendering when `strict=false`.

## Syntax
`$getErrors[]`

## Example
```bash
$createCanvas[400;200;white;strict=false]
$drawText[...invalid params...]
$drawText[10;10;Status: $getErrors[];red;12]
```
