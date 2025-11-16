#!/usr/bin/env guile
!#
(use-modules (ice-9 textual-ports))

(define (get-input)
  "Reads all text from STDIN or from a file if a filename was given as command-line argument."
  (let ((args (cdr (program-arguments))))
    (string-trim-both (if (null? args)
                          (get-string-all (current-input-port))
                          (call-with-input-file (car args) get-string-all)))))

(define input (get-input))

(define (paren->int c)
  "Convert '(' to 1 and ')' to -1."
  (cond
   ((char=? c #\( ) 1)
   ((char=? c #\) ) -1)
   (else 0)))

(define (part1 text)
  "Solves part 1."
  (string-fold (lambda (c acc) (+ acc (paren->int c))) 0 text))

(define (part2 text)
  "Solves part 2."
  (call/cc
   (lambda (exit)
     (string-fold
      (lambda (c aip) ; The accumulator is now a pair (acc . index)
        (let ((a (+ (car aip) (paren->int c)))
              (i (1+ (cdr aip))))
          (if (< a 0)
              (exit (1- i))
              (cons a i))))
      (cons 0 1)
      text))))

(display (part1 input)) (newline)
(display (part2 input)) (newline)


