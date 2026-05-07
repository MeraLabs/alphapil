# Examples

Here are some complete examples of what you can build with AlphaPIL.

## Discord Rank Card

This example demonstrates how to use variables, shapes, and images to create a profile card.

```bash
# Set up variables
$setVar[name;{name}]
$setVar[xp;{xp}]
$setVar[level;{level}]
$setVar[rank;{rank}]

# Create canvas
$createCanvas[400;200;#2C3E50]

# Draw background and border
$drawRect[10;10;380;180;#34495E;#1ABC9C;none;2]

# Draw user info
$drawText[200;40;$toUpper[{name}];white;20;center]
$drawText[200;80;Level: {level};white;16;center]
$drawText[200;110;XP: {xp};white;16;center]
$drawText[200;140;Rank: {rank};gold;14;center]

# Draw avatar
$if[{avatar_url};$drawImage[20;20;{avatar_url};60;60;circle=true];]

# Save output
$save[rank_card.png]
```

## Gradient Text Banner

```bash
$createCanvas[600;150;#000000]
$drawTextGradient[ALPHAPIL;300;75;60;red;blue;bold;center]
$drawRect[10;10;580;130;none;white;none;1]
$save[banner.png]
```
