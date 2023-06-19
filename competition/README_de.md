## Datenanalyse der SC2-Weltmeisterschaft

*Read this in: [RU](README_ru.md), [DE](README_de.md), [EN](README.md)*

Die StarCraft 2-Weltmeisterschaft in Kattowitz ist kürzlich zu Ende gegangen. Neben den Spielen selbst hat sie eine interessante Aufgabe für die Datenanalyse hinterlassen. Die Organisatoren haben großartige Arbeit geleistet und für jeden Spieler eine Karte mit einer numerischen Bewertung ihrer Parameter erstellt (zum Beispiel Geschwindigkeit). Dementsprechend ist es interessant herauszufinden, und die Frage zur Analyse lautet genau so: Welcher der Parameter korreliert am besten mit dem Platz des Spielers.

## Eingabedaten

Als Eingabe wird eine CSV-Datei mit Teilnehmerdaten eingereicht. Ein Beispiel für eine Datei befindet sich im Ordner "data". 

## Выходные данные

Eine sortierte Liste von Bewertungen von den besten bis zu den schlechtesten für alle möglichen Parameter.

## Algorithmus

Für jeden Spieler und jeden Parameter haben wir eine Reihe von Datenpunkten (Platzierung des Spielers, Parameterwert). Wir werden die Korrelation auf zwei Arten berechnen: anhand der absoluten Werte (Pearson-Methode) und anhand der Ränge (Spearman-Methode). In beiden Fällen liegt das Ergebnis im Bereich von (-1, 1) mit einem p-Wert, der das Vertrauensniveau in die Ergebnisse anzeigt.

## Ergebnisse

```
parameter          Pear   PearP  Spear  SpearP
['place',          0.99,  0.00,  1.00,  0.00]
['versatility',   -0.65,  0.00,  0.66,  0.00]
['avg',           -0.53,  0.01,  0.49,  0.01]
['multitasking',  -0.46,  0.02,  0.49,  0.02]
['speed',         -0.45,  0.03,  0.49,  0.02]
['offense',       -0.42,  0.04,  0.46,  0.02]
['mechanics',     -0.5,   0.01,  0.43,  0.04]
['ept_points',    -0.34,  0.11,  0.33,  0.11]
['defense',       -0.36,  0.08,  0.33,  0.12]

```

## Ergebnisanalyse

TBD
