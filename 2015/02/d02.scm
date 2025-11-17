#!/usr/bin/env guile
!#
(use-modules (srfi srfi-1))
(use-modules (ice-9 textual-ports))
(use-modules (ice-9 match))

(define (get-input)
  "Reads all text from STDIN or from a file if a filename was given as command-line argument."
  (let ((args (cdr (program-arguments))))
    (string-trim-both (if (null? args)
                          (get-string-all (current-input-port))
                          (call-with-input-file (car args) get-string-all)))))

(define input (get-input))
(define input-lines (string-split input #\newline))

(define (dimensions line) (map string->number (string-split line #\x)))
(define (side-areas l w h) (list (* l w) (* w h) (* h l)))
(define (side-circumferences l w h) (list (+ l w l w) (+ w h w h) (+ l h l h)))
(define (volume l w h) (* l w h))

(define (line->wrap line)
  "Convert line in input to feet of wrapping paper."
  (match-let* (((l w h) (dimensions line))
               ((sa sb sc) (side-areas l w h)))
    (+ (* 2 sa) (* 2 sb) (* 2 sc) (min sa sb sc))))

(define (line->ribbon line)
  "Convert line to feet of ribbon."
  (match-let* (((l w h) (dimensions line))
               ((pa pb pc) (side-circumferences l w h)))
    (+ (volume l w h) (min pa pb pc))))

(define (part1 input)
  "Solves part 1."
  (fold + 0 (map line->wrap input)))

(define (part2 input)
  "Solves part 2."
  (fold + 0 (map line->ribbon input)))

(display (part1 input-lines)) (newline)
(display (part2 input-lines)) (newline)

