import pygame
import math

class Wall:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
    
    def draw(self, screen, color=(0, 0, 0), thickness=3):
        pygame.draw.line(screen, color, (self.x1, self.y1), (self.x2, self.y2), thickness)
    
    def check_collision(self, player_x, player_y, player_radius):
        """
        Check if a circle (player) collides with this line segment (wall).
        Returns True if collision detected.
        """
        # Vector from wall start to end
        wall_dx = self.x2 - self.x1
        wall_dy = self.y2 - self.y1
        wall_length_sq = wall_dx * wall_dx + wall_dy * wall_dy
        
        # If wall is a point, check distance to that point
        if wall_length_sq < 0.0001:
            dist = math.sqrt((player_x - self.x1) ** 2 + (player_y - self.y1) ** 2)
            return dist < player_radius
        
        # Vector from wall start to player
        to_player_x = player_x - self.x1
        to_player_y = player_y - self.y1
        
        # Project player position onto wall line
        t = max(0, min(1, (to_player_x * wall_dx + to_player_y * wall_dy) / wall_length_sq))
        
        # Closest point on wall line to player
        closest_x = self.x1 + t * wall_dx
        closest_y = self.y1 + t * wall_dy
        
        # Distance from player to closest point on wall
        dist_x = player_x - closest_x
        dist_y = player_y - closest_y
        dist = math.sqrt(dist_x * dist_x + dist_y * dist_y)
        
        return dist < player_radius

class Player:
    def __init__(self, x, y, size, speed):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed

        self.image = pygame.image.load(r"assets/images/knight.png")
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect()

    def draw(self, screen):
        self.rect.center = (self.x, self.y)
        screen.blit(self.image, self.rect)

    def moveTowards(self, x, y, left, top, right, bottom, walls=None):
        if walls is None:
            walls = []
        
        distance = math.sqrt(math.pow(self.x - x, 2) + math.pow(self.y - y, 2))
        if distance < self.speed:
            return
        
        # Calculate desired movement
        new_x = self.x + self.speed * (x - self.x) / distance
        new_y = self.y + self.speed * (y - self.y) / distance
        
        # Clamp to boundaries first
        new_x = min(max(left, new_x), right)
        new_y = min(max(top, new_y), bottom)
        
        # Check wall collisions
        player_radius = self.size / 2
        if walls:
            # Check if the new position would collide with any wall
            collision = False
            for wall in walls:
                if wall.check_collision(new_x, new_y, player_radius):
                    collision = True
                    break
            
            if collision:
                # Try moving only in X direction
                test_x = new_x
                test_y = self.y
                x_collision = False
                for wall in walls:
                    if wall.check_collision(test_x, test_y, player_radius):
                        x_collision = True
                        break
                
                # Try moving only in Y direction
                test_x = self.x
                test_y = new_y
                y_collision = False
                for wall in walls:
                    if wall.check_collision(test_x, test_y, player_radius):
                        y_collision = True
                        break
                
                # If X direction is clear, allow X movement
                if not x_collision:
                    self.x = new_x
                
                # If Y direction is clear, allow Y movement
                if not y_collision:
                    self.y = new_y
            else:
                # No collision, move normally
                self.x = new_x
                self.y = new_y
        else:
            # No walls, move normally
            self.x = new_x
            self.y = new_y

    def touchingExit(self, exit):
        return abs(self.x - exit.x) < self.size and abs(self.y - exit.y) < self.size

class Exit:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

        self.image = pygame.image.load(r"assets/images/doorway.png")
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Door(Wall):
    """A door that acts as a wall but can be removed when the key is collected."""
    def __init__(self, x1, y1, x2, y2, door_id=1):
        super().__init__(x1, y1, x2, y2)
        self.door_id = door_id
        self.unlocked = False
    
    def draw(self, screen, color=(139, 69, 19), thickness=10):
        """Draw the door with a brown color to distinguish it from regular walls."""
        if not self.unlocked:
            super().draw(screen, color, thickness)

class Key:
    def __init__(self, x, y, size, key_id=1):
        self.x = x
        self.y = y
        self.size = size
        self.key_id = key_id
        self.collected = False

        self.image = pygame.image.load(r"assets/images/key.png")
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def draw(self, screen):
        """Draw the key image."""
        if not self.collected:
            self.rect.center = (self.x, self.y)
            screen.blit(self.image, self.rect)
    
    def check_collision(self, player_x, player_y, player_size):
        """Check if the player is touching the key."""
        if self.collected:
            return False
        distance = math.sqrt((player_x - self.x) ** 2 + (player_y - self.y) ** 2)
        return distance < (self.size / 2 + player_size / 2)

