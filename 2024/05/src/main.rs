use std::{io, iter};

const MAX_NUM: usize = 100; // No 3-digit number appears in input

fn main() {
    // Maps number to list of numbers that cannot occur before it
    let mut successors: Vec<Vec<usize>> = iter::repeat_with(|| Vec::new()).take(MAX_NUM).collect();
    // Maps number to list of numbers that cannot occur after it
    let mut predecessors: Vec<Vec<usize>> =
        iter::repeat_with(|| Vec::new()).take(MAX_NUM).collect();
    // The list of updates
    let mut updates: Vec<Vec<usize>> = Vec::new();

    let mut is_reading_rules = true;

    for line in io::stdin().lines() {
        let text = line.unwrap();
        if text.is_empty() {
            is_reading_rules = false;
            continue;
        }

        if is_reading_rules {
            let (a, b) = text
                .split_once("|")
                .expect("Should be two numbers separated by pipe.");

            match (a.parse::<usize>(), b.parse::<usize>()) {
                (Ok(before), Ok(after)) => {
                    successors[before].push(after);
                    predecessors[after].push(before);
                }
                _ => {
                    panic!("Invalid numbers");
                }
            }
        } else {
            // Gathering page order updates
            updates.push(
                text.split(',')
                    .map(|n| n.parse::<usize>().unwrap())
                    .collect(),
            );
        }
    }

    // Part 1 & 2
    let mut p1: usize = 0;
    let mut p2: usize = 0;
    let mut has_occurred: Vec<bool>;
    let mut middle: usize;

    for mut update in updates {
        middle = update.len() / 2;
        // Invalid report if any number in successors[curr] has already occurred in list
        has_occurred = vec![false; MAX_NUM];
        let mut valid = true;
        for &curr in update.iter() {
            // Mark as having occurred
            has_occurred[curr] = true;
            // Check if any successor already occurred, making this report invalid
            if successors[curr].iter().any(|&n| has_occurred[n]) {
                valid = false;
                break;
            }
        }
        if valid {
            p1 += update[middle];
            continue;
        }
        // Invalid report
        // Re-order first half of update to make it valid
        let mut i = 0;
        while i <= middle {
            let curr = update[i];
            if let Some(j) = update.iter().rposition(|x| predecessors[curr].contains(x)) {
                if j > i {
                    // Predecessor occurs after curr, insert curr after predecessor
                    // and increment middle instead of removing curr
                    update.insert(j + 1, curr);
                    middle += 1;
                }
            }
            i += 1;
        }
        p2 += update[middle];
    }
    println!("{p1}");
    println!("{p2}");
}
