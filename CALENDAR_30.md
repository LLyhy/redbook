# 红宝书 · 30 天日拱一卒

> "积小胜为大胜，以空间换时间" —— 论持久战

---

## 使用说明

每天一道题。先遮挡下方红宝书分析，用矛盾分析法自己做：
1. **调查** — 搞清输入、输出、约束
2. **找主要矛盾** — 暴力为什么不行？
3. **想解法** — 什么方法能解决这个矛盾？
4. **写代码** — 实现你的思路
5. **检验** — 跑通小例子，检查边界

做完后再展开红宝书分析对照。做对了看分析有没有遗漏洞察，做错了看矛盾分析哪里跑偏了。

---

## 第一周：日拱一卒（数组 + 哈希）

> **阶段**：战略防御。敌人（难题）强，我们弱。打牢基础。  
> **语录**："没有调查就没有发言权" — 先调查每道题的输入输出，再下笔。

---

### Day 1: 群众路线 — 发动群众的力量

【题目】LeetCode #1: Two Sum
难度: easy

【矛盾提示】暴力枚举每对组合 O(n²)，数组太大怎么办？想想「有没有办法一次记住所有见过的人？」

---

*（在此处作答，写好后对照下方分析）*

---

【红宝书分析】

【调查】
输入：整数数组 nums，目标值 target。
输出：两个下标 i、j，使 nums[i] + nums[j] = target。
约束：2 ≤ n ≤ 10⁴，必有唯一解。同一个元素不能用两次。

【主要矛盾】
暴力是枚举所有数对 O(n²)，n=10⁴ 时 ≈ 5000 万次比较，勉强能过但面试不行。
根本矛盾：对于每个数 x，我们都需要快速知道 target - x 是否在数组中。暴力找了 n 次，每次都扫描全数组。

【解法】
语录：群众路线——"从群众中来，到群众中去"。每个元素都是群众，把它们登记到哈希表里。遍历时查 target - num 是否已经登记过。O(n) 一次遍历解决。

```python
def twoSum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
```

【检验】
边界：必有唯一解，无需处理无解情况。复杂度 O(n) 时间 O(n) 空间。遍历一次，每次哈希查找 O(1)。✓

---

### Day 2: 群众路线（续）— 重复就是力量

【题目】LeetCode #217: Contains Duplicate
难度: easy

【矛盾提示】检查重复，暴力比较每一对 O(n²)。如果每个元素都登记在册，出现重复立刻就能发现。

---

*（在此处作答）*

---

【红宝书分析】

【调查】
输入：整数数组 nums。
输出：布尔值，是否存在重复元素。
约束：1 ≤ n ≤ 10⁵，-10⁹ ≤ nums[i] ≤ 10⁹。

【主要矛盾】
暴力双循环 O(n²)，n=10⁵ 直接超时。
矛盾本质：需要判断"元素是否出现过"，但数组不提供快速查找。每来一个元素都要遍历整个数组检查。

【解法】
语录：群众路线——发动群众的力量。哈希集合记录所有已见元素，O(n) 一次遍历，每个元素 O(1) 判断是否已存在。

```python
def containsDuplicate(nums):
    seen = set()
    for n in nums:
        if n in seen:
            return True
        seen.add(n)
    return False
```

【检验】
边界：单个元素无重复正确返回 False。全部重复返回 True。复杂度 O(n) 时间 O(n) 空间。✓

---

### Day 3: 群众路线（续）— 统计也是一种力量

【题目】LeetCode #242: Valid Anagram
难度: easy

【矛盾提示】两个字符串，判断字母组成是否相同。如果给每个字母建一个户口册，统计出现次数呢？

---

*（在此处作答）*

---

【红宝书分析】

【调查】
输入：两个字符串 s 和 t。
输出：布尔值，t 是否为 s 的字母异位词。
约束：1 ≤ len ≤ 5×10⁴，仅含小写字母。

【主要矛盾】
暴力是排序后比较 O(n log n)。能不能用线性的方法？
本质矛盾：需要统计每个字符的出现次数并比较。排序引入了不必要的 log n 因子。

【解法】
语录：群众路线——将所有字母登记造册。用一个大小为 26 的数组（或哈希表），s 中每个字母计数 +1，t 中每个字母计数 -1。最后所有计数为 0 即为异位词。

```python
def isAnagram(s, t):
    if len(s) != len(t):
        return False
    count = [0] * 26
    for i in range(len(s)):
        count[ord(s[i]) - ord('a')] += 1
        count[ord(t[i]) - ord('a')] -= 1
    return all(c == 0 for c in count)
```

【检验】
边界：长度不等直接 false。空字符串双方都是空。复杂度 O(n) 时间 O(1) 空间（固定 26 大小）。✓

---

### Day 4: 群众路线的威力 — 分组作战

【题目】LeetCode #49: Group Anagrams
难度: medium

【矛盾提示】昨天的题升级了——不止判断两个，要把一堆字符串分组。矛盾变复杂了：如何给每个字母异位词生成同一个"身份证"？

---

*（在此处作答）*

---

【红宝书分析】

【调查】
输入：字符串数组 strs。
输出：List[List[str]]，字母异位词分在同一组。
约束：1 ≤ n ≤ 10⁴，0 ≤ len(s) ≤ 100，仅小写字母。

【主要矛盾】
暴力：每对字符串比较是否为异位词 O(n²·k)。
关键矛盾：需要一个映射规则，让相同字母组成的字符串映射到同一个键上——这是分组的关键。

