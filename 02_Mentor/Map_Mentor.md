---
type: map
domain: meta
created: 2026-10-31
---
# Наставник — карта транскриптов

## Экспортированные дни
```dataview
TABLE file.link AS "Дата", source AS "Источник"
FROM "02_Mentor/Transcripts/ExportParsed"
SORT file.name DESC
```

## Ручные транскрипты
```dataview
LIST
FROM "02_Mentor/Transcripts"
WHERE source = "manual"
SORT file.name DESC
```

## Статистика авторов экспорта
- TheSeparatedOne🏴 — наставник основной поток
- Leo Erdman, Max 🌋 Rudra — участники практики
- Ошибки участников помечаются в `08_Reflections` как обучающий материал
