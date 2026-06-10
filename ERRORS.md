# 红宝书 · 错误案例画廊

> "错误常常是正确的先导。" — 《实践论》

30 个常见算法错误，按矛盾层次分类。每个案例 = 错误代码 + 现象 + 矛盾分析 + 语录 + 纠正代码。

---

## 一、逻辑错误（10 例）—— 思路根本不对

> "路线错了，知识再多也没用。"

---

### 错误 #1: 两数之和用双指针忘了排序

**错误代码：**
```python
def twoSum(nums, target):
    left, right = 0, len(nums) - 1
    while left < right:
        s = nums[left] + nums[right]
        if s == target:
            return [left, right]
        elif s < target:
            left += 1
        else:
            right -= 1
```

**现象：** 示例 `[3,2,4], 6` 应返回 `[1,2]`，实际返回 `[0,2]`（值对但下标错，因为没排序）。

**【矛盾分析】主要矛盾识别错误**：双指针能 O(n) 找到两数之和，但前提是数组**有序**。无序数组的双指针方向与值的大小没有单调关系——left 右移不一定让和变大，right 左移不一定让和变小。算法的核心假设（单调性）不成立。

**【语录】** "没有调查就没有发言权"——没调查数组是否有序就用了双指针。

**纠正代码：**
```python
def twoSum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
```

---

### 错误 #2: 最长回文子串用贪心

**错误代码：**
```python
def longestPalindrome(s):
    n = len(s)
    dp = [1] * n  # dp[i] = 以 i 结尾的最长回文长度
    for i in range(1, n):
        if s[i] == s[i-1]:
            dp[i] = dp[i-1] + 1
    return max(dp)
```

**现象：** `"babad"` 返回 `3`（期望 `"bab"` 或 `"aba"`），但 `"cbbd"` 返回 `2`（对了是巧合——`"bb"` 碰巧相邻）。`"aacabdkacaa"` 完全错误。

**【矛盾分析】主要矛盾识别错误**：把回文判断简化成"相邻相等"是**错误归纳**。回文的本质矛盾是**对称性**——以某个中心向两边扩展，而不是相邻相等。贪心从局部相等推到全局是错误的：`dp[i-1]` 最长回文的最后一个字符不一定和 `s[i]` 对称。

**【语录】** "矛盾的普遍性即寓于矛盾的特殊性之中"——回文的普遍规律是对称，不能简化为相邻相等这个"特殊性"。

**纠正代码：**
```python
def longestPalindrome(s):
    n = len(s)
    start, max_len = 0, 1
    for i in range(n):
        for l, r in [(i, i), (i, i + 1)]:
            while l >= 0 and r < n and s[l] == s[r]:
                if r - l + 1 > max_len:
                    start, max_len = l, r - l + 1
                l -= 1
                r += 1
    return s[start:start + max_len]
```

---

### 错误 #3: 岛屿数量 DFS 只搜一个方向

**错误代码：**
```python
def numIslands(grid):
    rows, cols = len(grid), len(grid[0])
    count = 0
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == '1':
                count += 1
                dfs(grid, i, j)
    return count

def dfs(grid, i, j):
    if i < 0 or i >= len(grid) or j < 0 or j >= len(grid[0]) or grid[i][j] == '0':
        return
    grid[i][j] = '0'
    dfs(grid, i + 1, j)  # 只往下搜！
```

**现象：** 岛屿被切成了碎片——只能纵向连通，横向和向上的 '1' 被当成新岛屿，count 偏大。

**【矛盾分析】主要矛盾识别错误**：岛屿的"连通性"是上下左右四个方向，只搜一个方向是对连通性的**不完整认知**。DFS 的本质是穷尽所有可达路径——缺了一个方向 = 缺了一条路径 = 矛盾没充分解决。

**【语录】** "研究问题，忌带主观性、片面性和表面性"——只搜下方向是片面认识岛屿。

**纠正代码：**
```python
def dfs(grid, i, j):
    if i < 0 or i >= len(grid) or j < 0 or j >= len(grid[0]) or grid[i][j] == '0':
        return
    grid[i][j] = '0'
    dfs(grid, i + 1, j)
    dfs(grid, i - 1, j)
    dfs(grid, i, j + 1)
    dfs(grid, i, j - 1)
```

---

### 错误 #4: 合并区间忘了按起点排序

**错误代码：**
```python
def merge(intervals):
    result = []
    for interval in intervals:
        if not result or result[-1][1] < interval[0]:
            result.append(interval)
        else:
            result[-1][1] = max(result[-1][1], interval[1])
    return result
```

**现象：** `[[1,4],[0,1]]` 返回 `[[1,4],[0,1]]`（期望 `[[0,4]]`）。区间顺序不确定时，前面的区间可能完全被后面的覆盖。