【解法】
语录：群众路线——化零为整，归队入列。关键是给每个异位词组一个唯一标识：计数数组转元组（或排序后的字符串）作为哈希键。

```python
from collections import defaultdict

def groupAnagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        count = [0] * 26
        for ch in s:
            count[ord(ch) - ord('a')] += 1
        key = tuple(count)
        groups[key].append(s)
    return list(groups.values())
```

【检验】
边界：空字符串 count 全是 0，正确分组。单个元素独自成组。复杂度 O(n·k) 时间（k 为字符串长度），O(n·k) 空间。相比排序作键 O(n·k log k) 更优。✓

---

### Day 5: 矛盾转化 — 连续序列的隐藏规律

【题目】LeetCode #128: Longest Consecutive Sequence
难度: medium

【矛盾提示】要求 O(n)，不能排序。乱序数组中找最长连续序列——矛盾在于"连续"暗示了顺序，但你又不能排序。想想怎么绕开排序？

---

*（在此处作答）*

---

【红宝书分析】

【调查】
输入：未排序的整数数组 nums。
输出：最长连续数字序列的长度。
约束：O(n) 时间。0 ≤ n ≤ 10⁵。

【主要矛盾】
想排序 O(n log n) 但不让，又不让用 O(n²)。
根本矛盾：连续序列的核心是每个数 x 需要快速知道 x+1、x-1 是否存在。如果 x-1 存在，那 x 不是序列起点——跳过即可。

【解法】
语录：抓住主要矛盾——只从序列的起点开始计数。先把所有数放进哈希集合，然后只对"起点"（x-1 不在集合中的数）向上扩展。

```python
def longestConsecutive(nums):
    num_set = set(nums)
    longest = 0
    for n in num_set:
        if n - 1 not in num_set:
            cur = n
            cur_streak = 1
            while cur + 1 in num_set:
                cur += 1
                cur_streak += 1
            longest = max(longest, cur_streak)
    return longest
```

【检验】
边界：空数组返回 0。单个元素返回 1。重复元素只算一次。每个数最多被访问两次（起点扫描一次、while 被扫一次），复杂度 O(n) 时间 O(n) 空间。✓

---

### Day 6: 矛盾的普遍性 — Top K 的两种解法

【题目】LeetCode #347: Top K Frequent Elements
难度: medium

【矛盾提示】统计频率容易，找出前 K 个最高频的却不容易。矛盾在于：既要按频率排序，又不能完整排序 O(n log n)。桶？堆？

---

*（在此处作答）*

---

【红宝书分析】

【调查】
输入：整数数组 nums 和整数 k。
输出：出现频率最高的前 k 个元素（顺序任意）。
约束：1 ≤ n ≤ 10⁵，k 在合理范围内，保证答案唯一。

【主要矛盾】
暴力是统计后排序 O(n log n)。能不能更快？
矛盾本质：只需要前 k 个，不需要全部排序。次要矛盾才是 k 个的选取方式。

【解法】
语录：集中优势兵力——桶排序。频率最大不超过 n，建 n+1 个桶，频率为 i 的放第 i 号桶。倒序遍历桶取前 k 个。

```python
def topKFrequent(nums, k):
    from collections import Counter
    freq = Counter(nums)
    bucket = [[] for _ in range(len(nums) + 1)]
    for num, f in freq.items():
        bucket[f].append(num)
    result = []
    for i in range(len(bucket) - 1, -1, -1):
        for num in bucket[i]:
            result.append(num)
            if len(result) == k:
                return result
```

【检验】
边界：k=1 取最高频，k=n 返回所有数。复杂度 O(n) 时间 O(n) 空间。桶排序在此场景击败堆解法(O(n log k))。✓

---

### Day 7: 第一周收关 — 前缀和 + 群众路线

【题目】LeetCode #560: Subarray Sum Equals K
难度: medium

【矛盾提示】子数组和为 K——前缀和大家都会，但 O(n²) 枚举所有子数组太慢。矛盾在于：需要快速知道"之前有几个前缀和等于当前前缀和减 K"。谁能帮你快速查？

---

*（在此处作答）*

---

【红宝书分析】

【调查】
输入：整数数组 nums 和整数 k。
输出：和为 k 的连续子数组个数。
约束：1 ≤ n ≤ 2×10⁴，-1000 ≤ nums[i] ≤ 1000，-10⁷ ≤ k ≤ 10⁷。

【主要矛盾】
前缀和本身是 O(n)，但枚举所有子数组比较前缀和是 O(n²)。
矛盾本质：对于当前位置总和 cur_sum，需要 O(1) 知道前面有多少个前缀和恰好等于 cur_sum - k。

【解法】
语录：群众路线——哈希表。边遍历边记录每个前缀和的出现次数，遇到新前缀和 cur_sum，查 cur_sum - k 出现过几次。

```python
def subarraySum(nums, k):
    count = 0
    prefix_sum = 0
    freq = {0: 1}
    for n in nums:
        prefix_sum += n
        if prefix_sum - k in freq:
            count += freq[prefix_sum - k]
        freq[prefix_sum] = freq.get(prefix_sum, 0) + 1
    return count
```

【检验】
边界：空数组返回 0。单元素等于 k 返回 1。含负数时前缀和可重复。freq[0]=1 处理从开头到当前位置恰好为 k 的情况。复杂度 O(n) 时间 O(n) 空间。✓

---

## 第二周：集中兵力（链表 + 栈 + 队列）

