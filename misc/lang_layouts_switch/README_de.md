# Zyklisches und azyklisches Umschalten von Sprachen

*Read this in: [RU](README_ru.md), [DE](README_de.md), [EN](README.md)*

## Problem

Manchmal ist es notwendig, mehrere Tastaturbelegungen zu haben und schnell dazwischen umzuschalten. In der Regel ist es am einfachsten, zyklisches Sprachumschalten einzurichten, und das ist für den Alltag ausreichend. Manchmal wollen wir eine Möglichkeit haben, die Sprache genau auszuwählen, dies kann man in Linux auf verschiedene Weise erreichen.

Getestet in Linux Mint.

## Anleitung

## Vorbereitung

Zuerst lass uns sehen, was wir schon im System haben. Es kann unterschiedlich sein, ungefähr ist es aber so:

```
setxkbmap -query
rules:      evdev
model:      pc105
layout:     de,us,ru
options:    terminate:ctrl_alt_bksp,grp:ctrl_shift_toggle

```

Hier sind drei Tastaturbelegungen, die durch Strg+Umschalttaste zyklisch durchgeschaltet werden (plus eine Tastenkombination, um die aktuelle Sitzung zu beenden).

Um diese Optionen festzulegen, müssen wir zwei Befehle ausführen, wo der erste die alten Optionen löscht:

```
setxkbmap -option; setxkbmap -layout de,us,ru -option terminate:ctrl_alt_bksp,grp:ctrl_shift_toggle

```

Jetzt haben wir alles für die Umsetzung.

## Konfiguration

Gehen wir zu Tastatur -> Anwendungsverknüpfungen und legen wir die gewünschte Tastenkombination für Sprache fest (hier für de):

```
sh -c "setxkbmap -option; setxkbmap -layout de,us,ru -option terminate:ctrl_alt_bksp,grp:ctrl_shift_toggle"

```
Zum Beispiel: um das US-Layout mit Strg+1 zu aktivieren, würde der Befehl so aussehen:

```
sh -c "setxkbmap -option; setxkbmap -layout us,ru,de -option terminate:ctrl_alt_bksp,grp:ctrl_shift_toggle"

```
Dann wird jedes Mal, wenn wir Strg+1 drücken, folgendes passieren: die alten Optionen werden gelöscht, neue werden angewendet, und das Layout wechselt zur ersten Sprache in der Liste.

## Ergebnis

Als Ergebnis können wir Tastatureinstellungen einfach und flexibel zuweisen und ändern. 

## Hinweis

1. Die Setxkbmap-Einstellungen werden in diesem Fall nicht gespeichert. Wenn die Experimente zu weit gingen sind, starten Sie einfach die Benutzersitzung oder das gesamte Betriebssystem neu.
2. In einigen Fällen, zum Beispiel bei der Konfiguration von "setxkbmap -layout de", hören Hotkeys (z.B. Strg+C) auf zu funktionieren. Hier hilft das Hinzufügen des US-Layouts: "setxkbmap -layout de,us".

