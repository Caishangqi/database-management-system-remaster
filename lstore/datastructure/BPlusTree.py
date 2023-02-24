import bisect

#test1

class BPlusTree:
    def __init__(self):
        self.root = None
        self.num_keys = 0

    def insert(self, key, value):
        if self.root is None:
            self.root = TreeNode(key, value)
            self.num_keys += 1
        else:
            self.root.insert(key, value)
            if self.root.is_full():
                self.split()
                self.num_keys += 1

    def split(self):
        left_child = self.root
        right_child = TreeNode(left_child.keys[self.root.order - 1], left_child.values[self.root.order - 1])

        # 将键和值的右半部分移动到child
        right_child.keys = left_child.keys[self.root.order:]
        right_child.values = left_child.values[self.root.order:]
        right_child.children = left_child.children[self.root.order:]

        # 从左child中删除右半边的键和值
        left_child.keys = left_child.keys[:self.root.order - 1]
        left_child.values = left_child.values[:self.root.order - 1]
        left_child.children = left_child.children[:self.root.order - 1]

        # 创建新的根节点
        new_root = TreeNode(left_child.keys[self.root.order - 2], left_child.values[self.root.order - 2])
        new_root.children.append(left_child)
        new_root.children.append(right_child)

        # 将新的根节点设置为树的根
        self.root = new_root

    def search(self, key):
        if self.root is None:
            return None
        else:
            return self.root.search(key)

    def delete(self, key):
        if self.root is None:
            return
        else:
            self.root.delete(key)
            if self.root.num_keys == 0 and self.root.children:
                self.root = self.root.children[0]
            self.num_keys -= 1


class TreeNode:
    def __init__(self, key, value):
        self.order = 4
        self.keys = [key]
        self.values = [value]
        self.children = []
        self.num_keys = 1

    def is_full(self):
        return self.num_keys == self.order - 1

    def insert(self, key, value):
        if self.is_full():
            self.split()
            self.insert(key, value)
        elif not self.children:
            self.keys.append(key)
            self.values.append(value)
            self.num_keys += 1
            self.keys.sort()
        else:
            index = bisect.bisect_left(self.keys, key)
            self.children[index].insert(key, value)
            if self.children[index].is_full():
                self.split_child(index)

    def split_child(self, index):
        left_child = self.children[index]
        right_child = TreeNode(left_child.keys[self.order - 1], left_child.values[self.order - 1])

        # 将键和值的右半部分移动到右child
        right_child.keys = left_child.keys[self.order:]
        right_child.values = left_child.values[self.order:]
        right_child.children = left_child.children[self.order:]

        # 从左child中删除右半边的键和值
        left_child.keys = left_child.keys[:self.order - 1]
        left_child.values = left_child.values[:self.order - 1]
        left_child.children = left_child.children[:self.order - 1]

        # 将新键和值插入当前节点
        self.keys.insert(index, left_child.keys[self.order - 2])
        self.values.insert(index, left_child.values[self.order - 2])

        # Insert the two new children into the current node
        self.children[index] = left_child
        self.children.insert(index + 1, right_child)
        self.num_keys += 1

    def search(self, key):
        index = bisect.bisect_left(self.keys, key)
        if index < len(self.keys) and self.keys[index] == key:
            return self.values[index]
        elif not self.children:
            return None
        else:
            return self.children[index].search(key)

    def delete(self, key):
        index = bisect.bisect_left(self.keys, key)
        if index < len(self.keys) and self.keys[index] == key:
            # key在这个节点中，所以删除它
            self.keys.pop(index)
            self.values.pop(index)
            self.num_keys -= 1
            # 如果到B树的尾端，必须是一个叶子，那么直接结束即可
            if not self.children:
                return
            # 如果该节点只有一个子节点，则将其替换为子节点
            if len(self.children) == 1:
                self.keys = self.children[0].keys
                self.values = self.children[0].values
                self.children = self.children[0].children
            # 如果节点有两个或多个子节点，找到父亲或后续子类，并用它替换删除的键
            else:
                if index == 0:
                    self.replace_with_predecessor()
                else:
                    self.replace_with_successor()
        elif not self.children:
            return
        else:
            self.children[index].delete(key)

    def replace_with_successor(self):
        right_child = self.children[1]
        self.keys[0] = right_child.keys[0]
        self.values[0] = right_child.values[0]
        right_child.keys.pop(0)
        right_child.values.pop(0)
        right_child.num_keys -= 1

    def replace_with_predecessor(self):
        left_child = self.children[0]
        self.keys[0] = left_child.keys[-1]
        self.values[0] = left_child.values[-1]
        left_child.keys.pop(-1)
        left_child.values.pop(-1)
        left_child.num_keys -= 1