> **阶段**：战略防御继续。从结构入手，理解链式结构矛盾。  
> **语录**："牵一发而动全身" — 链表改一个指针就改变了整个结构走向。

---

### Day 8: 牵一发 — 反转的矛盾

【题目】LeetCode #206: Reverse Linked List
难度: easy

【矛盾提示】链表只能顺着走，反转需要"掉头"。每走一步，后面的路就断了——矛盾在于既要往前走又要记住来的路。

---

*（在此处作答）*

---

【红宝书分析】

【调查】
输入：单链表头节点 head。
输出：反转后的链表头节点。
约束：节点数 0~5000。

【主要矛盾】
链表单向，要反转就要让每个节点指向前一个。但一旦改指向，就再也找不到原来后面的节点了。
矛盾本质：前进和后退的矛盾——必须前进（处理下一个节点），又必须后退（指向前一个）。

【解法】
语录：牵一发动全身——三指针接力。prev 记来的路，cur 站在当前，nxt 存将要走的路。三步操作改变指针方向。

```python
def reverseList(head):
    prev = None
    cur = head
    while cur:
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt
    return prev
```

【检验】
边界：空链表返回 None。单节点不变。复杂度 O(n) 时间 O(1) 空间。✓

---

### Day 9: 快慢之道 — 追击矛盾

【题目】LeetCode #141: Linked List Cycle
难度: easy

【矛盾提示】判断链表有没有环。如果沿着链表一直走，有环就永远走不到头——矛盾在于无法区分"还没到头"和"永远到不了头"。

---

*（在此处作答）*

---

【红宝书分析】

【调查】
输入：链表头节点 head。
输出：布尔值，是否有环。
约束：节点数 0~10⁴，pos 表示环的连接点。

【主要矛盾】
暴力做法是用哈希集合记录访问过的节点 O(n) 空间。能不能 O(1) 空间？
矛盾本质：快速判断"已访问过"需要某种标记——哈希表是显式标记，有没有隐式标记？

【解法】
语录：集中优势兵力——快慢指针。快指针两步、慢指针一步。如果有环，快指针必然追上慢指针（相对速度 1 步/次）；如果没环，快指针先到终点。

```python
def hasCycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False
```

【检验】
边界：空链表/单节点无环返回 False。两节点成环正确检测。复杂度 O(n) 时间 O(1) 空间。✓

---

### Day 10: 双链会师 — 归并的矛盾

【题目】LeetCode #21: Merge Two Sorted Lists
难度: easy

【矛盾提示】两个有序链表合成一个有序链表。暴力是全部拆下来排序，但链表已有顺序——矛盾是同时面对两条路，每一步都要选最小的走。

---

*（在此处作答）*

---

【红宝书分析】

【调查】
输入：两个升序链表的头节点 list1 和 list2。
输出：合并后的升序链表头。
约束：节点数 0~50。

【主要矛盾】
两个有序序列要合并成一个有序序列。每次要比较两个当前节点，选小的接上去。
矛盾本质：两条路线同时推进，要比较路线之间的差异而非路线内部的顺序。

【解法】
语录：集中优势兵力——虚拟头节点消除头节点的特殊性。每次比较两个当前节点，选小的接上。指针像坦克一样步步为营。

```python
def mergeTwoLists(list1, list2):
    dummy = ListNode(0)
    cur = dummy
    while list1 and list2:
        if list1.val <= list2.val:
            cur.next = list1
            list1 = list1.next
        else:
            cur.next = list2
            list2 = list2.next
        cur = cur.next
    cur.next = list1 or list2
    return dummy.next
```

【检验】
边界：两者皆空返回 None，只一者空返回另一者。复杂度 O(n+m) 时间 O(1) 空间。虚拟头节点避免了判断头节点为空的特殊情况。✓

---

### Day 11: 倒数的矛盾 — 快慢双指针

【题目】LeetCode #19: Remove Nth Node From End of List
难度: medium

【矛盾提示】删除倒数第 N 个节点。链表没有索引，不知道倒数——矛盾在于要从头走到尾才知道总长度，但知道了就还得从头走到目标。

---

*（在此处作答）*

---

【红宝书分析】

【调查】
输入：链表头 head 和整数 n。
输出：删除倒数第 n 个节点后的链表头。
约束：1 ≤ sz ≤ 30，1 ≤ n ≤ sz。

【主要矛盾】
两趟扫描可以解决（先求长度再定位）。能不能一趟？
矛盾本质：需要同时知道"总长度"和"当前位置"，但一趟中这两者还没相遇。用差值思维——让一个指针先走 n 步。

【解法】
语录：集中优势兵力——快慢指针。快指针先走 n 步，然后快慢同步走。快指针到末尾时，慢指针恰好指向要删除节点的前一个。

```python
def removeNthFromEnd(head, n):
    dummy = ListNode(0, head)
    fast = slow = dummy
    for _ in range(n + 1):
        fast = fast.next
    while fast:
        slow = slow.next
        fast = fast.next
    slow.next = slow.next.next
    return dummy.next
```

【检验】
边界：删除唯一节点返回空。删除头节点（n = 链表长度）虚拟头保证 slow 能指到 dummy。复杂度 O(n) 时间 O(1) 空间。✓

---

### Day 12: 矛盾的消解 — 括号匹配

【题目】LeetCode #20: Valid Parentheses
难度: easy

【矛盾提示】括号必须"先进后出"——最后开的括号必须最先关。什么数据结构天然支持"后进先出"？

---

*（在此处作答）*

---

【红宝书分析】

