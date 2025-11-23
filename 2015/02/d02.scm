#!/usr/bin/env guile
!#
(use-modules (srfi srfi-1))
(use-modules (ice-9 textual-ports))
(use-modules (ice-9 match))

(define (get-input)
  "Reads all text from './in' or from different file if specified as CLI argument."
  (string-trim-both
   (call-with-input-file
       (if (null? (cdr (program-arguments))) "./in" (car args))
     get-string-all)))

(define input (get-input))
(define input-lines (string-split input #\newline))
(define dimensions (map (lambda (line) (map string->number (string-split line #\x))) input-lines))

(define (side-areas l w h) (list (* l w) (* w h) (* h l)))
(define (side-circumferences l w h) (list (+ l w l w) (+ w h w h) (+ l h l h)))
(define (volume l w h) (* l w h))

(define (line->wrap line)
  "Convert line in input to feet of wrapping paper."
  (match-let* (((l w h) line)
               ((sa sb sc) (side-areas l w h)))
    (+ (* 2 sa) (* 2 sb) (* 2 sc) (min sa sb sc))))

(define (line->ribbon line)
  "Convert line to feet of ribbon."
  (match-let* (((l w h) line)
               ((pa pb pc) (side-circumferences l w h)))
    (+ (volume l w h) (min pa pb pc))))

(define part1
  (fold + 0 (map line->wrap dimensions)))

(define part2
  (fold + 0 (map line->ribbon dimensions)))


(display part1) (newline)
(display part2) (newline)

(cons part1 part2)
