package main

import (
	"bufio"
	"fmt"
	"os"
	"slices"
	"strconv"
	"strings"
)

func main() {
	scanner := bufio.NewScanner(os.Stdin)

	report_count := 0
	c := make(chan bool)
	for {
		scanner.Scan()
		line := scanner.Text()
		if len(line) == 0 {
			break
		}
		// Convert to list of numbers
		raw_nums := strings.Fields(line)
		nums := make([]int, len(raw_nums))
		for i, n := range raw_nums {
			nums[i], _ = strconv.Atoi(n)
		}

		report_count++
		go is_report_safe(nums, c)
	}

	safe_reports := 0
	for ; report_count > 0; report_count-- {
		if <-c {
			safe_reports++
		}
	}
	fmt.Println(safe_reports)
}

func is_report_safe(nums []int, c chan bool) {
	report_is_safe := true
	i := check_report(nums)
	if i >= 0 {
		report_is_safe = false
		// Inefficient
		for j := max(i-2, 0); j < min(i+1, len(nums)); j++ {
			if check_report(slices.Concat(nums[:j], nums[j+1:])) < 0 {
				report_is_safe = true
				break
			}
		}
	}
	c <- report_is_safe
}

func check_report(nums []int) int {
	is_increasing := nums[0] < nums[1]

	for i := 1; i < len(nums); i++ {
		prev := nums[i-1]
		curr := nums[i]
		diff := curr - prev
		if !((diff > 0 && diff < 4 && is_increasing) ||
			(diff < 0 && diff > -4 && !is_increasing)) {
			// fmt.Println(nums, "unsafe at index", i)
			return i
		}
	}
	return -1
}
