import pygame as py 

from random import randint  

from time import sleep  

import collections  

 

py.init() 

 

# --- LỚP LIBRABY (GIỮ NGUYÊN) --- 

class LIBRABY: 

    def __init__(self): 

        self.window_coordinates = py.Vector2(py.display.Info().current_w, py.display.Info().current_h) 

        self.scr = py.display.set_mode((self.window_coordinates.x, self.window_coordinates.y), py.FULLSCREEN)  

        self.r = True 

        self.COLOR() 

     

    def MOUSE_COORDINATES(m): 

        m.mouse_coordinates = py.Vector2(py.mouse.get_pos()) 

        m.font = py.font.SysFont(None, 30) 

        m.text = m.font.render(f"Mouse Position: ({m.mouse_coordinates.x},{m.mouse_coordinates.y})", True, (220, 20, 60)) 

         

    def COLOR(c): 

        c.color={ 

            "white":(255,255,255), 

            "black":(0,0,0), 

            "glay" : (200, 200, 200), 

            "red"  : (255, 0, 0), 

            "blue" : (0, 0, 255), 

            "brown": (139, 69, 19) # Màu Nâu mới 

        } 

 

# --- LỚP GRID (GIỮ NGUYÊN) --- 

class GRID(LIBRABY): 

    def __init__(self, square_size_m):  

        super().__init__() 

        self.square_size = square_size_m 

        self.square_coordinates = py.Vector2(int(self.window_coordinates.x) // self.square_size,  

                                             int(self.window_coordinates.y) // self.square_size) 

     

    def DRAW_GRID(d): 

        for d.x in range(0, int(d.window_coordinates.x), d.square_size): 

            py.draw.line(d.scr, d.color["glay"], (d.x, 0), (d.x, d.window_coordinates.y)) 

        for d.y in range(0, int(d.window_coordinates.y), d.square_size): 

            py.draw.line(d.scr, d.color["glay"], (0, d.y), (d.window_coordinates.x, d.y)) 

     

    def DRAW_BORDER(d): 

        for d.x in range(int(d.square_coordinates.x)): 

            for d.y in range(int(d.square_coordinates.y)): 

                d.rect = py.Rect(d.x * d.square_size, d.y * d.square_size, d.square_size, d.square_size) 

                py.draw.rect(d.scr, d.color["black"], d.rect, 1) 

 

# --- LỚP _MAIN_ (LOGIC ĐÃ CHỈNH SỬA) --- 

class _MAIN_(LIBRABY): 

    def __init__(self): 

        super().__init__() 

         

        SQUARE_SIZE_M = 40  

        self.grid = GRID(square_size_m=SQUARE_SIZE_M) 

        self.grid_w = int(self.grid.square_coordinates.x) 

        self.grid_h = int(self.grid.square_coordinates.y) 

        self.sq_size = self.grid.square_size 

        self.radius = self.sq_size // 3  

         

        self.clock = py.time.Clock() 

        self.FPS = 30  

         

        self.obstacles = set()  

        self.path = collections.deque()  

         

        self.red_moving = True 

        self.blue_moving = True 

         

        # --- THAY ĐỔI TỐC ĐỘ --- 

        self.RED_MOVE_RATE = 3  # Đỏ di chuyển mỗi 3 frame 

        self.BLUE_MOVE_RATE = 5 # Xanh di chuyển mỗi 5 frame (Xanh chậm hơn) 

         

        self.red_move_timer = 0 

        self.blue_move_timer = 0 

        # ------------------------ 

         

        # Thêm biến trạng thái và vị trí đích Nâu 

        self.caught = False  

        self.towing = False  

        self.towing_path = collections.deque()  

        self.target_pos = None  

         

        self.setup_circles() 

 

    def get_center_coords(self, grid_x, grid_y): 

        center_x = grid_x * self.sq_size + self.sq_size // 2 

        center_y = grid_y * self.sq_size + self.sq_size // 2 

        return py.Vector2(center_x, center_y) 

 

    def setup_circles(self): 

        """Tạo ngẫu nhiên chướng ngại vật, vị trí hình tròn, và tính toán đường đi.""" 

         

        MAX_TRIES = 100 # Giới hạn số lần thử tạo màn hình không bị kẹt 

 

        for attempt in range(MAX_TRIES): 

            # 1. RESET TRẠNG THÁI VÀ TẠO NGẪU NHIÊN 

            self.obstacles.clear() 

            self.path.clear() 

            self.towing_path.clear() 

            self.caught = False 

            self.towing = False 

            self.red_moving = True 

            self.blue_moving = True  

            self.red_move_timer = 0 

            self.blue_move_timer = 0 

             

            total_cells = self.grid_w * self.grid_h 

            num_obstacles = int(total_cells * 0.20) 

             

            for _ in range(num_obstacles): 

                ox = randint(0, self.grid_w - 1) 

                oy = randint(0, self.grid_h - 1) 

                self.obstacles.add((ox, oy)) 

 

            while True: 

                gx_blue = randint(0, self.grid_w - 1) 

                gy_blue = randint(0, self.grid_h - 1) 

                gx_red = randint(0, self.grid_w - 1) 

                gy_red = randint(0, self.grid_h - 1) 

                gx_target = randint(0, self.grid_w - 1) 

                gy_target = randint(0, self.grid_h - 1) 

 

                blue_coord = (gx_blue, gy_blue) 

                red_coord = (gx_red, gy_red) 

                target_coord = (gx_target, gy_target) 

                 

                if (blue_coord != red_coord and blue_coord != target_coord and red_coord != target_coord and 

                    blue_coord not in self.obstacles and  

                    red_coord not in self.obstacles and 

                    target_coord not in self.obstacles): 

                    break 

             

            self.blue_pos = py.Vector2(gx_blue, gy_blue) 

            self.red_pos = py.Vector2(gx_red, gy_red) 

            self.target_pos = py.Vector2(gx_target, gy_target) 

             

            # 2. KIỂM TRA TÍNH KẾT NỐI 

            if self.check_connectivity(self.red_pos, self.blue_pos, self.target_pos): 

                print(f"Màn chơi được tạo thành công sau {attempt + 1} lần thử.") 

                self.recalculate_path() 

                return 

 

        print(f"!!! KHÔNG THỂ TẠO MÀN CHƠI HỢP LỆ sau {MAX_TRIES} lần thử. Vui lòng kiểm tra lại kích thước lưới hoặc mật độ chướng ngại vật.") 

        # Vẫn cần thoát khỏi vòng lặp vô tận nếu không tìm được màn chơi hợp lệ 

        # Trong trường hợp này, chúng ta có thể gọi py.quit() để thoát hẳn, hoặc sử dụng màn chơi cuối cùng 

        # Ở đây tôi chọn tiếp tục với màn chơi cuối cùng, nhưng có thể sẽ bị kẹt. 

 

    def check_connectivity(self, red_start, blue_end, target_end): 

        """Kiểm tra xem có đường đi hợp lệ giữa các điểm chính không.""" 

         

        # 1. Kiểm tra Đỏ có thể đến Xanh không (Chế độ Rượt đuổi) 

        path_to_blue = self.bfs_internal(red_start, blue_end, check_target_access=False) 

        if not path_to_blue and red_start != blue_end: 

            # Nếu Đỏ và Xanh không trùng nhau nhưng không có đường đi 

            print("LỖI KẾT NỐI: Đỏ không thể đến Xanh.") 

            return False 

             

        # 2. Kiểm tra Đỏ có thể đến được ô cạnh Nâu không (Chế độ Kéo) 

        adj_target = self.find_adjacent_to_target(red_start, target_end) 

        if adj_target: 

             path_to_adj = self.bfs_internal(red_start, adj_target, check_target_access=True) 

             if not path_to_adj and red_start != adj_target: 

                 print("LỖI KẾT NỐI: Đỏ không thể đến ô cạnh Nâu.") 

                 return False 

        else: 

             print("LỖI KẾT NỐI: Không tìm thấy ô hợp lệ cạnh Nâu.") 

             return False # Không có ô hợp lệ cạnh Nâu để Đỏ dừng 

 

        return True 

 

 

    def recalculate_path(self, mode='chase'): 

        """Tính toán lại đường đi ngắn nhất (BFS) từ Đỏ đến Xanh (chase) hoặc Đỏ đến CẠNH Nâu (tow).""" 

         

        if mode == 'chase' and self.red_moving and not self.towing: 

            start = self.red_pos 

            end = self.blue_pos 

            self.path = self.bfs_internal(start, end, check_target_access=False) 

        elif mode == 'tow' and self.towing: 

            start = self.red_pos 

             

            # Đích đến khi kéo là ô BÊN CẠNH ô Nâu gần nhất. 

            end = self.find_adjacent_to_target(self.red_pos, self.target_pos) 

            if end: 

                 self.towing_path = self.bfs_internal(start, end, check_target_access=True) 

            else: 

                 self.towing_path.clear() 

        else: 

            self.path.clear()  

            self.towing_path.clear() 

             

    def find_adjacent_to_target(self, start_pos, target_pos): 

        """Tìm ô liền kề target_pos gần start_pos nhất.""" 

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)] 

        tx, ty = int(target_pos.x), int(target_pos.y) 

         

        best_adj_pos = None 

        min_dist = float('inf') 

         

        for dx, dy in directions: 

            adj_x, adj_y = tx + dx, ty + dy 

            adj_coord = (adj_x, adj_y) 

             

            if 0 <= adj_x < self.grid_w and 0 <= adj_y < self.grid_h and adj_coord not in self.obstacles: 

                # Tính khoảng cách Manhattan từ start_pos đến ô liền kề 

                dist = abs(int(start_pos.x) - adj_x) + abs(int(start_pos.y) - adj_y) 

                 

                if dist < min_dist: 

                    min_dist = dist 

                    best_adj_pos = py.Vector2(adj_x, adj_y) 

                     

        return best_adj_pos 

         

    # Đã đổi tên hàm ban đầu thành bfs_internal để phục vụ việc check_connectivity 

    def bfs_internal(self, start, end, check_target_access=False): 

        """Thuật toán BFS. Nếu check_target_access=True, ĐỎ KHÔNG ĐƯỢC ĐI VÀO Ô NÂU.""" 

        queue = collections.deque([ ( (int(start.x), int(start.y)), [] ) ]) 

        visited = set([(int(start.x), int(start.y))]) 

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)] 

         

        end_coord = (int(end.x), int(end.y)) 

        target_coord = (int(self.target_pos.x), int(self.target_pos.y)) 

 

        while queue: 

            (curr_x, curr_y), path = queue.popleft() 

             

            if curr_x == end_coord[0] and curr_y == end_coord[1]: 

                return collections.deque(path)  

             

            for dx, dy in directions: 

                next_x, next_y = curr_x + dx, curr_y + dy 

                next_coord = (next_x, next_y) 

                 

                # Bỏ qua chướng ngại vật 

                if next_coord in self.obstacles: 

                    continue  

 

                # QUAN TRỌNG: ĐỎ không bao giờ được bước vào ô Nâu 

                if check_target_access and next_coord == target_coord and next_coord != end_coord: 

                    continue 

 

                if 0 <= next_x < self.grid_w and 0 <= next_y < self.grid_h: 

                    if next_coord not in visited: 

                        visited.add(next_coord) 

                        new_path = path + [next_coord] 

                        queue.append((next_coord, new_path)) 

                         

        return collections.deque()  

         

    # Cập nhật lại tên hàm cũ, gọi lại bfs_internal 

    def bfs_shortest_path(self, start, end): 

        # Khi Đỏ rượt đuổi, ô Nâu không bị cấm 

        return self.bfs_internal(start, end, check_target_access=False) 

 

 

    def move_blue_circle(self): 

        """Cho hình tròn Xanh di chuyển ngẫu nhiên (chỉ khi không bị kéo).""" 

        if not self.blue_moving or self.towing: 

             return  

         

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)] 

        valid_moves = [] 

         

        for dx, dy in directions: 

            new_x = int(self.blue_pos.x) + dx 

            new_y = int(self.blue_pos.y) + dy 

            new_coord = (new_x, new_y) 

             

            # Không di chuyển vào chướng ngại vật, hoặc ô Đỏ, hoặc ô Nâu 

            if (0 <= new_x < self.grid_w and 0 <= new_y < self.grid_h and  

                new_coord not in self.obstacles and 

                (new_x, new_y) != (self.red_pos.x, self.red_pos.y) and 

                (new_x, new_y) != (self.target_pos.x, self.target_pos.y if self.target_pos else (-1,-1))): 

                valid_moves.append(new_coord) 

         

        if valid_moves: 

            new_bx, new_by = valid_moves[randint(0, len(valid_moves) - 1)] 

            self.blue_pos.x = new_bx 

            self.blue_pos.y = new_by 

             

            self.path.clear()  

 

    def move_red_circle(self): 

        """Di chuyển hình tròn Đỏ (chỉ khi đang rượt đuổi).""" 

        if not self.red_moving or self.towing: 

            return  

             

        if self.path: 

            next_grid_x, next_grid_y = self.path.popleft() 

            self.red_pos.x = next_grid_x 

            self.red_pos.y = next_grid_y 

 

    def tow_blue_circle(self): 

        """Đỏ kéo Xanh về ô Nâu.""" 

        if not self.towing: 

            return 

 

        # 1. Tính toán lộ trình kéo nếu cần (đích là ô cạnh Nâu) 

        if not self.towing_path: # Không cần kiểm tra self.red_pos != self.target_pos nữa 

            self.recalculate_path(mode='tow') 

         

        # 2. Thực hiện bước di chuyển (nếu có lộ trình) 

        if self.towing_path: 

            # Lưu lại vị trí cũ của Đỏ (vị trí Xanh sẽ được kéo đến) 

            old_red_pos = py.Vector2(self.red_pos.x, self.red_pos.y) 

             

            # Đỏ di chuyển 1 bước về phía CẠNH Nâu 

            next_grid_x, next_grid_y = self.towing_path.popleft() 

            self.red_pos.x = next_grid_x 

            self.red_pos.y = next_grid_y 

             

            # Xanh di chuyển đến vị trí cũ của Đỏ 

            self.blue_pos.x = old_red_pos.x 

            self.blue_pos.y = old_red_pos.y 

             

        # 3. Kiểm tra kết thúc kéo 

        # Điều kiện: Đỏ đã đến ô liền kề Nâu (lộ trình kéo hết) 

        if not self.towing_path: 

             # Bước cuối: Đỏ dừng, Xanh nhảy vào ô Nâu (nếu chưa ở đó) 

             if self.blue_pos != self.target_pos: 

                 self.blue_pos.x = self.target_pos.x 

                 self.blue_pos.y = self.target_pos.y 

                  

             self.caught = True  

             self.towing = False 

             print("--- ĐỎ ĐÃ DỪNG, XANH ĐÃ ĐẾN ĐÍCH NÂU ---") 

 

 

    def draw_obstacles(self): 

        """Vẽ các ô vuông màu đen làm chướng ngại vật.""" 

        for ox, oy in self.obstacles: 

            rect = py.Rect(ox * self.sq_size, oy * self.sq_size, self.sq_size, self.sq_size) 

            py.draw.rect(self.scr, self.color["black"], rect) 

 

    def draw_target_square(self): 

        """Vẽ ô đích màu Nâu.""" 

        if self.target_pos: 

             tx, ty = int(self.target_pos.x), int(self.target_pos.y) 

             rect = py.Rect(tx * self.sq_size, ty * self.sq_size, self.sq_size, self.sq_size) 

             py.draw.rect(self.scr, self.color["brown"], rect) 

             

    def draw_circles(self): 

        """Vẽ hình tròn Xanh và Đỏ.""" 

        # VẼ XANH 

        center_blue = self.get_center_coords(self.blue_pos.x, self.blue_pos.y) 

        blue_color = self.color["blue"] 

        # Đánh dấu Xanh đang bị kéo 

        if self.towing: 

             blue_color = (150, 150, 255) # Màu xanh nhạt khi bị kéo 

        py.draw.circle(self.scr, blue_color, center_blue, self.radius) 

        if not self.blue_moving: 

             py.draw.line(self.scr, self.color["black"], center_blue - py.Vector2(self.radius/2, self.radius/2), center_blue + py.Vector2(self.radius/2, self.radius/2), 2) 

             py.draw.line(self.scr, self.color["black"], center_blue + py.Vector2(self.radius/2, -self.radius/2), center_blue - py.Vector2(self.radius/2, -self.radius/2), 2) 

 

 

        # VẼ ĐỎ 

        center_red = self.get_center_coords(self.red_pos.x, self.red_pos.y) 

        red_color = self.color["red"] 

        # Đánh dấu Đỏ đang kéo 

        if self.towing: 

             red_color = (255, 150, 150) # Màu đỏ nhạt khi đang kéo 

        py.draw.circle(self.scr, red_color, center_red, self.radius) 

        if not self.red_moving: 

             py.draw.line(self.scr, self.color["black"], center_red - py.Vector2(self.radius/2, self.radius/2), center_red + py.Vector2(self.radius/2, self.radius/2), 2) 

             py.draw.line(self.scr, self.color["black"], center_red + py.Vector2(self.radius/2, -self.radius/2), center_red - py.Vector2(self.radius/2, -self.radius/2), 2) 

 

 

    def MAIN(m): 

        for m.e in py.event.get(): 

            if m.e.type == py.KEYDOWN: 

                if m.e.key == py.K_g: 

                    m.r = False 

             

            # XỬ LÝ NHẤP CHUỘT 

            if m.e.type == py.MOUSEBUTTONDOWN: 

                mx, my = m.e.pos 

                mouse_pos = py.Vector2(mx, my) 

 

                click_gx = int(mouse_pos.x // m.sq_size) 

                click_gy = int(mouse_pos.y // m.sq_size) 

                 

                blue_gx, blue_gy = int(m.blue_pos.x), int(m.blue_pos.y) 

                red_gx, red_gy = int(m.red_pos.x), int(m.red_pos.y) 

 

                # --- Kiểm tra click vào Xanh --- 

                if click_gx == blue_gx and click_gy == blue_gy: 

                    # Chỉ toggle khi không bị kéo 

                    if not m.towing: 

                        m.blue_moving = not m.blue_moving 

                        m.recalculate_path() 

                 

                # --- Kiểm tra click vào Đỏ --- 

                elif click_gx == red_gx and click_gy == red_gy: 

                    # Chỉ toggle khi không đang kéo 

                    if not m.towing: 

                        m.red_moving = not m.red_moving 

                        m.recalculate_path()  

     

    def RUN(r): 

         

        while r.r: 

            r.clock.tick(r.FPS) 

            r.m = py.Vector2(py.mouse.get_pos()) 

             

            # 1. Kiểm tra điều kiện KẾT THÚC chuỗi kéo (Xanh đã vào ô Nâu) 

            if r.caught and r.blue_pos == r.target_pos: 

                print("--- XANH ĐÃ ĐƯỢC KÉO VÀO Ô ĐÍCH NÂU! Chuyển màn hình ---") 

                sleep(2) 

                r.setup_circles()  

                continue 

 

            # 2. Xử lý logic BẮT và KÉO 

            if r.red_pos == r.blue_pos and not r.towing: 

                print("--- ĐỎ ĐÃ BẮT ĐƯỢC XANH! Bắt đầu kéo ---") 

                r.towing = True 

                r.red_moving = False  

                r.blue_moving = False  

                r.towing_path.clear() 

                r.recalculate_path(mode='tow') # Tính toán đường đi kéo đến CẠNH Nâu 

 

            # 3. Xử lý di chuyển 

             

            # Tăng bộ đếm thời gian 

            r.red_move_timer += 1 

            r.blue_move_timer += 1 

             

            # --- LOGIC DI CHUYỂN CỦA XANH --- 

            if not r.towing and r.blue_move_timer >= r.BLUE_MOVE_RATE: 

                r.move_blue_circle() 

                r.blue_move_timer = 0 

             

            # --- LOGIC DI CHUYỂN CỦA ĐỎ (RƯỢT ĐUỔI HOẶC KÉO) --- 

            if r.red_move_timer >= r.RED_MOVE_RATE: 

                 

                if r.towing: 

                    # Đỏ kéo Xanh (Đỏ đi đến ô cạnh Nâu) 

                    r.tow_blue_circle() 

                     

                else: 

                    # Logic Rượt Đuổi thông thường 

                     

                    # B. Đỏ cần lộ trình: Nếu lộ trình đã hết HOẶC bị xóa 

                    # Kiểm tra r.path trước khi truy cập r.path[-1] 

                    if r.red_moving and (not r.path or (not r.blue_moving and r.red_pos != r.blue_pos and r.path and r.path[-1] != (r.blue_pos.x, r.blue_pos.y))): 

                          r.recalculate_path(mode='chase') 

                     

                    # C. Đỏ di chuyển 

                    r.move_red_circle() 

                     

                r.red_move_timer = 0 

             

            # --- VẼ --- 

            r.scr.fill(r.color["white"]) 

            r.grid.DRAW_GRID() 

            r.grid.DRAW_BORDER() 

            r.draw_target_square() 

            r.draw_obstacles()  

            r.draw_circles() 

             

            # --- CẬP NHẬT --- 

            r.MAIN() 

            py.display.update() 

 

# --- CHẠY CHƯƠNG TRÌNH --- 

_MAIN_().RUN() 