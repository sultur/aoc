#!/usr/bin/env guile
!#
(use-modules (srfi srfi-1))
(use-modules (ice-9 textual-ports))

(define input-file "in")

;; Fetch puzzle input and example input from files
(define input (string-trim-both (call-with-input-file input-file get-string-all)))

;; Puzzle solving ---
(define ranges
  (map (lambda (l) (cons (string->number (car l)) (string->number (cadr l))))
       (map (lambda (lo-hi) (string-split lo-hi #\-))
            (string-split input #\,))))

(define (digits n)
  "Return number of decimal digits in positive integer n."
  (let rec ((i n) (acc 1))
    (if (< i 10) acc (rec (quotient i 10) (1+ acc)))))

(define (repeat-num n k)
  "Repeat number n k times, e.g. (42 3) -> 424242."
  (let ((len (digits n)))
    (let rec ((repeats (1- k)) (shift len) (acc n))
      (if (<= repeats 0)
          acc
          (rec (1- repeats) (+ shift len) (+ acc (* n (expt 10 shift))))))))

(define (is-k-repetition? n k)
  "Return #t if n is a number repeated k>2 times."
  (let ((num-digits (digits n)))
    (and
     (> k 1)
     (= (remainder num-digits k) 0)     ; k must divide number of digits in n
     (let ((splice (remainder n (expt 10 (quotient num-digits k)))))
       (= n (repeat-num splice k))))))

(define (is-2-repetition? n) (is-k-repetition? n 2))
(define (is-any-repetition? n)
  "#t if n is composed of a number repeated at least twice."
  (let rec ((i (digits n)))
    (and (> i 1) (or (is-k-repetition? n i) (rec (1- i))))))

(define (naive test range)
  "Iterate through integers in range, return sum of integers for which test returns #t."
  (let rec ((lo (car range)) (hi (cdr range)) (acc 0))
    (if (> lo hi)
        acc
        (rec (1+ lo) hi (if (test lo) (+ acc lo) acc)))))

(define (solve-p1)
  "Solves part 1."
  (fold (lambda (r acc) (+ (naive is-2-repetition? r) acc)) 0 ranges))

(define (solve-p2)
  "Solves part 2."
  (fold (lambda (r acc) (+ (naive is-any-repetition? r) acc)) 0 ranges))

;; Display solutions to part 1 & 2

(define p1 (solve-p1))
(display p1) (newline)

(define p2 (solve-p2))
(display p2) (newline)
