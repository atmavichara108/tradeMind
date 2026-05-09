---
type: map
domain: meta
created: 2026-05-07
---
# Плейбуки — карта

Протоколы действий: риск, фиксация, поведение.

```dataview
TABLE status, domain
FROM "06_Playbooks"
SORT file.name ASC

```
### Открытые вопросы по правилам
```dataview
LIST
FROM "06_Playbooks"
WHERE open_questions

```