class Dragon:
    def __init__(self, x, y, size, speed):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed

        self.image = pygame.image.load(r"assets/images/spiked-dragon-head.png")
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect()

    def draw(self, screen):
        self.rect.center = (self.x, self.y)
        screen.blit(self.image, self.rect)

    def moveTowards(self, target_x, target_y, left, top, right, bottom, walls=None):
        """Move the dragon towards a target position with improved wall collision handling."""
        if walls is None:
            walls = []
        
        distance = math.sqrt(math.pow(self.x - target_x, 2) + math.pow(self.y - target_y, 2))
        if distance < self.speed:
            return
        
        dragon_radius = self.size / 2
        
        # Calculate desired movement direction
        dx = target_x - self.x
        dy = target_y - self.y
        dir_length = math.sqrt(dx * dx + dy * dy)
        if dir_length > 0:
            dx = dx / dir_length
            dy = dy / dir_length
        
        # Calculate desired movement
        new_x = self.x + self.speed * dx
        new_y = self.y + self.speed * dy
        
        # Clamp to boundaries first
        new_x = min(max(left + dragon_radius, new_x), right - dragon_radius)
        new_y = min(max(top + dragon_radius, new_y), bottom - dragon_radius)
        
        # Check wall collisions
        if walls:
            # Check if the new position would collide with any wall
            collision = False
            for wall in walls:
                if wall.check_collision(new_x, new_y, dragon_radius):
                    collision = True
                    break
            
            if collision:
                # Try moving only in X direction
                test_x = new_x
                test_y = self.y
                x_collision = False
                for wall in walls:
                    if wall.check_collision(test_x, test_y, dragon_radius):
                        x_collision = True
                        break
                
                # Try moving only in Y direction
                test_x = self.x
                test_y = new_y
                y_collision = False
                for wall in walls:
                    if wall.check_collision(test_x, test_y, dragon_radius):
                        y_collision = True
                        break
                
                moved = False
                
                # If X direction is clear, allow X movement
                if not x_collision:
                    self.x = new_x
                    moved = True
                
                # If Y direction is clear, allow Y movement
                if not y_collision:
                    self.y = new_y
                    moved = True
                
                # If still stuck, try sliding along the wall (perpendicular movement)
                if not moved:
                    # Try sliding perpendicular to the movement direction
                    # Try both perpendicular directions
                    perp_dx = -dy
                    perp_dy = dx
                    
                    # Try first perpendicular direction
                    slide_x = self.x + self.speed * perp_dx
                    slide_y = self.y + self.speed * perp_dy
                    slide_x = min(max(left + dragon_radius, slide_x), right - dragon_radius)
                    slide_y = min(max(top + dragon_radius, slide_y), bottom - dragon_radius)
                    
                    slide_collision = False
                    for wall in walls:
                        if wall.check_collision(slide_x, slide_y, dragon_radius):
                            slide_collision = True
                            break
                    
                    if not slide_collision:
                        self.x = slide_x
                        self.y = slide_y
                        moved = True
                    else:
                        # Try opposite perpendicular direction
                        slide_x = self.x - self.speed * perp_dx
                        slide_y = self.y - self.speed * perp_dy
                        slide_x = min(max(left + dragon_radius, slide_x), right - dragon_radius)
                        slide_y = min(max(top + dragon_radius, slide_y), bottom - dragon_radius)
                        
                        slide_collision = False
                        for wall in walls:
                            if wall.check_collision(slide_x, slide_y, dragon_radius):
                                slide_collision = True
                                break
                        
                        if not slide_collision:
                            self.x = slide_x
                            self.y = slide_y
                            moved = True
                
                # If still completely stuck, try moving away from walls slightly
                if not moved:
                    # Try moving in reverse direction (away from target) to escape corner
                    reverse_x = self.x - self.speed * 0.5 * dx
                    reverse_y = self.y - self.speed * 0.5 * dy
                    reverse_x = min(max(left + dragon_radius, reverse_x), right - dragon_radius)
                    reverse_y = min(max(top + dragon_radius, reverse_y), bottom - dragon_radius)
                    
                    reverse_collision = False
                    for wall in walls:
                        if wall.check_collision(reverse_x, reverse_y, dragon_radius):
                            reverse_collision = True
                            break
                    
                    if not reverse_collision:
                        self.x = reverse_x
                        self.y = reverse_y
            else:
                # No collision, move normally
                self.x = new_x
                self.y = new_y
        else:
            # No walls, move normally
            self.x = new_x
            self.y = new_y

    def check_collision(self, player_x, player_y, player_size):
        """Check if the dragon is touching the player."""
        distance = math.sqrt((player_x - self.x) ** 2 + (player_y - self.y) ** 2)
        return distance < (self.size / 2 + player_size / 2)