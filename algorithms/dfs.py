"""
Depth-First Search (DFS) Algorithm
جستجوی اول عمق
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from state import State, get_successors, reconstruct_path, print_solution


def dfs(initial_state, goal_jug4=2, goal_jug3=0, max_depth=20):
    """
    الگوریتم جستجوی اول عمق (DFS)
    
    ویژگی‌ها:
    - ناکامل (Incomplete): ممکن است در فضاهای نامحدود گیر کند
    - غیربهینه (Non-optimal): اولین راه‌حل پیدا شده، لزوماً کوتاه‌ترین نیست
    - پیچیدگی زمانی: O(b^m) که m = حداکثر عمق
    - پیچیدگی مکانی: O(bm) - بسیار کمتر از BFS
    
    نحوه کار:
    1. از پشته (Stack) برای ذخیره گره‌ها استفاده می‌کند (LIFO)
    2. تا انتهای یک شاخه می‌رود، سپس backtrack می‌کند
    3. محدودیت عمق برای جلوگیری از گیر کردن در مسیرهای بی‌نهایت
    
    Args:
        max_depth: حداکثر عمق مجاز برای جلوگیری از infinite loop
    """
    
    # پشته برای نگهداری گره‌های در انتظار بررسی (LIFO)
    # در پایتون از لیست استفاده می‌کنیم (append = push, pop = pop)
    stack = [initial_state]
    
    # مجموعه حالت‌های بازدید شده در مسیر فعلی (برای تشخیص چرخه)
    visited = set()
    
    # شمارنده تعداد گره‌های بسط داده شده
    nodes_expanded = 0
    
    # حلقه اصلی جستجو
    while stack:
        # برداشتن آخرین گره از پشته (LIFO)
        current_state = stack.pop()
        
        # اگر قبلاً بازدید شده، رد شو
        if current_state in visited:
            continue
            
        visited.add(current_state)
        nodes_expanded += 1
        
        # بررسی اینکه آیا به هدف رسیدیم
        if current_state.is_goal(goal_jug4, goal_jug3):
            path = reconstruct_path(current_state)
            return path, nodes_expanded
        
        # اگر به حداکثر عمق رسیدیم، بسط نکن
        if current_state.depth >= max_depth:
            continue
        
        # بسط گره فعلی و تولید فرزندان
        # معکوس می‌کنیم تا ترتیب بهتری داشته باشیم
        successors = get_successors(current_state)
        for successor in reversed(successors):
            if successor not in visited:
                stack.append(successor)
    
    # اگر پشته خالی شد و راه‌حلی پیدا نشد
    return None, nodes_expanded


if __name__ == "__main__":
    # تست الگوریتم DFS
    print("Testing DFS Algorithm...")
    initial = State(0, 0)
    path, nodes_expanded = dfs(initial)
    print_solution(path, nodes_expanded, "Depth-First Search (DFS)")