【调查】
输入：只含 '()[]{}' 的字符串 s。
输出：布尔值，括号是否有效配对。
约束：1 ≤ len ≤ 10⁴。

【主要矛盾】
括号匹配要求嵌套正确。左括号"进来"后必须等对应的右括号来"关闭"它，而且后进来的先关闭。
矛盾本质：处理顺序的矛盾——先进的后出，后进的先出。

【解法】
语录：前路光明，道路曲折——栈。左括号入栈等待，遇到右括号时栈顶必须是匹配的左括号。

```python
def isValid(s):
    pairs = {')': '(', ']': '[', '}': '{'}
    stack = []
    for ch in s:
        if ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
        else:
            stack.append(ch)
    return not stack
```

【检验】
边界：空字符串有效。单字符无效。嵌套 "(())" 有效，交叉 "([)]" 无效。复杂度 O(n) 时间 O(n) 空间。✓

---

### Day 13: 矛盾的叠加 — 最小栈

【题目】LeetCode #155: Min Stack
难度: medium

【矛盾提示】普通栈只能查栈顶，要同时知道栈内最小值——矛盾在于最小值可能被新元素推出栈外，你需要记住历史的"最小值状态"。

---

*（在此处作答）*

---

【红宝书分析】

【调查】
要求：实现 MinStack 类，支持 push、pop、top、getMin 全部 O(1)。
约束：-2³¹ ≤ val ≤ 2³¹-1，操作 ≤ 3×10⁴。

【主要矛盾】
普通栈 push/pop/top 是 O(1)，但 getMin 需要遍历 O(n)。
关键矛盾：pop 操作会使最小值"过期"——需要能回退到上一个最小值。

【解法】
语录：实践论——感性认识上升到理性认识。使用辅助栈同步记录每个状态下的最小值。每次 push 时把 min(新值, 辅助栈顶) 压入辅助栈。

```python
class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, val):
        self.stack.append(val)
        if not self.min_stack:
            self.min_stack.append(val)
        else:
            self.min_stack.append(min(val, self.min_stack[-1]))

    def pop(self):
        self.stack.pop()
        self.min_stack.pop()

    def top(self):
        return self.stack[-1]

    def getMin(self):
        return self.min_stack[-1]
```

【检验】
边界：pop 空栈不会发生（题目保证）。连续 push 递减元素检验 min_stack 正确更新。所有操作 O(1)。O(n) 额外空间。✓

---

### Day 14: 矛盾的对立统一 — 栈实现队列

【题目】LeetCode #232: Implement Queue using Stacks
难度: easy

【矛盾提示】栈是后进先出，队列是先进先出——这两个刚好相反。如何用相反的武器打出相反的效果？矛盾的统一在于"翻转"。

---

*（在此处作答）*

---

【红宝书分析】

【调查】
要求：用两个栈实现队列的 push、pop、peek、empty。
约束：操作 ≤ 100，均摊 O(1)。

【主要矛盾】
栈 LIFO vs 队列 FIFO——根本对立。
矛盾转化：用了第一个栈是反的，再倒进第二个栈就是正的——两次反等于正。

【解法】
语录：矛盾转化——否定之否定。push 时放入 in_stack，需要 pop/peek 时若 out_stack 为空，把 in_stack 的全部倒入 out_stack，完成反转。

```python
class MyQueue:
    def __init__(self):
        self.in_stack = []
        self.out_stack = []

    def push(self, x):
        self.in_stack.append(x)

    def pop(self):
        self._transfer()
        return self.out_stack.pop()

    def peek(self):
        self._transfer()
        return self.out_stack[-1]

    def empty(self):
        return not self.in_stack and not self.out_stack

    def _transfer(self):
        if not self.out_stack:
            while self.in_stack:
                self.out_stack.append(self.in_stack.pop())
```

【检验】
边界：空队列 pop 不会发生。每个元素只被 push/pop 各两次（in_stack 一次 out_stack 一次），均摊 O(1)。O(n) 空间。✓

---

## 第三周：抓住主要矛盾（树 + 二分查找）

> **阶段**：战略相持开始。矛盾复杂度升级，从线性结构进入树形结构和二分。  
> **语录**："抓住主要矛盾" — 每棵树的问题归结于根节点。

---

### Day 15: 递归的本质矛盾

【题目】LeetCode #104: Maximum Depth of Binary Tree
难度: easy

【矛盾提示】树的深度——矛盾在于一棵树的深度由左子树和右子树的深度决定，但左和右是不同世界。如何统一？

---

*（在此处作答）*

---

【红宝书分析】

【调查】
输入：二叉树根节点 root。
输出：最大深度（从根到最远叶子的节点数）。
约束：节点数 0~10⁴。

【主要矛盾】
迭代 BFS/DFS 都行，但树的递归结构暗示了更优雅的解法。
矛盾本质：整棵树的深度 = max(左子树深度, 右子树深度) + 1。子问题和原问题结构相同——递归的矛盾被自身消解。

【解法】
语录：抓住主要矛盾——每个子树都是一棵树。自底向上：叶子返回 0，非叶子返回 max(左深度, 右深度) + 1。

```python
def maxDepth(root):
    if not root:
        return 0
    return max(maxDepth(root.left), maxDepth(root.right)) + 1
```

【检验】
边界：空树返回 0。单节点返回 1。链状树（退化为链表）返回 n。复杂度 O(n) 时间 O(h) 空间（递归栈）。✓

---

### Day 16: 镜像中的矛盾统一

