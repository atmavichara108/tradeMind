---
type: map
domain: meta
created: 2026-05-07
---
# Концепции метода — карта

Принципы и законы метода наставника. Не атомарные термины, а смысловые блоки.

## Активные концепции
```dataview
TABLE status, mastery
FROM "04_Concepts"
WHERE type = "concept"
SORT file.mtime DESC
```
## Тезисы ожидающие раскрытия
```dataview
LIST
FROM "04_Concepts"
WHERE status = "draft" OR contains(tags, "awaiting-examples")

```
## Открытые вопросы наставнику
```dataview
LIST file.link + ": " + open_questions
FROM "04_Concepts"
WHERE open_questions

```

