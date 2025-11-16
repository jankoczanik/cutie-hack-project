import pygame
import re
import os
from entity import Player, Exit, Wall, Key, Door, Dragon

class Level:

    def __init__(self, x, y, width, height, config):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.size = config['size']
        self.name = config['name']
        self.config = config  # Store config for reset
        
        # Load unlock sound effect
        self.unlock_sound = None
        unlock_sound_path = "assets/sounds/unlock.mp3"
        if os.path.exists(unlock_sound_path):
            try:
                self.unlock_sound = pygame.mixer.Sound(unlock_sound_path)
            except pygame.error as e:
                print(f"Error loading unlock sound: {e}")
        else:
            print(f"Unlock sound file not found: {unlock_sound_path}")
        
        # Load death sound effect
        self.death_sound = None
        death_sound_path = "assets/sounds/death.mp3"
        if os.path.exists(death_sound_path):
            try:
                self.death_sound = pygame.mixer.Sound(death_sound_path)
            except pygame.error as e:
                print(f"Error loading death sound: {e}")
        else:
            print(f"Death sound file not found: {death_sound_path}")
        
        # Play level sound
        self.play_level_sound()
        self.player = Player(x + width * config['spawn'][0], y + height * config['spawn'][1], self.size, self.size / 15)
        self.exit = Exit(x + width * config['exit'][0], y + height * config['exit'][1], self.size)
        
        # Create walls from config
        self.walls = []
        if 'walls' in config:
            for wall_data in config['walls']:
                # Walls are defined as [x1, y1, x2, y2] in relative coordinates (0-1)
                x1 = x + width * wall_data[0]
                y1 = y + height * wall_data[1]
                x2 = x + width * wall_data[2]
                y2 = y + height * wall_data[3]
                self.walls.append(Wall(x1, y1, x2, y2))
        
        # Create keys from config
        self.keys = []
        if 'keys' in config:
            for i, key_data in enumerate(config['keys']):
                # Keys are defined as [x, y] in relative coordinates (0-1)
                key_x = x + width * key_data[0]
                key_y = y + height * key_data[1]
                # Key IDs start at 1 (key #1, key #2, etc.)
                self.keys.append(Key(key_x, key_y, self.size * 1.5, key_id=i+1))
        
        # Create doors from config
        self.doors = []
        if 'doors' in config:
            for i, door_data in enumerate(config['doors']):
                # Doors are defined as [x1, y1, x2, y2] in relative coordinates (0-1)
                x1 = x + width * door_data[0]
                y1 = y + height * door_data[1]
                x2 = x + width * door_data[2]
                y2 = y + height * door_data[3]
                # Door IDs start at 1 (door #1, door #2, etc.)
                self.doors.append(Door(x1, y1, x2, y2, door_id=i+1))
        
        # Create dragons from config
        self.dragons = []
        if 'dragons' in config:
            for dragon_data in config['dragons']:
                # Dragons are defined as [x, y] in relative coordinates (0-1)
                dragon_x = x + width * dragon_data[0]
                dragon_y = y + height * dragon_data[1]
                # Dragon speed - faster than player
                dragon_speed = self.size / 12  # Faster than player (player is size/15)
                self.dragons.append(Dragon(dragon_x, dragon_y, self.size, dragon_speed))

    def draw(self, screen, font):
        temp_surface = pygame.Surface(
            (self.width, self.height), pygame.SRCALPHA
        )
        pygame.draw.rect(
            temp_surface,
            (255, 255, 255, 200),
            (0, 0, self.width, self.height)
        )
        screen.blit(temp_surface, (self.x, self.y))
        # Draw walls
        for wall in self.walls:
            wall.draw(screen)
        # Draw doors (only locked doors are drawn)
        for door in self.doors:
            if not door.unlocked:
                door.draw(screen)
        # Draw keys
        for key in self.keys:
            key.draw(screen)
        # Draw dragons
        for dragon in self.dragons:
            dragon.draw(screen)
        self.exit.draw(screen)
        self.player.draw(screen)
        text_surface = font.render(self.name, True, (255, 255, 255))
        screen.blit(text_surface, (10, 10))

    def play_level_sound(self):
        """Play the sound for the current level."""
        # Extract level number from name (e.g., "Level 1 - The Beginning" -> 1)
        level_match = re.search(r'Level\s+(\d+)', self.name)
        if level_match:
            level_num = level_match.group(1)
            sound_path = f"assets/sounds/Level {level_num}.wav"
            
            # Check if file exists
            if not os.path.exists(sound_path):
                print(f"Sound file not found: {sound_path}")
            else:
                try:
                    # Stop any currently playing music
                    pygame.mixer.music.stop()
                    # Load and play the WAV file
                    pygame.mixer.music.load(sound_path)
                    pygame.mixer.music.set_volume(0.7)  # Set volume (0.0 to 1.0)
                    pygame.mixer.music.play(0)  # 0 means play once
                except pygame.error as e:
                    print(f"Error loading sound file {sound_path}: {e}")
                except Exception as e:
                    print(f"Unexpected error loading sound file {sound_path}: {e}")
                    import traceback
                    traceback.print_exc()

    def reset(self):
        """Reset the level to its initial state."""
        # Replay the level sound
        self.play_level_sound()
        
        # Recreate all entities from config
        self.player = Player(self.x + self.width * self.config['spawn'][0], 
                            self.y + self.height * self.config['spawn'][1], 
                            self.size, self.size / 15)
        self.exit = Exit(self.x + self.width * self.config['exit'][0], 
                        self.y + self.height * self.config['exit'][1], 
                        self.size)
        
        # Recreate walls
        self.walls = []
        if 'walls' in self.config:
            for wall_data in self.config['walls']:
                x1 = self.x + self.width * wall_data[0]
                y1 = self.y + self.height * wall_data[1]
                x2 = self.x + self.width * wall_data[2]
                y2 = self.y + self.height * wall_data[3]
                self.walls.append(Wall(x1, y1, x2, y2))
        
        # Recreate keys
        self.keys = []
        if 'keys' in self.config:
            for i, key_data in enumerate(self.config['keys']):
                key_x = self.x + self.width * key_data[0]
                key_y = self.y + self.height * key_data[1]
                # Key IDs start at 1 (key #1, key #2, etc.)
                self.keys.append(Key(key_x, key_y, self.size * 1.5, key_id=i+1))
        
        # Recreate doors
        self.doors = []
        if 'doors' in self.config:
            for i, door_data in enumerate(self.config['doors']):
                x1 = self.x + self.width * door_data[0]
                y1 = self.y + self.height * door_data[1]
                x2 = self.x + self.width * door_data[2]
                y2 = self.y + self.height * door_data[3]
                # Door IDs start at 1 (door #1, door #2, etc.)
                self.doors.append(Door(x1, y1, x2, y2, door_id=i+1))
        
        # Recreate dragons
        self.dragons = []
        if 'dragons' in self.config:
            for dragon_data in self.config['dragons']:
                dragon_x = self.x + self.width * dragon_data[0]
                dragon_y = self.y + self.height * dragon_data[1]
                dragon_speed = self.size / 12  # Faster than player
                self.dragons.append(Dragon(dragon_x, dragon_y, self.size, dragon_speed))

    def tick(self):
        x, y = pygame.mouse.get_pos()
        player_radius = self.size / 2
        
        # Check for key collisions and collect keys
        for key in self.keys:
            if not key.collected and key.check_collision(self.player.x, self.player.y, self.player.size):
                key.collected = True
                # Play unlock sound
                if self.unlock_sound:
                    try:
                        self.unlock_sound.play()
                    except pygame.error as e:
                        print(f"Error playing unlock sound: {e}")
                # Unlock the door with matching ID (key #1 unlocks door #1, etc.)
                for door in self.doors:
                    if door.door_id == key.key_id:
                        door.unlocked = True
                        break
        
        # Combine walls and unlocked doors for collision detection (only locked doors block movement)
        all_walls = self.walls + [door for door in self.doors if not door.unlocked]
        
        self.player.moveTowards(x, y, self.x + player_radius, self.y + player_radius, 
                                self.x + self.width - player_radius, self.y + self.height - player_radius, all_walls)
        
        # Move dragons towards player
        for dragon in self.dragons:
            dragon.moveTowards(self.player.x, self.player.y, 
                              self.x + player_radius, self.y + player_radius,
                              self.x + self.width - player_radius, self.y + self.height - player_radius, 
                              all_walls)
            
            # Check if dragon touches player
            if dragon.check_collision(self.player.x, self.player.y, self.player.size):
                # Play death sound
                if self.death_sound:
                    try:
                        self.death_sound.play()
                    except pygame.error as e:
                        print(f"Error playing death sound: {e}")
                # Reset the level
                self.reset()
                return False  # Level not completed
        
        return self.player.touchingExit(self.exit)