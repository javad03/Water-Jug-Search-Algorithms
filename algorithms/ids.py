"""
Iterative Deepening Search (IDS) Algorithm
جستجوی عمقی با عمق‌یابی تکراری
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from state import State, get_successors, reconstruct_path, print_solution


def depth_limited_search(state, goal_jug4, goal_jug3, limit, visited):
    """
    جستجوی عمقی محدود (DLS) - کمکی برای IDS
    
    این تابع یک DFS است که فقط تا عمق limit می‌رود
    
    Returns:
        tuple: (راه‌حل, تعداد گره‌های بسط شده, وضعیت)
        وضعیت می‌تواند باشد: 'found', 'cutoff', 'failure'
    """
    nodes_expanded = 0
    
    # بررسی هدف
    if state.is_goal(goal_jug4, goal_jug3):
        return reconstruct_path(state), 1, 'found'
    
    # اگر به محدودیت عمق رسیدیم
    if limit == 0:
        return None, 1, 'cutoff'
    
    visited.add(state)
    nodes_expanded += 1
    cutoff_occurred = False
    
    # بسط فرزندان
    for successor in get_successors(state):
        if successor not in visited:
            result, expanded, status = depth_limited_search(
                successor, goal_jug4, goal_jug3, limit - 1, visited
            )
            nodes_expanded += expanded
            
            if status == 'found':
                return result, nodes_expanded, 'found'
            elif status == 'cutoff':
                cutoff_occurred = True
    
    visited.remove(state)  # backtrack
    
    if cutoff_occurred:
        return None, nodes_expanded, 'cutoff'
    else:
        return None, nodes_expanded, 'failure'


def ids(initial_state, goal_jug4=2, goal_jug3=0, max_depth=20):
    """
    الگوریتم جستجوی عمقی با عمق‌یابی تکراری (IDS)
    
    ویژگی‌ها:
    - کامل (Complete): مانند BFS، راه‌حل را پیدا می‌کند
    - بهینه (Optimal): کوتاه‌ترین راه را پیدا می‌کند
    - پیچیدگی زمانی: O(b^d) - مشابه BFS
    - پیچیدگی مکانی: O(bd) - بسیار کمتر از BFS!
    
    نحوه کار:
    1. جستجوی DFS را با عمق 0 شروع می‌کند
    2. اگر راه‌حل پیدا نشد، عمق را 1 افزایش می‌دهد
    3. این کار را تکرار می‌کند تا راه‌حل پیدا شود یا به max_depth برسد
    
    مزیت: ترکیب مزایای BFS (کامل و بهینه) و DFS (حافظه کم)
    """
    
    total_nodes_expanded = 0
    
    # تکرار با افزایش عمق
    for depth in range(max_depth + 1):
        visited = set()
        result, nodes_expanded, status = depth_limited_search(
            initial_state, goal_jug4, goal_jug3, depth, visited
        )
        
        total_nodes_expanded += nodes_expanded
        
        # اگر راه‌حل پیدا شد
        if status == 'found':
            return result, total_nodes_expanded
        
        # اگر در این عمق cutoff نشد، یعنی راه‌حلی وجود ندارد
        if status == 'failure':
            return None, total_nodes_expanded
    
    # اگر به max_depth رسیدیم و راه‌حل پیدا نشد
    return None, total_nodes_expanded


if __name__ == "__main__":
    # تست الگوریتم IDS
    print("Testing IDS Algorithm...")
    initial = State(0, 0)
    path, nodes_expanded = ids(initial)
    print_solution(path, nodes_expanded, "Iterative Deepening Search (IDS)")