# Suggestions from ChatGPT

## general

- Add support for syntax highlighting and code completion to make it easier for users to write and read code.
- Add support for multiple tabs or windows to allow users to edit multiple files at once.
- Add a search and replace function to make it easier to find and replace specific text within a file.
- Add support for saving and loading files in popular formats such as TXT, CSV, and JSON.
- Implement a line numbering feature to make it easier to reference specific lines within a file.
- Add a customizable interface with support for different color schemes and font sizes.
- Implement support for undo and redo actions to make it easier to fix mistakes and experiment with different edits.
- Add a built-in terminal or command prompt to allow users to run shell commands directly within the editor.
- Implement support for collaboration and real-time editing with other users.
- Add support for plugins or extensions to allow users to customize the editor and add additional features.

## more generic

--backup: create a backup copy of the file being edited
--readonly: open the file in read-only mode, without allowing changes to be saved
--find \<string>: search for the specified string within the file
--replace \<old> \<new>: replace occurrences of old with new within the file
--goto \<line>: go to the specified line number in the file
--sort: sort the lines of the file alphabetically or numerically
--undo: undo the last change made to the file
--help-macros: display a list of available macros and their usage
--load-defaults: load default settings for the editor

## coding specific

--indent \<n>: automatically indent new lines by n spaces
--line-numbers: display line numbers in the editor
--syntax \<language>: highlight syntax for the specified programming language
--highlight-matching: highlight matching brackets or quotes

## Scenarios where edlin could be better than full screen.

- A very large text file that is too big to open in a full-screen editor without causing performance issues
- A file that is being edited over a slow network connection, where using a full-screen editor would be impractical
- A file that contains sensitive or confidential information, and where the user wishes to avoid leaving temporary files or backups on the system
- A file that requires precise control over line endings or whitespace, and where a full-screen editor might make unwanted changes
- A file that is being edited from a remote terminal or command line, where a full-screen editor might not be available
- A file that is part of a larger project, and where the user wants to edit a specific portion of the file without loading the entire thing into memory
- A file that is being edited as part of a script or automated process, and where the user wants to use edlin as part of a larger workflow
- A file that is being edited from a system with limited resources, where using a full-screen editor might not be feasible
- A file that is being edited from a system with a small display, where using a full-screen editor might not be practical
- A file that is being edited by multiple users simultaneously, and where using edlin can provide a simple and straightforward way to make changes without conflicts.
