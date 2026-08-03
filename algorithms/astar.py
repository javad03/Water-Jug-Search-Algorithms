"""
A* Search Algorithm
الگوریتم جستجوی A ستاره
"""

import heapq
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from state import State, get_successors, reconstruct_path, print_solution, heuristic


class PriorityQueue:
    """
    صف اولویت‌دار برای الگوریتم A*
    از heap برای مدیریت اولویت‌ها استفاده می‌کند
    """
    def __init__(self):
        self.heap = []
        self.counter = 0  # برای حفظ ترتیب درج در صورت برابری f
    
    def push(self, priority, item):
        """اضافه کردن یک آیتم با اولویت مشخص"""
        # (اولویت, شمارنده, آیتم) - شمارنده برای FIFO در صورت برابری
        heapq.heappush(self.heap, (priority, self.counter, item))
        self.counter += 1
    
    def pop(self):
        """برداشتن آیتم با کمترین اولویت"""
        if self.heap:
            return heapq.heappop(self.heap)[2]  # برگرداندن فقط آیتم
        return None
    
    def is_empty(self):
        """بررسی خالی بودن صف"""
        return len(self.heap) == 0


def astar(initial_state, goal_jug4=2, goal_jug3=0):
    """
    الگوریتم جستجوی A* (A-Star)
    
    ویژگی‌ها:
    - کامل (Complete): راه‌حل را پیدا می‌کند اگر وجود داشته باشد
    - بهینه (Optimal): بهترین راه‌حل را پیدا می‌کند (با heuristic admissible)
    - پیچیدگی: بستگی به کیفیت heuristic دارد
    
    فرمول: f(n) = g(n) + h(n)
    - g(n): هزینه واقعی از شروع تا n
    - h(n): تخمین هزینه از n تا هدف (heuristic)
    - f(n): تخمین کل هزینه مسیر از شروع تا هدف عبور از n
    
    نحوه کار:
    1. از صف اولویت‌دار استفاده می‌کند
    2. همیشه گره با کمترین f(n) را بسط می‌دهد
    3. با heuristic admissible، تضمین می‌کند که بهینه‌ترین راه را پیدا کند
    """
    
    # صف اولویت‌دار برای نگهداری گره‌ها براساس f(n)
    frontier = PriorityQueue()
    
    # محاسبه f برای گره اولیه
    h = heuristic(initial_state, goal_jug4, goal_jug3)
    f = initial_state.cost + h  # f = g + h
    frontier.push(f, initial_state)
    
    # دیکشنری برای نگهداری بهترین هزینه تا هر حالت
    # اگر مسیر بهتری به یک حالت پیدا کنیم، آن را به‌روز می‌کنیم
    best_cost = {initial_state: initial_state.cost}
    
    # شمارنده تعداد گره‌های بسط داده شده
    nodes_expanded = 0
    
    # حلقه اصلی جستجو
    while not frontier.is_empty():
        # برداشتن گره با کمترین f(n)
        current_state = frontier.pop()
        nodes_expanded += 1
        
        # بررسی اینکه آیا به هدف رسیدیم
        if current_state.is_goal(goal_jug4, goal_jug3):
            path = reconstruct_path(current_state)
            return path, nodes_expanded
        
        # بسط گره فعلی و تولید فرزندان
        for successor in get_successors(current_state):
            # هزینه رسیدن به successor از طریق current
            new_cost = successor.cost
            
            # اگر این مسیر بهتر از مسیرهای قبلی است یا اولین باری است که می‌بینیمش
            if successor not in best_cost or new_cost < best_cost[successor]:
                best_cost[successor] = new_cost
                
                # محاسبه f(n) = g(n) + h(n)
                h = heuristic(successor, goal_jug4, goal_jug3)
                f = new_cost + h
                
                # اضافه کردن به صف اولویت‌دار
                frontier.push(f, successor)
    
    # اگر صف خالی شد و راه‌حلی پیدا نشد
    return None, nodes_expanded


if __name__ == "__main__":
    # تست الگوریتم A*
    print("Testing A* Algorithm...")
    initial = State(0, 0)
    path, nodes_expanded = astar(initial)
    print_solution(path, nodes_expanded, "A* Search")
    
    # نمایش مقادیر heuristic برای چند حالت
    print("\nSample Heuristic Values:")
    print("-" * 40)
    test_states = [
        State(0, 0),
        State(4, 0),
        State(4, 3),
        State(1, 3),
        State(2, 0),
    ]
    for s in test_states:
        h = heuristic(s)
        print(f"State(4L={s.jug4}, 3L={s.jug3}) -> h={h}")