**【矛盾分析】主要矛盾识别错误**：合并的前提是**相邻区间能比较**。不排序时，`result[-1]` 和 `interval` 可能是任意两个不相邻的区间——它们本来就不该合并，却强行判断了重叠。排序是"集中兵力"——把可能合并的区间集中到一起。

**【语录】** "集中优势兵力，各个击破"——先排序把可能重叠的区间集中，再各个突破。

**纠正代码：**
```python
def merge(intervals):
    intervals.sort(key=lambda x: x[0])
    result = []
    for interval in intervals:
        if not result or result[-1][1] < interval[0]:
            result.append(interval)
        else:
            result[-1][1] = max(result[-1][1], interval[1])
    return result
```

---

### 错误 #5: 括号生成回溯缺少右括号条件

**错误代码：**
```python
def generateParenthesis(n):
    result = []
    def backtrack(s, left, right):
        if len(s) == 2 * n:
            result.append(s)
            return
        if left < n:
            backtrack(s + '(', left + 1, right)
        backtrack(s + ')', left, right + 1)  # 无条件加右括号！
    backtrack('', 0, 0)
    return result
```

**现象：** 生成 `"())(()"` 这种非法括号序列——右括号数量在某个前缀中超过了左括号。

**【矛盾分析】主要矛盾识别错误**：括号合法的本质矛盾不是"左右括号总数相等"，而是**任意前缀中右括号数 ≤ 左括号数**。少了一条规则：`right < left` 才能加右括号。错误代码只控制了总数，没控制前缀——这就是主要矛盾和次要矛盾的混淆。

**【语录】** "在复杂的事物的发展过程中，有许多的矛盾存在，其中必有一种是主要的矛盾"——总数相等是次要矛盾，前缀合法性是主要矛盾。

**纠正代码：**
```python
def generateParenthesis(n):
    result = []
    def backtrack(s, left, right):
        if len(s) == 2 * n:
            result.append(s)
            return
        if left < n:
            backtrack(s + '(', left + 1, right)
        if right < left:  # 关键条件
            backtrack(s + ')', left, right + 1)
    backtrack('', 0, 0)
    return result
```

---

### 错误 #6: 三数之和去重逻辑写反

**错误代码：**
```python
def threeSum(nums):
    nums.sort()
    result = []
    for i in range(len(nums)):
        if nums[i] > 0: break
        left, right = i + 1, len(nums) - 1
        while left < right:
            s = nums[i] + nums[left] + nums[right]
            if s == 0:
                result.append([nums[i], nums[left], nums[right]])
                left += 1   # 先去重? 错了 —— 应该先加结果再移动
                while left < right and nums[left] == nums[left - 1]:
                    left += 1
            elif s < 0:
                left += 1
            else:
                right -= 1
    return result
```

**现象：** 去重逻辑放在了 `left += 1` 之后——但这只是会漏掉重复组合，不是致命 bug。**真正的问题是**：外层循环 i 的去重也容易写错。`[-1,0,1,2,-1,-4]` 排序后 `[-4,-1,-1,0,1,2]`，两个 `-1` 都会产生相同的 triplet。

**【矛盾分析】主要矛盾识别错误**：重复的矛盾根源在于**外层循环对同一个值的多次处理**，而不在内层双指针。if `i > 0 and nums[i] == nums[i-1]: continue` 才是治本。

**【语录】** "抓住主要矛盾"——外层循环的去重是主要矛盾，内层指针的去重是次要矛盾。

**纠正代码：**
```python
def threeSum(nums):
    nums.sort()
    result = []
    for i in range(len(nums)):
        if nums[i] > 0: break
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        left, right = i + 1, len(nums) - 1
        while left < right:
            s = nums[i] + nums[left] + nums[right]
            if s == 0:
                result.append([nums[i], nums[left], nums[right]])
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                left += 1
                right -= 1
            elif s < 0:
                left += 1
            else:
                right -= 1
    return result
```

---

### 错误 #7: 全排列 visited 忘记回溯撤销

**错误代码：**
```python
def permute(nums):
    result = []
    visited = [False] * len(nums)
    def backtrack(path):
        if len(path) == len(nums):
            result.append(path[:])
            return
        for i in range(len(nums)):
            if visited[i]: continue
            visited[i] = True
            path.append(nums[i])
            backtrack(path)
            # 忘了撤销！visited[i] = False
            # 忘了撤销！path.pop()
    backtrack([])
    return result
```

**现象：** 只输出 `[[1,2,3]]` 一个排列——其他路径全部被 visited 封死了。每个数字只用了一次就无法再探索其他组合。

**【矛盾分析】主要矛盾识别错误**：回溯的矛盾是前进和后退的对立统一。前进后不后退 = 这条路走到底就无路可走。"撤销选择"不是可选的——它是回溯的定义本身。缺了撤销 = 不是回溯，而是简单的 DFS 搜索。

**【语录】** "敌进我退，敌退我进"——前进后必须能后退，后退是为了下一次更好地前进。

