#!/usr/bin/env guile
!#
(use-modules (srfi srfi-1))
(use-modules (ice-9 textual-ports))
(use-modules (ice-9 match))

(define input-file "in")

;; Fetch puzzle input and example input from files
(define input (string-trim-both (call-with-input-file input-file get-string-all)))
(define input-lines (string-split input #\newline))

;; Puzzle solving ---
(define (digit->integer d) (- (char->integer d) 48))
(define digit-lists
  (map (lambda (line) (map digit->integer (string->list line))) input-lines))

(define (find-largest-in-range digits end)
  "Find largest digit before index end."
  (let rec ((li digits) (i 0) (largest 0) (largest-i 0))
    (cond
     ((or (null? li) (>= i end)) (cons largest largest-i))
     ((< largest (car li)) (rec (cdr li) (1+ i) (car li) i)) ; new largest found
     (else (rec (cdr li) (1+ i) largest largest-i)))))

(define (largest-n-digit-number digits n)
  "Construct the largest possible n digit number from an ordered list of digits."
  (if (<= n 0) 0
      (match-let* ((n-1 (1- n))
                   ((largest . largest-i) (find-largest-in-range digits (- (length digits) n-1)))
                   (remaining (list-tail digits (1+ largest-i))))
        (+ (* largest (expt 10 n-1))
           (largest-n-digit-number remaining n-1)))))

(define (solve-p1)
  "Solves part 1."
  (reduce + 0 (map (lambda (d) (largest-n-digit-number d 2)) digit-lists)))

(define (solve-p2)
  "Solves part 2."
  (reduce + 0 (map (lambda (d) (largest-n-digit-number d 12)) digit-lists)))

;; Display solutions to part 1 & 2

(define p1 (solve-p1))
(display p1) (newline)

(define p2 (solve-p2))
(display p2) (newline)
