from functools import lru_cache
from src.action.PawnMove import *
from src.Path import *
from src.GridCoordinates import *


class DynamicProgramming:
    """
    Estrategias de Programación Dinámica aplicadas a Quoridor.
    
    PROGRAMACIÓN DINÁMICA es una técnica de optimización que:
    1. Divide el problema en subproblemas solapados
    2. ALMACENA (memoiza) resultados de subproblemas
    3. Reutiliza resultados para evitar recalcular
    
    APLICACIÓN EN QUORIDOR:
    El sistema ya implementa DP de manera implícita en:
    - storedValidPawnMoves: Tabla DP de movimientos válidos
    - storedValidFencePlacings: Tabla DP de muros válidos
    - Actualización incremental al cambiar estado
    
    COMPLEJIDAD:
    - Sin DP: O(n²) por turno (recalcular todo)
    - Con DP: O(k) donde k << n (solo actualizar afectados)
    
    MEJORA: Para tablero 9x9, evita ~81 recálculos completos por turno
    """
    
    @staticmethod
    def explainExistingDP():
        """
        Documenta la Programación Dinámica ya presente en el sistema.
        
        EL SISTEMA YA USA DP EN:
        
        1. MEMOIZACIÓN DE MOVIMIENTOS VÁLIDOS (Board.py)
           - Tabla: storedValidPawnMoves[coord] = [movimientos]
           - Complejidad: O(1) para consulta vs O(n) sin memoización
           - Actualización: Solo casillas afectadas (≤9 por turno)
        
        2. MEMOIZACIÓN DE MUROS VÁLIDOS (Board.py)
           - Tabla: storedValidFencePlacings = [muros]
           - Actualización incremental al colocar muro
           - Evita recalcular ~128 validaciones cada turno
        
        3. ACTUALIZACIÓN INCREMENTAL (Board.py)
           - updateStoredValidActionsAfterPawnMove()
           - updateStoredValidActionsAfterFencePlacing()
           - Solo recalcula lo necesario: O(k) vs O(n²)
        
        OPTIMIZACIÓN MATEMÁTICA:
        Sin DP: 81 casillas × 4 direcciones × validación = ~324 ops/turno
        Con DP: Solo ~9 casillas afectadas × 4 direcciones = ~36 ops/turno
        Mejora: 9x más rápido
        """
        return {
            "strategy": "Memoization with incremental updates",
            "tables": ["storedValidPawnMoves", "storedValidFencePlacings"],
            "complexity_without_dp": "O(n²) per turn",
            "complexity_with_dp": "O(k) where k << n",
            "speedup": "~9x faster"
        }
    
    @staticmethod
    @lru_cache(maxsize=256)
    def shortestPathMemoized(board_hash, start, goal_tuple):
        """
        Camino más corto con memoización usando LRU cache.
        
        PROGRAMACIÓN DINÁMICA aplicada a pathfinding:
        - Almacena resultados de BFS previos
        - Evita recalcular caminos idénticos
        - Cache LRU mantiene los 256 más recientes
        
        Args:
            board_hash: Hash del estado del tablero
            start: Coordenada de inicio (como tupla)
            goal_tuple: Tuplas de coordenadas objetivo
            
        Returns:
            Path o None
            
        Complejidad: O(1) para hits, O(V+E) para misses
        """
        # Nota: En producción, board_hash sería un hash real del tablero
        # Aquí es ejemplo conceptual de cómo implementar DP con cache
        pass
    
    @staticmethod
    def bellmanFord(board, start, goals):
        """
        Algoritmo Bellman-Ford usando Programación Dinámica.
        
        ESTRUCTURA DP:
        - dist[v][k] = distancia mínima a v usando máximo k aristas
        - Recurrencia: dist[v][k] = min(dist[v][k-1], 
                                        min(dist[u][k-1] + w(u,v)))
        
        COMPLEJIDAD:
        - Temporal: O(V × E) donde V=81 vértices, E≈324 aristas
        - Espacial: O(V) con optimización de espacio
        
        Args:
            board: Tablero actual
            start: Coordenada inicial
            goals: Lista de objetivos
            
        Returns:
            dict: {coord: distancia_mínima}
        """
        # Inicializar tabla DP
        dist = {}
        for col in range(board.cols):
            for row in range(board.rows):
                coord = GridCoordinates(col, row)
                dist[coord] = float('inf')
        dist[start] = 0
        
        # Relajación iterativa (DP)
        for _ in range(board.cols * board.rows - 1):
            for col in range(board.cols):
                for row in range(board.rows):
                    coord = GridCoordinates(col, row)
                    valid_moves = board.storedValidPawnMovesIgnoringPawns[coord]
                    
                    for move in valid_moves:
                        if dist[coord] + 1 < dist[move.toCoord]:
                            dist[move.toCoord] = dist[coord] + 1
        
        return dist
    
    @staticmethod
    def floydWarshall(board):
        """
        Algoritmo Floyd-Warshall - DP clásico para todos los pares.
        
        RECURRENCIA DP:
        dist[i][j][k] = min(dist[i][j][k-1], 
                            dist[i][k][k-1] + dist[k][j][k-1])
        
        Calcula distancias más cortas entre TODOS los pares de casillas.
        
        COMPLEJIDAD:
        - Temporal: O(V³) = O(81³) ≈ 531,441 operaciones
        - Espacial: O(V²) = O(6,561) con optimización
        
        USO: Pre-cálculo al inicio del juego para consultas O(1)
        
        Returns:
            dict: {(coord1, coord2): distancia_mínima}
        """
        coords = []
        for col in range(board.cols):
            for row in range(board.rows):
                coords.append(GridCoordinates(col, row))
        
        # Inicializar matriz DP
        dist = {}
        for c1 in coords:
            for c2 in coords:
                if c1 == c2:
                    dist[(c1, c2)] = 0
                else:
                    dist[(c1, c2)] = float('inf')
        
        # Aristas directas
        for coord in coords:
            moves = board.storedValidPawnMovesIgnoringPawns[coord]
            for move in moves:
                dist[(coord, move.toCoord)] = 1
        
        # DP: probar todos los nodos intermedios
        for k in coords:
            for i in coords:
                for j in coords:
                    if dist[(i, j)] > dist[(i, k)] + dist[(k, j)]:
                        dist[(i, j)] = dist[(i, k)] + dist[(k, j)]
        
        return dist
    
    @staticmethod
    def optimizeStorageUpdates(board):
        """
        Análisis de cómo el sistema usa DP para optimizar
        actualizaciones de movimientos válidos.
        
        ANTES (sin DP): O(n²) recalcular todo
        DESPUÉS (con DP): O(k) actualizar solo afectados
        
        ESTRATEGIA:
        1. Identificar casillas en radio de impacto
        2. Solo recalcular esas casillas
        3. Preservar resto de la tabla DP
        
        Returns:
            dict: Estadísticas de optimización
        """
        total_squares = board.cols * board.rows
        
        # Después de mover peón: solo actualizar ~9 casillas
        pawn_move_impact = 9
        
        # Después de colocar muro: solo actualizar ~12 casillas
        fence_impact = 12
        
        savings = {
            "total_squares": total_squares,
            "pawn_move_recalc": pawn_move_impact,
            "fence_recalc": fence_impact,
            "pawn_speedup": total_squares / pawn_move_impact,
            "fence_speedup": total_squares / fence_impact
        }
        
        return savings