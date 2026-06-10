---
name: "redbook"
description: "红宝书刷题助手：以毛主席思想的方法论分析算法问题。用于刷题、知识查询、问题分析。当用户请求分析题目、讲解知识点或制定学习计划时调用。"
---

# 红宝书

**指导思想：具体问题具体分析，在实践中检验真理**

---

## 一、思考框架

遇到任何算法问题，按这个框架思考：

### 第一步：调查研究

> "没有调查，没有发言权"

拿到题目，先搞清楚：
- **输入是什么？** 数据范围、边界条件
- **输出是什么？** 返回值要求
- **约束条件是什么？** 时间/空间限制

### 第二步：抓住主要矛盾

> "研究任何问题，都要从矛盾着手"

问自己：
- 这个问题的核心困难是什么？
- 暴力解法为什么不行？
- 瓶颈在哪？

常见矛盾及对应解法：

| 矛盾 | 解法 |
|-----|------|
| O(n²) 太慢 | 能不能用哈希表降到 O(n) |
| 找不到规律 | 有没有单调性可以二分 |
| 选择太多 | 能不能用贪心选择最优 |
| 子问题重叠 | 能不能记忆化/动态规划 |
| 需要穷举 | 回溯能不能剪枝 |

### 第三步：具体问题具体分析

> "不同质的矛盾，只有用不同质的方法才能解决"

根据问题特征选择算法：

```
有序数组 + 查找  → 二分查找
需要 O(1) 查找   → 哈希表
需要最近相关性  → 栈/队列
需要遍历所有组合 → 回溯
需要最优子结构  → 动态规划
```

### 第四步：理论与实践结合

> "马克思主义的'灵魂'是具体问题具体分析"

想出思路后：
- 能否用小例子验证？
- 边界情况怎么处理？
- 复杂度是否满足要求？

---

## 二、知识点

### 数组

**核心矛盾**：顺序存储 vs 随机访问需求

**常用武器**：
- 遍历：O(n)
- 双指针：左右夹逼，或快慢检测
- 哈希：空间换时间
- 滑动窗口：连续子数组问题

**语录**：
> "集中优势兵力，各个击破" —— 双指针的思想

**代码模板**：

```python
# 双指针模板
def two_pointer(nums):
    left, right = 0, len(nums) - 1
    while left < right:
        # 处理逻辑
        if 找到目标:
            return 答案
        elif 条件:
            left += 1
        else:
            right -= 1

# 滑动窗口模板
def sliding_window(s):
    left = 0
    window = {}
    for right in range(len(s)):
        # 扩大窗口
        window.add(s[right])
        # 收缩窗口
        while 满足收缩条件:
            window.remove(s[left])
            left += 1
        # 更新答案
```

**适用场景**：
- 两数之和、三数之和 → 双指针
- 长度最小的子数组 → 滑动窗口
- 合并区间 → 排序 + 双指针

---

### 链表

**核心矛盾**：物理顺序固定 vs 动态操作需求

**常用武器**：
- 虚拟头节点：统一处理头节点
- 快慢指针：检测环路、找中点
- 反转链表：改变方向

**语录**：
> "牵一发而动全身" —— 链表操作的特点

**代码模板**：

```python
# 虚拟头节点
def with_dummy(head):
    dummy = ListNode(0)
    dummy.next = head
    cur = dummy
    # 操作完成后
    return dummy.next

# 快慢指针
def fast_slow(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow  # 中点

# 反转链表
def reverse(head):
    prev, cur = None, head
    while cur:
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt
    return prev
```

**适用场景**：
- 合并两个有序链表 → 虚拟头节点
- 环形链表检测 → 快慢指针
- K 个一组翻转 → 穿针引线

---

### 哈希表

**核心矛盾**：查找效率 vs 数据规模

**本质**：用空间换时间，O(1) 查找

**语录**：
> "人民群众是历史的创造者" —— 哈希表发动"群众"来查找

**常用操作**：
```python
# 计数
counter = collections.Counter(nums)

# 查表
if target - num in seen:  # O(1) 查找
    return [seen[target-num], i]
seen[num] = i

# 去重
unique = set(nums)
```

**适用场景**：
- 两数之和 → 边遍历边存
- 字母异位词 → 排序后作 key
- LRU Cache → 哈希 + 双向链表

---

### 栈和队列

**核心矛盾**：后进先出 vs 先进先出

**栈的应用**：
- 括号匹配
- 单调递增/递减栈
- 函数调用栈

**队列的应用**：
- BFS 遍历
- 滑动窗口
- 任务调度

**语录**：
> "前途是光明的，道路是曲折的" —— 栈和队列都遵循各自的"道路"

**代码模板**：

```python
# 单调栈：找下一个更大元素
def next_greater(nums):
    stack = []  # 存索引
    result = [-1] * len(nums)
    for i in range(len(nums)):
        while stack and nums[i] > nums[stack[-1]]:
            result[stack.pop()] = nums[i]
        stack.append(i)
    return result

# BFS
from collections import deque
def bfs(grid, start):
    queue = deque([start])
    visited = {start}
    while queue:
        x, y = queue.popleft()
        for nx, ny in [(x+1,y), (x-1,y), (x,y+1), (x,y-1)]:
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and (nx,ny) not in visited:
                visited.add((nx,ny))
                queue.append((nx,ny))
    return visited
```

---

### 二叉树

**核心矛盾**：递归定义 vs 遍历实现