**纠正代码：**
```python
def permute(nums):
    result = []
    visited = [False] * len(nums)
    def backtrack(path):
        if len(path) == len(nums):
            result.append(path[:])
            return
        for i in range(len(nums)):
            if visited[i]: continue
            visited[i] = True
            path.append(nums[i])
            backtrack(path)
            path.pop()
            visited[i] = False
    backtrack([])
    return result
```

---

### 错误 #8: 最大子数组和负数直接归零

**错误代码：**
```python
def maxSubArray(nums):
    cur_sum = 0
    max_sum = float('-inf')
    for num in nums:
        cur_sum += num
        if cur_sum < 0:
            cur_sum = 0  # 负数归零 —— 错！
        max_sum = max(max_sum, cur_sum)
    return max_sum
```

**现象：** `[-1]` 返回 `0`（期望 `-1`）。全负数数组返回 `0` 而非最大负数。`[-2,-1]` 返回 `0`（期望 `-1`）。

**【矛盾分析】主要矛盾识别错误**：在 Kadane 算法中，"丢弃负数前缀"的逻辑适用于**存在正数**的数组。全负数数组时，最大子数组和是最大的那个负数。`cur_sum < 0` 归零的前提是"后面有正数能拉回来"——但全负数时这个前提不成立。

**【语录】** "具体问题具体分析"——不能把"负数归零"当成普遍真理。全负数数组是矛盾的特殊性。

**纠正代码：**
```python
def maxSubArray(nums):
    cur_sum = max_sum = nums[0]
    for num in nums[1:]:
        cur_sum = max(num, cur_sum + num)
        max_sum = max(max_sum, cur_sum)
    return max_sum
```

---

### 错误 #9: 跳跃游戏 II 边界判断顺序错误

**错误代码：**
```python
def jump(nums):
    n = len(nums)
    jumps = 0
    cur_end = 0
    farthest = 0
    for i in range(n):
        farthest = max(farthest, i + nums[i])
        if i == cur_end:
            jumps += 1
            cur_end = farthest
        if cur_end >= n - 1:
            return jumps
    return jumps
```

**现象：** `[0]` 返回 `1`（期望 `0`，已经在终点）。`[2,3,1,1,4]` 返回 `3`（期望 `2`）——因为在 `i==n-1` 时多跳了一次。

**【矛盾分析】主要矛盾识别错误**：`jumps++` 的条件 `i == cur_end` 不能包含 `i == n-1`（已经到达终点）。终点不需要再扩展可达边界——这是"还没到"和"已经到了"的逻辑混淆。

**【语录】** "一切矛盾都依一定条件向它们的反面转化"——`cur_end` 在到达终点后从"需要扩展"转化为"已经到达"的矛盾反面。

**纠正代码：**
```python
def jump(nums):
    n = len(nums)
    if n <= 1: return 0
    jumps = 0
    cur_end = 0
    farthest = 0
    for i in range(n - 1):  # 不到终点
        farthest = max(farthest, i + nums[i])
        if i == cur_end:
            jumps += 1
            cur_end = farthest
    return jumps
```

---

### 错误 #10: 二叉树层序遍历循环中修改队列长度

**错误代码：**
```python
def levelOrder(root):
    if not root: return []
    queue = [root]
    result = []
    while queue:
        level = []
        size = len(queue)
        for i in range(size):
            node = queue.pop(0)
            level.append(node.val)
            if node.left: queue.append(node.left)
            if node.right: queue.append(node.right)
        result.append(level)
    return result
```

**现象：** 这段代码其实是**正确的**。上面的写法用 `size = len(queue)` 缓存了长度。

**真正容易犯的错误是下面这样：**

```python
def levelOrder(root):
    if not root: return []
    queue = [root]
    result = []
    while queue:
        level = []
        for i in range(len(queue)):  # len(queue) 在循环中动态变化！
            node = queue.pop(0)
            level.append(node.val)
            if node.left: queue.append(node.left)
            if node.right: queue.append(node.right)
        result.append(level)
    return result
```

**现象：** `range(len(queue))` 在每次迭代都重新计算长度，但 `queue` 在循环中不断增长（孩子节点被追加），导致循环次数远超当前层应有的节点数——层与层之间混乱了。

**【矛盾分析】主要矛盾识别错误**：`len(queue)` 是**动态**的，而层序遍历需要**静态**的当前层大小。用动态长度控制静态需求 = 矛盾错位。

**【语录】** "凡事预则立，不预则废"——必须预先（进入循环前）确定当前层的节点数。

**纠正代码（错误版本修正）：**
```python
size = len(queue)
for i in range(size):
    ...
```

---

## 二、边界遗漏（10 例）—— 空数组 / 单元素 / 极值

> "没有调查就没有发言权"——没调查边界就写代码。

---

### 错误 #11: 二分查找 while left <= right 写成了 <

