import raylib as rl
import random
import math
from battle_pals.constants import (
    COLOR_BG_DARK, COLOR_BG_PANEL, COLOR_BORDER, 
    COLOR_TEXT_PRIMARY, COLOR_TEXT_MUTED,
    COLOR_HP_GREEN, COLOR_HP_YELLOW, COLOR_HP_RED, COLOR_HP_BG,
    COLOR_TYPE_FIRE, COLOR_TYPE_WATER, COLOR_TYPE_GRASS, COLOR_TYPE_NORMAL,
    COLOR_TYPE_ELECTRIC, COLOR_TYPE_ICE, COLOR_TYPE_EARTH, COLOR_TYPE_WIND,
    COLOR_TYPE_TOXIC, COLOR_TYPE_MIND, COLOR_TYPE_METAL, COLOR_TYPE_LIGHT,
    COLOR_TYPE_SHADOW
)
from battle_pals.views.game_over_view import GameOverView
from battle_pals.models.state import GameState, PRECINCTS
from ai4animation import AI4Animation, Vector3

# Battle States
STATE_INTRO = 0
STATE_MOVE_SELECT = 1
STATE_COMBAT_LOGS = 2
STATE_CATCH_PHASE = 3
STATE_CATCH_LOGS = 4

class MoveButton:
    def __init__(self, move, lx, ty, w, h):
        self.move = move
        self.lx = lx
        self.ty = ty
        self.w = w
        self.h = h
        self.hovered = False

    def check_mouse(self, mx, my):
        self.hovered = (self.lx <= mx <= self.lx + self.w) and (self.ty <= my <= self.ty + self.h)
        return self.hovered

    def draw(self, sw, sh):
        type_colors = {
            "Normal": COLOR_TYPE_NORMAL,
            "Fire": COLOR_TYPE_FIRE,
            "Water": COLOR_TYPE_WATER,
            "Grass": COLOR_TYPE_GRASS,
            "Electric": COLOR_TYPE_ELECTRIC,
            "Ice": COLOR_TYPE_ICE,
            "Earth": COLOR_TYPE_EARTH,
            "Wind": COLOR_TYPE_WIND,
            "Toxic": COLOR_TYPE_TOXIC,
            "Mind": COLOR_TYPE_MIND,
            "Metal": COLOR_TYPE_METAL,
            "Light": COLOR_TYPE_LIGHT,
            "Shadow": COLOR_TYPE_SHADOW
        }
        accent_color = type_colors.get(self.move.type, COLOR_BORDER)
        
        bg_color = COLOR_BG_PANEL if not self.hovered else (45, 52, 68, 255)
        border_color = accent_color if self.hovered else COLOR_BORDER
        border_thickness = 4 if self.hovered else 2

        rl.DrawRectangle(int(self.lx), int(self.ty), int(self.w), int(self.h), bg_color)
        rl.DrawRectangleLinesEx([self.lx, self.ty, self.w, self.h], border_thickness, border_color)

        cx_norm = (self.lx + self.w / 2) / sw
        cy_norm = (self.ty + self.h / 2 - 10) / sh
        
        AI4Animation.Draw.Text(
            self.move.name,
            cx_norm, cy_norm,
            0.02, COLOR_TEXT_PRIMARY, 0.5
        )

