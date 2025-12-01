#!/usr/bin/env guile
!#
(use-modules (srfi srfi-1))
(use-modules (ice-9 textual-ports))

(define input-file "in")

;; Fetch puzzle input and example input from files
(define input (string-trim-both (call-with-input-file input-file get-string-all)))
(define input-lines (string-split input #\newline))

;; Puzzle solving ---

;; Constants
(define left #\L)
(define start-pos 50)
(define num-dials 100)

;; Parse each line, turn into signed integer (e.g. L50 -> -50 and R37 -> 37)
(define (line->turn str) (* (if (char=? left (string-ref str 0)) -1 1) (string->number (substring str 1))))
(define turns (map line->turn input-lines))

(define (turn-dial turn pos)
  "Apply turn to dial position."
  (euclidean-remainder (+ pos turn) num-dials))

(define (zero-crossings turn pos)
  "Count how often a turn would cross 0 on dial for given dial position."
  (+ (abs (euclidean-quotient (+ pos turn) num-dials))
     (if (and (zero? pos) (< turn 0)) -1 0)
     (if (and (zero? (turn-dial turn pos)) (< turn 0)) 1 0)))

(define (turn-and-count-zero-stops turn acc)
  "Perform turn, update dial position and increment counter if the new position is 0."
  (let* ((pos (car acc))
         (zero-stops (cdr acc))
         (new-pos (turn-dial turn pos)))
    (cons new-pos (+ zero-stops (if (zero? new-pos) 1 0)))))

(define (turn-and-count-all-zeros turn acc)
  "Perform turn, update dial position and increment counter by number of times dial clicks on 0."
  (let* ((pos (car acc))
         (zero-count (cdr acc))
         (new-pos (turn-dial turn pos)))
    (cons new-pos (+ zero-count (zero-crossings turn pos)))))

(define (solve-p1)
  "Solves part 1."
  (cdr (fold turn-and-count-zero-stops (cons start-pos 0) turns)))

(define (solve-p2)
  "Solves part 2."
  (cdr (fold turn-and-count-all-zeros (cons start-pos 0) turns)))

;; Display solutions to part 1 & 2

(define p1 (solve-p1))
(display p1) (newline)

(define p2 (solve-p2))
(display p2) (newline)
