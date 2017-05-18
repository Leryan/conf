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
`C-x C-c`  | Quit
-----------|-----------
`C-x C-s`  | Save
-----------|-----------
