# Import statements at the very top
from kivy.config import Config
# Force portrait BEFORE creating the window
Config.set('graphics', 'orientation', 'portrait')
Config.set('graphics', 'width', '540')  # Standard phone width
Config.set('graphics', 'height', '960')  # Standard phone height
Config.write()

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.properties import StringProperty
from kivy.clock import Clock
from datetime import datetime, timedelta
from kivy.utils import platform

# Force rotation to portrait mode
Window.size = (540, 960)
Window.rotation = 0
Window.orientation = 'portrait'

if platform == 'android':
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.INTERNET])
    Window.softinput_mode = 'below_target'
    
    # Additional Android-specific orientation settings
    from jnius import autoclass
    activity = autoclass('org.kivy.android.PythonActivity').mActivity
    activity.setRequestedOrientation(1)  # 1 = SCREEN_ORIENTATION_PORTRAIT
    
# Definición del diseño en KV Language
KV = '''
#:import utils kivy.utils

<ScrollableLabel>:
    Label:
        size_hint_y: None
        height: self.texture_size[1]
        text_size: self.width, None
        text: root.text
        color: utils.get_color_from_hex('#333333')
        padding: 10, 10

<TurnosScreen>:
    orientation: 'vertical'
    padding: '10dp'
    spacing: '10dp'
    canvas.before:
        Color:
            rgba: utils.get_color_from_hex('#f0f0f0')
        Rectangle:
            pos: self.pos
            size: self.size
    
    Label:
        text: 'Sorteo de Turnos UCI-S.Lucía'
        size_hint_y: None
        height: '60dp'
        color: utils.get_color_from_hex('#333333')
        bold: True
        font_size: '20sp'
    
    BoxLayout:
        size_hint_y: None
        height: '60dp'
        spacing: '5dp'
        padding: '5dp'
        
        TextInput:
            id: worker_input
            hint_text: 'Nombre del médico'
            multiline: False
            size_hint_x: 0.7
            font_size: '16sp'
            padding: '10dp'
            
        Button:
            text: 'Añadir'
            size_hint_x: 0.3
            background_normal: ''
            background_color: utils.get_color_from_hex('#2196F3')
            on_release: root.add_worker()
    
    Label:
        text: 'Médicos añadidos:'
        size_hint_y: None
        height: '40dp'
        color: utils.get_color_from_hex('#333333')
        halign: 'left'
        text_size: self.size
        
    ScrollView:
        size_hint_y: 0.25
        
        Label:
            id: workers_list
            size_hint_y: None
            height: self.texture_size[1]
            text_size: self.width, None
            padding: '10dp'
            color: utils.get_color_from_hex('#333333')
    
    BoxLayout:
        orientation: 'vertical'
        size_hint_y: None
        height: '160dp'
        spacing: '5dp'
        padding: '5dp'
        
        Label:
            text: 'Hora de inicio (HH:MM):'
            size_hint_y: None
            height: '40dp'
            color: utils.get_color_from_hex('#333333')
            halign: 'left'
            text_size: self.size
            
        TextInput:
            id: start_time
            multiline: False
            size_hint_y: None
            height: '40dp'
            padding: '10dp'
            
        Label:
            text: 'Hora de fin (HH:MM):'
            size_hint_y: None
            height: '40dp'
            color: utils.get_color_from_hex('#333333')
            halign: 'left'
            text_size: self.size
            
        TextInput:
            id: end_time
            multiline: False
            size_hint_y: None
            height: '40dp'
            padding: '10dp'
    
    Button:
        text: 'Generar Turnos'
        size_hint_y: None
        height: '60dp'
        background_normal: ''
        background_color: utils.get_color_from_hex('#4CAF50')
        on_release: root.generate_shifts()
    
    ScrollView:
        ScrollableLabel:
            id: results
'''

class ScrollableLabel(ScrollView):
    text = StringProperty('')

class TurnosScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.workers = []
        Clock.schedule_once(self.set_default_values, 0)

    def set_default_values(self, dt):
        now = datetime.now()
        self.ids.start_time.text = now.strftime("%H:%M")
        self.ids.end_time.text = "08:00"

    def add_worker(self):
        worker = self.ids.worker_input.text.strip()
        if worker:
            self.workers.append(worker)
            current_text = self.ids.workers_list.text
            self.ids.workers_list.text = (current_text + '\n' + worker).strip()
            self.ids.worker_input.text = ''

    def validate_time(self, time_str):
        try:
            return datetime.strptime(time_str, "%H:%M")
        except ValueError:
            return None

    def show_error(self, message):
        popup = Popup(title='Error',
                     content=Label(text=message),
                     size_hint=(0.8, 0.4))
        popup.open()

    def generate_shifts(self):
        if len(self.workers) < 2:
            self.show_error("Debe añadir al menos  a 2 médicos")
            return

        # Obtener y validar horas
        now = datetime.now()
        
        # Procesar hora de inicio
        start_time_str = self.ids.start_time.text.strip()
        if not start_time_str:
            start_time_dt = now.replace(microsecond=0, second=0, minute=now.minute)
        else:
            start_time_dt = self.validate_time(start_time_str)
            if not start_time_dt:
                self.show_error("Formato de hora de inicio inválido")
                return
            start_time_dt = start_time_dt.replace(
                year=now.year,
                month=now.month,
                day=now.day
            )

        # Procesar hora de fin
        end_time_str = self.ids.end_time.text.strip()
        if not end_time_str:
            end_time_dt = now.replace(hour=8, minute=0, second=0, microsecond=0)
            if start_time_dt >= end_time_dt:
                end_time_dt += timedelta(days=1)
        else:
            end_time_dt = self.validate_time(end_time_str)
            if not end_time_dt:
                self.show_error("Formato de hora de fin inválido")
                return
            end_time_dt = end_time_dt.replace(
                year=now.year,
                month=now.month,
                day=now.day
            )
            if end_time_dt <= start_time_dt:
                end_time_dt += timedelta(days=1)

        # Calcular turnos
        total_duration = (end_time_dt - start_time_dt).total_seconds() / 3600
        shift_duration = total_duration / len(self.workers)

        # Mezclar trabajadores
        shuffled_workers = self.workers.copy()
        random.shuffle(shuffled_workers)

        # Generar y mostrar turnos
        results = []
        current_time = start_time_dt
        
        for worker in shuffled_workers:
            shift_end = current_time + timedelta(hours=shift_duration)
            
            if current_time.date() == shift_end.date():
                shift_str = (f"Médico: {worker}\n"
                           f"Horario: {current_time.strftime('%H:%M')} - "
                           f"{shift_end.strftime('%H:%M')} "
                           f"({current_time.strftime('%d/%m/%Y')})\n")
            else:
                shift_str = (f"Médico: {worker}\n"
                           f"Horario: {current_time.strftime('%H:%M')} "
                           f"({current_time.strftime('%d/%m/%Y')}) - "
                           f"{shift_end.strftime('%H:%M')} "
                           f"({shift_end.strftime('%d/%m/%Y')})\n")
            
            results.append(shift_str + "-" * 40)
            current_time = shift_end
        
        self.ids.results.text = '\n'.join(results)

class TurnosApp(App):
    def build(self):
        # Cargar el diseño KV
        from kivy.lang import Builder
        Builder.load_string(KV)
        return TurnosScreen()

if __name__ == '__main__':
    TurnosApp().run()
