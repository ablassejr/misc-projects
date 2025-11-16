# Space Invaders - Education Aide
## Building a 2D Game from First Principles

### Overview
This guide teaches you fundamental game development concepts by building a Space Invaders clone. You'll learn about game loops, entity management, collision detection, and rendering - skills that apply to any game.

---

## Part 1: Understanding Game Architecture

### Question 1: What Makes a Game Different from Regular Programs?
**Think about this:** How does a game differ from a calculator or text editor?

**Your Answer:** _[Write your thoughts]_

<details>
<summary>Fundamental Difference</summary>

**Regular programs:** Event-driven (wait for user input)
```
while True:
    input = wait_for_user()
    process(input)
    display_output()
```

**Games:** Time-driven (continuous update loop)
```
while game_running:
    input = check_input()      # Don't wait
    update(delta_time)         # Update game state
    render()                    # Draw to screen
    limit_frame_rate()         # Run at consistent speed
```

**Key insight:** Games must update smoothly whether or not user provides input. Enemies move, bullets fly, even if player does nothing!
</details>

### Question 2: The Game Loop
**Question:** What should happen in each frame of a game?

**Your Answer:** _[List the steps]_

<details>
<summary>Game Loop Structure</summary>

**Basic game loop:**
```python
import time

FPS = 60
FRAME_TIME = 1.0 / FPS  # 16.67ms per frame

last_time = time.time()
running = True

while running:
    current_time = time.time()
    delta_time = current_time - last_time
    last_time = current_time

    # 1. Process input (non-blocking)
    handle_input()

    # 2. Update game state
    update_game(delta_time)

    # 3. Render
    draw_everything()

    # 4. Frame limiting
    frame_duration = time.time() - current_time
    if frame_duration < FRAME_TIME:
        time.sleep(FRAME_TIME - frame_duration)
```

**Why delta_time?**
Different computers run at different speeds. By using delta_time (time since last frame), we ensure consistent game speed.

Example:
```python
# Without delta_time (BAD):
player.x += 5  # Moves 5 pixels per frame
                # Fast computer: 120 FPS → 600 pixels/sec
                # Slow computer: 30 FPS → 150 pixels/sec

# With delta_time (GOOD):
speed = 200  # pixels per second
player.x += speed * delta_time  # Same speed on all computers!
```
</details>

---

## Part 2: Entities and State Management

### Understanding Game Objects

**Question:** What information does a game object (like player or enemy) need?

**Your Answer:** _[List the properties]_

<details>
<summary>Entity Components</summary>

**Minimum requirements:**
```python
class Entity:
    def __init__(self, x, y):
        self.x = x          # Position
        self.y = y
        self.width = 32     # Size (for collision)
        self.height = 32
        self.alive = True   # State

    def update(self, delta_time):
        pass  # Override in subclasses

    def draw(self, screen):
        pass  # Override in subclasses
```

**For Space Invaders, we need:**
```python
class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.speed = 200  # pixels/second
        self.bullet = None

class Enemy(Entity):
    def __init__(self, x, y, type):
        super().__init__(x, y)
        self.type = type   # Different enemy types
        self.points = 10   # Score value

class Bullet(Entity):
    def __init__(self, x, y, direction):
        super().__init__(x, y)
        self.speed = 300
        self.direction = direction  # 1 = up, -1 = down
```
</details>

### Managing Multiple Entities

**Question:** How do you keep track of dozens of enemies and bullets?

**Your Answer:** _[Describe your approach]_

<details>
<summary>Entity Lists</summary>

**Simple approach:**
```python
class Game:
    def __init__(self):
        self.player = Player(400, 550)
        self.enemies = []
        self.bullets = []
        self.enemy_bullets = []

        # Create enemy formation (5 rows × 11 columns)
        for row in range(5):
            for col in range(11):
                x = 100 + col * 50
                y = 50 + row * 40
                enemy = Enemy(x, y, row // 2)  # Different types
                self.enemies.append(enemy)

    def update(self, delta_time):
        # Update player
        self.player.update(delta_time)

        # Update all enemies
        for enemy in self.enemies:
            enemy.update(delta_time)

        # Update bullets
        for bullet in self.bullets:
            bullet.update(delta_time)

        # Remove off-screen bullets
        self.bullets = [b for b in self.bullets
                        if 0 <= b.y <= 600]

        # Remove dead enemies
        self.enemies = [e for e in self.enemies
                        if e.alive]

    def draw(self, screen):
        self.player.draw(screen)
        for enemy in self.enemies:
            enemy.draw(screen)
        for bullet in self.bullets:
            bullet.draw(screen)
```

**Try to answer:** What happens if you forget to remove dead entities?