【题目】LeetCode #226: Invert Binary Tree
难度: easy

【矛盾提示】翻转二叉树——左右子树交换。矛盾在于：交换了两个指针，但子树内部的节点也要随之翻转。

---

*（在此处作答）*

---

【红宝书分析】

【调查】
输入：二叉树根节点 root。
输出：翻转后的二叉树根（左右子树互换）。
约束：节点数 0~100。

【主要矛盾】
交换左右子是 O(1)，但子树内部的节点也必须翻转。
本质矛盾：全局翻转 = 每个节点的局部翻转之和。递归拆到每个节点。

【解法】
语录：抓住主要矛盾——从根节点开始，交换左右子树。然后递归翻转左右子树本身。自底向上，层层翻转。

```python
def invertTree(root):
    if not root:
        return None
    root.left, root.right = root.right, root.left
    invertTree(root.left)
    invertTree(root.right)
    return root
```

【检验】
边界：空树返回 None。单节点不变。复杂度 O(n) 时间 O(h) 空间。✓

---

### Day 17: 矛盾的界限 — 验证 BST

【题目】LeetCode #98: Validate Binary Search Tree
难度: medium

【矛盾提示】BST 要求左边全小、右边全大。只比较当前节点和直接孩子不够——矛盾在于约束传递：根的左子树的右子节点仍必须小于根。

---

*（在此处作答）*

---

【红宝书分析】

【调查】
输入：二叉树根节点 root。
输出：是否为有效 BST。
约束：节点数 1~10⁴，节点值可能等于 INT_MIN/MAX。

【主要矛盾】
常见误区：只比较 node.left.val < node.val < node.right.val。这不够——左子树的右孙可能比根还大。
本质矛盾：约束是传递性的，需要维护一个取值范围 [low, high]。

【解法】
语录：实事求是——不带主观臆断。递归维护上下界，每深入一层收紧范围。

```python
def isValidBST(root):
    def validate(node, low, high):
        if not node:
            return True
        if node.val <= low or node.val >= high:
            return False
        return validate(node.left, low, node.val) and validate(node.right, node.val, high)
    return validate(root, float('-inf'), float('inf'))
```

【检验】
边界：单节点是 BST。值等于边界不允许（严格小于/大于）。注意用 -inf/inf 而不是 INT_MIN/MAX 来避免边界值误判。复杂度 O(n) 时间 O(h) 空间。✓

---

### Day 18: 按层斗争 — BFS 的矛盾

【题目】LeetCode #102: Binary Tree Level Order Traversal
难度: medium

【矛盾提示】树的层序遍历。DFS 容易按深度走，但你需要按层输出——矛盾在于一层可能跨越多条路径，你需要把水平关系从垂直递归中剥离出来。

---

*（在此处作答）*

---

【红宝书分析】

【调查】
输入：二叉树根节点 root。
输出：List[List[int]]，按层分组节点值。
约束：节点数 0~2000。

【主要矛盾】
DFS 递归是纵向的，层序遍历是横向的。
矛盾本质：需要同时维护位置信息（在哪一层）和遍历顺序。队列天然支持按层处理。

【解法】
语录：集中优势兵力——BFS + 队列。每轮处理队列中的全部节点（即当前层的全部节点），把它们的孩子加入下一层队列。

```python
from collections import deque

def levelOrder(root):
    if not root:
        return []
    result = []
    q = deque([root])
    while q:
        level = []
        for _ in range(len(q)):
            node = q.popleft()
            level.append(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        result.append(level)
    return result
```

【检验】
边界：空树返回 []。单节点返回 [[val]]。按 for _ in range(len(q)) 确保每次只处理当前层。复杂度 O(n) 时间 O(n) 空间（队列最大宽度 ~n/2）。✓

---

### Day 19: 消灭一半 — 二分查找

【题目】LeetCode #704: Binary Search
难度: easy

【矛盾提示】有序数组找目标值。从头找到尾 O(n)，但数组有序——矛盾在于你可以直接跳到中间，根据大小消灭一半。

---

*（在此处作答）*

---

【红宝书分析】

【调查】
输入：升序整数数组 nums，目标值 target。
输出：目标下标，不存在返回 -1。
约束：1 ≤ n ≤ 10⁴，元素唯一。

【主要矛盾】
线性扫描 O(n)，但数组有序这一信息被浪费了。
矛盾转化：有序 → 中点值与 target 比较 → 砍掉不可能的一半。

【解法】
语录：集中优势兵力，各个击破——二分查找。每次集中火力检查中点，排除掉一半候选区间。

```python
def search(nums, target):
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

【检验】
边界：target 在两端、不存在、数组只有一个元素。用 left + (right-left)//2 防止溢出。复杂度 O(log n) 时间 O(1) 空间。✓

---

### Day 20: 矛盾的特殊性 — 旋转数组二分

【题目】LeetCode #33: Search in Rotated Sorted Array
难度: medium

【矛盾提示】旋转后的数组不是完全有序的——二分查找的前提被破坏了。但矛盾有特殊性：旋转之后，数组变成了"两段有序"。怎么把二分的威力用在这里？

---

*（在此处作答）*

---

【红宝书分析】

【调查】
输入：旋转后的升序数组 nums（不重复），目标值 target。
输出：目标下标，不存在返回 -1。
约束：O(log n)，1 ≤ n ≤ 5000。

【主要矛盾】
数组被旋转打乱了全局有序性，但局部有序仍然保留。
矛盾特殊性：mid 将数组分成两半，其中至少一半是完全有序的。先判断哪一半有序，再用二分。

【解法】
语录：矛盾的特殊性——具体问题具体分析。每次二分时先判断左半还是右半有序，然后判断 target 是否在有序区间内。

```python
def search(nums, target):
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid
        if nums[left] <= nums[mid]:
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
    return -1
