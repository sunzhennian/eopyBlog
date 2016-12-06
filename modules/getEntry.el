#!/usr/bin/emacs --script 


(require 'ox-publish)

(defun s-match (regexp s &optional start)
  "When the given expression matches the string, this function returns a list
of the whole matching string and a string for each matched subexpressions.
If it did not match the returned value is an empty list (nil).
When START is non-nil the search will start at that index."
  (save-match-data
    (if (string-match regexp s start)
        (let ((match-data-list (match-data))
              result)
          (while match-data-list
            (let* ((beg (car match-data-list))
                   (end (cadr match-data-list))
                   (subs (if (and beg end) (substring s beg end) nil)))
              (setq result (cons subs result))
              (setq match-data-list
                    (cddr match-data-list))))
          (nreverse result)))))

(defun s-trim-left (s)
  "Remove whitespace at the beginning of S."
  (save-match-data
    (if (string-match "\\`[ \t\n\r]+" s)
        (replace-match "" t t s)
      s)))

(defun s-trim-right (s)
  "Remove whitespace at the end of S."
  (save-match-data
    (if (string-match "[ \t\n\r]+\\'" s)
        (replace-match "" t t s)
      s)))

(defun s-trim (s)
  "Remove whitespace at the beginning and end of S."
  (s-trim-left (s-trim-right s)))

(defun s-replace (old new s)
  "Replaces OLD with NEW in S."
  (replace-regexp-in-string (regexp-quote old) new s t t))

(defun org-html-get-content-without-toc (org-html)
 (let ((toc-regexp "<div id=\"table-of-.*\">\\(.\\|\n\\)*?</div>")
        (text-toc-regexp "<div id=\"text-table-of-.*\">\\(.\\|\n\\)*?</div>"))
    (s-trim
     (reduce
      #'(lambda (regexp string)
          (replace-regexp-in-string regexp "" string))
      (list toc-regexp text-toc-regexp)
      :initial-value org-html
      :from-end t)))
)

(defun file-to-string (file)
  (with-temp-buffer
    (insert-file-contents file)
(buffer-string)))

(defun eob-get-entry (org-file)
  (interactive)
  (let ((file-all (file-to-string org-file))
        (more-regexp "#\\+Title.*\\(.\\|\n\\)*?<!-- more -->"))
    (setq file-all (s-replace "toc:t" "toc:nil" file-all))
    (setq result (car (s-match more-regexp file-all)))
    (if (equal result nil)
     (with-temp-buffer
      (insert (substring file-all 0 500))
      (org-html-export-as-html nil nil nil t nil)
      (setq org-html (substring-no-properties (buffer-string)))
      (message "%s" org-html)
     )
     (with-temp-buffer
       (insert result)
       (org-html-export-as-html nil nil nil t nil)
      (setq org-html (substring-no-properties (buffer-string)))
      (message "%s" org-html)
     )
    )
    )
)

(eob-get-entry (elt argv 0))