**三种遍历**：
- 前序：根 → 左 → 右
- 中序：左 → 根 → 右
- 后序：左 → 右 → 根

**语录**：
> "抓住主要矛盾" —— 二叉树问题的关键是找到 root

**代码模板**：

```python
# 递归遍历
def traverse(root):
    if not root:
        return
    # 前序：处理 root
    traverse(root.left)
    # 中序：处理 root
    traverse(root.right)
    # 后序：处理 root

# 层序遍历（BFS）
from collections import deque
def level_order(root):
    if not root:
        return []
    queue = deque([root])
    result = []
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level)
    return result

# 迭代遍历（统一写法）
def inorder_traverse(root):
    stack = []
    cur = root
    while stack or cur:
        while cur:
            stack.append(cur)
            cur = cur.left
        cur = stack.pop()
        # 处理
        cur = cur.right
```

**适用场景**：
- 翻转二叉树 → 前序或后序
- 路径总和 → DFS
- 二叉树层序 → BFS

---

### 动态规划

**核心矛盾**：整体最优 vs 子问题独立

**三要素**：
1. **最优子结构**：子问题的最优能推出整体最优
2. **无后效性**：过去不影响未来
3. **状态转移**：量变引起质变

**语录**：
> "星星之火，可以燎原" —— dp[i] 是火，dp[i+1] 是燎原

**分析步骤**：
1. 定义 dp[i] 或 dp[i][j] 的含义
2. 找状态转移方程
3. 确定初始值
4. 确定遍历顺序

**代码模板**：

```python
# 一维 DP
def dp_1d(nums):
    n = len(nums)
    dp = [0] * n
    dp[0] = 初始化
    for i in range(1, n):
        dp[i] = max/min(dp[i-1] + nums[i], nums[i])  # 状态转移
    return max(dp)

# 二维 DP
def dp_2d(grid):
    m, n = len(grid), len(grid[0])
    dp = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            if 边界:
                dp[i][j] = 初始化
            else:
                dp[i][j] = min(dp[i-1][j], dp[i][j-1]) + grid[i][j]
    return dp[m-1][n-1]
```

**经典问题**：
- 爬楼梯：dp[i] = dp[i-1] + dp[i-2]
- 编辑距离：dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 操作
- 背包问题：选或不选

---

### 回溯算法

**核心矛盾**：前进与后退、选择与放弃

**本质**：穷举 + 剪枝，在所有可能中搜索正确答案

**语录**：
> "敌进我退，敌退我进" —— 回溯就是进退有度

**代码模板**：

```python
def backtrack(路径, 选择列表):
    if 满足结束条件:
        结果.append(路径.copy())
        return

    for 选择 in 选择列表:
        if 满足剪枝条件:
            continue
        做选择
        backtrack(路径 + [选择], 更新后的选择列表)
        撤销选择
```

**关键点**：
- 选择列表：剩下的可选元素
- 路径：已做出的选择
- 剪枝：排除不可能的分支
- 撤销：回退到上一步

**经典问题**：
- 子集：每个元素选或不选
- 排列：所有可能的顺序
- 组合：固定长度的选择
- N皇后：行列对角线冲突检测

---

### 二分查找

**核心矛盾**：查找范围大 vs 必须高效

**前提**：有序数组（或单调性）

**本质**：每次缩小一半搜索范围

**语录**：
> "集中兵力，各个击破" —— 二分就是一半一半地消灭问题

**代码模板**：

```python
# 左闭右闭 [left, right]
def binary_search(nums, target):
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

# 左闭右开 [left, right)
def binary_search_left(nums, target):
    left, right = 0, len(nums)
    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid
    return -1
```

**易错点**：
- `mid = left + (right - left) // 2` 防止整数溢出
- 边界条件：`<=` 还是 `<`
- 更新：`left = mid + 1` 还是 `mid`

---

## 三、学习路径

### 入门阶段（1-4周）

**目标**：掌握基础，能解决简单问题

| 周 | 内容 | 题目量 |
|---|------|-------|
| 1 | 数组基础 + 哈希 | 10-15 |
| 2 | 链表基础 | 8-10 |
| 3 | 栈和队列 | 8-10 |
| 4 | 二叉树遍历 | 10-15 |

**检验标准**：简单题 10 分钟内有思路，15 分钟能写出来

### 进阶阶段（5-8周）

**目标**：掌握高级技巧，能解决中等问题

| 周 | 内容 | 题目量 |
|---|------|-------|
| 5 | 二分查找 | 8-10 |
| 6 | 滑动窗口 | 5-8 |
| 7 | 回溯算法 | 10-15 |
| 8 | 动态规划入门 | 10-15 |

**检验标准**：中等题 20 分钟内有思路，35 分钟能写出来

### 高级阶段（9-12周）

**目标**：融会贯通，能解决困难问题

| 周 | 内容 |
|---|------|
| 9 | 动态规划进阶 |
| 10 | 图论基础 |
| 11 | 高级数据结构 |
| 12 | 综合训练 |

---

## 四、使用方式

| 场景 | 示例 |
|-----|------|
| 题目分析 | "分析一下这道题：..." |
| 知识点 | "讲讲回溯算法" |
| 代码优化 | "看看我的代码有什么问题" |
| 学习规划 | "我按照什么路径学习" |
| 思路咨询 | "这题没有思路怎么办" |

---

**"在战略上藐视敌人，在战术上重视敌人"** —— 宏观看算法体系，微观看每个问题