class BattleView:
    def __init__(self, player_party, opponent_data, mode="WILD"):
        self.state_mgr = GameState.get_instance()
        self.mode = mode  # "WILD" or "BOSS"
        
        # 1. Player setup: Load active party list
        self.player_party = player_party
        self.player_idx = 0
        while self.player_idx < len(self.player_party) and self.player_party[self.player_idx].hp <= 0:
            self.player_idx += 1
            
        self.player = self.player_party[self.player_idx]
        self.player.is_player = True
        self.player.reset_battle_stats()

        # 2. Opponent setup: Load opponent list
        if isinstance(opponent_data, list):
            self.opponent_list = opponent_data
        else:
            self.opponent_list = [opponent_data]
            
        self.opponent_idx = 0
        self.opponent = self.opponent_list[self.opponent_idx]
        self.opponent.is_player = False
        self.opponent.reset_battle_stats()

        self.state = STATE_INTRO
        self.log_queue = []
        self.current_log = ""
        self.move_buttons = []
        self.turn_order = []  
        self.blink_timer = 0.0
        self.show_arrow = True
        self.game_ending = False

        self.rebuild_move_buttons()

    def rebuild_move_buttons(self):
        self.move_buttons = []
        sw = rl.GetScreenWidth()
        sh = rl.GetScreenHeight()
        
        btn_w = sw * 0.12 
        btn_h = sh * 0.055 
        spacing_x = sw * 0.015
        spacing_y = sh * 0.015
        
        start_x = sw * 0.08
        start_y = sh * 0.81
        
        for idx, move in enumerate(self.player.moves):
            row = idx // 2
            col = idx % 2
            bx = start_x + col * (btn_w + spacing_x)
            by = start_y + row * (btn_h + spacing_y)
            self.move_buttons.append(MoveButton(move, bx, by, btn_w, btn_h))

    def on_show_view(self):
        # Intro Log setup
        if self.mode == "BOSS":
            bureaucrat = PRECINCTS[self.state_mgr.current_precinct]["bureaucrat"]
            self.log_queue = [
                f"{bureaucrat} challenged you to a battle!",
                f"{bureaucrat} sent out {self.opponent.name}!",
                f"Go! {self.player.name}!"
            ]
        else:
            self.log_queue = [
                f"A wild {self.opponent.name} appeared (Lv{self.opponent.level})!",
                f"Go! {self.player.name}!"
            ]
        self.advance_log()

    def advance_log(self):
        """Advances to the next message in the log, checking for end-of-battle conditions."""
        if self.log_queue:
            self.state = STATE_COMBAT_LOGS
            self.current_log = self.log_queue.pop(0)
        else:
            # Check for faint conditions
            if self.player.hp <= 0 or self.opponent.hp <= 0:
                self.turn_order = []  
                
                # Active player Pal fainted
                if self.player.hp <= 0 and not self.player.is_fainted:
                    self.player.faint_timer = 0.01
                    self.log_queue.append(f"{self.player.name} fainted!")
                    self.advance_log()
                    
                # Active opponent Pal fainted
                elif self.opponent.hp <= 0 and not self.opponent.is_fainted:
                    self.opponent.faint_timer = 0.01
                    self.log_queue.append(f"The opponent's {self.opponent.name} fainted!")
                    self.advance_log()
                    
                else:
                    # Resolve replacement or battle end
                    if self.player.hp <= 0:
                        # Check for next player Pal
                        next_idx = self.player_idx + 1
                        while next_idx < len(self.player_party) and self.player_party[next_idx].hp <= 0:
                            next_idx += 1
                            
                        if next_idx < len(self.player_party):
                            self.player_idx = next_idx
                            self.player = self.player_party[self.player_idx]
                            self.player.is_player = True
                            self.player.reset_battle_stats()
                            self.rebuild_move_buttons()
                            self.log_queue.append(f"Go! {self.player.name}!")
                            self.advance_log()
                        else:
                            # Defeat
                            self.game_ending = True
                            from battle_pals.game import BattlePalsGame
                            BattlePalsGame.get_instance().switch_to_view(
                                GameOverView(victory=False, player_pal=self.player, opponent_pal=self.opponent)
                            )
                            
                    elif self.opponent.hp <= 0:
                        # Add to paldex
                        self.state_mgr.add_to_paldex(self.opponent.name, "defeated")
                        
                        # Check for next opponent Pal (Boss mode)
                        next_idx = self.opponent_idx + 1
                        if next_idx < len(self.opponent_list):
                            self.opponent_idx = next_idx
                            self.opponent = self.opponent_list[self.opponent_idx]
                            self.opponent.is_player = False
                            self.opponent.reset_battle_stats()
                            
                            bureaucrat = PRECINCTS[self.state_mgr.current_precinct]["bureaucrat"] if self.mode == "BOSS" else "Opponent"
                            self.log_queue.append(f"{bureaucrat} sent out {self.opponent.name}!")
                            self.advance_log()
                        else:
                            # Victory - Award EXP & RP
                            self.game_ending = True
                            
                            # Calculate total EXP award
                            tot_level = sum(opp.level for opp in self.opponent_list)
                            exp_gained = max(10, tot_level * 15)
                            rp_gained = max(20, tot_level * 10)
                            
                            self.state_mgr.gain_research_points(rp_gained)
                            self.log_queue.append(f"Victory! Gained {rp_gained} Research Points (RP)!")
                            
                            # Award to current active Pal
                            self.log_queue.append(f"{self.player.name} gained {exp_gained} EXP!")
                            level_logs = self.player.gain_experience(exp_gained)
                            self.log_queue.extend(level_logs)
                            
                            if self.mode == "WILD":
                                # Catch Phase
                                self.state = STATE_CATCH_PHASE
                            else:
                                # Boss Beat - Update state gates
                                self.state_mgr.defeated_bureaucrats.append(self.state_mgr.current_precinct)
                                next_precinct_idx = self.state_mgr.current_precinct + 1
                                if next_precinct_idx < 9 and next_precinct_idx not in self.state_mgr.unlocked_precincts:
                                    self.state_mgr.unlocked_precincts.append(next_precinct_idx)
                                
                                from battle_pals.game import BattlePalsGame
                                BattlePalsGame.get_instance().switch_to_view(
                                    GameOverView(victory=True, player_pal=self.player, opponent_pal=self.opponent)
                                )
                                
            elif self.turn_order:
                # Process the second attacker's turn
                attacker, move, defender = self.turn_order.pop(0)
                if attacker.hp > 0:
                    logs = attacker.use_move(move, defender)
                    self.log_queue.extend(logs)
                    self.advance_log()
                else:
                    self.advance_log()
            else:
                # Return to move selection
                self.state = STATE_MOVE_SELECT
                self.current_log = ""

    def execute_turn(self, player_move):
        """Computes combat turns using Speeds to determine priority."""
        self.log_queue = []
        opponent_move = random.choice(self.opponent.moves)

        player_first = self.player.speed >= self.opponent.speed
        
        if player_first:
            self.turn_order = [
                (self.player, player_move, self.opponent),
                (self.opponent, opponent_move, self.player)
            ]
        else:
            self.turn_order = [
                (self.opponent, opponent_move, self.player),
                (self.player, player_move, self.opponent)
            ]

        # Execute the first attacker's turn
        attacker, move, defender = self.turn_order.pop(0)
        logs = attacker.use_move(move, defender)
        self.log_queue.extend(logs)
        self.advance_log()

    def on_update(self, dt):
        self.blink_timer += dt
        if self.blink_timer >= 0.5:
            self.blink_timer = 0.0
            self.show_arrow = not self.show_arrow

        # Update animations
        self.player.update_animation(dt)
        self.opponent.update_animation(dt)

        mouse_pos = rl.GetMousePosition()
        mx, my = mouse_pos.x, mouse_pos.y

        if self.state == STATE_MOVE_SELECT:
            for btn in self.move_buttons:
                btn.check_mouse(mx, my)

        # Handle clicks
        if rl.IsMouseButtonPressed(rl.MOUSE_BUTTON_LEFT):
            if self.state == STATE_COMBAT_LOGS or self.state == STATE_INTRO:
                self.advance_log()
            elif self.state == STATE_CATCH_LOGS:
                # Transition to Game Over (Victory) after catching screen
                from battle_pals.game import BattlePalsGame
                BattlePalsGame.get_instance().switch_to_view(
                    GameOverView(victory=True, player_pal=self.player, opponent_pal=self.opponent)
                )
            elif self.state == STATE_MOVE_SELECT:
                for btn in self.move_buttons:
                    if btn.hovered:
                        self.execute_turn(btn.move)
                        break
            elif self.state == STATE_CATCH_PHASE:
                # Button positions inside dialogue panel
                sw = rl.GetScreenWidth()
                sh = rl.GetScreenHeight()
                panel_w = sw * 0.90
                panel_h = sh * 0.22
                panel_x = (sw - panel_w) / 2
                panel_y = sh * 0.74
                
                cw = 180
                ch = 45
                by = panel_y + panel_h * 0.45
                start_bx = panel_x + 80
                
                # Check Basic Cube button (x = start_bx)
                if check_rect_collision(mx, my, start_bx, by, cw, ch):
                    self.throw_capture_cube("Basic Cube", 1.0)
                # Check Mega Cube button (x = start_bx + 220)
                elif check_rect_collision(mx, my, start_bx + 220, by, cw, ch):
                    self.throw_capture_cube("Mega Cube", 1.8)
                # Check Ultra Cube button (x = start_bx + 440)
                elif check_rect_collision(mx, my, start_bx + 440, by, cw, ch):
                    self.throw_capture_cube("Ultra Cube", 2.8)
                # Check Flee button (x = start_bx + 660)
                elif check_rect_collision(mx, my, start_bx + 660, by, cw, ch):
                    self.log_queue.append(f"You left the wild {self.opponent.name} behind.")
                    self.state = STATE_CATCH_LOGS
                    self.advance_log()

    def throw_capture_cube(self, cube_name, multiplier):
        if self.state_mgr.inventory[cube_name] <= 0:
            return
            
        self.state_mgr.inventory[cube_name] -= 1
        
        # Calculate capture rate (wild Pal is fainted, giving high capture rate)
        base_rate = 0.50
        catch_chance = base_rate * multiplier
        
        self.log_queue = [f"Threw a {cube_name}! (Inventory: {self.state_mgr.inventory[cube_name]})"]
        
        roll = random.random()
        if roll <= catch_chance:
            self.log_queue.append("One... Two... Three... Click!")
            # Add to party or box
            added_loc = self.state_mgr.add_pal_to_party_or_box(self.opponent)
            self.state_mgr.add_to_paldex(self.opponent.name, "captured")
            self.log_queue.append(f"Captured wild {self.opponent.name}! Transferred to {added_loc}!")
        else:
            self.log_queue.append("Oh no! The wild Pal broke free and fled!")
            
        self.state = STATE_CATCH_LOGS
        self.advance_log()

    def draw_pal_3d(self, pal):
        if pal.is_fainted:
            return
        scale = 1.0
        if pal.faint_timer > 0.0:
            scale = max(0.01, 1.0 - pal.faint_timer)
        facing = 1.0 if pal.is_player else -1.0
        pal.draw_3d(facing, scale)

    def on_draw(self):
        # Draw platform ground
        rl.DrawPlane([0.0, 0.0, 0.0], [30.0, 30.0], (25, 30, 42, 255))
        
        # Player platform
        rl.DrawPlane([-4.0, 0.02, -2.0], [4.5, 4.5], (45, 55, 75, 255))
        
        # Opponent platform
        rl.DrawPlane([4.0, 0.02, 2.0], [4.5, 4.5], (45, 55, 75, 255))

        # Render Pals
        self.draw_pal_3d(self.player)
        self.draw_pal_3d(self.opponent)

    def on_gui(self):
        sw = rl.GetScreenWidth()
        sh = rl.GetScreenHeight()

        # Opponent HUD (Top Left)
        opp_hud_txt = f"{self.opponent.name} (Lv{self.opponent.level})"
        if self.mode == "BOSS":
            opp_hud_txt += f" [{self.opponent_idx+1}/{len(self.opponent_list)}]"
        self.draw_hud_box(sw * 0.06, sh * 0.08, sw * 0.28, sh * 0.12, self.opponent, header_override=opp_hud_txt)
        
        # Player HUD (Bottom Right)
        player_hud_txt = f"{self.player.name} (Lv{self.player.level}) [{self.player_idx+1}/{len(self.player_party)}]"
        self.draw_hud_box(sw * 0.66, sh * 0.60, sw * 0.28, sh * 0.12, self.player, header_override=player_hud_txt, show_numbers=True)

        # Draw Dialogue Console Box (Bottom Panel)
        panel_w = sw * 0.90
        panel_h = sh * 0.22
        panel_x = (sw - panel_w) / 2
        panel_y = sh * 0.74
        
        rl.DrawRectangle(int(panel_x), int(panel_y), int(panel_w), int(panel_h), COLOR_BG_PANEL)
        rl.DrawRectangleLinesEx([panel_x, panel_y, panel_w, panel_h], 3, COLOR_BORDER)

        if self.state in [STATE_COMBAT_LOGS, STATE_INTRO, STATE_CATCH_LOGS]:
            # Draw Dialogue Text
            AI4Animation.Draw.Text(
                self.current_log,
                (panel_x + sw * 0.03) / sw,
                (panel_y + sh * 0.04) / sh,
                0.026, COLOR_TEXT_PRIMARY, 0.0
            )
            # Arrow indicator
            if self.show_arrow:
                AI4Animation.Draw.Text(
                    "▼",
                    (panel_x + panel_w - sw * 0.03) / sw,
                    (panel_y + panel_h - sh * 0.05) / sh,
                    0.025, COLOR_TEXT_PRIMARY, 0.5
                )
                
        elif self.state == STATE_MOVE_SELECT:
            # Draw Move Buttons
            for btn in self.move_buttons:
                btn.draw(sw, sh)
                
            # Draw Hover Info Panel on the right side of the bottom panel
            hovered_btn = next((b for b in self.move_buttons if b.hovered), None)
            if hovered_btn:
                move = hovered_btn.move
                
                # Vertical Divider Line
                divider_x = panel_x + panel_w * 0.4
                rl.DrawLineEx([divider_x, panel_y + 15], [divider_x, panel_y + panel_h - 15], 2, COLOR_BORDER)
                
                details_x = (divider_x + sw * 0.02) / sw
                
                AI4Animation.Draw.Text(
                    f"Type: {move.type}",
                    details_x, (panel_y + sh * 0.03) / sh,
                    0.022, COLOR_TEXT_PRIMARY, 0.0
                )
                AI4Animation.Draw.Text(
                    f"Power: {move.power if move.power > 0 else '-'}",
                    details_x, (panel_y + sh * 0.07) / sh,
                    0.016, COLOR_TEXT_MUTED, 0.0
                )
                AI4Animation.Draw.Text(
                    move.description,
                    details_x, (panel_y + sh * 0.12) / sh,
                    0.016, COLOR_TEXT_PRIMARY, 0.0
                )

        elif self.state == STATE_CATCH_PHASE:
            # Render Cube Capture Buttons
            AI4Animation.Draw.Text(
                "Wild Pal defeated! Throw a Capture Cube?",
                (panel_x + sw * 0.03) / sw,
                (panel_y + sh * 0.02) / sh,
                0.018, COLOR_TEXT_MUTED, 0.0
            )
            
            cw = 180
            ch = 45
            by = panel_y + panel_h * 0.45
            start_bx = panel_x + 80
            
            # Check Cube mouse positions for button hover styling
            mx, my = rl.GetMousePosition().x, rl.GetMousePosition().y
            
            cubes = [
                ("Basic Cube", start_bx, COLOR_TYPE_GRASS),
                ("Mega Cube", start_bx + 220, COLOR_TYPE_WATER),
                ("Ultra Cube", start_bx + 440, COLOR_TYPE_FIRE),
                ("Leave Pal", start_bx + 660, COLOR_BORDER)
            ]
            
            for c_name, bx, color in cubes:
                is_hover = check_rect_collision(mx, my, bx, by, cw, ch)
                
                qty = ""
                enabled = True
                if c_name != "Leave Pal":
                    count = self.state_mgr.inventory[c_name]
                    qty = f" (x{count})"
                    if count <= 0:
                        enabled = False
                        
                bg_col = (45, 55, 75, 255) if is_hover and enabled else COLOR_BG_DARK
                border_col = color if is_hover and enabled else COLOR_BORDER
                text_col = COLOR_TEXT_PRIMARY if enabled else COLOR_TEXT_MUTED
                
                rl.DrawRectangle(int(bx), int(by), cw, ch, bg_col)
                rl.DrawRectangleLinesEx([bx, by, cw, ch], 2 if is_hover and enabled else 1, border_col)
                AI4Animation.Draw.Text(f"{c_name}{qty}", (bx + cw // 2) / sw, (by + 14) / sh, 0.016, text_col, 0.5)

    def draw_hud_box(self, lx, ty, w, h, pal, header_override=None, show_numbers=False):
        # Draw background and border
        rl.DrawRectangle(int(lx), int(ty), int(w), int(h), COLOR_BG_PANEL)
        rl.DrawRectangleLinesEx([lx, ty, w, h], 2, COLOR_BORDER)

        sw = rl.GetScreenWidth()
        sh = rl.GetScreenHeight()

        # Header Text (Name and level info)
        title_txt = header_override if header_override else f"{pal.name} (Lv{pal.level})"
        AI4Animation.Draw.Text(
            title_txt,
            (lx + w * 0.05) / sw,
            (ty + h * 0.15) / sh,
            0.022, COLOR_TEXT_PRIMARY, 0.0
        )

        # HP Bar geometry
        bar_w = w * 0.90
        bar_h = h * 0.15
        bar_x = lx + w * 0.05
        bar_y = ty + h * 0.50

        # Background
        rl.DrawRectangle(int(bar_x), int(bar_y), int(bar_w), int(bar_h), COLOR_HP_BG)
        
        # Calculate HP Fill
        hp_percent = max(0.0, pal.hp / pal.max_hp)
        if hp_percent > 0.5:
            hp_color = COLOR_HP_GREEN
        elif hp_percent > 0.2:
            hp_color = COLOR_HP_YELLOW
        else:
            hp_color = COLOR_HP_RED

        if hp_percent > 0:
            fill_w = bar_w * hp_percent
            rl.DrawRectangle(int(bar_x), int(bar_y), int(fill_w), int(bar_h), hp_color)

        # Health Numbers
        if show_numbers:
            AI4Animation.Draw.Text(
                f"{pal.hp} / {pal.max_hp}",
                (lx + w * 0.95) / sw,
                (ty + h * 0.72) / sh,
                0.015, COLOR_TEXT_PRIMARY, 1.0
            )