**错误代码：**
```python
def binarySearch(nums, target):
    left, right = 0, len(nums) - 1
    while left < right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

**现象：** 单元素数组 `[5], target=5` 返回 `-1`（期望 `0`）。因为 `left=0, right=0`，`0 < 0` 为 False，直接跳出循环。

**【矛盾分析】主要矛盾识别错误**：`left < right` 在区间长度为 1 时放弃了最后一个元素。而二分查找的矛盾在于"区间收缩到最后恰好剩一个元素"，不应该在检查前就排除它。

**【语录】** "扫帚不到，灰尘照例不会自己跑掉"——不检查最后一个元素，它就不会被找到。

**纠正代码：**
```python
def binarySearch(nums, target):
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

---

### 错误 #12: 链表反转空链表

**错误代码：**
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

**现象：** 这段代码对空链表 `head=None` 实际是**正确的**（`cur=None` 跳过 while，返回 `prev=None`）。

**容易犯错的是递归版：**

```python
def reverseList(head):
    if not head.next:  # 空链表直接炸了
        return head
    new_head = reverseList(head.next)
    head.next.next = head
    head.next = None
    return new_head
```

**现象：** `None` 没有 `.next` 属性 → `AttributeError`。

**【矛盾分析】主要矛盾识别错误**：未调查空链表的特殊情况。空链表是"没有矛盾"的特殊状态，但代码假设了至少有一个节点。

**【语录】** "没有调查就没有发言权"——没调查链表长度就假设了至少一个节点。

**纠正代码：**
```python
def reverseList(head):
    if not head or not head.next:
        return head
    new_head = reverseList(head.next)
    head.next.next = head
    head.next = None
    return new_head
```

---

### 错误 #13: 爬楼梯 n=1 时 dp[2] 越界

**错误代码：**
```python
def climbStairs(n):
    dp = [0] * (n + 1)
    dp[1] = 1
    dp[2] = 2  # n=1 时越界！
    for i in range(3, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]
```

**现象：** `n=1` → `IndexError: list assignment index out of range`。

**【矛盾分析】主要矛盾识别错误**：dp[2] 在 n=1 时不存在。初始化时只考虑了"一般情况"（n≥2），没调查"特殊情况"（n=1）。这是先入为主，"我默认输入是常规输入"。

**【语录】** "矛盾的普遍性即寓于矛盾的特殊性之中"——处理 n≥2 的一般情况前，必须先处理 n=1 的特殊情况。

**纠正代码：**
```python
def climbStairs(n):
    if n <= 2:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    dp[2] = 2
    for i in range(3, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]
```

---

### 错误 #14: 有效括号栈空时 pop

**错误代码：**
```python
def isValid(s):
    stack = []
    for ch in s:
        if ch in '({[':
            stack.append(ch)
        else:
            top = stack.pop()  # 栈空时直接炸
            if (ch == ')' and top != '(') or \
               (ch == ']' and top != '[') or \
               (ch == '}' and top != '{'):
                return False
    return len(stack) == 0
```

**现象：** `")"` → `IndexError: pop from empty list`（期望 `False`）。

**【矛盾分析】主要矛盾识别错误**：pop 之前没有检查栈是否为空。栈空意味着"右括号没有对应的左括号"——这是一个合法的 false 判定，不是异常。

**【语录】** "凡事预则立，不预则废"——pop 前必须先检查，否则遇到意外输入就崩溃。

**纠正代码：**
```python
def isValid(s):
    stack = []
    pairs = {')': '(', ']': '[', '}': '{'}
    for ch in s:
        if ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
        else:
            stack.append(ch)
    return len(stack) == 0
```

---

### 错误 #15: 两数之和只有一个元素

**错误代码：**
```python
def twoSum(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []
```

**现象：** `[5], 5` 返回 `[]`（期望也是没有解，但至少应该显式处理）。如果题意保证必有解，那更严重——直接返回空数组不符合题意。

**【矛盾分析】主要矛盾识别错误**：未考虑输入长度 < 2 的特殊情况。数组长度不足时根本没有"两数"这个概念，题目约束失效。

**【语录】** "没有调查就没有发言权"——没调查数组长度就进入了两层循环。

**纠正代码：**
```python
def twoSum(nums, target):
    if len(nums) < 2:
        return []
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
```

---

### 错误 #16: 反转整数溢出判断顺序错误

**错误代码：**
```python
def reverse(x):
    result = 0
    while x != 0:
        result = result * 10 + x % 10
        x //= 10
        if result > 2**31 - 1 or result < -2**31:
            return 0
    return result
```

**现象：** `1534236469` 反转后应在溢出前触发判断……但这里**先加了再判断**——在 Python 中不会溢出（因为 Python 的 int 是无限精度的），但在 Java/C++ 中会。不过在 Python 中，逻辑上应该是**在加之前判断**。

**【矛盾分析】主要矛盾识别错误**：溢出判断应该在操作前做，而不是操作后补救。"先做了再检查"相当于先跳进坑里再喊疼。