```

【检验】
边界：数组未旋转（完全有序）正常工作。单元素直接匹配。二分中注意 nums[left] <= nums[mid] 的等号处理。复杂度 O(log n)。✓

---

### Day 21: 寻找拐点 — 旋转的极值矛盾

【题目】LeetCode #153: Find Minimum in Rotated Sorted Array
难度: medium

【矛盾提示】旋转数组找最小值。昨天学会了在旋转数组中搜索，今天是找拐点——矛盾更集中了：最小值恰好是"下跌"的发生点。

---

*（在此处作答）*

---

【红宝书分析】

【调查】
输入：不重复的旋转升序数组 nums。
输出：数组中的最小值。
约束：O(log n)，1 ≤ n ≤ 5000。

【主要矛盾】
线性的 O(n) 显然可以，但要求 O(log n)。
本质矛盾：旋转点将数组分成两段升序。最小值就是"右半段"的第一个元素。用二分找到左右分界点。

【解法】
语录：集中优势兵力——二分查找。如果 nums[mid] > nums[right]，说明 mid 在左半段，最小值在右边；否则 mid 在右半段，最小值在左边（含 mid）。

```python
def findMin(nums):
    left, right = 0, len(nums) - 1
    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] > nums[right]:
            left = mid + 1
        else:
            right = mid
    return nums[left]
```

【检验】
边界：未旋转（完全升序）返回 nums[0]。两个元素正确判断。while left < right（不是 <=）避免死循环，因为 right = mid（不是 mid-1）。复杂度 O(log n)。✓

---

## 第四周：星星之火（动态规划 + 回溯）

> **阶段**：战略相持深入。从量变到质变，从子问题到全局最优。  
> **语录**："星星之火，可以燎原" — dp[0] 的火种蔓延成 dp[n] 的燎原大火。

---

### Day 22: 量变引起质变 — 爬楼梯

【题目】LeetCode #70: Climbing Stairs
难度: easy

【矛盾提示】爬到第 n 阶，要么从 n-1 来要么从 n-2 来。每步的选择看似很多，但——到达每级台阶的方法数只和前两级有关。这是什么规律？

---

*（在此处作答）*

---

【红宝书分析】

【调查】
输入：整数 n（楼梯阶数）。
输出：爬到顶部的不同方法数（每次 1 或 2 步）。
约束：1 ≤ n ≤ 45。

【主要矛盾】
暴力枚举所有爬法指数级 O(2ⁿ)。
关键矛盾：大量重复子问题——到第 i 阶的方法数 dp[i] = dp[i-1] + dp[i-2]。子问题 dp[i-1] 和 dp[i-2] 被反复计算。

【解法】
语录：星星之火，可以燎原——dp[1]=1, dp[2]=2 是火种，一路蔓延到 dp[n]。

```python
def climbStairs(n):
    if n <= 2:
        return n
    prev2, prev1 = 1, 2
    for i in range(3, n + 1):
        curr = prev1 + prev2
        prev2, prev1 = prev1, curr
    return prev1
```

【检验】
边界：n=1 返回 1，n=2 返回 2。O(n) 时间 O(1) 空间（只用两个变量滚动）。这本质是斐波那契数列。✓

---

### Day 23: 隔一个抢一个 — 不相邻的矛盾

【题目】LeetCode #198: House Robber
难度: medium

【矛盾提示】不能偷相邻两家。到了第 i 家，偷不偷？矛盾：偷它就跳过了 i-1 家，不偷就拿不到 i 家的钱。如何抉择？

---

*（在此处作答）*

---

【红宝书分析】

【调查】
输入：整数数组 nums 表示每家金额。
输出：不触发警报（不偷相邻）的最大金额。
约束：1 ≤ n ≤ 100。

【主要矛盾】
暴力枚举 O(2ⁿ)。每到一个房子面临"偷 vs 不偷"的抉择，两个选择互相排斥又互相关联。
矛盾转化：dp[i] = max(dp[i-1], dp[i-2] + nums[i])——不偷则继承 i-1 的结果，偷则跳过 i-1 拿 i-2 的结果加当前。

【解法】
语录：星星之火——dp[0] 和 dp[1] 的火种，一路蔓延到末尾。

```python
def rob(nums):
    if len(nums) == 1:
        return nums[0]
    prev2, prev1 = nums[0], max(nums[0], nums[1])
    for i in range(2, len(nums)):
        curr = max(prev1, prev2 + nums[i])
        prev2, prev1 = prev1, curr
    return prev1
