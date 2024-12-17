import re
import sys

mul_re = re.compile(r"mul\((\d+),(\d+)\)")
dont_do_re = re.compile(r"don't\(\).*?do\(\)", flags=re.DOTALL)

text = sys.stdin.read()

# Part 1
print(sum(int(m.group(1)) * int(m.group(2)) for m in mul_re.finditer(text)))

# Part 2
text = " ".join(dont_do_re.split(text))
print(sum(int(m.group(1)) * int(m.group(2)) for m in mul_re.finditer(text)))