**【语录】** "在战术上重视敌人"——溢出这个敌人要在它发生之前就防御，而不是事后补救。

**纠正代码：**
```python
def reverse(x):
    result = 0
    INT_MAX = 2**31 - 1
    INT_MIN = -2**31
    while x != 0:
        digit = x % 10
        x //= 10
        if result > INT_MAX // 10 or (result == INT_MAX // 10 and digit > 7):
            return 0
        if result < INT_MIN // 10 or (result == INT_MIN // 10 and digit > 8):
            return 0
        result = result * 10 + digit
    return result
```

---

### 错误 #17: 二叉树最大深度空节点返回 1

**错误代码：**
```python
def maxDepth(root):
    if not root:
        return 1  # 空节点返回 1？大错！
    return 1 + max(maxDepth(root.left), maxDepth(root.right))
```

**现象：** 空树返回 `1`（期望 `0`）。每个叶子节点的左右孩子都是空节点，返回 `1`，导致深度被多算了整棵树的叶子数量。

**【矛盾分析】主要矛盾识别错误**：空节点是"无"，深度是 0。把空节点当"有（深度为 0 的节点）"和当"深度为 1"是两回事——这混淆了"节点不存在"和"节点存在但无子节点"。

**【语录】** "量变引起质变"——每个空节点多加 1，累积起来就彻底改变了深度的定义（质变）。

**纠正代码：**
```python
def maxDepth(root):
    if not root:
        return 0
    return 1 + max(maxDepth(root.left), maxDepth(root.right))
```

---

### 错误 #18: 滑动窗口右移先移动再判断

**错误代码：**
```python
def minSubArrayLen(target, nums):
    left = 0
    cur_sum = 0
    min_len = float('inf')
    for right in range(len(nums)):
        cur_sum += nums[right]
        right += 1  # 错误：在 for 循环中又手动右移！
        while cur_sum >= target:
            min_len = min(min_len, right - left)
            cur_sum -= nums[left]
            left += 1
    return min_len if min_len != float('inf') else 0
```

**现象：** 窗口大小计算完全错乱——`right` 在 `for` 循环中已经被 `range` 自动递增，又手动 `right += 1` 导致跳过了元素。

**【矛盾分析】主要矛盾识别错误**：`for right in range(...)` 已经管理了 right 的移动，再手动修改 right 造成了双重控制——同一个变量被两个机制控制，矛盾乱象。

**【语录】** "牵一发动全身"——right 指针的每次移动都牵动着整个窗口的计算。

**纠正代码：**
```python
def minSubArrayLen(target, nums):
    left = 0
    cur_sum = 0
    min_len = float('inf')
    for right in range(len(nums)):
        cur_sum += nums[right]
        while cur_sum >= target:
            min_len = min(min_len, right - left + 1)
            cur_sum -= nums[left]
            left += 1
    return min_len if min_len != float('inf') else 0
```

---

### 错误 #19: 找峰值单元素数组 mid 越界

**错误代码：**
```python
def findPeakElement(nums):
    left, right = 0, len(nums) - 1
    while left < right:
        mid = (left + right) // 2
        if nums[mid] > nums[mid + 1]:  # mid+1 可能越界？
            right = mid
        else:
            left = mid + 1
    return left
```

**现象：** `mid` 在 `left < right` 条件下永远小于 `right`，所以 `mid + 1 <= right`——不越界。这段代码看起来正确。

**真正容易犯错的版本：**

```python
def findPeakElement(nums):
    if len(nums) == 1:
        return 0
    left, right = 0, len(nums) - 1
    while left <= right:  # 用了 <=
        mid = (left + right) // 2
        if nums[mid] < nums[mid + 1]:  # 单元素时 mid=0, mid+1=1 越界
            left = mid + 1
        else:
            right = mid - 1
    return left
```

**现象：** `[1]` → `IndexError`。因为在进入循环前虽然判断了 `len(nums) == 1`，但如果 while 条件是 `<=` 且元素判断写在了越界检查之前，单元素情况无法被 while 正确退出。

**【矛盾分析】主要矛盾识别错误**：`while left <= right` 意味着区间为空时才退出，单元素时 `left=right=0`，进入循环，`mid=0`，`nums[0+1]` 越界。

**【语录】** "具体问题具体分析"——单元素数组不需要二分，直接返回 0。

**纠正代码：**
```python
def findPeakElement(nums):
    left, right = 0, len(nums) - 1
    while left < right:
        mid = (left + right) // 2
        if nums[mid] > nums[mid + 1]:
            right = mid
        else:
            left = mid + 1
    return left
```

---

### 错误 #20: 旋转数组找最小值有重复元素

