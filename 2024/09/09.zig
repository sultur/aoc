const std = @import("std");
const print = std.debug.print;

pub fn main() !void {
    // Create buffer on stack
    var buffer: [20_001]u8 = undefined;
    // Create an allocator for this buffer region
    var fba = std.heap.FixedBufferAllocator.init(&buffer);
    const allocator = fba.allocator();

    const diskmap = try allocator.alloc(u8, 20_001);
    // Dont need to free^ as it freed upon exiting function
    var reader = std.io.getStdIn().reader();
    const n_bytes = try reader.read(diskmap) - 1; // -1 to skip the newline

    // Part 1
    const c1 = calc_checksum(diskmap, n_bytes);
    // Part 2
    const c2 = calc_checksum_contig(diskmap, n_bytes);
    print("{}\n{}\n", .{ c1, c2 });
}

inline fn conv(b: u8) u8 {
    return b - 48; // Convert "0" -> 0, "1" -> 1, ...
}

inline fn min(a: u8, b: u8) u8 {
    return if (b < a) b else a;
}

/// Return sum of (a, a+1, ..., b-1, b)
inline fn sum_range(a: usize, b: usize) usize {
    return ((a + b - 1) * (b - a)) / 2;
}

fn calc_checksum(diskmap: []u8, length: usize) usize {
    var l: usize = 0; // Left index into condensed disk representation
    var r: usize = length - 1; // Right index into condensed disk representation
    var pos: usize = 0; // Current position on disk

    var lfid: usize = 0; // Leftmost file ID
    var rfid: usize = length / 2; // Rightmost file ID
    var lblocks: u8 = 0; // Number of blocks allocated for file on left OR number of blocks in empty space
    var rblocks: u8 = conv(diskmap[r]); // Number of blocks left to allocate for file on right

    var alloc: u8 = 0;
    var empty = false; // Whether diskmap[l] represent a sequence of empty blocks
    var checksum: usize = 0;

    while (l < r) {
        lblocks = conv(diskmap[l]);
        if (empty) {
            // Move from right end
            while (lblocks > 0) {
                alloc = min(lblocks, rblocks);
                checksum += rfid * sum_range(pos, pos + alloc);
                pos += alloc;
                lblocks -= alloc;
                rblocks -= alloc;
                if (rblocks == 0) {
                    r -= 2;
                    rfid -= 1;
                    rblocks = conv(diskmap[r]);
                }
            }
        } else {
            checksum += lfid * sum_range(pos, pos + lblocks);
            lfid += 1;
            pos += lblocks;
        }

        l += 1; // Advance left index
        empty = !empty; // Toggle between empty space and file on left side
    }
    if (rblocks > 0) { // Remaining rblocks
        checksum += rfid * sum_range(pos, pos + rblocks);
    }

    return checksum;
}

/// This function modifies diskmap in-place
fn calc_checksum_contig(diskmap: []u8, length: usize) usize {
    var r: usize = length - 1; // Right index into condensed disk representation
    var pos: usize = 0; // Current position on disk
    var checksum: usize = 0;

    var posmap: [20_000]usize = undefined; // Map each condensed item to a start position
    var i: usize = 0;
    while (i < length) : (i += 1) {
        posmap[i] = pos;
        pos += conv(diskmap[i]);
    }
    pos = 0;

    var rfid: usize = length / 2; // Rightmost file ID
    while (0 < r) : (r -= 2) {
        i = 1; // First gap at i=1
        // Find gap
        while (i < r) : (i += 2) {
            if (diskmap[i] >= diskmap[r]) {
                // Enough space to move file
                diskmap[i] = diskmap[i] - conv(diskmap[r]);
                checksum += rfid * sum_range(posmap[i], posmap[i] + conv(diskmap[r]));
                posmap[i] += conv(diskmap[r]);
                break;
            }
        } else {
            checksum += rfid * sum_range(posmap[r], posmap[r] + conv(diskmap[r]));
        }
        rfid -= 1;
    }

    return checksum;
}
