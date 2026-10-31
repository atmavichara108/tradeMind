---
type: map
domain: meta
created: 2026-10-31
---
# Reflections — карта

## Вопросы наставнику
```dataview
LIST
FROM "08_Reflections"
WHERE question_for_mentor = true
SORT created ASC
```

## Ошибки участников
```dataview
LIST
FROM "08_Reflections"
WHERE learn_from_mistake = true
SORT file.name ASC
```

## Все рефлексии
```dataview
LIST
FROM "08_Reflections"
SORT created DESC
```