**错误代码：**
```python
def findMin(nums):
    left, right = 0, len(nums) - 1
    while left < right:
        mid = (left + right) // 2
        if nums[mid] > nums[right]:
            left = mid + 1
        else:
            right = mid  # nums[mid] == nums[right] 时也走这里 → 死循环或错误
    return nums[left]
```

**现象：** `[2,2,2,0,1]` —— `mid=2`, `nums[2]=2`, `nums[4]=1`, 走 `right=mid=2`。下一步 `mid=1`, `nums[1]=2`, `nums[2]=2`, `right=1`。最终返回 `2`（期望 `0`）。

**【矛盾分析】主要矛盾识别错误**：`nums[mid] == nums[right]` 时，不知道最小值在左边还是右边（因为有重复元素）。不能简单归到哪个分支——必须单独处理。

**【语录】** "不同质的矛盾要用不同质的方法解决"——相等情况的矛盾（不确定方向）不同于 < 或 > 的情况。

**纠正代码：**
```python
def findMin(nums):
    left, right = 0, len(nums) - 1
    while left < right:
        mid = (left + right) // 2
        if nums[mid] > nums[right]:
            left = mid + 1
        elif nums[mid] < nums[right]:
            right = mid
        else:
            right -= 1  # nums[mid] == nums[right]，无法判断，保守缩小
    return nums[left]
```

---

## 三、工具误用（5 例）—— 数据结构选错了

> "不同质的矛盾要用不同质的方法解决。"

---

### 错误 #21: 用 list.pop(0) 当队列用

**错误代码：**
```python
from collections import deque

def bfs(graph, start):
    queue = []  # 用 list 当队列
    queue.append(start)
    visited = set()
    while queue:
        node = queue.pop(0)  # O(n) 操作！
        if node in visited:
            continue
        visited.add(node)
        for neighbor in graph[node]:
            queue.append(neighbor)
    return visited
```

**现象：** 对于 10 万个节点的 BFS，`pop(0)` 每次都要搬移整个列表，导致 O(n²) 时间。

**【矛盾分析】主要矛盾识别错误**：队列的矛盾是"先进先出"，需要高效的头部移除。`list` 底层是数组，`pop(0)` 需要移动所有后续元素。`deque` 底层是双向链表，`popleft()` 是 O(1)。选了错误的武器去打仗。

**【语录】** "不同质的矛盾要用不同质的方法解决"——先进先出（队列）和后进先出（栈）是不同的矛盾，需要不同的数据结构。

**纠正代码：**
```python
from collections import deque

def bfs(graph, start):
    queue = deque([start])
    visited = set()
    while queue:
        node = queue.popleft()  # O(1)
        if node in visited:
            continue
        visited.add(node)
        for neighbor in graph[node]:
            queue.append(neighbor)
    return visited
```

---

### 错误 #22: 用栈做 BFS 最短路径

**错误代码：**
```python
def shortestPath(grid, start, end):
    rows, cols = len(grid), len(grid[0])
    stack = [start]  # 用栈做最短路径搜索
    visited = set()
    dist = {start: 0}
    while stack:
        x, y = stack.pop()  # DFS 顺序，不是 BFS！
        if (x, y) == end:
            return dist[(x, y)]
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == 0:
                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    stack.append((nx, ny))
                    dist[(nx, ny)] = dist[(x, y)] + 1
    return -1
```

**现象：** 找到了路径但**不是最短的**。因为 DFS（栈）是深度优先，先走到深层，记录的距离可能不是最短的。在 BFS 中第一次到达终点一定是最短路径，但 DFS 不是。

**【矛盾分析】主要矛盾识别错误**：Dijkstra/BFS 的"无权重图最短路径"依赖于**按层扩展**，栈（LIFO）无法保证这一点。栈的本质是"先苦后甜"，先深入再撤回——不是按距离排序的。

**【语录】** "前途是光明的，道路是曲折的"——栈走的路是曲折的（深度优先），而最短路径需要光明的直达（宽度优先）。

**纠正代码：**
```python
from collections import deque

def shortestPath(grid, start, end):
    rows, cols = len(grid), len(grid[0])
    queue = deque([start])
    visited = {start}
    dist = {start: 0}
    while queue:
        x, y = queue.popleft()  # BFS
        if (x, y) == end:
            return dist[(x, y)]
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == 0:
                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append((nx, ny))
                    dist[(nx, ny)] = dist[(x, y)] + 1
    return -1
```

---

### 错误 #23: Top K 用了大顶堆

**错误代码：**
```python
import heapq

def topKFrequent(nums, k):
    from collections import Counter
    freq = Counter(nums)
    heap = []
    for num, count in freq.items():
        heapq.heappush(heap, (-count, num))  # 大顶堆：取反后入小顶堆
    result = []
    for _ in range(k):
        result.append(heapq.heappop(heap)[1])
    return result
```

**现象：** 这段代码虽然**能工作**，但把所有 n 个元素都入了堆（O(n log n)），而只需要 k 个。