<details>
<summary>Answer</summary>
**Memory leak!** The lists keep growing, slowing down the game. Always clean up dead entities.

**Better approach (advanced):**
```python
# Use object pooling - reuse objects instead of creating/destroying
class BulletPool:
    def __init__(self, size=50):
        self.pool = [Bullet(0, 0, 1) for _ in range(size)]
        self.active = []

    def spawn(self, x, y, direction):
        for bullet in self.pool:
            if bullet not in self.active:
                bullet.x, bullet.y = x, y
                bullet.direction = direction
                self.active.append(bullet)
                return bullet

    def remove(self, bullet):
        if bullet in self.active:
            self.active.remove(bullet)
```
</details>
</details>

---

## Part 3: Collision Detection

### Bounding Box Collision

**Question:** How do you detect if a bullet hits an enemy?

**Your Answer:** _[Write pseudocode]_

<details>
<summary>Rectangle Collision (AABB)</summary>

**Axis-Aligned Bounding Box (AABB):**
```python
def check_collision(entity1, entity2):
    """Check if two rectangular entities overlap"""
    # Calculate edges
    left1 = entity1.x
    right1 = entity1.x + entity1.width
    top1 = entity1.y
    bottom1 = entity1.y + entity1.height

    left2 = entity2.x
    right2 = entity2.x + entity2.width
    top2 = entity2.y
    bottom2 = entity2.y + entity2.height

    # Check if rectangles overlap
    if (right1 >= left2 and left1 <= right2 and
        bottom1 >= top2 and top1 <= bottom2):
        return True

    return False

# Simplified version:
def collides(a, b):
    return (a.x < b.x + b.width and
            a.x + a.width > b.x and
            a.y < b.y + b.height and
            a.y + a.height > b.y)
```

**Visual explanation:**
```
No collision:           Collision:
┌───┐                  ┌───┐
│ A │  ┌───┐          │ A┌┼──┐
└───┘  │ B │          └──┼┘B │
       └───┘              └───┘
```

**Testing collision in game loop:**
```python
def update(self, delta_time):
    # Check bullet-enemy collisions
    for bullet in self.bullets[:]:  # Copy list (modifying during iteration)
        for enemy in self.enemies[:]:
            if collides(bullet, enemy):
                enemy.alive = False
                bullet.alive = False
                self.score += enemy.points
                break  # Bullet can only hit one enemy
```
</details>

### Collision Optimization

**Question:** If you have 100 bullets and 50 enemies, how many collision checks?

**Your Answer:** _[Calculate]_

<details>
<summary>Collision Performance</summary>

**Naive approach:** Check every bullet against every enemy
- Checks: 100 bullets × 50 enemies = **5000 checks per frame**
- At 60 FPS: 300,000 checks per second!

**For Space Invaders:** This is actually fine! Small numbers.

**For bigger games:** Use spatial partitioning

**Simple optimization - Spatial Grid:**
```python
class SpatialGrid:
    def __init__(self, width, height, cell_size):
        self.cell_size = cell_size
        self.grid = {}

    def _get_cell(self, x, y):
        return (int(x // self.cell_size),
                int(y // self.cell_size))

    def insert(self, entity):
        cell = self._get_cell(entity.x, entity.y)
        if cell not in self.grid:
            self.grid[cell] = []
        self.grid[cell].append(entity)

    def get_nearby(self, entity):
        cell = self._get_cell(entity.x, entity.y)
        nearby = []
        # Check this cell and neighbors
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                neighbor = (cell[0] + dx, cell[1] + dy)
                if neighbor in self.grid:
                    nearby.extend(self.grid[neighbor])
        return nearby

# Usage: Only check entities in nearby cells
for bullet in bullets:
    for enemy in spatial_grid.get_nearby(bullet):
        if collides(bullet, enemy):
            # Handle collision
```

**Result:** Reduces checks from O(n²) to O(n)
</details>

---

## Part 4: Enemy Movement Patterns

### Space Invaders Formation

**Question:** How do enemies move together as a group?

**Your Answer:** _[Describe the algorithm]_

<details>
<summary>Formation Movement Logic</summary>

**Classic Space Invaders behavior:**
1. Enemies move horizontally as a group
2. When any enemy reaches edge, entire group:
   - Drops down one row
   - Reverses direction
3. Speed increases as enemies are destroyed

