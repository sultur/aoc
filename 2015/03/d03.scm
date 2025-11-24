#!/usr/bin/env guile
!#
(use-modules (srfi srfi-1)) ; For folding
(use-modules (ice-9 textual-ports)) ; For reading and writing to files

(define input-file "in")

;; Fetch puzzle input and example input from files
(define input (string-trim-both
               (if (file-exists? input-file) (call-with-input-file input-file get-string-all) "")))
;; (define input-lines (string-split input #\newline))
(define input-chars (string->list input))

;; Puzzle solving
(define (char->move c)
  (cond
   ((char=? c #\^) '(0 . 1))
   ((char=? c #\>) '(1 . 0))
   ((char=? c #\v) '(0 . -1))
   ((char=? c #\<) '(-1 . 0))))

(define (add-coords c1 c2) (cons (+ (car c1) (car c2)) (+ (cdr c1) (cdr c2))))

(define (moves->coordinates moves)
  (reverse
   (let chart-positions ((pos (cons 0 0))
                         (remaining moves)
                         (li '()))
     (if (null? remaining)
         (cons pos li)                   ; No chars left
         (chart-positions
          (add-coords pos (char->move (car remaining)))
          (cdr remaining)
          (cons pos li))))))

(define (solve-p1)
  "Solves part 1."
  (length (delete-duplicates (moves->coordinates input-chars))))

(define (even-indices li)
  (unfold
   (lambda (seed) (>= seed (length li)))
   (lambda (seed) (list-ref li seed))
   (lambda (seed) (+ seed 2))
   0))

(define (solve-p2)
  "Solves part 2."
  (let ((santa-moves (moves->coordinates (even-indices input-chars)))
        (robo-moves (moves->coordinates (even-indices (cdr input-chars)))))
    (length (delete-duplicates (append santa-moves robo-moves)))))

;; Display solutions to part 1 & 2

(define p1 (solve-p1))
(display p1) (newline)

(define p2 (solve-p2))
(display p2) (newline)

