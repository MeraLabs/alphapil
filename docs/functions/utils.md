# Utils & Logic

Helper functions for calculations and conditional rendering.

| Function | Syntax |
| :--- | :--- |
| **math** | `$math[expression]` |
| **if** | `$if[condition;true_val;false_val]` |
| **random** | `$random[min;max]` |

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
