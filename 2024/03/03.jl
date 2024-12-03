mul_re = r"mul\((\d+),(\d+)\)" 
dont_do_re = r"don't\(\).*?do\(\)"

text = join(split(join(readlines()), dont_do_re))
numbers = map(eachmatch(mul_re, text)) do m
    parse(Int64, m.captures[1]) * parse(Int64, m.captures[2])
end

println(sum(numbers))

