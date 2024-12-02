package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {
	scanner := bufio.NewScanner(os.Stdin)

	var i = 0
	c := make(chan bool)
	for {
		scanner.Scan()
		line := scanner.Text()
		if len(line) == 0 {
			break
		}
		i++
		// Start parsing line
		go is_report_safe(line, c)
	}

	var safe_lines = 0
	for ; i > 0; i-- {
		if <-c {
			safe_lines++
		}
	}
	fmt.Println(safe_lines)
}

func is_report_safe(line string, c chan bool) {
	var nums = strings.Split(line, " ")
	var prev_num, _ = strconv.ParseInt(nums[0], 10, 0)

	var is_increasing = false
	var is_decreasing = false
	var is_safe = true

	var curr_num int64
	var diff int64
	for i := 1; i < len(nums); i++ {
		curr_num, _ = strconv.ParseInt(nums[i], 10, 0)
		diff = prev_num - curr_num
		if diff == 0 || diff < -3 || diff > 3 {
			is_safe = false
			break
		} else if diff > 0 {
			is_increasing = true
		} else {
			is_decreasing = true
		}
		if is_increasing && is_decreasing {
			is_safe = false
			break
		}
		prev_num = curr_num
	}

	// fmt.Println(line, is_safe)
	c <- is_safe
}
