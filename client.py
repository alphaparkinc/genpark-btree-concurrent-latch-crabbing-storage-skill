class BPlusTreeNode:
    def __init__(self, is_leaf=False):
        self.is_leaf = is_leaf
        self.keys = []
        self.children = []
        self.next = None

class BPlusTreeEngine:
    """
    B+ Tree storage engine with latch crabbing emulation,
    multi-level routing, and range-scannable leaf nodes.
    """
    def __init__(self, order=4):
        self.root = BPlusTreeNode(is_leaf=True)
        self.order = order

    def search(self, key):
        curr = self.root
        latches = ["HOLD_READ_ROOT"]
        while not curr.is_leaf:
            idx = 0
            while idx < len(curr.keys) and key >= curr.keys[idx]:
                idx += 1
            latches.append(f"CRAB_READ_CHILD_{idx}")
            curr = curr.children[idx]
        for i, k in enumerate(curr.keys):
            if k == key:
                return curr.children[i], latches
        return None, latches

    def insert(self, key, value):
        root = self.root
        if len(root.keys) >= self.order - 1:
            new_root = BPlusTreeNode(is_leaf=False)
            new_root.children.append(self.root)
            self._split_child(new_root, 0)
            self.root = new_root
        self._insert_non_full(self.root, key, value)

    def _split_child(self, parent, i):
        node = parent.children[i]
        mid = len(node.keys) // 2
        split_key = node.keys[mid]
        sibling = BPlusTreeNode(is_leaf=node.is_leaf)
        if node.is_leaf:
            sibling.keys = node.keys[mid:]
            sibling.children = node.children[mid:]
            node.keys = node.keys[:mid]
            node.children = node.children[:mid]
            sibling.next = node.next
            node.next = sibling
            parent.keys.insert(i, split_key)
            parent.children.insert(i + 1, sibling)
        else:
            sibling.keys = node.keys[mid+1:]
            sibling.children = node.children[mid+1:]
            node.keys = node.keys[:mid]
            node.children = node.children[:mid+1]
            parent.keys.insert(i, split_key)
            parent.children.insert(i + 1, sibling)

    def _insert_non_full(self, node, key, value):
        if node.is_leaf:
            idx = 0
            while idx < len(node.keys) and node.keys[idx] < key:
                idx += 1
            if idx < len(node.keys) and node.keys[idx] == key:
                node.children[idx] = value
            else:
                node.keys.insert(idx, key)
                node.children.insert(idx, value)
        else:
            idx = len(node.keys) - 1
            while idx >= 0 and key < node.keys[idx]:
                idx -= 1
            idx += 1
            if len(node.children[idx].keys) >= self.order - 1:
                self._split_child(node, idx)
                if key > node.keys[idx]:
                    idx += 1
            self._insert_non_full(node.children[idx], key, value)