**真正糟糕的版本：**
```python
def topKFrequent(nums, k):
    freq = Counter(nums)
    heap = []
    for num, count in freq.items():
        heapq.heappush(heap, (count, num))
    return [heapq.heappop(heap)[1] for _ in range(min(k, len(heap)))]
```

**现象：** 小顶堆弹出的是最小值，`heappop` 会弹出频次**最低**的元素，而不是最高的 k 个。期望 Top-K 高频，实际返回 Bottom-K 低频。

**【矛盾分析】主要矛盾识别错误**：Top K 的堆算法应该是**小顶堆维护 k 个最大元素**，满了就弹掉最小的。而不是把所有元素入大顶堆再弹 k 次——空间和时间都浪费了。混淆了"筛选 Top K"和"排序取前 K"。

**【语录】** "集中优势兵力"——只维护 k 个元素的小顶堆，而不是所有 n 个。

**纠正代码：**
```python
import heapq

def topKFrequent(nums, k):
    freq = Counter(nums)
    heap = []
    for num, count in freq.items():
        heapq.heappush(heap, (count, num))
        if len(heap) > k:
            heapq.heappop(heap)
    return [num for _, num in heap]
```

---

### 错误 #24: 用数组实现 O(1) 双端操作

**错误代码：**
```python
def slidingWindowMax(nums, k):
    result = []
    window = []  # 用 list 维护窗口
    for i, num in enumerate(nums):
        window.append(num)
        if i >= k:
            window.pop(0)  # O(k) 移除最左元素
        if i >= k - 1:
            result.append(max(window))  # O(k) 取最大值
    return result
```

**现象：** 每次滑动做 O(k) 操作，总共 O(n·k)，数据一大就超时。

**【矛盾分析】主要矛盾识别错误**：滑动窗口需要两端操作——加在右边、从左边删、查最大值。list 只擅长尾部操作，头部操作是 O(n)。应该用**双端队列（deque）+ 单调递减**维护最大值。选择了不支持双端 O(1) 的工具。

**【语录】** "工具是矛盾解决的物质手段"——没有合适的工具，矛盾就解决不了。

**纠正代码：**
```python
from collections import deque

def slidingWindowMax(nums, k):
    result = []
    dq = deque()
    for i, num in enumerate(nums):
        while dq and nums[dq[-1]] <= num:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            result.append(nums[dq[0]])
    return result
```

---

### 错误 #25: LRU 缓存只用了数组

**错误代码：**
```python
class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}  # key -> value
        self.order = []  # 记录访问顺序

    def get(self, key):
        if key not in self.cache:
            return -1
        self.order.remove(key)  # O(n)!
        self.order.append(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.order.remove(key)  # O(n)!
        elif len(self.cache) >= self.capacity:
            lru = self.order.pop(0)  # O(n)!
            del self.cache[lru]
        self.order.append(key)
        self.cache[key] = value
```

**现象：** `remove` 和 `pop(0)` 都是 O(n)，导致 get/put 都是 O(n)，而非题目要求的 O(1)。

**【矛盾分析】主要矛盾识别错误**：LRU 的矛盾是"快速找到最近最少使用的元素并删除，同时快速更新访问顺序"。数组无法同时满足这两点——它要么擅长尾部（O(1) append），要么支持 O(1) 删除（不能）。需要**双向链表（O(1) 删除 + 移动）+ 哈希表（O(1) 查找）**的组合。

**【语录】** "集中优势兵力，各个击破"——哈希表负责查找（O(1)），双向链表负责顺序维护（O(1)），分工明确。

**纠正代码：**
```python
class Node:
    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_tail(self, node):
        node.prev = self.tail.prev
        node.next = self.tail
        self.tail.prev.next = node
        self.tail.prev = node

    def get(self, key):
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._remove(node)
        self._add_to_tail(node)
        return node.value

    def put(self, key, value):
        if key in self.cache:
            self._remove(self.cache[key])
        elif len(self.cache) >= self.capacity:
            lru = self.head.next
            self._remove(lru)
            del self.cache[lru.key]
        node = Node(key, value)
        self._add_to_tail(node)
        self.cache[key] = node
```

---

## 四、效率浪费（5 例）—— O(n) 写成了 O(n²)

> "在战术上重视敌人"——细节决定成败。

---

### 错误 #26: 两数之和暴力双重循环

**错误代码：**
```python
def twoSum(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
```

**现象：** 能通过小数据，但 n = 10⁴ 时 O(n²) 超时。LeetCode 判题直接 TLE。

**【矛盾分析】主要矛盾识别错误**：查找 "target - num" 的 index 是核心操作——这个操作应该 O(1) 而不是 O(n)。双重循环把每个元素都当作独立候选去逐个匹配，没有利用"哈希表 O(1) 查找"这个武器。

**【语录】** "群众路线"——每个元素都是群众，存入哈希表后发动群众 O(1) 帮你查找。

