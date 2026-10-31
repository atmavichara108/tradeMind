---
type: map
domain: meta
created: 2026-10-31
---
# Charts — карта разборов

## Все чарты
```dataview
TABLE author, date, transcript
FROM "02_Mentor/Charts"
SORT date DESC
```

## Чарты наставника
```dataview
TABLE date, transcript
FROM "02_Mentor/Charts"
WHERE author = "TheSeparatedOne🏴"
SORT date DESC
```

## Разметки участников
```dataview
TABLE author, date
FROM "02_Mentor/Charts"
WHERE author != "TheSeparatedOne🏴"
SORT date DESC
```

## Ошибки разметки
```dataview
LIST
FROM "02_Mentor/Charts"
WHERE author != "TheSeparatedOne🏴" AND contains(file.tags, "learn_from_mistake")
```