**Implementation:**
```python
class EnemyFormation:
    def __init__(self):
        self.enemies = []
        self.direction = 1  # 1 = right, -1 = left
        self.speed = 30     # pixels/second
        self.drop_distance = 20

    def update(self, delta_time):
        if not self.enemies:
            return

        # Move all enemies
        move_x = self.direction * self.speed * delta_time

        # Check if any enemy hits edge
        should_drop = False
        for enemy in self.enemies:
            new_x = enemy.x + move_x
            if new_x <= 0 or new_x >= 750:
                should_drop = True
                break

        if should_drop:
            # Drop down and reverse direction
            for enemy in self.enemies:
                enemy.y += self.drop_distance
            self.direction *= -1  # Reverse
        else:
            # Normal horizontal movement
            for enemy in self.enemies:
                enemy.x += move_x

        # Speed up as enemies die
        alive_count = len(self.enemies)
        self.speed = 30 + (55 - alive_count) * 2
```

**Try it:** What happens when only 1 enemy remains?

<details>
<summary>Answer</summary>
Speed becomes: 30 + (55 - 1) * 2 = **138 pixels/second**

Much faster than the initial 30! This is how Space Invaders gets harder.
</details>
</details>

### Advanced: Sine Wave Pattern

**Extension:** Make enemies move in a wave pattern

<details>
<summary>Wave Movement</summary>

```python
import math

class WaveEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.start_x = x
        self.time = 0
        self.amplitude = 50  # Wave height
        self.frequency = 2   # Wave speed

    def update(self, delta_time):
        self.time += delta_time
        # Sine wave for smooth side-to-side motion
        self.x = self.start_x + math.sin(self.time * self.frequency) * self.amplitude
        # Move down slowly
        self.y += 20 * delta_time
```

This creates smooth, wave-like enemy movement!
</details>

---

## Part 5: Rendering and Graphics

### Drawing Sprites

**Question:** How do you display game objects on screen?

<details>
<summary>Basic Rendering with Pygame</summary>

```python
import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Load images
player_img = pygame.image.load('player.png')
enemy_img = pygame.image.load('enemy.png')
bullet_img = pygame.image.load('bullet.png')

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = player_img

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear screen
    screen.fill((0, 0, 0))  # Black background

    # Draw everything
    player.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)

    # Update display
    pygame.display.flip()

    # Limit to 60 FPS
    clock.tick(60)
```

**No images? Draw rectangles:**
```python
class Player:
    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0),  # Green
                         (self.x, self.y, 32, 32))
```
</details>

### Animation

**Question:** How do you animate sprites (like enemy movement)?

<details>
<summary>Sprite Animation</summary>

**Frame-based animation:**
```python
class AnimatedEnemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frames = [
            pygame.image.load('enemy1.png'),
            pygame.image.load('enemy2.png'),
        ]
        self.current_frame = 0
        self.animation_time = 0
        self.animation_speed = 0.5  # Seconds per frame

    def update(self, delta_time):
        self.animation_time += delta_time
        if self.animation_time >= self.animation_speed:
            self.animation_time = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)

    def draw(self, screen):
        frame = self.frames[self.current_frame]
        screen.blit(frame, (self.x, self.y))
```

**Result:** Enemies alternate between two images, creating animation effect!
</details>

---

## Part 6: Input Handling

### Keyboard Input

**Question:** How do you make the player move when arrow keys are pressed?

<details>
<summary>Input Processing</summary>

**Event-based (discrete actions):**
```python
for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            player.shoot()
```

**State-based (continuous movement):**
```python
keys = pygame.key.get_pressed()

def update(self, delta_time):
    speed = 200  # pixels/second

    if keys[pygame.K_LEFT]:
        self.x -= speed * delta_time
    if keys[pygame.K_RIGHT]:
        self.x += speed * delta_time

    # Keep player on screen
    self.x = max(0, min(800 - self.width, self.x))
```

**Why two approaches?**
- **Events:** For one-time actions (shoot, jump)
- **State:** For continuous actions (move, hold to charge)

**Complete player control:**
```python
class Player:
    def __init__(self):
        self.x = 400
        self.y = 550
        self.speed = 200
        self.can_shoot = True
        self.shoot_cooldown = 0.5  # Seconds between shots
        self.time_since_shot = 0

    def update(self, delta_time, keys, bullets):
        # Movement
        if keys[pygame.K_LEFT]:
            self.x -= self.speed * delta_time
        if keys[pygame.K_RIGHT]:
            self.x += self.speed * delta_time

        # Shooting
        self.time_since_shot += delta_time
        if keys[pygame.K_SPACE] and self.time_since_shot >= self.shoot_cooldown:
            bullets.append(Bullet(self.x, self.y, -1))
            self.time_since_shot = 0

        # Boundary
        self.x = max(0, min(768, self.x))
```
</details>

---

## Part 7: Sound and Scoring

### Adding Sound Effects

<details>
<summary>Sound with Pygame</summary>

