from gale.ui import Container, Panel, Label, ProgressBar
from src.gui.theme import BAR_THEME 
import settings

class CharacterStatusPanel(Container):
    def __init__(self, x, y, width, height, character, multiple_chars=False, title_override=None):

        name_text = f"<  {character.name}  >" if multiple_chars else character.name
        children = []

        # --- LEFT PANEL (Statistics) ---
        children.append(Panel(0, 0, width, height))


        if title_override:
            name_text = title_override

        else:
            # Determine whether it is alive or dead.
            status = "Dead" if character.dead else "Alive"
            name_text = f"Name: {character.name} - {status}" if multiple_chars else f"{character.name} - {status}"
        
        # Inherited attributes
        children.append(Label(15, 15, text=name_text, font=settings.FONTS["medium"]))
        children.append(Label(15, 40, text=f"Lv: {character.level}"))
        children.append(Label(110, 40, text=f"Mg: {character.magic}"))
        children.append(Label(15, 60, text=f"Atk: {character.attack}"))
        children.append(Label(110, 60, text=f"Def: {character.defense}"))

        # Health Points (HP)
        children.append(Label(15, 85, text="HP:"))
        children.append(ProgressBar(
            45, 85, 150, 10, 
            character.current_hp, 
            character.hp, 
            theme=BAR_THEME
        ))

        # Experience Bar (EXP)
        children.append(Label(15, 105, text="XP:"))
        children.append(ProgressBar(
            45, 105, 150, 10, 
            character.current_exp, 
            character.exp_to_level, 
            theme=BAR_THEME
        ))
        super().__init__(x, y, width, height, children=children)