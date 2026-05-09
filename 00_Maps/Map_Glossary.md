---
type: map
domain: meta
created: 2026-05-07
---
# Глоссарий — карта терминов

Все атомарные термины из языка наставника и базовой матчасти.

## По освоенности

### Active (понимаю и применяю)
```dataview
LIST
FROM "03_Glossary"
WHERE type = "glossary" AND mastery = "applied"
SORT file.name ASC
```

### Known (понимаю)
```dataview
LIST
FROM "03_Glossary"
WHERE type = "glossary" AND mastery = "known"
SORT file.name ASC

```
### Заглушки и непонятное
```dataview
LIST
FROM "03_Glossary"
WHERE type = "glossary" AND (mastery = "unclear" OR status = "stub")
SORT file.name ASC

```
## По домену

### TA (технический анализ)
```dataview
LIST
FROM "03_Glossary"
WHERE domain = "TA"
SORT file.name ASC

```
### Risk (риск-менеджмент)
```dataview
LIST
FROM "03_Glossary"
WHERE domain = "Risk"
SORT file.name ASC

```
### Psychology
```dataview
LIST
FROM "03_Glossary"
WHERE domain = "Psychology"
SORT file.name ASC

```
