"""
Water Jug Problem Solver
حل مسئله پارچ‌های آب با الگوریتم‌های مختلف جستجو

مسئله: 
دو پارچ آب داریم، یکی 4 لیتری و دیگری 3 لیتری
هدف: رساندن دقیقاً 2 لیتر آب به پارچ 4 لیتری

الگوریتم‌های پیاده‌سازی شده:
1. Breadth-First Search (BFS)
2. Depth-First Search (DFS)
3. Iterative Deepening Search (IDS)
4. A* Search
5. Recursive Best-First Search (RBFS)
"""

import time
from state import State, print_solution
from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.ids import ids
from algorithms.astar import astar
from algorithms.rbfs import rbfs


def run_algorithm(algorithm_name, algorithm_func, initial_state):
    """
    اجرای یک الگوریتم و اندازه‌گیری زمان اجرا
    
    Args:
        algorithm_name: نام الگوریتم
        algorithm_func: تابع الگوریتم
        initial_state: حالت اولیه
    """
    print(f"\n{'#'*70}")
    print(f"Running: {algorithm_name}")
    print(f"{'#'*70}")
    
    # اندازه‌گیری زمان شروع
    start_time = time.time()
    
    # اجرای الگوریتم
    path, nodes_expanded = algorithm_func(initial_state)
    
    # اندازه‌گیری زمان پایان
    end_time = time.time()
    execution_time = end_time - start_time
    
    # چاپ نتایج
    print_solution(path, nodes_expanded, algorithm_name)
    print(f"Execution Time: {execution_time:.6f} seconds")
    print(f"{'='*70}\n")
    
    return {
        'algorithm': algorithm_name,
        'path_length': len(path) - 1 if path else None,
        'nodes_expanded': nodes_expanded,
        'execution_time': execution_time,
        'solution_found': path is not None
    }


def print_comparison_table(results):
    """
    چاپ جدول مقایسه‌ای نتایج الگوریتم‌ها
    """
    print("\n" + "="*90)
    print("COMPARISON TABLE - ALGORITHM PERFORMANCE")
    print("="*90)
    print(f"{'Algorithm':<30} {'Path Length':<15} {'Nodes Expanded':<20} {'Time (s)':<15}")
    print("-"*90)
    
    for result in results:
        algo = result['algorithm']
        path_len = result['path_length'] if result['path_length'] is not None else 'N/A'
        nodes = result['nodes_expanded']
        exec_time = f"{result['execution_time']:.6f}"
        
        print(f"{algo:<30} {str(path_len):<15} {nodes:<20} {exec_time:<15}")
    
    print("="*90)
    
    # تحلیل نتایج
    print("\nANALYSIS:")
    print("-" * 90)
    
    # الگوریتم با کمترین گره بسط داده شده
    min_nodes = min(results, key=lambda x: x['nodes_expanded'])
    print(f"✓ Most Efficient (Fewest Nodes): {min_nodes['algorithm']} ({min_nodes['nodes_expanded']} nodes)")
    
    # الگوریتم با کمترین زمان اجرا
    min_time = min(results, key=lambda x: x['execution_time'])
    print(f"✓ Fastest Execution: {min_time['algorithm']} ({min_time['execution_time']:.6f} seconds)")
    
    # الگوریتم‌های بهینه (کوتاه‌ترین مسیر)
    optimal_length = min(r['path_length'] for r in results if r['path_length'] is not None)
    optimal_algorithms = [r['algorithm'] for r in results if r['path_length'] == optimal_length]
    print(f"✓ Optimal Solution Length: {optimal_length} steps")
    print(f"✓ Algorithms Finding Optimal Solution: {', '.join(optimal_algorithms)}")
    
    print("="*90 + "\n")


def main():
    """
    تابع اصلی برنامه
    """
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                    WATER JUG PROBLEM SOLVER                          ║
║                                                                      ║
║  Problem: Given two jugs (4L and 3L) with no markings,               ║
║           fill exactly 2 liters in the 4L jug.                       ║
║                                                                      ║
║  Algorithms: BFS, DFS, IDS, A*, RBFS                                 ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    # تعریف حالت اولیه (هر دو پارچ خالی)
    initial_state = State(0, 0)
    
    # لیست الگوریتم‌ها برای اجرا
    algorithms = [
        ("Breadth-First Search (BFS)", bfs),
        ("Depth-First Search (DFS)", dfs),
        ("Iterative Deepening Search (IDS)", ids),
        ("A* Search", astar),
        ("Recursive Best-First Search (RBFS)", rbfs)
    ]
    
    # اجرای تمام الگوریتم‌ها و جمع‌آوری نتایج
    results = []
    for name, func in algorithms:
        result = run_algorithm(name, func, initial_state)
        results.append(result)
    
    # نمایش جدول مقایسه
    print_comparison_table(results)
    
    # توضیحات اضافی
    print("\nKEY CONCEPTS:")
    print("-" * 90)
    print("• Uninformed Search (BFS, DFS, IDS): No domain knowledge, explore blindly")
    print("• Informed Search (A*, RBFS): Use heuristics to guide search")
    print("• Complete: Algorithm always finds solution if one exists")
    print("• Optimal: Algorithm finds the shortest path")
    print("• Space Complexity: Memory required during search")
    print("  - BFS: O(b^d) - High memory")
    print("  - DFS: O(bd) - Low memory")
    print("  - IDS: O(bd) - Low memory, complete & optimal")
    print("  - A*: O(b^d) - High memory, optimal with admissible heuristic")
    print("  - RBFS: O(bd) - Low memory, optimal with admissible heuristic")
    print("="*90)


if __name__ == "__main__":
    main()