**纠正代码：**
```python
def twoSum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        if target - num in seen:
            return [seen[target - num], i]
        seen[num] = i
```

---

### 错误 #27: 斐波那契纯递归无记忆化

**错误代码：**
```python
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)
```

**现象：** n = 40 时计算超过 1 秒；n = 50 时几乎算不出来。因为大量重复计算——`fib(5)` 被计算了 8 次，`fib(40)` 的计算量是指数级的 O(2ⁿ)。

**【矛盾分析】主要矛盾识别错误**：递归树中有大量重叠子树，但每次遇到都重新计算一遍。子问题被重复解决 = 重复劳动。记忆化搜索的本质是"已经解决的问题不再解决"——用空间换时间。

**【语录】** "星星之火，可以燎原"——从 dp[0]、dp[1] 这个星火开始，一直蔓延到 dp[n]。如果每次都从星火重新蔓延，那永远烧不到远方。

**纠正代码：**
```python
def fib(n):
    memo = {}
    def dp(i):
        if i <= 1:
            return i
        if i not in memo:
            memo[i] = dp(i - 1) + dp(i - 2)
        return memo[i]
    return dp(n)

# 或迭代版
def fib(n):
    if n <= 1: return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
```

---

### 错误 #28: 查询区间和每次重新遍历

**错误代码：**
```python
def rangeSum(nums, queries):
    result = []
    for l, r in queries:
        total = 0
        for i in range(l, r + 1):
            total += nums[i]
        result.append(total)
    return result
```

**现象：** m 个查询，每个 O(n)，总共 O(m·n)。n = 10⁵、m = 10⁵ 时直接超时。

**【矛盾分析】主要矛盾识别错误**：区间求和是"预处理 vs 即时计算"的矛盾。暴力是每次即时计算。正确做法是预先计算前缀和数组，查询时 O(1) 相减——把 O(n) 的重复劳动转化为 O(1) 的一步操作。

**【语录】** "凡事预则立，不预则废"——预处理前缀和是"预"，查询时 O(1) 是"立"。

**纠正代码：**
```python
def rangeSum(nums, queries):
    prefix = [0]
    for num in nums:
        prefix.append(prefix[-1] + num)
    result = []
    for l, r in queries:
        result.append(prefix[r + 1] - prefix[l])
    return result
```

---

### 错误 #29: 字符串拼接用 += 在循环里

**错误代码：**
```python
def buildString(words):
    result = ""
    for w in words:
        result += w  # 每次创建新字符串，拷贝所有已有内容
    return result
```

**现象：** n 个单词总长度 M，循环中 `result += w` 每次创建新字符串时拷贝的字符数递增：1 + 2 + 3 + ... + M ≈ O(M²)。M = 10⁶ 时极慢。

**【矛盾分析】主要矛盾识别错误**：Python 中字符串是不可变的，`+=` 并非原地修改——而是创建新字符串并拷贝全部内容。这导致了重复劳动。应该用 `''.join()` 一次性拼接，只需一次遍历。

**【语录】** "集中优势兵力，各个击破"——不要把兵力（字符拷贝）分散在每次迭代中，集中在最后一次性完成。

**纠正代码：**
```python
def buildString(words):
    return ''.join(words)
```

---

### 错误 #30: 去重用线性搜索替代哈希检查

**错误代码：**
```python
def removeDuplicates(arr):
    result = []
    for x in arr:
        found = False
        for y in result:  # O(n) 查找
            if x == y:
                found = True
                break
        if not found:
            result.append(x)
    return result
```

**现象：** 内层循环每次遍历 result，总复杂度 O(n²)。10⁵ 个元素超时。

**【矛盾分析】主要矛盾识别错误**：去重的核心操作是"判断是否已存在"——应该是 O(1) 的哈希查找，而不是 O(n) 的线性扫描。每增加一个元素都重新遍历所有已有元素，重复劳动成倍增长。

**【语录】** "群众路线"——把已有元素发动到哈希集合里，新元素来时 O(1) 就能判断是否见过。

**纠正代码：**
```python
def removeDuplicates(arr):
    seen = set()
    result = []
    for x in arr:
        if x not in seen:
            seen.add(x)
            result.append(x)
    return result
```

---

## 总结：错误分类速查表

| 类别 | 错误号 | 矛盾本质 | 语录 |
|-----|--------|---------|------|
| **逻辑错误** | #1-#10 | 思路根本不对，算法假设不成立 | "路线错了" |
| **边界遗漏** | #11-#20 | 只考虑一般情况，忽略极端 | "没有调查就没有发言权" |
| **工具误用** | #21-#25 | 数据结构与操作需求不匹配 | "不同质的矛盾不同方法" |
| **效率浪费** | #26-#30 | 重复劳动、未利用空间换时间 | "在战术上重视敌人" |

> "错误和挫折教训了我们，使我们比较地聪明起来了。" —— 《毛泽东选集》第三卷

