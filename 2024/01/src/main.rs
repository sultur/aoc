use ahash::AHashMap;
use std::io;
use std::iter::zip;
extern crate ahash;

fn main() {
    let mut left: Vec<u64> = Vec::new();
    let mut right: Vec<u64> = Vec::new();
    let mut counter: AHashMap<u64, u64> = AHashMap::new();

    for line in io::stdin().lines() {
        for (i, num) in line
            .expect("Should be able to read line from stdin")
            .split_whitespace()
            .enumerate()
        {
            let number = num.parse().expect("Should be number in input");
            if i == 0 {
                left.push(number);
                counter.entry(number).or_insert(0);
            } else {
                right.push(number);
                counter.entry(number).and_modify(|x| *x += 1).or_insert(1);
            }
        }
    }
    left.sort();
    right.sort();

    // Part 1
    // println!(
    //     "{}",
    //     zip(left, right).map(|(l, r)| l.abs_diff(r)).sum::<u64>()
    // );

    // Part 2
    println!("{}", left.iter().fold(0, |acc, n| acc + n * counter[n]));
}
