from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import *
from kivy.properties import NumericProperty, StringProperty
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.audio import SoundLoader


class MainWidget(Widget):

    ball_center_x = NumericProperty(0)
    ball_center_y = NumericProperty(0)

    bat_center_x = NumericProperty(0)
    bat_center_y = NumericProperty(0)

    bat_x = NumericProperty(0)

    SPEED_X = dp(3)
    SPEED_Y = dp(3)

    radius = dp(30)

    bat_speed = dp(10)

    game_started = False
    game_end = False

    score = NumericProperty(0)
    highscore = NumericProperty(0)

    game_button = StringProperty("START GAME")

    inc_speed_cond = True

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.ball_center()
        self.bat_center()
        self.menu_control_line()
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_down=self._on_keyboard_up)
        Clock.schedule_interval(self.move_ball, 1/60)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        x,y = self.bat.pos 
        if not self.game_end:       
            if keycode[1] == 'left':
                if x > 150:
                    x -= self.bat_speed
                self.bat.pos = (x, y)
            elif keycode[1] == 'right':
                if x < self.bat_x - 80:
                    x += self.bat_speed
                self.bat.pos = (x, y)
        return True

    def _on_keyboard_up(self, keyboard, keycode, text, modifiers):
        pass    
    
    def ball_center(self):
        with self.canvas:
            Color(1, 0, 0)
            self.ball = Ellipse(size=(self.radius, self.radius)) 

    def on_size(self, *args):
        self.ball_center_x = self.width/2
        self.ball_center_y = self.height*0.75
        cx = self.ball_center_x - (self.radius/2)
        cy = self.ball_center_y - (self.radius/2)
        self.ball.pos = (cx, cy)
        self.bat.pos = ((self.width/2) - 40, 0)
        self.menu_line.points = [150, 0, 150,self.height]
        self.bat_x = self.width
        self.ids.lbl.pos = self.width/2, self.height/2
        self.ids.lblscore.pos = 50, self.height - 40
        self.ids.lblHscore.pos = 50, self.height - 80
        self.ids.lblgover.pos = (self.width/2, (self.height/2) - 50)
        self.ids.btnrestartgame.pos = (20, self.height/2)
    


    def move_ball(self, dt):
        x,y = self.ball.pos 
        bat_x, bat_y = self.bat.pos        
        if x + self.radius > self.width and self.SPEED_X>0:
            x = self.width - self.radius
            self.SPEED_X = -self.SPEED_X
        if x < 155 and self.SPEED_X < 0:
            x = 155
            self.SPEED_X = -self.SPEED_X
        if y + self.radius > self.height and self.SPEED_Y > 0:
            y = self.height - self.radius
            self.SPEED_Y = -self.SPEED_Y
        if (y < 20 and self.SPEED_Y < 0) and (bat_x-30 <= x <= bat_x+80):
            y = 20
            self.SPEED_Y = -self.SPEED_Y 
            self.score += 1
        elif (y<0) and ((x>bat_x+80) or (x<bat_x-30)):
            y = 0
            self.game_over_state()
        if self.game_started and not self.game_end:                  
            x += self.SPEED_X
            y += self.SPEED_Y
        self.ball.pos = (x, y)     

    def bat_center(self):
        with self.canvas:
            Color(0, 1, 0)
            self.bat = Rectangle(size=(80, 20))

    def menu_control_line(self):
        with self.canvas:
            Color(1, 0.3, 0.4)
            self.menu_line = Line(width = 2)   

    def start_game(self):
        self.game_started = True
        self.ids.btn.opacity = 0

    def game_over_state(self):
        self.game_end = True
        self.game_started = False
        self.ids.lbl.opacity = 1  
        self.ids.lblgover.text = "SCORE: "+str(self.score)
        self.ids.lblgover.opacity = 1
        self.ids.btnrestartgame.opacity = 1 
        SoundLoader.load("audio/gameover_voice.wav").play()

    def game_reset(self):
        self.game_end = False
        self.ids.lblgover.opacity = 0
        if self.score > self.highscore:
            self.highscore = self.score    
        self.score = 0 
        self.ids.lbl.opacity = 0
        self.ids.btnrestartgame.opacity = 0
        self.ball.pos = (self.ball_center_x, self.ball_center_y)
        self.bat.pos = ((self.width/2) - 40, 0)
        self.SPEED_X = dp(3)
        self.SPEED_Y = dp(3)
        self.game_started = True

    def inc_speed(self):
        self.SPEED_X += 1
        self.SPEED_Y += 1 
        self.inc_speed_cond = False  

    def bg_sound(self):
        song = SoundLoader.load("audio/begin.wav")
        if self.game_started:
            song.play()     


class ModelApp(App):
    def build(self):
        return MainWidget()


ModelApp().run()