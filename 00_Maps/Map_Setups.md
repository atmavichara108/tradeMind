---
type: map
domain: meta
created: 2026-05-07
---
# Сетапы — карта

Конкретные торговые ситуации с правилами входа/стопа/целей.

## Все сетапы
```dataview
TABLE timeframe, market_context, status
FROM "05_Setups"
WHERE type = "setup"
SORT file.name ASC
```
## По таймфрейму

### LTF (5m-15m)
```dataview
LIST
FROM "05_Setups"
WHERE contains(timeframe, "5m") OR contains(timeframe, "15m")

```
### MTF (1h-4h)
```dataview
LIST
FROM "05_Setups"
WHERE contains(timeframe, "1h") OR contains(timeframe, "4h")

```
### HTF (1D+)
```dataview
LIST
FROM "05_Setups"
WHERE contains(timeframe, "1D") OR contains(timeframe, "1W")

```
## Связанные разборы
```dataview
LIST
FROM "07_Canvases/Setups"
SORT file.mtime DESC
LIMIT 10

```

