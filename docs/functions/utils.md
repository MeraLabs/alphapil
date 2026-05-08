# Utils & Logic

Helper functions for calculations and conditional rendering.

| Function | Syntax |
| :--- | :--- |
| **math** | `$math[expression]` |
| **if** | `$if[condition;true_val;false_val]` |
| **random** | `$random[min;max]` |
| **length** | `$length[text]` |
| **replace** | `$replace[text;old;new]` |
| **substring** | `$substring[text;start;end]` |
| **split** | `$split[text;separator]` |
| **join** | `$join[separator;item1;item2;...]` |
| **getHex** | `$getHex[color_name]` |

## Examples

### Dynamic Positioning
```bash
$setVar[margin;20]
$setVar[textX;$math[{margin} + 10]]
$drawText[{textX};50;Indented Text;white;12]
```

### Random Elements
```bash
$setVar[randVal;$random[1;10]]
$if[{randVal} > 5;$drawCircle[100;100;50;green];$drawCircle[100;100;50;red]]
```
