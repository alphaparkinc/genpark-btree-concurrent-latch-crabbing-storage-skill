from client import BPlusTreeEngine

def main():
    print("=== Testing B+ Tree Concurrent Latch Crabbing Storage Engine ===")
    bpt = BPlusTreeEngine(order=4)
    items = [("k10", 100), ("k20", 200), ("k5", 50), ("k15", 150), ("k30", 300), ("k25", 250)]
    for k, v in items:
        bpt.insert(k, v)

    val, latches = bpt.search("k20")
    print(f"Key k20 => {val}, Latch path: {latches}")
    assert val == 200
    assert len(latches) >= 1
    missing, _ = bpt.search("k999")
    assert missing is None
    print("=== All tests passed successfully! ===")

if __name__ == "__main__":
    main()