```python
# Load sounds
shoot_sound = pygame.mixer.Sound('shoot.wav')
explosion_sound = pygame.mixer.Sound('explosion.wav')
pygame.mixer.music.load('background.mp3')
pygame.mixer.music.play(-1)  # Loop forever

# Play on events
def shoot(self):
    shoot_sound.play()
    bullets.append(Bullet(self.x, self.y))

# In collision detection:
if collides(bullet, enemy):
    explosion_sound.play()
    enemy.alive = False
```
</details>

### Score System

<details>
<summary>Implementing Score</summary>

```python
class Game:
    def __init__(self):
        self.score = 0
        self.high_score = self.load_high_score()
        self.font = pygame.font.Font(None, 36)

    def update_score(self, points):
        self.score += points
        if self.score > self.high_score:
            self.high_score = self.score

    def draw_hud(self, screen):
        score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        high_text = self.font.render(f'High: {self.high_score}', True, (255, 255, 0))
        screen.blit(high_text, (10, 50))

    def load_high_score(self):
        try:
            with open('highscore.txt', 'r') as f:
                return int(f.read())
        except:
            return 0

    def save_high_score(self):
        with open('highscore.txt', 'w') as f:
            f.write(str(self.high_score))
```
</details>

---

## Part 8: Putting It All Together

### Complete Space Invaders (Simplified)

<details>
<summary>Full Game Code</summary>

```python
import pygame
import random

# Initialize
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

class Player:
    def __init__(self):
        self.x, self.y = 400, 550
        self.width, self.height = 40, 30
        self.speed = 300

    def update(self, dt, keys):
        if keys[pygame.K_LEFT]:
            self.x -= self.speed * dt
        if keys[pygame.K_RIGHT]:
            self.x += self.speed * dt
        self.x = max(0, min(760, self.x))

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, self.width, self.height))

class Enemy:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.width, self.height = 30, 30
        self.alive = True

    def draw(self, screen):
        if self.alive:
            pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))

class Bullet:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.width, self.height = 4, 10
        self.speed = 400

    def update(self, dt):
        self.y -= self.speed * dt

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 0), (self.x, self.y, self.width, self.height))

# Create entities
player = Player()
enemies = [Enemy(50 + i * 60, 50 + j * 50) for j in range(5) for i in range(11)]
bullets = []

# Game state
score = 0
font = pygame.font.Font(None, 36)
running = True
last_time = pygame.time.get_ticks() / 1000.0

# Game loop
while running:
    current_time = pygame.time.get_ticks() / 1000.0
    dt = current_time - last_time
    last_time = current_time

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append(Bullet(player.x + 18, player.y))

    # Update
    keys = pygame.key.get_pressed()
    player.update(dt, keys)

    for bullet in bullets[:]:
        bullet.update(dt)
        if bullet.y < 0:
            bullets.remove(bullet)

    # Collision
    for bullet in bullets[:]:
        for enemy in enemies:
            if enemy.alive:
                if (bullet.x < enemy.x + enemy.width and
                    bullet.x + bullet.width > enemy.x and
                    bullet.y < enemy.y + enemy.height and
                    bullet.y + bullet.height > enemy.y):
                    enemy.alive = False
                    bullets.remove(bullet)
                    score += 10
                    break

    # Draw
    screen.fill((0, 0, 0))
    player.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)

    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```

**Try it!** This is a playable (though simple) Space Invaders game!
</details>

---

## Learning Projects

### Project 1: Minimal Playable (1 week)
- [ ] Player moves left/right
- [ ] Player shoots bullets
- [ ] Enemies in formation
- [ ] Collision detection
- [ ] Score display

### Project 2: Classic Features (2 weeks)
- [ ] Enemy movement (group behavior)
- [ ] Enemy shooting
- [ ] Player shields
- [ ] Lives system
- [ ] Game over screen

### Project 3: Polish (1 week)
- [ ] Sound effects
- [ ] Particle effects (explosions)
- [ ] Smooth animations
- [ ] High score persistence
- [ ] Main menu

### Project 4: Extensions
- [ ] Power-ups
- [ ] Multiple enemy types
- [ ] Boss battles
- [ ] Level progression
- [ ] Multiplayer

---

## Key Concepts Summary

1. **Game Loop:** Update → Render → Sleep
2. **Delta Time:** Consistent speed across hardware
3. **Entity Management:** Lists of objects
4. **Collision Detection:** Bounding boxes
5. **State Machine:** Menu → Playing → Game Over
6. **Input:** Events (discrete) vs State (continuous)

---

**Next Steps:** Build it! Start simple, add features gradually!

*Have fun!*
