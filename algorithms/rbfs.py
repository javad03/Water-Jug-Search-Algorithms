"""
Recursive Best-First Search (RBFS) Algorithm
جستجوی بازگشتی اول بهترین
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from state import State, get_successors, reconstruct_path, print_solution, heuristic


class RBFSResult:
    """کلاس کمکی برای نگهداری نتیجه RBFS"""
    def __init__(self, solution=None, f_value=float('inf')):
        self.solution = solution  # راه‌حل پیدا شده (یا None)
        self.f_value = f_value    # بهترین مقدار f که دیده شده


def rbfs_recursive(state, goal_jug4, goal_jug3, f_limit, nodes_expanded):
    """
    تابع بازگشتی اصلی RBFS
    
    Args:
        state: حالت فعلی
        goal_jug4, goal_jug3: حالت هدف
        f_limit: محدودیت f که نباید از آن تجاوز کنیم
        nodes_expanded: لیست برای شمارش گره‌های بسط شده (pass by reference)
    
    Returns:
        RBFSResult شامل راه‌حل (یا None) و بهترین f-value
    """
    
    nodes_expanded[0] += 1
    
    # محاسبه f برای گره فعلی
    h = heuristic(state, goal_jug4, goal_jug3)
    f = max(state.cost + h, state.cost)  # f = max(g+h, parent's f)
    
    # اگر f از محدودیت بیشتر شد، برگرد
    if f > f_limit:
        return RBFSResult(None, f)
    
    # بررسی هدف
    if state.is_goal(goal_jug4, goal_jug3):
        return RBFSResult(reconstruct_path(state), f)
    
    # تولید فرزندان و محاسبه f برای هر کدام
    successors = get_successors(state)
    
    if not successors:
        return RBFSResult(None, float('inf'))
    
    # محاسبه f برای تمام فرزندان
    successor_f_values = []
    for successor in successors:
        h = heuristic(successor, goal_jug4, goal_jug3)
        successor_f = max(successor.cost + h, f)
        successor_f_values.append((successor_f, successor))
    
    # حلقه اصلی RBFS
    while True:
        # مرتب‌سازی براساس f-value (پیدا کردن بهترین و دومین بهترین)
        successor_f_values.sort(key=lambda x: x[0])
        
        best_f, best = successor_f_values[0]
        
        # اگر بهترین f بیشتر از محدودیت است، برگرد
        if best_f > f_limit:
            return RBFSResult(None, best_f)
        
        # پیدا کردن دومین بهترین f برای تعیین محدودیت جدید
        if len(successor_f_values) > 1:
            alternative_f = successor_f_values[1][0]
        else:
            alternative_f = float('inf')
        
        # جستجوی بازگشتی روی بهترین فرزند
        # محدودیت: کمترین مقدار بین f_limit و دومین بهترین
        result = rbfs_recursive(
            best,
            goal_jug4,
            goal_jug3,
            min(f_limit, alternative_f),
            nodes_expanded
        )
        
        # به‌روزرسانی f-value این فرزند
        successor_f_values[0] = (result.f_value, best)
        
        # اگر راه‌حل پیدا شد، برگردان
        if result.solution is not None:
            return result


def rbfs(initial_state, goal_jug4=2, goal_jug3=0):
    """
    الگوریتم جستجوی بازگشتی اول بهترین (RBFS)
    
    ویژگی‌ها:
    - کامل (Complete): راه‌حل را پیدا می‌کند اگر وجود داشته باشد
    - بهینه (Optimal): با heuristic admissible، بهینه است
    - پیچیدگی مکانی: O(bd) - خیلی کمتر از A*
    - پیچیدگی زمانی: ممکن است بیشتر از A* باشد (به دلیل regeneration)
    
    نحوه کار:
    1. شبیه A* است اما فضای حافظه خطی دارد
    2. به جای نگهداری تمام گره‌ها، فقط مسیر فعلی را نگه می‌دارد
    3. وقتی یک مسیر بهتر پیدا می‌شود، مسیر قبلی را رها می‌کند
    4. f-value را برای backtracking نگه می‌دارد
    
    تفاوت با A*:
    - RBFS: حافظه کم، ممکن است گره‌ها را مجدداً تولید کند
    - A*: حافظه زیاد، گره‌ها را فقط یکبار بسط می‌دهد
    """
    
    # شمارنده تعداد گره‌های بسط داده شده (به صورت list برای pass by reference)
    nodes_expanded = [0]
    
    # فراخوانی تابع بازگشتی با محدودیت بی‌نهایت
    result = rbfs_recursive(
        initial_state,
        goal_jug4,
        goal_jug3,
        float('inf'),
        nodes_expanded
    )
    
    return result.solution, nodes_expanded[0]


if __name__ == "__main__":
    # تست الگوریتم RBFS
    print("Testing RBFS Algorithm...")
    initial = State(0, 0)
    path, nodes_expanded = rbfs(initial)
    print_solution(path, nodes_expanded, "Recursive Best-First Search (RBFS)")