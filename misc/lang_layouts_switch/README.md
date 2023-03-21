# Cyclical and Acyclical Language Switching

*Read this in: [RU](README_ru.md), [DE](README_de.md), [EN](README.md)*

## Problem

Sometimes it's necessary to have multiple keyboard layouts and quickly switch between them. The easiet way is to set up cyclical language switching, and that's enough for everyday life. However, sometimes you might want to have the ability to select the desired language and it can be done in Linux in different ways.

Tested in Linux Mint.

## Instruction

## Prerequisite

First, let's see what we already have in the system. It might be different, but will be like this:

```
setxkbmap -query
rules:      evdev
model:      pc105
layout:     de,us,ru
options:    terminate:ctrl_alt_bksp,grp:ctrl_shift_toggle

```

Here are three keyboard layouts swtiched by pressing ctrl+shift (and a key combination for the current session termination).

To set these options, you need to run two commands (the first one clears old options):

```
setxkbmap -option; setxkbmap -layout de,us,ru -option terminate:ctrl_alt_bksp,grp:ctrl_shift_toggle

```

Now we have everything for implementation.

## Configuration

Go to Keyboard -> Applications shortcuts, set the the desired key combination with this command:

```
sh -c "setxkbmap -option; setxkbmap -layout de,us,ru -option terminate:ctrl_alt_bksp,grp:ctrl_shift_toggle"

```

put the language you need in the first position. For example, the command for switching to the US layout with ctrl+1:

```
sh -c "setxkbmap -option; setxkbmap -layout us,ru,de -option terminate:ctrl_alt_bksp,grp:ctrl_shift_toggle"

```

When you press ctrl+1, the following will happen: old options will be cleared, new ones will be applied, and the layout will be switched to the first language in the list.

## Result

As a result, you can easily and quick assign and change keyboard settings.

## Note

1. Setxkbmap settings in this case are not permanent, so if something went wrong, you could just restart the user session or OS.
2. In some cases, with confiuration like "setxkbmap -layout de", hotkeys (e.g., ctrl+c) stop working, and adding the US layout will help: "setxkbmap -layout de,us".

