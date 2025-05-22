import re
import random
import time

# Common algorithm solutions for different problem types
SOLUTIONS = {
    "array": {
        "templates": [
            """def twoSum(nums, target):
    # Time: O(n), Space: O(n)
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []""",
            
            """def maxSubArray(nums):
    # Kadane's algorithm
    # Time: O(n), Space: O(1)
    max_so_far = nums[0]
    max_ending_here = nums[0]
    
    for i in range(1, len(nums)):
        max_ending_here = max(nums[i], max_ending_here + nums[i])
        max_so_far = max(max_so_far, max_ending_here)
    
    return max_so_far"""
        ]
    },
    "string": {
        "templates": [
            """def isPalindrome(s):
    # Time: O(n), Space: O(1)
    left, right = 0, len(s) - 1
    
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        
        if s[left].lower() != s[right].lower():
            return False
        
        left += 1
        right -= 1
    
    return True""",
            
            """def longestPalindrome(s):
    # Time: O(n²), Space: O(1)
    if not s:
        return ""
    
    start = 0
    max_len = 1
    
    def expand_around_center(left, right):
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return right - left - 1
    
    for i in range(len(s)):
        # Odd length
        len1 = expand_around_center(i, i)
        # Even length
        len2 = expand_around_center(i, i + 1)
        
        length = max(len1, len2)
        if length > max_len:
            max_len = length
            start = i - (length - 1) // 2
    
    return s[start:start + max_len]"""
        ]
    },
    "linked-list": {
        "templates": [
            """class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverseLinkedList(head):
    # Time: O(n), Space: O(1)
    prev = None
    current = head
    
    while current:
        next_temp = current.next
        current.next = prev
        prev = current
        current = next_temp
    
    return prev""",
            
            """class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def detectCycle(head):
    # Floyd's Tortoise and Hare (Cycle Detection)
    # Time: O(n), Space: O(1)
    if not head or not head.next:
        return None
    
    slow = head
    fast = head
    
    # Find meeting point
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            break
    
    if slow != fast:
        return None
    
    # Find cycle start
    slow = head
    while slow != fast:
        slow = slow.next
        fast = fast.next
    
    return slow"""
        ]
    },
    "tree": {
        "templates": [
            """class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def inorderTraversal(root):
    # Time: O(n), Space: O(n)
    result = []
    
    def dfs(node):
        if not node:
            return
        dfs(node.left)
        result.append(node.val)
        dfs(node.right)
    
    dfs(root)
    return result""",
            
            """class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def isValidBST(root):
    # Time: O(n), Space: O(n)
    def validate(node, low=float('-inf'), high=float('inf')):
        if not node:
            return True
        
        if node.val <= low or node.val >= high:
            return False
        
        return (validate(node.left, low, node.val) and 
                validate(node.right, node.val, high))
    
    return validate(root)"""
        ]
    },
    "dynamic-programming": {
        "templates": [
            """def fibonacci(n):
    # Time: O(n), Space: O(n)
    if n <= 1:
        return n
    
    dp = [0] * (n + 1)
    dp[1] = 1
    
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    
    return dp[n]""",
            
            """def longestIncreasingSubsequence(nums):
    # Time: O(n²), Space: O(n)
    if not nums:
        return 0
    
    n = len(nums)
    dp = [1] * n
    
    for i in range(1, n):
        for j in range(i):
            if nums[i] > nums[j]:
                dp[i] = max(dp[i], dp[j] + 1)
    
    return max(dp)"""
        ]
    },
    "graph": {
        "templates": [
            """def dfs(graph, start, visited=None):
    # Time: O(V + E), Space: O(V)
    if visited is None:
        visited = set()
    
    visited.add(start)
    print(start, end=' ')  # Process node
    
    for neighbor in graph[start]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
    
    return visited""",
            
            """from collections import deque

def bfs(graph, start):
    # Time: O(V + E), Space: O(V)
    visited = set([start])
    queue = deque([start])
    result = []
    
    while queue:
        node = queue.popleft()
        result.append(node)
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return result"""
        ]
    },
    "math": {
        "templates": [
            """def isPrime(n):
    # Time: O(sqrt(n)), Space: O(1)
    if n <= 1:
        return False
    if n <= 3:
        return True
    
    if n % 2 == 0 or n % 3 == 0:
        return False
    
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    
    return True""",
            
            """def gcd(a, b):
    # Euclidean algorithm
    # Time: O(log(min(a, b))), Space: O(log(min(a, b)))
    if b == 0:
        return a
    return gcd(b, a % b)
    
def lcm(a, b):
    return a * b // gcd(a, b)"""
        ]
    }
}

def extract_key_details(problem_text):
    """Extract key details from problem description."""
    # Look for common patterns in problem statements
    patterns = {
        "array_sum": r"(sum|total|add).*?(array|list|nums)",
        "palindrome": r"(palindrome|palindromic)",
        "linked_list": r"(linked list|listnode)",
        "tree_traversal": r"(tree|traversal|inorder|preorder|postorder)",
        "dynamic": r"(minimum|maximum|optimal|subarray|subsequence)",
        "binary_search": r"(sorted array|search|find.*in.*array)",
    }
    
    details = {}
    for key, pattern in patterns.items():
        if re.search(pattern, problem_text, re.IGNORECASE):
            details[key] = True
    
    return details

def get_solution(problem_text, problem_type):
    """Generate a solution based on problem description and type."""
    # Simulate thinking time to make it less suspicious
    time.sleep(random.uniform(1.5, 3.0))
    
    # Extract key details from problem text
    details = extract_key_details(problem_text)
    
    # Get solution template
    if problem_type in SOLUTIONS:
        templates = SOLUTIONS[problem_type]["templates"]
        solution = random.choice(templates)
        
        # Add explanation
        explanation = f"""
# Solution for the {problem_type} problem
# 
# Analysis:
# This problem can be approached using {'dynamic programming' if 'dynamic' in details else 
                                      'two pointers' if 'palindrome' in details else
                                      'depth-first search' if problem_type == 'tree' else
                                      'hash table for O(1) lookups' if problem_type == 'array' else
                                      'standard algorithms for this type of problem'}
#
# Time Complexity: {'O(n)' if problem_type in ['array', 'string', 'linked-list'] else 'O(n²)' if problem_type in ['dynamic-programming'] else 'O(n log n)'}
# Space Complexity: {'O(1)' if problem_type in ['array', 'linked-list'] else 'O(n)'}

{solution}

# To test this solution:
# 1. Define your test cases
# 2. Run the function with your inputs
# 3. Verify the outputs match expected results
"""
        return explanation
    else:
        return "No solution template available for this problem type. Please select a different type." 