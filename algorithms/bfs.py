"""
Breadth-First Search (BFS) Algorithm
جستجوی اول سطح (پهنا)
"""

from collections import deque
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from state import State, get_successors, reconstruct_path, print_solution


def bfs(initial_state, goal_jug4=2, goal_jug3=0):
    """
    الگوریتم جستجوی اول سطح (BFS)
    
    ویژگی‌ها:
    - کامل (Complete): همیشه راه‌حل را پیدا می‌کند اگر وجود داشته باشد
    - بهینه (Optimal): کوتاه‌ترین مسیر را پیدا می‌کند (در صورت یکسان بودن هزینه اضلاع)
    - پیچیدگی زمانی: O(b^d) که b = branching factor و d = عمق راه‌حل
    - پیچیدگی مکانی: O(b^d)
    
    نحوه کار:
    1. از صف (Queue) برای ذخیره گره‌ها استفاده می‌کند (FIFO)
    2. ابتدا گره‌های سطح اول، سپس سطح دوم و ... را بررسی می‌کند
    3. از visited set برای جلوگیری از بررسی مجدد حالت‌ها استفاده می‌کند
    """
    
    # صف برای نگهداری گره‌های در انتظار بررسی (FIFO)
    frontier = deque([initial_state])
    
    # مجموعه حالت‌های بازدید شده برای جلوگیری از چرخه
    visited = set()
    visited.add(initial_state)
    
    # شمارنده تعداد گره‌های بسط داده شده
    nodes_expanded = 0
    
    # حلقه اصلی جستجو
    while frontier:
        # برداشتن اولین گره از صف (FIFO)
        current_state = frontier.popleft()
        nodes_expanded += 1
        
        # بررسی اینکه آیا به هدف رسیدیم
        if current_state.is_goal(goal_jug4, goal_jug3):
            path = reconstruct_path(current_state)
            return path, nodes_expanded
        
        # بسط گره فعلی و تولید فرزندان
        for successor in get_successors(current_state):
            # اگر این حالت قبلاً بازدید نشده، آن را اضافه کن
            if successor not in visited:
                visited.add(successor)
                frontier.append(successor)
    
    # اگر صف خالی شد و راه‌حلی پیدا نشد
    return None, nodes_expanded


if __name__ == "__main__":
    # تست الگوریتم BFS
    print("Testing BFS Algorithm...")
    initial = State(0, 0)
    path, nodes_expanded = bfs(initial)
    print_solution(path, nodes_expanded, "Breadth-First Search (BFS)")