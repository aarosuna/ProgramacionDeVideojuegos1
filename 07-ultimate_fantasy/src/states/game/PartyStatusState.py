from gale.ui import Container
from gale.state import BaseState
from src.gui.CharacterStatusPanel import CharacterStatusPanel
from src.gui.Menu import Menu
import settings

class PartyStatusState(BaseState):
    def __init__(self, state_machine, party):
        super().__init__(state_machine)   
        self.characters = list(party.characters.values())
        self.current_index = 0
        # Keep track of who is casting the spell.
        self.actor_index = 0 
        # Modes: "browse" or "target"
        self.mode = "browse" 

        self.current_action = None
        self._create_ui()

    def _create_ui(self):
        character = self.characters[self.current_index]
        multiple_chars = len(self.characters) > 1

        stats_width = 210
        actions_width = 110
        panel_height = 135
        spacing = 5
        
        total_width = stats_width + spacing + actions_width
        pos_x = (settings.VIRTUAL_WIDTH - total_width) // 2
        pos_y = (settings.VIRTUAL_HEIGHT - panel_height) // 2

        # Visual indicator for target mode
        title = None
        if self.mode == "target":
            title = f"< TARGET: {character.name} >" if multiple_chars else f"TARGET: {character.name}"

        # Left panel
        self.stats_panel = CharacterStatusPanel(
            pos_x, pos_y, stats_width, panel_height, character, multiple_chars, title_override=title
        )
        self.ui = Container(0, 0, settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT, children=[self.stats_panel])
        
        # Right Panel (Real and interactive menu)
        if self.mode == "browse":
            items = []
            if hasattr(character, 'actions'):
                for action in character.actions:
                    action_name = action.get("name", "").lower()
                    is_heal = "heal" in action_name or action.get("target_type") == "party"
                    
                    alpha_value = 255 if is_heal else 80
                    
                    # Associate the function only if it is curative.
                    if is_heal:
                        func = lambda a=action: self._on_action_select(a)
                    else:
                        func = lambda: None
                        
                    items.append((action["name"], func, alpha_value))
            
            items.append(("Close", self._close, 255))
            
            self.menu = Menu(
                pos_x + stats_width + spacing, pos_y, actions_width, panel_height, items=items
            )

    def _close(self):
        self.state_machine.pop()

    def _on_action_select(self, action):
        self.actor_index = self.current_index

        # If a target is required, change mode.
        if action.get("require_target"):
            self.mode = "target"
            self.current_action = action
            # Hides the menu cursor
            self.menu.cursor = None
            # Refrescamos para mostrar la etiqueta "TARGET"
            self._create_ui()

        # If it involves a comprehensive treatment, it is applied immediately.
        else:
            actor = self.characters[self.actor_index]
            alive_targets = [c for c in self.characters if not c.dead]
            
            if "func" in action:
                action["func"](actor, alive_targets, action.get("strength"))
                sound = action.get("sound_effect")
                if sound and sound in settings.SOUNDS:
                    settings.SOUNDS[sound].play()
            
            self._close()

    def render(self, surface):
        self.ui.render(surface)
        if self.menu:
            self.menu.render(surface)

    def on_input(self, input_id, input_data):
        if not input_data.pressed:
            return

        # ---- NORMAL NAVIGATION MODE ----
        if self.mode == "browse":
            # P para salir
            if input_id in ("pause"):
                self._close()
            elif input_id == "move_left":
                if len(self.characters) > 1:
                    settings.SOUNDS["blip"].play()
                    self.current_index = (self.current_index - 1) % len(self.characters)
                    self._create_ui()
            elif input_id == "move_right":
                if len(self.characters) > 1:
                    settings.SOUNDS["blip"].play()
                    self.current_index = (self.current_index + 1) % len(self.characters)
                    self._create_ui()
            elif input_id == "move_up":
                self.menu.navigate((0, -1))
            elif input_id == "move_down":
                self.menu.navigate((0, 1))
            elif input_id in ("enter", "space"):
                self.menu.confirm()
                
        # ---- TARGET SELECTION MODE ----
        elif self.mode == "target":
            # Cancel selection
            if input_id in ("pause"):
                self.mode = "browse"
                self.current_index = self.actor_index
                self._create_ui()
            elif input_id == "move_left":
                if len(self.characters) > 1:
                    settings.SOUNDS["blip"].play()
                    self.current_index = (self.current_index - 1) % len(self.characters)
                    self._create_ui()
            elif input_id == "move_right":
                if len(self.characters) > 1:
                    settings.SOUNDS["blip"].play()
                    self.current_index = (self.current_index + 1) % len(self.characters)
                    self._create_ui()

             # Confirm heal
            elif input_id in ("enter", "space"):
                target = self.characters[self.current_index]
                actor = self.characters[self.actor_index]
                action = self.current_action
                
                if not target.dead:
                    if "func" in action:
                        action["func"](actor, target, action.get("strength"))
                        sound = action.get("sound_effect")
                        if sound and sound in settings.SOUNDS:
                            settings.SOUNDS[sound].play()
                            
                    # Return to browse mode, centered on the spellcaster.
                    self.mode = "browse"
                    self.current_index = self.actor_index
                    self._create_ui()
                else:
                    settings.SOUNDS["blip"].play()