import heapq
import copy
import pygame

# Cấu hình trò chơi
WIDTH, HEIGHT = 600, 400
BACKGROUND_COLOR = (240, 240, 240)
PEG_COLOR = (150, 150, 150)
RING_COLORS = {"red": (255, 0, 0), "blue": (0, 0, 255), "green": (0, 255, 0), "yellow": (255, 255, 0), "purple": (160, 32, 240), "brown": (139, 69, 19)}
PEG_POSITIONS = [(100, 300), (200, 300), (300, 300), (400, 300), (500, 300), (600, 300)]

# Khởi tạo Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sorting Rings Game")

# Kiểm tra trạng thái đích
def is_goal(state):
    return all(len(set(stack)) <= 1 for stack in state if stack)

# Lấy danh sách các bước di chuyển hợp lệ
def get_valid_moves(state):
    moves = []
    for i in range(len(state)):
        if state[i]:
            for j in range(len(state)):
                if i != j and (not state[j] or state[j][-1] == state[i][-1]):
                    moves.append((i, j))
    return moves

# Áp dụng nước đi
def apply_move(state, move):
    new_state = copy.deepcopy(state)
    from_col, to_col = move
    color = new_state[from_col][-1]
    while new_state[from_col] and new_state[from_col][-1] == color:
        new_state[to_col].append(new_state[from_col].pop())
    return new_state

# Heuristic đánh giá trạng thái
def heuristic(state):
    misplaced = 0
    for stack in state:
        if stack:
            color = stack[0]
            misplaced += sum(1 for ring in stack if ring != color)
    return misplaced

# Thuật toán A*
def a_star(start_state):
    priority_queue = []
    heapq.heappush(priority_queue, (0, start_state, []))
    visited = set()
    while priority_queue:
        cost, current_state, path = heapq.heappop(priority_queue)
        state_tuple = tuple(tuple(stack) for stack in current_state)
        if state_tuple in visited:
            continue
        visited.add(state_tuple)
        if is_goal(current_state):
            return path
        for move in get_valid_moves(current_state):
            new_state = apply_move(current_state, move)
            new_path = path + [move]
            new_cost = len(new_path) + heuristic(new_state)
            heapq.heappush(priority_queue, (new_cost, new_state, new_path))
    return None

# Hiển thị trạng thái trò chơi
def draw_state(state):
    screen.fill(BACKGROUND_COLOR)
    for i, peg in enumerate(PEG_POSITIONS):
        pygame.draw.rect(screen, PEG_COLOR, (peg[0] - 10, peg[1] - 100, 20, 100))
        stack = state[i]
        for j, ring in enumerate(stack):
            color = RING_COLORS.get(ring, (0, 0, 0))
            pygame.draw.circle(screen, color, (peg[0], peg[1] - (j * 20)), 15)
    pygame.display.flip()

# Nhận lệnh từ người chơi
def get_user_move():
    try:
        from_col = int(input("Nhập cột nguồn (0-5): "))
        to_col = int(input("Nhập cột đích (0-5): "))
        return from_col, to_col
    except ValueError:
        return None

# Trạng thái ban đầu
initial_state = [
    ["red", "blue", "green", "yellow"],   # Cột 1: chứa 4 màu khác nhau
    ["yellow", "green", "blue", "red"],   # Cột 2: chứa 4 màu khác nhau
    ["blue", "yellow", "red", "green"],   # Cột 3: chứa 4 màu khác nhau
    ["green", "red", "yellow", "blue"],   # Cột 4: chứa 4 màu khác nhau
    [],  # Cột 5 (trống)
    []   # Cột 6 (trống)
]


solution = a_star(initial_state)
if solution:
    print("Các bước di chuyển:")
    for step in solution:
        print(f"Di chuyển từ cột {step[0]} sang cột {step[1]}")
else:
    print("Không tìm thấy giải pháp.")

# Vòng lặp game
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    draw_state(initial_state)
    
    move = get_user_move()
    if move in get_valid_moves(initial_state):
        initial_state = apply_move(initial_state, move)
    else:
        print("Nước đi không hợp lệ, vui lòng thử lại!")

pygame.quit()