```

【检验】
边界：单元素返回该值。两个元素返回较大者。O(n) 时间 O(1) 空间。状态转移方程体现了矛盾的二重性（偷 vs 不偷）。✓

---

### Day 24: 换零钱的矛盾 — 最少硬币

【题目】LeetCode #322: Coin Change
难度: medium

【矛盾提示】给定面额凑出总金额，要求硬币数最少。贪心不一定对（1,3,4 凑 6：贪心 4+1+1=3 枚，最优 3+3=2 枚）。矛盾在于贪心的短视 vs 全局最优。

---

*（在此处作答）*

---

【红宝书分析】

【调查】
输入：硬币面额数组 coins 和目标金额 amount。
输出：凑出 amount 的最少硬币数，凑不出返回 -1。
约束：1 ≤ n ≤ 12，1 ≤ amount ≤ 10⁴。

【主要矛盾】
贪心不可行——局部最优 ≠ 全局最优。
本质矛盾：dp[i] = min(dp[i - coin] + 1)，每种硬币都是一条路，选择最短的那条。

【解法】
语录：星星之火——dp[0]=0 是火种（0 元需要 0 枚硬币）。金额从小到大推，每个金额试所有硬币面额。

```python
def coinChange(coins, amount):
    dp = [amount + 1] * (amount + 1)
    dp[0] = 0
    for i in range(1, amount + 1):
        for coin in coins:
            if i >= coin:
                dp[i] = min(dp[i], dp[i - coin] + 1)
    return dp[amount] if dp[amount] != amount + 1 else -1
```

【检验】
边界：amount=0 返回 0。无解返回 -1（用 amount+1 做哨兵）。硬币面额可能大于 amount，跳过。复杂度 O(amount × n)。✓

---

### Day 25: 最长上升 — 子序列矛盾

【题目】LeetCode #300: Longest Increasing Subsequence
难度: medium

【矛盾提示】最长上升子序列。暴力枚举所有子序列 O(2ⁿ)。矛盾：后面的元素能否"接上"前面的序列，只取决于最后一个元素的值——你不需要知道整个历史。

---

*（在此处作答）*

---

【红宝书分析】

【调查】
输入：整数数组 nums。
输出：最长严格递增子序列长度。
约束：1 ≤ n ≤ 2500。

【主要矛盾】
暴力枚举指数级。每个位置 i 的结果需要知道前面所有 j < i 的结果。
矛盾转化：dp[i] = 以 nums[i] 结尾的最长递增子序列长度。dp[i] = max(dp[j] + 1) 对所有满足 nums[j] < nums[i] 的 j。

【解法】
语录：星星之火——每个 dp[i] 从前面最长的可接序列燃起。

```python
def lengthOfLIS(nums):
    dp = [1] * len(nums)
    for i in range(len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)
```

【检验】
边界：单元素返回 1。全部递减返回 1。复杂度 O(n²) 时间 O(n) 空间。进阶 O(n log n) 解法用 patience sorting（二分贪心），矛盾更高阶。✓

---

### Day 26: 前进与后退的统一 — 全排列

【题目】LeetCode #46: Permutations
难度: medium

【矛盾提示】输出数组的所有排列。每个位置都要选一个数，但选过的就不能再选——矛盾：一次选择缩小了后续的选择空间。如何系统地试遍所有可能？

---

*（在此处作答）*

---

【红宝书分析】

【调查】
输入：不含重复数字的数组 nums。
输出：所有可能的排列 List[List[int]]。
约束：1 ≤ n ≤ 6。

【主要矛盾】
排列总数 n!，必须全部枚举。但每个位置的选择有约束（不能重复）。
本质矛盾：需要维护"已选"和"可选"两个集合，每次选一个从可选移到已选。

【解法】
语录：敌进我退，敌退我进——回溯。做选择（前进），递归，撤销选择（后退）。前进与后退互相依存。

```python
def permute(nums):
    result = []
    def backtrack(path, used):
        if len(path) == len(nums):
            result.append(path[:])
            return
        for i in range(len(nums)):
            if used[i]:
                continue
            used[i] = True
            path.append(nums[i])
            backtrack(path, used)
            path.pop()
            used[i] = False
    backtrack([], [False] * len(nums))
    return result
```

【检验】
边界：n=1 返回 [[nums[0]]]。使用 used 数组标记或 path 内判断重复。回溯模板成体系。复杂度 O(n×n!)。✓

---

### Day 27: 选或不选 — 子集的矛盾

【题目】LeetCode #78: Subsets
难度: medium

【矛盾提示】返回所有子集。每个元素只有两种命运——被选入子集或被跳过。一共 2ⁿ 个子集。与全排列的区别在哪？

---

*（在此处作答）*

---

【红宝书分析】

【调查】
输入：不含重复数字的数组 nums。
输出：所有可能的子集 List[List[int]]（幂集）。
约束：1 ≤ n ≤ 10。

【主要矛盾】
每个元素面临"选/不选"的二重性抉择，共 2ⁿ 种结果。
与排列的区别：子集的无序性——[1,2] 和 [2,1] 是同一个子集。不需要标记 used，只需正向推进 index 避免重复。

【解法】
语录：敌进我退——回溯。从 index 开始，选择当前元素（前进），递归（index+1），撤销选择（后退）。每走一步都把当前路径加入结果。

```python
def subsets(nums):
    result = []
    def backtrack(start, path):
        result.append(path[:])
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()
    backtrack(0, [])
    return result
```

【检验】
边界：n=1 返回 [[], [nums[0]]]。空集总在第一位。注意 start=i+1 不是 start+1。复杂度 O(n×2ⁿ)。✓

---

### Day 28: 可重复选择的回溯

【题目】LeetCode #39: Combination Sum
难度: medium

【矛盾提示】选一些数使得和等于 target，同一个数可以重复选。这跟子集问题很像，但多了两个矛盾：约束目标变成了 target，数字可以复用。

---

*（在此处作答）*

---

【红宝书分析】

【调查】
输入：不重复候选数组 candidates，目标 target。
输出：所有和为 target 的组合（数可重复使用）。
约束：1 ≤ n ≤ 30，1 ≤ candidates[i] ≤ 200，1 ≤ target ≤ 500。

【主要矛盾】
回溯框架 + 可重复选择。
核心差异：递归时 start 不 +1（允许重复选当前数）。剪枝：排序后若当前数已超 target，后面更大，直接 break。

【解法】
语录：敌进我退——回溯 + 排序剪枝。排序两用：让结果有序、提前剪断不可能的分支。

```python
def combinationSum(candidates, target):
    result = []
    candidates.sort()
    def backtrack(start, path, remaining):
        if remaining == 0:
            result.append(path[:])
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break
            path.append(candidates[i])
            backtrack(i, path, remaining - candidates[i])
            path.pop()
    backtrack(0, [], target)
    return result
