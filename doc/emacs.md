# Emacs memo

## Modes

### MELPA

```
;; INSTALL PACKAGES
;; --------------------------------------

(require 'package)

(add-to-list 'package-archives
       '("melpa" . "http://melpa.org/packages/") t)

(package-initialize)
(when (not package-archive-contents)
  (package-refresh-contents))

(defvar myPackages
  '(pkg1
    pkg2
    pkg3...))

(mapc #'(lambda (package)
    (unless (package-installed-p package)
      (package-install package)))
      myPackages)
```

### Installed modes

 * elpy
 * flycheck
 * ac-php
 * php-mode
 * company
 * company-php
 * py-autopep8
 * material-theme

### elpy, flycheck, py-autopep8

Install `python-jedi` for completion, `python-autopep8` for pep8 and `flake8` for flycheck.

### markdown-mode

Install `markdown`

## Shortcuts

Shortcut   | Use for
-----------|-----------
`C-x C-f`  | Open new file
`C-x C-c`  | Quit
`C-x C-s`  | Save
`C-spc`    | Select text
`C-w`      | Cut
`M-w`      | Copy
`C-y`      | Paste
`C-n`      | Jump to next line
`C-p`      | Jump to previous line
`C-x b <name>`| Create/go to buffer
`C-x C-b`     | List buffers
`C-x k <name>`| Kill buffer
`C-x 2` | Horizontal window split
`C-x 3` | Vertical window split
`C-o`   | Select another window
`C-e`   | Move to EOF
`C-a`   | Move to line start
`M-g g` | Move to line number [input]
`M-g c` | Mot to char number [input]
`M-<`   | Move to buffer start
`M->`   | Move to buffer end
