#!/usr/bin/emacs --script 


(require 'ox-publish)
(defun eob-get-content(org-file)
  (interactive)
  (with-temp-buffer
    (insert-file-contents org-file)
    (org-html-export-as-html nil nil nil t nil)
    (setq org-html (substring-no-properties (buffer-string)))
    (kill-buffer "*Org HTML Export*")
    (setq content org-html)
    (message "%s" content)
   )
)

(eob-get-content (elt argv 0))
