import time
import functools
from collections import defaultdict
from typing import Callable, Any, Dict
from src.Path import *
import json


class Profiler:
    """
    Sistema de profiling para medir rendimiento de algoritmos.
    
    USO:
        @Profiler.profile
        def my_function():
            # código
    
    Genera reportes de:
    - Número de llamadas
    - Tiempo total
    - Tiempo promedio
    - Tiempo min/max
    """
    
    stats = defaultdict(lambda: {
        "calls": 0,
        "total_time": 0.0,
        "min_time": float('inf'),
        "max_time": 0.0,
        "avg_time": 0.0
    })
    
    call_stack = []  # Para detectar recursión
    enabled = True
    
    @staticmethod
    def profile(func: Callable) -> Callable:
        """
        Decorador para medir rendimiento de funciones.
        
        Ejemplo:
            @Profiler.profile
            def buscar_camino(board, start, end):
                return Path.BreadthFirstSearch(...)
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not Profiler.enabled:
                return func(*args, **kwargs)
            
            name = f"{func.__module__}.{func.__name__}"
            
            # Detectar recursión
            depth = Profiler.call_stack.count(name)
            Profiler.call_stack.append(name)
            
            start_time = time.perf_counter()
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                elapsed = time.perf_counter() - start_time
                
                # Actualizar estadísticas
                s = Profiler.stats[name]
                s["calls"] += 1
                s["total_time"] += elapsed
                s["min_time"] = min(s["min_time"], elapsed)
                s["max_time"] = max(s["max_time"], elapsed)
                s["avg_time"] = s["total_time"] / s["calls"]
                s["recursion_depth"] = max(s.get("recursion_depth", 0), depth)
                
                Profiler.call_stack.pop()
        
        return wrapper
    
    @staticmethod
    def report(sort_by='total_time', top_n=20):
        """
        Genera reporte de rendimiento.
        
        Args:
            sort_by: 'total_time', 'calls', 'avg_time', 'max_time'
            top_n: Número de funciones a mostrar
        """
        print("\n" + "="*100)
        print("PROFILER REPORT - ANÁLISIS DE RENDIMIENTO")
        print("="*100)
        
        # Ordenar por criterio
        sorted_stats = sorted(
            Profiler.stats.items(),
            key=lambda x: x[1][sort_by],
            reverse=True
        )
        
        # Header
        print(f"{'Function':<50} | {'Calls':>8} | {'Total(s)':>10} | "
              f"{'Avg(ms)':>10} | {'Min(ms)':>10} | {'Max(ms)':>10}")
        print("-" * 100)
        
        # Datos
        for func_name, data in sorted_stats[:top_n]:
            print(f"{func_name:<50} | {data['calls']:>8} | "
                  f"{data['total_time']:>10.4f} | "
                  f"{data['avg_time']*1000:>10.4f} | "
                  f"{data['min_time']*1000:>10.4f} | "
                  f"{data['max_time']*1000:>10.4f}")
        
        print("="*100)
        
        # Resumen
        total_time = sum(s["total_time"] for s in Profiler.stats.values())
        total_calls = sum(s["calls"] for s in Profiler.stats.values())
        print(f"\nTOTAL: {total_calls} llamadas, {total_time:.4f} segundos")
        print(f"Función más costosa (Top): {sorted_stats[0][0]}")
        print(f"Más llamada: {max(Profiler.stats.items(), key=lambda x: x[1]['calls'])[0]}")
    
    @staticmethod
    def export_json(filename='profiler_results.json'):
        """Exporta resultados a JSON para análisis externo."""
        data = {
            "stats": dict(Profiler.stats),
            "summary": {
                "total_calls": sum(s["calls"] for s in Profiler.stats.values()),
                "total_time": sum(s["total_time"] for s in Profiler.stats.values())
            }
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Datos del profiler exportados a {filename}")
    
    @staticmethod
    def reset():
        """Reinicia todas las estadísticas."""
        Profiler.stats.clear()
        Profiler.call_stack.clear()
    
    @staticmethod
    def enable():
        """Habilita profiling."""
        Profiler.enabled = True
    
    @staticmethod
    def disable():
        """Deshabilita profiling (útil en producción)."""
        Profiler.enabled = False


class ComplexityAnalyzer:
    """
    Analiza complejidad empírica de funciones.
    """
    
    @staticmethod
    def measure_complexity(func, input_sizes, *args, **kwargs):
        """
        Mide tiempo de ejecución para diferentes tamaños de entrada.
        
        Args:
            func: Función a analizar
            input_sizes: Lista de tamaños [10, 100, 1000, ...]
            *args, **kwargs: Argumentos adicionales
            
        Returns:
            dict: {size: time}
        """
        results = {}
        
        for size in input_sizes:
            # Generar entrada de tamaño 'size'
            start = time.perf_counter()
            func(size, *args, **kwargs)
            elapsed = time.perf_counter() - start
            
            results[size] = elapsed
        
        return results
    
    @staticmethod
    def estimate_complexity_class(results):
        """
        Estima clase de complejidad basado en tiempos medidos.
        
        Returns:
            str: "O(1)", "O(log n)", "O(n)", "O(n log n)", "O(n²)", etc.
        """
        sizes = sorted(results.keys())
        times = [results[s] for s in sizes]
        
        if len(sizes) < 3:
            return "Insufficient data"
        
        # Calcular ratios
        ratios = []
        for i in range(1, len(sizes)):
            size_ratio = sizes[i] / sizes[i-1]
            time_ratio = times[i] / times[i-1] if times[i-1] > 0 else 0
            ratios.append((size_ratio, time_ratio))
        
        # Analizar ratios
        avg_time_ratio = sum(r[1] for r in ratios) / len(ratios)
        avg_size_ratio = sum(r[0] for r in ratios) / len(ratios)
        
        # Heurísticas de clasificación
        if avg_time_ratio < 1.2:
            return "O(1) - Constant"
        elif avg_time_ratio < avg_size_ratio * 0.5:
            return "O(log n) - Logarithmic"
        elif avg_time_ratio < avg_size_ratio * 1.5:
            return "O(n) - Linear"
        elif avg_time_ratio < avg_size_ratio * 2:
            return "O(n log n) - Linearithmic"
        elif avg_time_ratio < avg_size_ratio ** 2 * 1.5:
            return "O(n²) - Quadratic"
        else:
            return "O(n³) or worse - Cubic+"


class Benchmarker:
    """
    Benchmarks específicos para algoritmos de Quoridor.
    """
    
    @staticmethod
    def benchmark_pathfinding(board, iterations=100):
        """Benchmark de algoritmos de búsqueda de caminos."""
        import random
        from src.GridCoordinates import GridCoordinates
        
        print("\n=== BENCHMARK: BÚSQUEDA DE CAMINOS ===")
        
        results = {
            "BreadthFirstSearch": [],
            "DepthFirstSearch": [],
            "Dijkstra": []
        }
        
        for _ in range(iterations):
            # Generar coordenadas aleatorias
            start = GridCoordinates(
                random.randint(0, board.cols-1),
                random.randint(0, board.rows-1)
            )
            goals = [GridCoordinates(
                random.randint(0, board.cols-1),
                random.randint(0, board.rows-1)
            )]
            
            # BFS
            start_time = time.perf_counter()
            Path.BreadthFirstSearch(board, start, goals)
            results["BreadthFirstSearch"].append(
                time.perf_counter() - start_time
            )
        
        # Reporte
        for algo, times in results.items():
            if times:
                avg = sum(times) / len(times)
                print(f"{algo:25} | Promedio: {avg*1000:8.4f}ms | "
                      f"Mín: {min(times)*1000:8.4f}ms | "
                      f"Máx: {max(times)*1000:8.4f}ms")
    
    @staticmethod
    def benchmark_strategies(game, rounds=10):
        """
        Compara rendimiento de diferentes estrategias de IA.
        
        Mide:
        - Tiempo por turno
        - Número de turnos hasta victoria
        - Tasa de victoria
        """
        print("\n=== BENCHMARK: ESTRATEGIAS ===")
        
        from player.RunnerBotImproved import RunnerBot
        from src.player.BuilderBot import BuilderBot
        from src.player.RandomBot import RandomBot
        
        strategies = {
            "RandomBot": RandomBot,
            "RunnerBot": RunnerBot,
            "BuilderBot": BuilderBot
        }
        
        results = defaultdict(lambda: {
            "wins": 0,
            "total_time": 0,
            "avg_time_per_move": 0,
            "moves_count": 0
        })
        
        # TODO: Implementar torneo completo
        
        print("El benchmark de estrategias requiere una simulación completa del juego")
        print("Ver `Game.py` para la integración")
        
        return results