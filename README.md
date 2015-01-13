sublime-coffee-to-js
====================

Sublime plugin to convert coffeescript to javascript.

## Functions:

* Convert .coffee file to .js (keymap - `shift+alt+f`)
* Copy coffeescript to clipboard paste as javascript (keymap - `shift+alt+j`)
* Convert highlighted code snippet into javascript (keymap - `shift+alt+v`)

## Requirements:
Coffee to Javascript requires a coffee script binary to be accessible on the users path. This is commonly achieved using nodeJS and installing coffee through npm.

## Plugin Settings:

__Default settings:__

```json
    {
      "coffeeCommand": "coffee",
      // inline operations, paste, code block
      "inlineArgs": ["--no-header", "--bare"],
      // File operation only
      "fileArgs": ["--no-header",],
      "debug": false,
    }
```

##### coffeeCommand
This is the executable which is used to convert coffeescript to javascript. This can be changed to be another coffeescript executable (either on the path or absolute path).

##### inlineArgs
These are the arguements which affect the inline functions provided by this plugin. (Convert highlighted code snippet into javascript, copy coffeescript to clipboard paste as javascript).
This should be a list of strings. Default arguments will provide javascript with no header and no function wrapping.

##### fileArgs
These are the arguements which will affect the file functions provided by this plugin. (Convert .coffeescript file to .js).
This should be a list of strings. Default arguments will provide javascript with no header.


##### debug
This option prints to console the command which is executed to convert coffeescript into javascript.
