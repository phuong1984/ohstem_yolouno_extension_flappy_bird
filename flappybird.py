from ssd1306 import *
import framebuf
import time
import random



# Thông số trò chơi
SCREEN_WIDTH = 128
SCREEN_HEIGHT = 64
BIRD_SIZE = 4
PIPE_WIDTH = 10
MIN_PIPE_HEIGHT = 10
PIPE_SPEED = 2



class FlappyBird():
    def __init__(self):
        self.oled = SSD1306_I2C()
        self.oled.fill(0)
        # Biến trạng thái
        self.bird_y = SCREEN_HEIGHT // 2  # Vị trí y của chim
        self.bird_velocity = 0
        self.pipes = []  # Danh sách cột ống: (x, gap_y)
        self.score = 0
        self.last_pipe_time = time.ticks_ms()
        self.game_state = 0
        self.gravity = 0.2 # tốc độ rơi tự do
        self.fly_velocity = -2 # tốc độ bay lên
        self.pipe_gap = 20 # Khoảng cách giữa hai phần ống
        
    def create(self, gravity = 0.2, fly = 2):
        self.gravity = gravity
        self.fly_velocity = -fly
        
    def draw(self):
        """Vẽ các thành phần trò chơi"""
        self.oled.fill(0)  # Xóa màn hình
        # Vẽ chim
        self.oled.fill_rect(20, int(self.bird_y), BIRD_SIZE, BIRD_SIZE, 1)
        # Vẽ các cột ống
        for x, gap_y in self.pipes:
            # Ống trên
            self.oled.fill_rect(x, 0, PIPE_WIDTH, gap_y, 1)
            # Ống dưới
            self.oled.fill_rect(x, gap_y + self.pipe_gap, PIPE_WIDTH, SCREEN_HEIGHT - (gap_y + self.pipe_gap), 1)
        # Vẽ điểm số
        self.oled.text(f"Score: {self.score}", 0, 0, 1)
        
        self.oled.show()

    def add_pipe(self):
        """Thêm cột ống mới"""
        if (self.score < 20): self.pipe_gap = 20
        elif (self.score < 30): self.pipe_gap = 18
        elif (self.score < 40): self.pipe_gap = 16
        else: self.pipe_gap = 14
        gap_y = random.randint(MIN_PIPE_HEIGHT, SCREEN_HEIGHT - self.pipe_gap - MIN_PIPE_HEIGHT)
        self.pipes.append((SCREEN_WIDTH, gap_y))

    def check_collision(self):
        """Kiểm tra va chạm"""
        bird_top = self.bird_y
        bird_bottom = self.bird_y + BIRD_SIZE
        bird_left = 20
        bird_right = 20 + BIRD_SIZE

        # Va chạm với mép màn hình
        if bird_top <= 0 or bird_bottom >= SCREEN_HEIGHT:
            return True
        # Va chạm với cột ống
        for x, gap_y in self.pipes:
            if bird_right > x and bird_left < x + PIPE_WIDTH:
                if bird_top < gap_y or bird_bottom > gap_y + self.pipe_gap:
                    return True
        return False
        
    def start_game(self):
        self.bird_y = SCREEN_HEIGHT // 2
        self.bird_velocity = 0
        self.pipes = []
        self.score = 0
        self.game_over = False
        self.add_pipe()
        self.last_pipe_time = time.ticks_ms()
        self.game_state = 1
        
    def play(self):        
        if(self.game_state == 0):
            self.oled.fill(0)  # Xóa màn hình
            self.oled.text("Press button", 10, 20, 1)
            self.oled.text("to play", 10, 40, 1)
            self.oled.show()
        elif(self.game_state == 1):
            # Cập nhật vị trí chim
            self.bird_velocity += self.gravity
            self.bird_y += self.bird_velocity
            # Cập nhật cột ống
            new_pipes = []
            for x, gap_y in self.pipes:
                new_x = x - PIPE_SPEED
                if new_x > -PIPE_WIDTH:
                    new_pipes.append((new_x, gap_y))
                if x + PIPE_WIDTH > 20 >= new_x + PIPE_WIDTH:  # Vượt qua cột
                    self.score += 1
            self.pipes = new_pipes
            # Thêm cột ống mới sau khoảng thời gian
            if time.ticks_diff(time.ticks_ms(), self.last_pipe_time) > 2000:  # Mỗi 2 giây
                self.add_pipe()
                self.last_pipe_time = time.ticks_ms()
            # Kiểm tra va chạm
            if self.check_collision():
                self.game_state = 2
            # Vẽ màn hình
            self.draw()
        elif(self.game_state == 2):
            # Hiển thị Game Over nếu thua
            self.oled.fill(0)  # Xóa màn hình
            self.oled.text("Game Over", 30, 0, 1)
            self.oled.text(f"Score: {self.score}", 30, 15, 1)
            self.oled.text("Press button", 10, 40, 1)
            self.oled.text("to replay", 10, 55, 1)
            self.oled.show()            
        
    def handle_button_pressed(self):
        if(self.game_state == 0):            
            self.start_game()
        elif(self.game_state == 1):            
            self.bird_velocity = self.fly_velocity
            time.sleep(0.05)  # Debounce nút
        elif(self.game_state == 2):            
            self.start_game()
