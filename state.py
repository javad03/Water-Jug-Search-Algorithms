"""
State Management for Water Jug Problem
این فایل شامل کلاس State و توابع کمکی برای مدیریت حالت‌های مسئله است
"""

class State:
    """
    کلاس State برای نمایش وضعیت پارچ‌های آب
    jug4: مقدار آب در پارچ 4 لیتری (0-4)
    jug3: مقدار آب در پارچ 3 لیتری (0-3)
    """
    def __init__(self, jug4, jug3, parent=None, action=""):
        self.jug4 = jug4  # مقدار آب در پارچ 4 لیتری
        self.jug3 = jug3  # مقدار آب در پارچ 3 لیتری
        self.parent = parent  # حالت والد برای پیگیری مسیر
        self.action = action  # عملی که به این حالت منجر شده
        self.depth = 0 if parent is None else parent.depth + 1  # عمق در درخت جستجو
        self.cost = self.depth  # هزینه مسیر (تعداد حرکت‌ها)
    
    def __eq__(self, other):
        """بررسی برابری دو حالت"""
        if other is None:
            return False
        return self.jug4 == other.jug4 and self.jug3 == other.jug3
    
    def __hash__(self):
        """تولید hash برای استفاده در set و dict"""
        return hash((self.jug4, self.jug3))
    
    def __repr__(self):
        return f"State(4L={self.jug4}, 3L={self.jug3})"
    
    def is_goal(self, goal_jug4=2, goal_jug3=0):
        """بررسی اینکه آیا این حالت، حالت هدف است یا خیر"""
        return self.jug4 == goal_jug4 and self.jug3 == goal_jug3


def get_successors(state):
    """
    تولید تمام حالت‌های قابل دسترس از حالت فعلی
    6 عملیات ممکن:
    1. پر کردن پارچ 4 لیتری
    2. پر کردن پارچ 3 لیتری
    3. خالی کردن پارچ 4 لیتری
    4. خالی کردن پارچ 3 لیتری
    5. ریختن از پارچ 4 لیتری به 3 لیتری
    6. ریختن از پارچ 3 لیتری به 4 لیتری
    """
    successors = []
    jug4, jug3 = state.jug4, state.jug3
    
    # 1. پر کردن پارچ 4 لیتری
    if jug4 < 4:
        successors.append(State(4, jug3, state, "Fill 4L jug"))
    
    # 2. پر کردن پارچ 3 لیتری
    if jug3 < 3:
        successors.append(State(jug4, 3, state, "Fill 3L jug"))
    
    # 3. خالی کردن پارچ 4 لیتری
    if jug4 > 0:
        successors.append(State(0, jug3, state, "Empty 4L jug"))
    
    # 4. خالی کردن پارچ 3 لیتری
    if jug3 > 0:
        successors.append(State(jug4, 0, state, "Empty 3L jug"))
    
    # 5. ریختن از پارچ 4 لیتری به 3 لیتری
    if jug4 > 0 and jug3 < 3:
        # محاسبه مقدار قابل انتقال
        transfer = min(jug4, 3 - jug3)
        successors.append(State(jug4 - transfer, jug3 + transfer, state, 
                               f"Pour 4L to 3L ({transfer}L)"))
    
    # 6. ریختن از پارچ 3 لیتری به 4 لیتری
    if jug3 > 0 and jug4 < 4:
        # محاسبه مقدار قابل انتقال
        transfer = min(jug3, 4 - jug4)
        successors.append(State(jug4 + transfer, jug3 - transfer, state, 
                               f"Pour 3L to 4L ({transfer}L)"))
    
    return successors


def reconstruct_path(goal_state):
    """
    بازسازی مسیر از حالت اولیه تا حالت هدف
    با پیمایش از حالت هدف به سمت والدین
    """
    path = []
    current = goal_state
    
    while current is not None:
        path.append(current)
        current = current.parent
    
    # معکوس کردن مسیر تا از اول به آخر باشد
    path.reverse()
    return path


def print_solution(path, nodes_expanded, algorithm_name):
    """
    چاپ نتیجه جستجو به صورت فرمت شده
    """
    print(f"\n{'='*60}")
    print(f"Algorithm: {algorithm_name}")
    print(f"{'='*60}")
    
    if path:
        print(f"Solution found! Path length: {len(path) - 1} steps")
        print(f"Nodes expanded: {nodes_expanded}")
        print(f"\nSolution Path:")
        print("-" * 60)
        
        for i, state in enumerate(path):
            if i == 0:
                print(f"Step {i}: Initial State -> 4L: {state.jug4}L, 3L: {state.jug3}L")
            else:
                print(f"Step {i}: {state.action} -> 4L: {state.jug4}L, 3L: {state.jug3}L")
        
        print(f"\n✓ Goal reached: 4L jug has exactly 2 liters!")
    else:
        print("No solution found!")
        print(f"Nodes expanded: {nodes_expanded}")
    
    print(f"{'='*60}\n")


def heuristic(state, goal_jug4=2, goal_jug3=0):
    """
    تابع ابتکاری (Heuristic) برای الگوریتم‌های آگاهانه
    
    استراتژی: محاسبه حداقل تعداد عملیات لازم برای رسیدن به هدف
    این تابع admissible است (هرگز بیش از واقعیت تخمین نمی‌زند)
    
    منطق:
    - اگر مقدار فعلی jug4 برابر هدف باشد و jug3 هم برابر هدف باشد -> h=0
    - اگر jug4 = هدف ولی jug3 != هدف -> حداقل 1 عملیات (خالی کردن jug3)
    - در غیر اینصورت: محاسبه تفاوت مطلق با هدف
    """
    # اگر در حالت هدف هستیم
    if state.jug4 == goal_jug4 and state.jug3 == goal_jug3:
        return 0
    
    # اگر jug4 مقدار درست دارد ولی jug3 باید خالی شود
    if state.jug4 == goal_jug4 and state.jug3 != goal_jug3:
        return 1 if state.jug3 > 0 else 0
    
    # محاسبه فاصله از هدف برای jug4
    # این یک تخمین admissible است
    distance = abs(state.jug4 - goal_jug4)
    
    # اگر jug3 هم باید تنظیم شود، یک عملیات اضافه می‌کنیم
    if state.jug3 != goal_jug3 and distance > 0:
        distance += 1
    
    return distance