```

【检验】
边界：无解返回 []。注意 start 传入 i（不是 i+1）允许重复使用同一个数。排序后剪枝大幅提速。复杂度 O(n^(target/min)) 级。✓

---

## 第五周开端：反攻开始（复习 + 困难挑战）

> **阶段**：从战略相持转入战略反攻。用两周积累去攻克困难题。  
> **语录**："在战术上重视敌人" — 困难题也要用矛盾分析法拆解。

---

### Day 29: 综合复习 + 接雨水

【题目】LeetCode #42: Trapping Rain Water
难度: hard

【矛盾提示】每个柱子能接多少水，取决于左右两边最高的柱子——矛盾在于当前位置不知道自己左边最高和右边最高是多少，暴力预计算左右最大高度需要 O(n) 空间。能不能双指针？

---

*（在此处作答）*

---

【红宝书分析】

【调查】
输入：非负整数数组 height 表示柱子高度。
输出：下雨后能接的雨水总量。
约束：n ≥ 0。

【主要矛盾】
暴力：每个位置找左右最大值 O(n²)。
矛盾层次：每个位置的水量 = min(左边最高, 右边最高) - 自身高度。如果左边最高 < 右边最高，水量由左边决定——此时可以边移动边计算。

【解法】
语录：集中优势兵力——双指针两头夹击。维护 left_max 和 right_max，谁小移谁，水量由较小的一侧决定。

```python
def trap(height):
    if not height:
        return 0
    left, right = 0, len(height) - 1
    left_max = height[left]
    right_max = height[right]
    water = 0
    while left < right:
        if left_max < right_max:
            left += 1
            left_max = max(left_max, height[left])
            water += left_max - height[left]
        else:
            right -= 1
            right_max = max(right_max, height[right])
            water += right_max - height[right]
    return water
```

【检验】
边界：n<3 无法积水返回 0。单调递增/递减返回 0。注意 left_max - height[left] 在更新 left_max 后计算。复杂度 O(n) 时间 O(1) 空间。✓

---

### Day 30: 三十年 · 最小覆盖子串

【题目】LeetCode #76: Minimum Window Substring
难度: hard

【矛盾提示】在 s 中找覆盖 t 所有字符的最短子串。暴力枚举所有子串 O(n²)。矛盾：子串是连续的，你需要动态扩展和收缩窗口来找到"刚刚好"覆盖的长度。

---

*（在此处作答）*

---

【红宝书分析】

【调查】
输入：字符串 s 和 t。
输出：s 中覆盖 t 所有字符的最短子串，不存在返回 ""。
约束：1 ≤ len(s), len(t) ≤ 10⁵，英文字母。

【主要矛盾】
暴力 O(n²) 枚举所有子串不可行。
本质矛盾：如何动态地扩大和缩小窗口，使得窗口始终"尽量小地满足覆盖条件"？滑动窗口——右指针扩大直到满足，左指针收缩直到不满足。

【解法】
语录：集中优势兵力——滑动窗口。维护两个哈希表（t 的需求和窗口的状态）。右指针扩展直到全部匹配，左指针收缩找最小满足窗口。

```python
from collections import Counter

def minWindow(s, t):
    need = Counter(t)
    window = {}
    have, need_count = 0, len(need)
    left = 0
    min_len = float('inf')
    result = ""
    for right in range(len(s)):
        ch = s[right]
        window[ch] = window.get(ch, 0) + 1
        if ch in need and window[ch] == need[ch]:
            have += 1
        while have == need_count:
            if right - left + 1 < min_len:
                min_len = right - left + 1
                result = s[left:right+1]
            left_ch = s[left]
            window[left_ch] -= 1
            if left_ch in need and window[left_ch] < need[left_ch]:
                have -= 1
            left += 1
    return result
```

【检验】
边界：s=t 返回 s。s 不覆盖 t 返回 ""。注意 window[ch]==need[ch] 恰好满足时 have++，window[ch] < need[ch] 时 have--。复杂度 O(n+m) 时间。这题是滑动窗口的集大成者，矛盾层层递进。✓

---

## 后记：30 天后，然后呢？

> "夺取全国胜利，这只是万里长征走完了第一步。"

30 天刷完不是终点。真正的矛盾分析能力是从"会做"到"能分析任何题"。

接下来的方向：
- **二刷模式**：遮住分析再做一遍，看独立分析能力是否提升
- **面试模式**：对着 `REDBOOK_INTERVIEW.md` 做模拟面试
- **出题模式**：试着自己出题——能出好题说明真正理解了矛盾结构
- **大量实战**：LeetCode 周赛，限时压力下找矛盾

---

> **完整方法论** 见 `SKILL.md`  
> **系统提示词** 见 `finetune/REDBOOK_SYSTEM_PROMPT.md`  
> **面试模式** 见 `finetune/REDBOOK_INTERVIEW.md`
