import os
import re
import webbrowser
import tempfile
from datetime import datetime

import fitz  # PyMuPDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from kivy.uix.screenmanager import Screen, FadeTransition
from kivy.uix.image import Image as KivyImage
from kivy.animation import Animation
from kivy.clock import Clock

from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.textfield import MDTextField

# ─────────────────────────────────────────────
#  PALETA GLOBAL
# ─────────────────────────────────────────────
COLOR_BG        = (0.05, 0.05, 0.08, 1)
COLOR_SURFACE   = (0.10, 0.10, 0.14, 1)
COLOR_CARD      = (0.13, 0.13, 0.18, 1)
COLOR_ACCENT    = (0.20, 0.85, 0.65, 1)    # verde-esmeralda
COLOR_ACCENT2   = (0.45, 0.35, 0.95, 1)    # violeta
COLOR_ACCENT3   = (1.00, 0.55, 0.20, 1)    # naranja
COLOR_ACCENT4   = (0.25, 0.65, 1.00, 1)    # azul cielo
COLOR_TEXT      = (1.00, 1.00, 1.00, 1)
COLOR_MUTED     = (0.55, 0.55, 0.65, 1)
COLOR_DIVIDER   = (1, 1, 1, 0.07)
COLOR_ERROR     = (1.0, 0.35, 0.35, 1)

ACCENTS = [COLOR_ACCENT, COLOR_ACCENT2, COLOR_ACCENT3, COLOR_ACCENT4]

COURSE_ICONS = [
    'food-apple-outline',
    'translate',
    'heart-pulse',
    'shield-lock-outline',
]

COURSE_TAGS = [
    'Salud · 5 módulos',
    'Idiomas · 5 módulos',
    'Salud · 5 módulos',
    'Tecnología · 5 módulos',
]

# ─────────────────────────────────────────────
#  KV  STRING
# ─────────────────────────────────────────────
KV = '''
#:import get_color_from_hex kivy.utils.get_color_from_hex
#:import FadeTransition kivy.uix.screenmanager.FadeTransition

ScreenManager:
    transition: FadeTransition(duration=0.18)
    LoginScreen:
    HomeScreen:
    QuizScreen:
    ResultScreen:
    PresentationScreen:

# ══════════════════════════════════════════════════
#  LOGIN SCREEN
# ══════════════════════════════════════════════════
<LoginScreen>:
    name: 'login'

    MDScreen:
        md_bg_color: 0.05, 0.05, 0.08, 1

        MDBoxLayout:
            orientation: 'vertical'

            MDTopAppBar:
                title: ''
                right_action_items: [['close', lambda x: app.stop()]]
                elevation: 0
                md_bg_color: 0.08, 0.08, 0.12, 1

            MDBoxLayout:
                orientation: 'vertical'
                padding: '40dp', '0dp'
                spacing: 0

            # Espacio superior
            MDBoxLayout:
                size_hint_y: 0.05

            # Logo / ícono central
            MDBoxLayout:
                size_hint_y: None
                height: '80dp'
                MDLabel:
                    text: 'Edu'
                    font_size: '52sp'
                    halign: 'center'
                    valign: 'center'

            MDBoxLayout:
                size_hint_y: None
                height: '14dp'

            # Título
            MDLabel:
                text: 'EduCursos'
                font_style: 'H4'
                bold: True
                halign: 'center'
                theme_text_color: 'Custom'
                text_color: 0.20, 0.85, 0.65, 1
                size_hint_y: None
                height: '44dp'

            MDLabel:
                text: 'Plataforma de aprendizaje en línea'
                font_style: 'Body2'
                halign: 'center'
                theme_text_color: 'Custom'
                text_color: 0.55, 0.55, 0.65, 1
                size_hint_y: None
                height: '28dp'

            MDBoxLayout:
                size_hint_y: None
                height: '36dp'

            # Card del formulario
            MDCard:
                size_hint: 1, None
                height: '280dp'
                padding: '28dp', '24dp'
                radius: [20]
                md_bg_color: 0.10, 0.10, 0.14, 1
                spacing: '16dp'
                orientation: 'vertical'

                MDLabel:
                    text: 'Iniciar sesión'
                    font_style: 'H6'
                    bold: True
                    theme_text_color: 'Custom'
                    text_color: 1, 1, 1, 1
                    size_hint_y: None
                    height: '32dp'

                MDTextField:
                    id: field_nombre
                    hint_text: 'Nombre de usuario'
                    icon_right: 'account-outline'
                    mode: 'rectangle'
                    line_color_focus: 0.20, 0.85, 0.65, 1
                    text_color_focus: 1, 1, 1, 1
                    hint_text_color_normal: 0.55, 0.55, 0.65, 1
                    size_hint_y: None
                    height: '52dp'

                MDTextField:
                    id: field_pass
                    hint_text: 'Contraseña'
                    icon_right: 'lock-outline'
                    password: True
                    mode: 'rectangle'
                    line_color_focus: 0.20, 0.85, 0.65, 1
                    hint_text_color_normal: 0.55, 0.55, 0.65, 1
                    size_hint_y: None
                    height: '52dp'

                MDLabel:
                    id: lbl_error
                    text: ''
                    font_style: 'Caption'
                    theme_text_color: 'Custom'
                    text_color: 1.0, 0.35, 0.35, 1
                    halign: 'center'
                    size_hint_y: None
                    height: '20dp'

            MDBoxLayout:
                size_hint_y: None
                height: '18dp'

            # Botón entrar
            MDRaisedButton:
                text: 'Entrar'
                md_bg_color: 0.20, 0.85, 0.65, 1
                theme_text_color: 'Custom'
                text_color: 0.05, 0.05, 0.08, 1
                size_hint_x: 1
                height: '52dp'
                font_size: '16sp'
                bold: True
                on_release: app.do_login()

            MDBoxLayout:
                size_hint_y: None
                height: '10dp'

            MDLabel:
                text: 'Hint: cualquier usuario y contraseña funciona para demo'
                font_style: 'Caption'
                halign: 'center'
                theme_text_color: 'Custom'
                text_color: 0.40, 0.40, 0.50, 1
                size_hint_y: None
                height: '20dp'

            MDBoxLayout:
                size_hint_y: 1

# ══════════════════════════════════════════════════
#  HOME SCREEN
# ══════════════════════════════════════════════════
<HomeScreen>:
    name: 'home'

    MDScreen:
        md_bg_color: 0.05, 0.05, 0.08, 1

        MDBoxLayout:
            orientation: 'vertical'
            spacing: 0

            # TOP BAR
            MDBoxLayout:
                size_hint_y: None
                height: '68dp'
                padding: '20dp', '12dp'
                md_bg_color: 0.05, 0.05, 0.08, 1
                spacing: '12dp'

                MDBoxLayout:
                    orientation: 'vertical'
                    spacing: '2dp'

                    MDLabel:
                        id: lbl_bienvenida
                        text: 'Hola 👋'
                        font_style: 'Caption'
                        theme_text_color: 'Custom'
                        text_color: 0.55, 0.55, 0.65, 1
                        size_hint_y: None
                        height: '18dp'

                    MDLabel:
                        text: 'EduCursos'
                        font_style: 'H6'
                        bold: True
                        theme_text_color: 'Custom'
                        text_color: 0.20, 0.85, 0.65, 1
                        size_hint_y: None
                        height: '30dp'

                MDIconButton:
                    icon: 'logout'
                    theme_text_color: 'Custom'
                    text_color: 0.55, 0.55, 0.65, 1
                    user_font_size: '22sp'
                    on_release: app.do_logout()

            # SEPARADOR
            MDBoxLayout:
                size_hint_y: None
                height: '1dp'
                md_bg_color: 1, 1, 1, 0.07

            # HERO SECTION
            MDBoxLayout:
                orientation: 'vertical'
                size_hint_y: None
                height: '76dp'
                padding: '20dp', '14dp'
                spacing: '4dp'
                md_bg_color: 0.05, 0.05, 0.08, 1

                MDLabel:
                    text: 'Mis cursos'
                    font_style: 'H6'
                    bold: True
                    theme_text_color: 'Custom'
                    text_color: 1, 1, 1, 1
                    size_hint_y: None
                    height: '30dp'

                MDLabel:
                    text: 'Completa los módulos y obtén tu certificado'
                    font_style: 'Caption'
                    theme_text_color: 'Custom'
                    text_color: 0.55, 0.55, 0.65, 1
                    size_hint_y: None
                    height: '20dp'

            # GRID DE CURSOS
            ScrollView:
                MDGridLayout:
                    id: grid_cursos
                    cols: 1
                    adaptive_height: True
                    spacing: '14dp'
                    padding: '16dp', '10dp', '16dp', '24dp'

# ══════════════════════════════════════════════════
#  QUIZ SCREEN
# ══════════════════════════════════════════════════
<QuizScreen>:
    name: 'quiz'

    MDScreen:
        md_bg_color: 0.05, 0.05, 0.08, 1

        MDBoxLayout:
            orientation: 'vertical'
            spacing: 0

            MDTopAppBar:
                title: root.screen_title
                left_action_items: [['arrow-left', lambda x: app.finish_quiz()]]
                right_action_items: [['close', lambda x: app.stop()]]
                elevation: 0
                md_bg_color: 0.08, 0.08, 0.12, 1

            # ── Barra de progreso superior ──────────
            MDProgressBar:
                value: root.progress_value
                color: root.card_color_r, root.card_color_g, root.card_color_b, 1
                size_hint_y: None
                height: '5dp'

            MDBoxLayout:
                orientation: 'vertical'
                padding: '18dp', '14dp'
                spacing: '14dp'

                # ── Fila de estado: módulo + contador ──
                MDBoxLayout:
                    size_hint_y: None
                    height: '26dp'
                    spacing: '8dp'

                    MDLabel:
                        text: root.modulo_badge
                        font_style: 'Caption'
                        bold: True
                        theme_text_color: 'Custom'
                        text_color: root.card_color_r, root.card_color_g, root.card_color_b, 1

                    MDLabel:
                        text: root.status_text
                        font_style: 'Caption'
                        theme_text_color: 'Custom'
                        text_color: 0.55, 0.55, 0.65, 1
                        halign: 'right'

                # ── Card de pregunta — parte superior, altura fija ──
                MDCard:
                    size_hint: 1, None
                    height: '140dp'
                    padding: '20dp', '16dp'
                    radius: [16]
                    md_bg_color: root.card_color_r, root.card_color_g, root.card_color_b, 0.12
                    elevation: 0

                    MDLabel:
                        text: root.question_text
                        font_style: 'H6'
                        bold: True
                        theme_text_color: 'Custom'
                        text_color: 1, 1, 1, 1
                        halign: 'left'
                        valign: 'middle'
                        text_size: self.width, None

                # ── Respuestas: 1 columna, botones grandes ──
                ScrollView:
                    MDGridLayout:
                        id: answers_box
                        cols: 1
                        adaptive_height: True
                        spacing: '10dp'
                        padding: 0, '4dp', 0, 0

# ══════════════════════════════════════════════════
#  RESULT SCREEN
# ══════════════════════════════════════════════════
<ResultScreen>:
    name: 'result'

    MDScreen:
        md_bg_color: 0.05, 0.05, 0.08, 1

        MDBoxLayout:
            orientation: 'vertical'
            padding: '32dp'
            spacing: '20dp'

            MDBoxLayout:
                size_hint_y: None
                height: '30dp'

            # Emoji trofeo
            MDLabel:
                text: root.result_emoji
                font_size: '64sp'
                halign: 'center'
                size_hint_y: None
                height: '80dp'

            MDLabel:
                text: root.result_title
                font_style: 'H5'
                bold: True
                halign: 'center'
                theme_text_color: 'Custom'
                text_color: 1, 1, 1, 1
                size_hint_y: None
                height: '44dp'

            MDLabel:
                text: root.result_subtitle
                font_style: 'Body1'
                halign: 'center'
                theme_text_color: 'Custom'
                text_color: 0.55, 0.55, 0.65, 1
                size_hint_y: None
                height: '32dp'

            # Card de estadísticas
            MDCard:
                size_hint: 1, None
                height: '130dp'
                padding: '24dp'
                radius: [16]
                md_bg_color: 0.10, 0.10, 0.14, 1
                orientation: 'vertical'
                spacing: '8dp'

                MDLabel:
                    text: root.result_stats
                    font_style: 'H6'
                    bold: True
                    halign: 'center'
                    theme_text_color: 'Custom'
                    text_color: 0.20, 0.85, 0.65, 1

                MDLabel:
                    text: root.result_detail
                    font_style: 'Body2'
                    halign: 'center'
                    theme_text_color: 'Custom'
                    text_color: 0.55, 0.55, 0.65, 1

            MDBoxLayout:
                size_hint_y: 1

            # Botones
            MDRaisedButton:
                text: '📄  Descargar Certificado'
                md_bg_color: 0.20, 0.85, 0.65, 1
                theme_text_color: 'Custom'
                text_color: 0.05, 0.05, 0.08, 1
                size_hint_x: 1
                height: '52dp'
                font_size: '15sp'
                bold: True
                on_release: app.generate_certificate()

            MDFlatButton:
                text: 'Volver al inicio'
                theme_text_color: 'Custom'
                text_color: 0.55, 0.55, 0.65, 1
                size_hint_x: 1
                on_release: app.go_home()

            MDBoxLayout:
                size_hint_y: None
                height: '16dp'

# ══════════════════════════════════════════════════
#  PRESENTATION SCREEN
# ══════════════════════════════════════════════════
<PresentationScreen>:
    name: 'presentation'

    MDScreen:
        md_bg_color: 0.05, 0.05, 0.08, 1

        MDBoxLayout:
            orientation: 'vertical'

            MDTopAppBar:
                title: root.screen_title
                left_action_items: [['arrow-left', lambda x: app.close_presentation()]]
                right_action_items: [['close', lambda x: app.stop()]]
                elevation: 0
                md_bg_color: 0.08, 0.08, 0.12, 1

            ScrollView:
                MDGridLayout:
                    id: pdf_container
                    cols: 1
                    adaptive_height: True
                    spacing: '10dp'
                    padding: '10dp'
'''


# ─────────────────────────────────────────────
#  SCREEN CLASSES
# ─────────────────────────────────────────────
class LoginScreen(Screen):
    pass

class HomeScreen(Screen):
    pass

class QuizScreen(Screen):
    screen_title   = StringProperty('')
    question_text  = StringProperty('')
    status_text    = StringProperty('')
    modulo_badge   = StringProperty('')
    progress_value = NumericProperty(0)
    card_color_r   = NumericProperty(0.20)
    card_color_g   = NumericProperty(0.85)
    card_color_b   = NumericProperty(0.65)

class ResultScreen(Screen):
    result_emoji    = StringProperty('¡Felicidades!')
    result_title    = StringProperty('')
    result_subtitle = StringProperty('')
    result_stats    = StringProperty('')
    result_detail   = StringProperty('')

class PresentationScreen(Screen):
    screen_title = StringProperty('')


# ─────────────────────────────────────────────
#  MAIN APP
# ─────────────────────────────────────────────
class MainApp(MDApp):

    current_user   = ''
    current_curso  = None
    blocks         = []
    block          = 0
    q_idx          = 0
    correct        = 0
    total_correct  = 0
    total_questions_done = 0
    final_pct      = 0

    def build(self):
        self.theme_cls.primary_palette = 'Teal'
        self.theme_cls.theme_style     = 'Dark'
        Window.borderless = True
        Window.maximize()

        self.sm = Builder.load_string(KV)

        # ── Definición de cursos ──────────────────────────────────────
        self.cursos = [
            {
                'titulo': 'Fundamentos de Alimentación Saludable',
                'pdf': 'alimentacion.pdf',
                'desc': 'Aprende a comer bien para vivir mejor',
            },
            {
                'titulo': 'Inglés Básico',
                'pdf': 'ingles.pdf',
                'desc': 'Da tus primeros pasos en el idioma universal',
            },
            {
                'titulo': 'Primeros Auxilios Básicos',
                'pdf': 'primeros_auxilios.pdf',
                'desc': 'Actúa con confianza en situaciones de emergencia',
            },
            {
                'titulo': 'Seguridad Digital Básica',
                'pdf': 'seguridad_digital.pdf',
                'desc': 'Protege tu información y navega de forma segura',
            },
        ]

        self.quiz_data = {
            'Fundamentos de Alimentación Saludable': self.build_alimentacion(),
            'Inglés Básico':                         self.build_ingles(),
            'Primeros Auxilios Básicos':              self.build_primeros_auxilios(),
            'Seguridad Digital Básica':               self.build_seguridad_digital(),
        }

        return self.sm

    # ─────────────────────────────────────────
    #  LOGIN
    # ─────────────────────────────────────────
    def do_login(self):
        login_screen = self.sm.get_screen('login')
        nombre = login_screen.ids.field_nombre.text.strip()
        passw  = login_screen.ids.field_pass.text.strip()

        if not nombre:
            login_screen.ids.lbl_error.text = 'Por favor ingresa tu nombre de usuario.'
            return
        if not passw:
            login_screen.ids.lbl_error.text = 'Por favor ingresa tu contraseña.'
            return

        self.current_user = nombre
        login_screen.ids.lbl_error.text = ''
        self._build_home()
        self.sm.current = 'home'

    def do_logout(self):
        self.current_user = ''
        login_screen = self.sm.get_screen('login')
        login_screen.ids.field_nombre.text = ''
        login_screen.ids.field_pass.text   = ''
        login_screen.ids.lbl_error.text    = ''
        self.sm.current = 'login'

    # ─────────────────────────────────────────
    #  HOME: construir cards
    # ─────────────────────────────────────────
    def _build_home(self):
        home = self.sm.get_screen('home')
        home.ids.lbl_bienvenida.text = f'Hola, {self.current_user} 👋'
        grid = home.ids.grid_cursos
        grid.clear_widgets()

        for i, curso in enumerate(self.cursos):
            acc = ACCENTS[i % len(ACCENTS)]

            # ── CARD ─────────────────────────────────────────────────
            card = MDCard(
                orientation='vertical',
                size_hint=(1, None),
                height='168dp',
                padding='0dp',
                radius=[18],
                md_bg_color=COLOR_CARD,
                ripple_behavior=True,
            )

            # Barra superior de acento
            bar = MDBoxLayout(size_hint=(1, None), height='4dp', md_bg_color=acc)
            card.add_widget(bar)

            # Cuerpo
            body = MDBoxLayout(orientation='vertical', padding='18dp', spacing='10dp')

            # Fila: número + título + ícono
            row_top = MDBoxLayout(
                orientation='horizontal', size_hint_y=None, height='38dp', spacing='12dp'
            )

            num_lbl = MDLabel(
                text=str(i + 1),
                font_style='H6', bold=True,
                theme_text_color='Custom', text_color=acc,
                size_hint_x=None, width='24dp',
            )

            titulo_col = MDBoxLayout(orientation='vertical', spacing='2dp')

            t_lbl = MDLabel(
                text=curso['titulo'],
                font_style='Subtitle1', bold=True,
                theme_text_color='Custom', text_color=COLOR_TEXT,
            )
            tag_lbl = MDLabel(
                text=COURSE_TAGS[i],
                font_style='Caption',
                theme_text_color='Custom', text_color=COLOR_MUTED,
            )
            titulo_col.add_widget(t_lbl)
            titulo_col.add_widget(tag_lbl)

            row_top.add_widget(num_lbl)
            row_top.add_widget(titulo_col)
            body.add_widget(row_top)

            # Descripción
            desc_lbl = MDLabel(
                text=curso['desc'],
                font_style='Caption',
                theme_text_color='Custom', text_color=COLOR_MUTED,
                size_hint_y=None, height='22dp',
            )
            body.add_widget(desc_lbl)

            # Separador
            sep = MDBoxLayout(size_hint=(1, None), height='1dp', md_bg_color=COLOR_DIVIDER)
            body.add_widget(sep)

            # Fila de botones
            row_btns = MDBoxLayout(
                orientation='horizontal', size_hint_y=None, height='44dp', spacing='10dp'
            )

            btn_quiz = MDRaisedButton(
                text='▶  Iniciar curso',
                md_bg_color=acc,
                theme_text_color='Custom',
                text_color=(0.05, 0.05, 0.08, 1),
                elevation=0,
                font_size='13sp',
                on_release=lambda x, c=curso: self.start_quiz(c),
            )

            btn_pdf = MDFlatButton(
                text='Presentación',
                theme_text_color='Custom',
                text_color=COLOR_MUTED,
                on_release=lambda x, c=curso: self.open_presentation(c),
            )

            row_btns.add_widget(btn_quiz)
            row_btns.add_widget(btn_pdf)
            body.add_widget(row_btns)

            card.add_widget(body)
            grid.add_widget(card)

    # ─────────────────────────────────────────
    #  QUIZ: lógica
    # ─────────────────────────────────────────
    def start_quiz(self, curso):
        self.current_curso   = curso
        self.blocks          = self.quiz_data.get(curso['titulo'], [])
        self.block           = 0
        self.q_idx           = 0
        self.correct         = 0
        self.total_correct   = 0
        self.total_questions_done = 0

        idx = self.cursos.index(curso)
        acc = ACCENTS[idx % len(ACCENTS)]

        screen = self.sm.get_screen('quiz')
        screen.screen_title  = curso['titulo']
        screen.card_color_r  = acc[0]
        screen.card_color_g  = acc[1]
        screen.card_color_b  = acc[2]

        self.show_question()
        self.sm.current = 'quiz'

    def show_question(self):
        q      = self.blocks[self.block][self.q_idx]
        screen = self.sm.get_screen('quiz')
        n_preg = len(self.blocks[self.block])

        screen.question_text  = q['question']
        screen.status_text    = f'Pregunta {self.q_idx + 1}/{n_preg}  ·  Aciertos: {self.correct}'
        screen.modulo_badge   = f'Módulo {self.block + 1} de {len(self.blocks)}'

        total_q = sum(len(b) for b in self.blocks)
        done    = sum(len(self.blocks[b]) for b in range(self.block)) + self.q_idx + 1
        screen.progress_value = (done / total_q) * 100 if total_q else 0

        box = screen.ids.answers_box
        box.clear_widgets()

        idx = self.cursos.index(self.current_curso)
        acc = ACCENTS[idx % len(ACCENTS)]

        for op in q['options']:
            box.add_widget(MDRaisedButton(
                text=op,
                md_bg_color=(0.13, 0.13, 0.22, 1),
                theme_text_color='Custom',
                text_color=COLOR_TEXT,
                size_hint_x=1,
                size_hint_y=None,
                height='72dp',
                elevation=0,
                font_size='15sp',
                on_release=lambda x, o=op: self.answer(o)
            ))

    def answer(self, op):
        q      = self.blocks[self.block][self.q_idx]
        n_preg = len(self.blocks[self.block])

        if op == q['answer']:
            self.correct += 1
            self.total_correct += 1
        self.total_questions_done += 1

        if self.q_idx == n_preg - 1:
            # fin de módulo
            if self.correct >= 8:
                self.block  += 1
                self.q_idx   = 0
                self.correct = 0

                if self.block >= len(self.blocks):
                    # Curso completo
                    self._show_result_screen()
                else:
                    # Siguiente módulo
                    self._show_module_passed_dialog()
            else:
                self._show_module_failed_dialog()
        else:
            self.q_idx += 1
            self.show_question()

    def _show_module_passed_dialog(self):
        dlg = MDDialog(
            title='Módulo superado',
            text=f'¡Muy bien! Pasas al módulo {self.block + 1}.',
            buttons=[MDRaisedButton(
                text='Continuar',
                md_bg_color=COLOR_ACCENT,
                theme_text_color='Custom',
                text_color=COLOR_BG,
                on_release=lambda x: (dlg.dismiss(), self.show_question()),
            )]
        )
        dlg.open()

    def _show_module_failed_dialog(self):
        dlg = MDDialog(
            title='❌ Módulo no superado',
            text='Necesitas al menos 8/10 respuestas correctas para avanzar.\nVuelve a intentarlo.',
            buttons=[MDRaisedButton(
                text='Reintentar módulo',
                md_bg_color=COLOR_ACCENT3,
                theme_text_color='Custom',
                text_color=COLOR_BG,
                on_release=lambda x: (dlg.dismiss(), self._retry_module()),
            ), MDFlatButton(
                text='Salir',
                theme_text_color='Custom',
                text_color=COLOR_MUTED,
                on_release=lambda x: (dlg.dismiss(), self.go_home()),
            )]
        )
        dlg.open()

    def _retry_module(self):
        self.q_idx  = 0
        self.correct = 0
        self.show_question()

    def _show_result_screen(self):
        total_q = self.total_questions_done
        pct     = round((self.total_correct / total_q) * 100) if total_q else 0
        self.final_pct = pct

        screen = self.sm.get_screen('result')
        screen.result_emoji    = '¡Excelente!' if pct >= 90 else '¡Felicidades!'
        screen.result_title    = '¡Curso completado!'
        screen.result_subtitle = self.current_curso['titulo']
        screen.result_stats    = f'{pct}% de aciertos'
        screen.result_detail   = f'{self.total_correct} correctas de {total_q} preguntas'
        self.sm.current = 'result'

    def finish_quiz(self):
        self.sm.current = 'home'

    def go_home(self):
        self.sm.current = 'home'

    # ─────────────────────────────────────────
    #  CERTIFICADO PDF
    # ─────────────────────────────────────────
    def generate_certificate(self):
        if not self.current_curso:
            return

        output_dir = 'certificados'
        os.makedirs(output_dir, exist_ok=True)

        safe_name   = re.sub(r'[^a-zA-Z0-9_]', '_', self.current_user)
        safe_course = re.sub(r'[^a-zA-Z0-9_]', '_', self.current_curso['titulo'])
        timestamp   = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename    = f'certificado_{safe_name}_{safe_course}_{timestamp}.pdf'
        filepath    = os.path.join(output_dir, filename)

        W, H = landscape(A4)
        c    = canvas.Canvas(filepath, pagesize=landscape(A4))

        # Fondo oscuro degradado simulado
        c.setFillColor(HexColor('#0D0D14'))
        c.rect(0, 0, W, H, fill=1, stroke=0)

        # Franjas decorativas laterales
        for x_off, col in [(0, '#34D9A4'), (W - 8, '#7357F2')]:
            c.setFillColor(HexColor(col))
            c.rect(x_off, 0, 8, H, fill=1, stroke=0)

        # Borde interior decorativo
        c.setStrokeColor(HexColor('#34D9A4'))
        c.setLineWidth(1.5)
        c.rect(30, 30, W - 60, H - 60, fill=0, stroke=1)

        c.setStrokeColor(HexColor('#7357F2'))
        c.setLineWidth(0.5)
        c.rect(36, 36, W - 72, H - 72, fill=0, stroke=1)

        # Emoji / ícono superior
        c.setFont('Helvetica-Bold', 36)
        c.setFillColor(HexColor('#34D9A4'))
        c.drawCentredString(W / 2, H - 80, '🎓  EduCursos')

        # Título
        c.setFont('Helvetica', 16)
        c.setFillColor(HexColor('#9A9AB0'))
        c.drawCentredString(W / 2, H - 110, 'CERTIFICADO DE FINALIZACIÓN')

        # Línea decorativa
        c.setStrokeColor(HexColor('#34D9A4'))
        c.setLineWidth(2)
        c.line(W / 2 - 180, H - 122, W / 2 + 180, H - 122)

        # "Se certifica que"
        c.setFont('Helvetica', 13)
        c.setFillColor(HexColor('#9A9AB0'))
        c.drawCentredString(W / 2, H - 155, 'Se certifica que')

        # Nombre del usuario
        c.setFont('Helvetica-Bold', 32)
        c.setFillColor(white)
        c.drawCentredString(W / 2, H - 200, self.current_user)

        # Línea bajo nombre
        c.setStrokeColor(HexColor('#7357F2'))
        c.setLineWidth(1)
        c.line(W / 2 - 220, H - 210, W / 2 + 220, H - 210)

        # Texto "ha completado satisfactoriamente"
        c.setFont('Helvetica', 13)
        c.setFillColor(HexColor('#9A9AB0'))
        c.drawCentredString(W / 2, H - 238, 'ha completado satisfactoriamente el curso:')

        # Nombre del curso
        c.setFont('Helvetica-Bold', 20)
        c.setFillColor(HexColor('#34D9A4'))
        c.drawCentredString(W / 2, H - 272, self.current_curso['titulo'])

        # Porcentaje
        c.setFont('Helvetica-Bold', 15)
        c.setFillColor(HexColor('#7357F2'))
        c.drawCentredString(W / 2, H - 305, f'Porcentaje de aciertos: {self.final_pct}%')

        # Fecha
        fecha_str = datetime.now().strftime('%d de %B de %Y').replace(
            'January','enero').replace('February','febrero').replace(
            'March','marzo').replace('April','abril').replace(
            'May','mayo').replace('June','junio').replace(
            'July','julio').replace('August','agosto').replace(
            'September','septiembre').replace('October','octubre').replace(
            'November','noviembre').replace('December','diciembre')

        c.setFont('Helvetica', 12)
        c.setFillColor(HexColor('#9A9AB0'))
        c.drawCentredString(W / 2, H - 335, f'Fecha de emisión: {fecha_str}')

        c.save()

        # Abrir PDF
        try:
            webbrowser.open(f'file://{os.path.abspath(filepath)}')
            self.show_dialog('Certificado generado',
                             f'Guardado en:\n{filepath}')
        except Exception as e:
            self.show_dialog('Certificado guardado', filepath)

    # ─────────────────────────────────────────
    #  PRESENTACIÓN PDF
    # ─────────────────────────────────────────
    def open_presentation(self, curso):
        pdf_path = os.path.join('presentaciones', curso['pdf'])
        if not os.path.exists(pdf_path):
            self.show_dialog('Archivo no encontrado',
                             f"Coloca '{curso['pdf']}' en la carpeta 'presentaciones/'.")
            return
        try:
            doc    = fitz.open(pdf_path)
            screen = self.sm.get_screen('presentation')
            screen.screen_title = curso['titulo']
            screen.ids.pdf_container.clear_widgets()

            tmp_dir = os.path.join(tempfile.gettempdir(),
                                   f"kivy_pdf_{curso['pdf'].replace('.pdf','')}")
            os.makedirs(tmp_dir, exist_ok=True)
            for f in os.listdir(tmp_dir):
                try: os.remove(os.path.join(tmp_dir, f))
                except: pass

            for i, page in enumerate(doc):
                pix = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5))
                img_path = os.path.join(tmp_dir, f'p{i}.png')
                pix.save(img_path)
                screen.ids.pdf_container.add_widget(
                    KivyImage(source=img_path, size_hint_y=None, height=400)
                )
            doc.close()
            self.sm.current = 'presentation'
        except Exception as e:
            self.show_dialog('Error', str(e))

    def close_presentation(self):
        self.sm.current = 'home'

    # ─────────────────────────────────────────
    #  UTILIDADES
    # ─────────────────────────────────────────
    def show_dialog(self, title, text):
        dlg = MDDialog(
            title=title, text=text,
            buttons=[MDFlatButton(
                text='OK',
                theme_text_color='Custom',
                text_color=COLOR_ACCENT,
                on_release=lambda x: dlg.dismiss()
            )]
        )
        dlg.open()

    # ═════════════════════════════════════════
    #  DATOS DE QUIZ
    # ═════════════════════════════════════════

    # ── ALIMENTACIÓN SALUDABLE ────────────────
    def build_alimentacion(self):
        return [
            # Módulo 1
            [
                {"question":"¿Qué es la alimentación saludable?","options":["Comer solo frutas","Comer de forma equilibrada y variada","Comer poco","Evitar todos los carbohidratos"],"answer":"Comer de forma equilibrada y variada"},
                {"question":"¿Por qué es importante alimentarse bien?","options":["Solo para bajar de peso","Para tener energía y salud","Para comer más","No es importante"],"answer":"Para tener energía y salud"},
                {"question":"¿Cuál es un ejemplo de comida saludable?","options":["Refresco y papas","Hamburguesa","Pollo con verduras","Dulces"],"answer":"Pollo con verduras"},
                {"question":"¿Cuál es un ejemplo de comida no saludable?","options":["Ensalada","Fruta","Comida rápida en exceso","Agua"],"answer":"Comida rápida en exceso"},
                {"question":"¿La alimentación influye en la salud?","options":["No","Sí, mucho","Solo en adultos","Solo en niños"],"answer":"Sí, mucho"},
                {"question":"¿Qué pasa si no te alimentas bien?","options":["Nada","Mejora tu salud","Puede afectar tu salud","Te da más energía"],"answer":"Puede afectar tu salud"},
                {"question":"¿Las frutas son importantes?","options":["No","Sí","Solo a veces","No aportan nada"],"answer":"Sí"},
                {"question":"¿Las verduras son necesarias?","options":["No","Sí","Solo si haces ejercicio","Solo en dietas"],"answer":"Sí"},
                {"question":"¿El agua forma parte de una buena alimentación?","options":["No","Sí","Solo en verano","No es necesaria"],"answer":"Sí"},
                {"question":"¿Comer solo comida rápida es saludable?","options":["Sí","No","Depende","A veces"],"answer":"No"},
            ],
            # Módulo 2
            [
                {"question":"¿Qué nutriente ayuda a construir músculo?","options":["Grasas","Proteínas","Azúcar","Agua"],"answer":"Proteínas"},
                {"question":"¿Qué nutriente da energía principal?","options":["Proteínas","Carbohidratos","Vitaminas","Agua"],"answer":"Carbohidratos"},
                {"question":"¿Qué nutriente almacena energía?","options":["Proteínas","Grasas","Minerales","Agua"],"answer":"Grasas"},
                {"question":"¿Las proteínas son importantes?","options":["No","Sí","Solo para atletas","Solo para adultos"],"answer":"Sí"},
                {"question":"¿Los carbohidratos son malos?","options":["Sí","No, son necesarios","Siempre","Solo en dietas"],"answer":"No, son necesarios"},
                {"question":"¿Las grasas tienen función?","options":["No","Sí","Solo engordan","No sirven"],"answer":"Sí"},
                {"question":"Ejemplo de proteína:","options":["Pollo","Pan","Refresco","Dulces"],"answer":"Pollo"},
                {"question":"Ejemplo de carbohidrato:","options":["Arroz","Carne","Aceite","Huevo"],"answer":"Arroz"},
                {"question":"Ejemplo de grasa saludable:","options":["Papas fritas","Aguacate","Refresco","Dulces"],"answer":"Aguacate"},
                {"question":"¿Se deben eliminar las grasas?","options":["Sí","No, son necesarias","Solo algunas","Siempre"],"answer":"No, son necesarias"},
            ],
            # Módulo 3
            [
                {"question":"¿Qué es una caloría?","options":["Un nutriente","Energía que da la comida","Una vitamina","Un mineral"],"answer":"Energía que da la comida"},
                {"question":"¿Para qué sirven las calorías?","options":["Para engordar","Para dar energía","Para hidratar","No sirven"],"answer":"Para dar energía"},
                {"question":"Comer más calorías de las necesarias provoca:","options":["Pérdida de peso","Aumento de peso","Nada","Más agua"],"answer":"Aumento de peso"},
                {"question":"Comer menos calorías provoca:","options":["Subir de peso","Bajar de peso","Nada","Aumentar músculo"],"answer":"Bajar de peso"},
                {"question":"¿Todos necesitan las mismas calorías?","options":["Sí","No","Solo adultos","Solo niños"],"answer":"No"},
                {"question":"¿El ejercicio influye en las calorías?","options":["No","Sí","Solo a veces","No importa"],"answer":"Sí"},
                {"question":"¿Las calorías dan energía?","options":["No","Sí","Solo en deporte","No siempre"],"answer":"Sí"},
                {"question":"¿Se pueden controlar las calorías?","options":["No","Sí","Solo médicos","No importa"],"answer":"Sí"},
                {"question":"¿Las bebidas tienen calorías?","options":["No","Sí","Solo agua","No siempre"],"answer":"Sí"},
                {"question":"¿El exceso de calorías afecta la salud?","options":["No","Sí","A veces","No importa"],"answer":"Sí"},
            ],
            # Módulo 4
            [
                {"question":"¿Qué es un plato balanceado?","options":["Comer mucho","Comer equilibrado","Comer solo proteína","Comer rápido"],"answer":"Comer equilibrado"},
                {"question":"¿Qué debe incluir un plato balanceado?","options":["Solo carne","Solo verduras","Varios grupos de alimentos","Dulces"],"answer":"Varios grupos de alimentos"},
                {"question":"¿Las verduras ocupan gran parte del plato?","options":["No","Sí","Poco","Nada"],"answer":"Sí"},
                {"question":"¿Debe haber proteína en el plato?","options":["No","Sí","Solo a veces","No importa"],"answer":"Sí"},
                {"question":"¿Se incluyen carbohidratos en el plato?","options":["No","Sí","Nunca","Solo en dieta"],"answer":"Sí"},
                {"question":"¿Un plato sin verduras es balanceado?","options":["Sí","No","A veces","Siempre"],"answer":"No"},
                {"question":"¿La variedad es importante?","options":["No","Sí","Poco","No importa"],"answer":"Sí"},
                {"question":"¿El agua acompaña el plato?","options":["No","Sí","Solo jugos","No importa"],"answer":"Sí"},
                {"question":"¿Las porciones importan?","options":["No","Sí","Poco","Nunca"],"answer":"Sí"},
                {"question":"¿El equilibrio es clave en la alimentación?","options":["No","Sí","A veces","No importa"],"answer":"Sí"},
            ],
            # Módulo 5
            [
                {"question":"¿Cuánta agua se recomienda beber al día?","options":["Nada","Aprox. 1.5–2 litros","Solo refresco","No importa"],"answer":"Aprox. 1.5–2 litros"},
                {"question":"¿Los ultraprocesados son saludables?","options":["Sí","No","A veces","Siempre"],"answer":"No"},
                {"question":"¿Dormir bien influye en la alimentación?","options":["No","Sí","Poco","No importa"],"answer":"Sí"},
                {"question":"¿El ejercicio ayuda a la salud?","options":["No","Sí","Poco","No importa"],"answer":"Sí"},
                {"question":"¿Saltarse comidas es bueno?","options":["Sí","No","A veces","Siempre"],"answer":"No"},
                {"question":"¿Comer frutas es saludable?","options":["No","Sí","Poco","No importa"],"answer":"Sí"},
                {"question":"¿El exceso de azúcar es malo?","options":["No","Sí","A veces","No importa"],"answer":"Sí"},
                {"question":"¿Los hábitos afectan la salud?","options":["No","Sí","Poco","No importa"],"answer":"Sí"},
                {"question":"¿Se pueden mejorar los hábitos alimenticios?","options":["No","Sí","Poco","No importa"],"answer":"Sí"},
                {"question":"¿Es importante tener horarios de comida?","options":["No","Sí","Poco","No importa"],"answer":"Sí"},
            ],
        ]

    # ── INGLÉS BÁSICO ─────────────────────────
    def build_ingles(self):
        return [
            # Módulo 1
            [
                {"question":"What does 'Hello' mean?","options":["Adiós","Hola","Gracias","Por favor"],"answer":"Hola"},
                {"question":"What is the correct greeting in the morning?","options":["Good night","Good afternoon","Good morning","Goodbye"],"answer":"Good morning"},
                {"question":"How do you say '¿Cómo estás?' in English?","options":["What is your name?","Where are you?","How are you?","Who are you?"],"answer":"How are you?"},
                {"question":"What is the correct way to introduce yourself?","options":["I name is John","My name is John","Name is John","Me name John"],"answer":"My name is John"},
                {"question":"What does 'Good evening' mean?","options":["Buenos días","Buenas tardes","Buenas noches (al saludar)","Adiós"],"answer":"Buenas noches (al saludar)"},
                {"question":"What is the correct response to 'How are you?'","options":["My name is Ana","I am fine","Hello","Goodbye"],"answer":"I am fine"},
                {"question":"What does 'Hi' mean?","options":["Adiós","Hola","Gracias","Perdón"],"answer":"Hola"},
                {"question":"Choose the correct goodbye expression:","options":["Hello","Hi","Goodbye","Good morning"],"answer":"Goodbye"},
                {"question":"How do you say 'Mucho gusto'?","options":["Nice to meet you","See you later","Good night","Thank you"],"answer":"Nice to meet you"},
                {"question":"What is the correct question to ask someone's name?","options":["How are you?","What is your name?","Where are you?","How old are you?"],"answer":"What is your name?"},
            ],
            # Módulo 2
            [
                {"question":"What number is 'one'?","options":["Uno","Dos","Tres","Cuatro"],"answer":"Uno"},
                {"question":"What number is 'five'?","options":["Cuatro","Cinco","Seis","Siete"],"answer":"Cinco"},
                {"question":"What number is 'ten'?","options":["Ocho","Nueve","Diez","Once"],"answer":"Diez"},
                {"question":"How do you say 'veinte' in English?","options":["Ten","Fifteen","Twenty","Twelve"],"answer":"Twenty"},
                {"question":"What number is 'hundred'?","options":["Mil","Cien","Diez","Cincuenta"],"answer":"Cien"},
                {"question":"How do you say 'primero' in English?","options":["Second","Third","First","Fourth"],"answer":"First"},
                {"question":"What does 'last' mean?","options":["Primero","Segundo","Último","Siguiente"],"answer":"Último"},
                {"question":"How do you say 'la mitad'?","options":["A quarter","A third","A half","A double"],"answer":"A half"},
                {"question":"What is 'double' in Spanish?","options":["Mitad","Triple","Doble","Cuádruple"],"answer":"Doble"},
                {"question":"How do you say 'cero'?","options":["One","Zero","None","Null"],"answer":"Zero"},
            ],
            # Módulo 3
            [
                {"question":"What color is 'red'?","options":["Rojo","Azul","Verde","Amarillo"],"answer":"Rojo"},
                {"question":"What color is 'blue'?","options":["Rojo","Azul","Verde","Negro"],"answer":"Azul"},
                {"question":"What color is 'green'?","options":["Rojo","Azul","Verde","Blanco"],"answer":"Verde"},
                {"question":"What color is 'yellow'?","options":["Amarillo","Rojo","Azul","Negro"],"answer":"Amarillo"},
                {"question":"What color is 'black'?","options":["Negro","Blanco","Azul","Rojo"],"answer":"Negro"},
                {"question":"What color is 'white'?","options":["Negro","Blanco","Azul","Rojo"],"answer":"Blanco"},
                {"question":"What color is 'orange'?","options":["Naranja","Rojo","Amarillo","Verde"],"answer":"Naranja"},
                {"question":"What color is 'pink'?","options":["Rosa","Rojo","Morado","Azul"],"answer":"Rosa"},
                {"question":"What color is 'purple'?","options":["Morado","Rojo","Azul","Verde"],"answer":"Morado"},
                {"question":"What color is 'gray'?","options":["Gris","Negro","Blanco","Azul"],"answer":"Gris"},
            ],
            # Módulo 4
            [
                {"question":"How do you say 'casa' in English?","options":["Car","House","Tree","Dog"],"answer":"House"},
                {"question":"What does 'cat' mean?","options":["Perro","Gato","Pájaro","Pez"],"answer":"Gato"},
                {"question":"How do you say 'libro' in English?","options":["Pen","Pencil","Book","Notebook"],"answer":"Book"},
                {"question":"What does 'water' mean?","options":["Fuego","Tierra","Agua","Aire"],"answer":"Agua"},
                {"question":"How do you say 'escuela' in English?","options":["Office","School","Hospital","Park"],"answer":"School"},
                {"question":"What does 'friend' mean?","options":["Enemigo","Conocido","Amigo","Familiar"],"answer":"Amigo"},
                {"question":"How do you say 'comida' in English?","options":["Drink","Food","Sleep","Work"],"answer":"Food"},
                {"question":"What does 'sun' mean?","options":["Luna","Estrella","Sol","Nube"],"answer":"Sol"},
                {"question":"How do you say 'tiempo' (weather) in English?","options":["Time","Weather","Season","Climate"],"answer":"Weather"},
                {"question":"What does 'happy' mean?","options":["Triste","Enojado","Feliz","Cansado"],"answer":"Feliz"},
            ],
            # Módulo 5
            [
                {"question":"What tense is 'I eat'?","options":["Pasado","Futuro","Presente","Condicional"],"answer":"Presente"},
                {"question":"What tense is 'I ate'?","options":["Pasado","Futuro","Presente","Condicional"],"answer":"Pasado"},
                {"question":"What tense is 'I will eat'?","options":["Pasado","Futuro","Presente","Condicional"],"answer":"Futuro"},
                {"question":"Choose the correct form: 'She ___ a teacher.'","options":["am","are","is","be"],"answer":"is"},
                {"question":"Choose the correct form: 'They ___ happy.'","options":["am","is","are","be"],"answer":"are"},
                {"question":"What is the plural of 'child'?","options":["Childs","Childes","Children","Childrens"],"answer":"Children"},
                {"question":"What does 'Can you help me?' mean?","options":["¿Puedes ayudarme?","¿Dónde estás?","¿Cómo te llamas?","¿Qué hora es?"],"answer":"¿Puedes ayudarme?"},
                {"question":"What does 'I don't understand' mean?","options":["No me importa","No entiendo","No puedo","No quiero"],"answer":"No entiendo"},
                {"question":"How do you say 'Por favor repite.'?","options":["Please repeat.","Please stop.","Please wait.","Please go."],"answer":"Please repeat."},
                {"question":"What does 'See you tomorrow' mean?","options":["Hasta luego","Hasta mañana","Hasta la vista","Adiós"],"answer":"Hasta mañana"},
            ],
        ]

    # ── PRIMEROS AUXILIOS BÁSICOS ─────────────
    def build_primeros_auxilios(self):
        return [
            # Módulo 1: ¿Qué son los primeros auxilios?
            [
                {"question":"¿Qué son los primeros auxilios?","options":["Un tipo de medicamento","Atención inmediata antes de ayuda médica","Una operación quirúrgica","Un examen médico"],"answer":"Atención inmediata antes de ayuda médica"},
                {"question":"¿Cuál es el primer paso ante una emergencia?","options":["Entrar en pánico","Evaluar la seguridad del lugar","Llamar a amigos","Ignorar la situación"],"answer":"Evaluar la seguridad del lugar"},
                {"question":"¿A qué número se llama a emergencias en México?","options":["100","066","911","112"],"answer":"911"},
                {"question":"¿Quién puede aplicar primeros auxilios?","options":["Solo médicos","Solo enfermeras","Cualquier persona capacitada","Solo paramédicos"],"answer":"Cualquier persona capacitada"},
                {"question":"¿Cuál es la regla PAS?","options":["Proteger, Avisar, Socorrer","Preguntar, Actuar, Salvar","Pausar, Asistir, Seguir","Prevenir, Atar, Salir"],"answer":"Proteger, Avisar, Socorrer"},
                {"question":"¿Qué significa triaje?","options":["Tipo de venda","Clasificar heridos por gravedad","Anestesia local","Un tipo de camilla"],"answer":"Clasificar heridos por gravedad"},
                {"question":"¿Se debe mover a una persona con posible lesión en columna?","options":["Sí, inmediatamente","No, a menos que haya peligro inminente","Siempre","Si está consciente"],"answer":"No, a menos que haya peligro inminente"},
                {"question":"¿Para qué sirve el botiquín de primeros auxilios?","options":["Para guardar medicinas caras","Para atender emergencias básicas","Para hacer operaciones","Para diagnosticar enfermedades"],"answer":"Para atender emergencias básicas"},
                {"question":"¿Qué NO debe faltar en un botiquín básico?","options":["Aspirinas únicamente","Gasas, vendas, antiséptico y tijeras","Solo alcohol","Solo termómetro"],"answer":"Gasas, vendas, antiséptico y tijeras"},
                {"question":"¿Cuál es el objetivo principal de los primeros auxilios?","options":["Curar completamente al paciente","Preservar la vida y evitar complicaciones","Reemplazar al médico","Administrar medicamentos fuertes"],"answer":"Preservar la vida y evitar complicaciones"},
            ],
            # Módulo 2: RCP básico
            [
                {"question":"¿Qué significa RCP?","options":["Reanimación Cardio Pulmonar","Revisión Clínica Práctica","Recuperación Completa Pronta","Revisión Corporal Principal"],"answer":"Reanimación Cardio Pulmonar"},
                {"question":"¿Cuántas compresiones por minuto se realizan en RCP adulto?","options":["30–40","60–70","100–120","150–180"],"answer":"100–120"},
                {"question":"¿Cuántas compresiones se dan antes de 2 respiraciones en RCP?","options":["10","20","30","40"],"answer":"30"},
                {"question":"¿Dónde se colocan las manos para compresiones en adultos?","options":["En el estómago","En el centro del pecho","En el cuello","En los hombros"],"answer":"En el centro del pecho"},
                {"question":"¿A qué profundidad se comprimen en adultos?","options":["1 cm","2 cm","5–6 cm","10 cm"],"answer":"5–6 cm"},
                {"question":"¿Qué verificar antes de iniciar RCP?","options":["Si la persona está dormida","Si la persona responde y respira","El color de la piel","El pulso en el pie"],"answer":"Si la persona responde y respira"},
                {"question":"¿El DEA (desfibrilador) puede usarse en niños?","options":["No, nunca","Sí, con parches pediátricos","Solo adultos mayores","No existe para niños"],"answer":"Sí, con parches pediátricos"},
                {"question":"¿Cuándo se detiene el RCP?","options":["Nunca","Cuando lleguen los servicios de emergencia o la persona reaccione","Después de 5 minutos siempre","Cuando te canses"],"answer":"Cuando lleguen los servicios de emergencia o la persona reaccione"},
                {"question":"¿Es necesario dar respiraciones de rescate si no estás capacitado?","options":["Sí, siempre","No, las compresiones solas son suficientes para iniciar","Solo en adultos","Solo en niños"],"answer":"No, las compresiones solas son suficientes para iniciar"},
                {"question":"¿La posición de la persona en RCP es?","options":["De lado","Boca abajo","Boca arriba en superficie firme","Sentada"],"answer":"Boca arriba en superficie firme"},
            ],
            # Módulo 3: Heridas y quemaduras
            [
                {"question":"¿Qué se debe hacer primero ante una hemorragia?","options":["Aplicar hielo","Presionar directamente sobre la herida","Dar agua al herido","Aplicar mantequilla"],"answer":"Presionar directamente sobre la herida"},
                {"question":"¿Qué tipo de quemadura es solo superficial (enrojecimiento)?","options":["Primer grado","Segundo grado","Tercer grado","Cuarto grado"],"answer":"Primer grado"},
                {"question":"¿Cómo se atiende una quemadura de primer grado?","options":["Con hielo directo","Con agua fría corriente por 10–20 minutos","Con mantequilla","Con alcohol"],"answer":"Con agua fría corriente por 10–20 minutos"},
                {"question":"¿Qué NO debes hacer con una quemadura?","options":["Enfriar con agua","Cubrir con gasa","Reventar las ampollas","Buscar atención médica"],"answer":"Reventar las ampollas"},
                {"question":"¿Qué indica una hemorragia arterial?","options":["Sangre oscura que fluye lento","Sangre roja brillante que sale a borbotones","Sangre negra","No hay diferencia"],"answer":"Sangre roja brillante que sale a borbotones"},
                {"question":"¿Se debe extraer un objeto incrustado en una herida?","options":["Sí, siempre","No, se inmoviliza y busca ayuda médica","Solo si es pequeño","Solo si duele"],"answer":"No, se inmoviliza y busca ayuda médica"},
                {"question":"¿Qué es un torniquete?","options":["Un tipo de venda para cabeza","Dispositivo para detener hemorragia en extremidades","Un medicamento","Un tipo de escayola"],"answer":"Dispositivo para detener hemorragia en extremidades"},
                {"question":"¿Cuándo se usa el torniquete?","options":["En cualquier herida","Solo cuando la hemorragia no se controla con presión directa","Siempre que haya herida","Nunca"],"answer":"Solo cuando la hemorragia no se controla con presión directa"},
                {"question":"¿Qué cubre una quemadura de tercer grado?","options":["Solo la superficie","Afecta capas profundas incluyendo tejidos bajo la piel","Solo enrojece","Solo produce ampollas"],"answer":"Afecta capas profundas incluyendo tejidos bajo la piel"},
                {"question":"¿Se debe limpiar una herida con agua y jabón?","options":["No, nunca","Sí, con agua limpia y jabón suave","Solo con alcohol","Solo con agua"],"answer":"Sí, con agua limpia y jabón suave"},
            ],
            # Módulo 4: Atragantamiento y desmayo
            [
                {"question":"¿Qué hacer si alguien se atraganta y puede toser con fuerza?","options":["Golpear su espalda inmediatamente","Animarlo a seguir tosiendo","Darle agua","Hacer maniobra de Heimlich"],"answer":"Animarlo a seguir tosiendo"},
                {"question":"¿Qué es la maniobra de Heimlich?","options":["Masaje en el pecho","Compresiones abdominales para expulsar obstrucción","Respiración boca a boca","Presión en la garganta"],"answer":"Compresiones abdominales para expulsar obstrucción"},
                {"question":"¿Dónde se colocan las manos en la maniobra de Heimlich en adulto?","options":["En el pecho","Por encima del ombligo y bajo el esternón","En la cadera","En el cuello"],"answer":"Por encima del ombligo y bajo el esternón"},
                {"question":"¿Qué hacer si alguien se desmaya?","options":["Ponerlo de pie inmediatamente","Recostarlo, elevar piernas, asegurar que respire","Darle agua fría en la cara","Dejarlo solo"],"answer":"Recostarlo, elevar piernas, asegurar que respire"},
                {"question":"¿Cuál es la posición de recuperación?","options":["Boca abajo","De lado con brazo bajo la cabeza","Boca arriba con piernas elevadas","Sentado"],"answer":"De lado con brazo bajo la cabeza"},
                {"question":"¿Cuándo se usa la posición de recuperación?","options":["Cuando la persona está consciente y respira","Cuando hace RCP","En fracturas","En quemaduras"],"answer":"Cuando la persona está consciente y respira"},
                {"question":"¿Qué indica un desmayo repentino sin causa aparente?","options":["Nada importante","Puede requerir evaluación médica","Solo cansancio","Solo hambre"],"answer":"Puede requerir evaluación médica"},
                {"question":"¿Se debe dar agua a alguien inconsciente?","options":["Sí, siempre","No, puede causar asfixia","Solo un poco","Depende"],"answer":"No, puede causar asfixia"},
                {"question":"En atragantamiento de bebé, ¿qué se hace?","options":["Igual que en adulto","5 palmadas en espalda y 5 compresiones en pecho","Solo compresiones abdominales","Solo palmadas"],"answer":"5 palmadas en espalda y 5 compresiones en pecho"},
                {"question":"¿Qué no debes hacer si alguien tiene una convulsión?","options":["Proteger su cabeza","Aflojar ropa ajustada","Meter algo en su boca","Esperar a que termine"],"answer":"Meter algo en su boca"},
            ],
            # Módulo 5: Fracturas, esguinces y emergencias generales
            [
                {"question":"¿Cómo se detecta una posible fractura?","options":["Solo con rayos X","Dolor intenso, deformidad, inflamación o incapacidad de mover","Solo con dolor","Solo con sangrado"],"answer":"Dolor intenso, deformidad, inflamación o incapacidad de mover"},
                {"question":"¿Qué se aplica en una fractura?","options":["Calor directo","Inmovilización con férula o tablilla","Masaje intenso","Movimiento para probar si duele"],"answer":"Inmovilización con férula o tablilla"},
                {"question":"¿Qué es un esguince?","options":["Fractura de hueso","Estiramiento o desgarro de ligamentos","Infección de músculo","Luxación de articulación"],"answer":"Estiramiento o desgarro de ligamentos"},
                {"question":"¿Qué aplicar en un esguince las primeras horas?","options":["Calor","Frío (hielo envuelto)","Masaje fuerte","Venda apretada sin más"],"answer":"Frío (hielo envuelto)"},
                {"question":"¿Qué es un shock?","options":["Un susto fuerte","Estado de insuficiencia circulatoria que amenaza la vida","Un tipo de fractura","Un desmayo común"],"answer":"Estado de insuficiencia circulatoria que amenaza la vida"},
                {"question":"¿Cómo se atiende el shock?","options":["Dar de comer al paciente","Acostar, abrigar, elevar piernas y esperar ayuda","Hacer RCP siempre","Dar agua fría"],"answer":"Acostar, abrigar, elevar piernas y esperar ayuda"},
                {"question":"¿Qué hacer ante una intoxicación leve?","options":["Inducir el vómito siempre","Llamar a urgencias o centro de control de intoxicaciones","Dar leche y esperar","Ignorarla"],"answer":"Llamar a urgencias o centro de control de intoxicaciones"},
                {"question":"¿Se debe inducir el vómito en intoxicaciones con ácidos o bases?","options":["Sí, siempre","No, puede causar más daño","Solo con ácidos","Solo con bases"],"answer":"No, puede causar más daño"},
                {"question":"¿Qué hacer ante un golpe en la cabeza con pérdida de conciencia?","options":["Dar medicamentos","Acudir a urgencias inmediatamente","Dejar dormir sin supervisión","Aplicar hielo y listo"],"answer":"Acudir a urgencias inmediatamente"},
                {"question":"¿Los primeros auxilios reemplazan la atención médica profesional?","options":["Sí","No, son una medida temporal","Solo en adultos","Solo en emergencias menores"],"answer":"No, son una medida temporal"},
            ],
        ]

    # ── SEGURIDAD DIGITAL BÁSICA ──────────────
    def build_seguridad_digital(self):
        return [
            # Módulo 1: Contraseñas seguras
            [
                {"question":"¿Cuántos caracteres debe tener una contraseña segura mínimo?","options":["4","6","8","12 o más"],"answer":"12 o más"},
                {"question":"¿Cuál de estas contraseñas es más segura?","options":["123456","miperro","P@ssw0rd!2024#","contraseña"],"answer":"P@ssw0rd!2024#"},
                {"question":"¿Qué es la autenticación de dos factores (2FA)?","options":["Usar dos contraseñas iguales","Una capa extra de verificación además de la contraseña","Un antivirus doble","Dos correos electrónicos"],"answer":"Una capa extra de verificación además de la contraseña"},
                {"question":"¿Se debe reutilizar la misma contraseña en varios sitios?","options":["Sí, es más fácil","No, es un riesgo de seguridad","Solo en sitios confiables","Solo dos veces"],"answer":"No, es un riesgo de seguridad"},
                {"question":"¿Qué es un gestor de contraseñas?","options":["Una libreta física","Aplicación que almacena y genera contraseñas seguras","Un tipo de antivirus","Una contraseña maestra"],"answer":"Aplicación que almacena y genera contraseñas seguras"},
                {"question":"¿Con qué frecuencia se recomienda cambiar contraseñas importantes?","options":["Nunca","Cada 10 años","Cada 6–12 meses o si hay brecha","Solo cuando te pidan"],"answer":"Cada 6–12 meses o si hay brecha"},
                {"question":"¿Qué es una brecha de datos?","options":["Un error de tipeo","Exposición no autorizada de información personal","Un tipo de virus","Un fallo de internet"],"answer":"Exposición no autorizada de información personal"},
                {"question":"¿Es seguro guardar contraseñas en notas del teléfono sin cifrar?","options":["Sí, está bien","No, es inseguro","Solo si el teléfono tiene PIN","Depende del teléfono"],"answer":"No, es inseguro"},
                {"question":"¿Qué debe incluir una contraseña fuerte?","options":["Solo letras","Solo números","Letras, números y símbolos","Solo mayúsculas"],"answer":"Letras, números y símbolos"},
                {"question":"¿Cuál de estos es un ejemplo de información que NO debe estar en tu contraseña?","options":["Símbolos especiales","Tu fecha de nacimiento","Letras mayúsculas","Números aleatorios"],"answer":"Tu fecha de nacimiento"},
            ],
            # Módulo 2: Phishing y estafas
            [
                {"question":"¿Qué es el phishing?","options":["Un tipo de virus informático","Técnica para robar información engañando al usuario","Un tipo de contraseña","Un antivirus"],"answer":"Técnica para robar información engañando al usuario"},
                {"question":"¿Cómo se detecta un correo de phishing?","options":["Por su diseño bonito","Errores ortográficos, remitente raro, urgencia falsa","Si llega en la noche","Por el asunto del correo"],"answer":"Errores ortográficos, remitente raro, urgencia falsa"},
                {"question":"¿Qué hacer si recibes un correo sospechoso que pide tus datos?","options":["Responder con tus datos","Ignorarlo y reportarlo como spam","Hacer clic para ver qué es","Reenviarlo a amigos"],"answer":"Ignorarlo y reportarlo como spam"},
                {"question":"¿Los bancos piden contraseñas por correo?","options":["Sí, siempre","No, nunca solicitan datos sensibles por correo","Solo los bancos digitales","A veces"],"answer":"No, nunca solicitan datos sensibles por correo"},
                {"question":"¿Qué es el smishing?","options":["Phishing por correo","Phishing por mensaje de texto SMS","Un tipo de malware","Un antivirus móvil"],"answer":"Phishing por mensaje de texto SMS"},
                {"question":"¿Qué es el vishing?","options":["Virus de video","Phishing por llamada telefónica","Una red segura","Un tipo de antivirus"],"answer":"Phishing por llamada telefónica"},
                {"question":"¿Es seguro hacer clic en links de correos no esperados?","options":["Sí, si el diseño parece real","No, pueden llevar a sitios falsos","Solo si el enlace es corto","Solo si conoces el remitente"],"answer":"No, pueden llevar a sitios falsos"},
                {"question":"¿Qué indica un sitio web seguro en la barra del navegador?","options":["Un candado y https://","Solo www","El logo de la empresa","El color azul de la URL"],"answer":"Un candado y https://"},
                {"question":"¿Qué hacer si ya caíste en un phishing?","options":["No hacer nada","Cambiar contraseñas y avisar a tu banco inmediatamente","Formatear el teléfono","Ignorarlo"],"answer":"Cambiar contraseñas y avisar a tu banco inmediatamente"},
                {"question":"¿Las redes sociales pueden ser usadas para phishing?","options":["No, son seguras","Sí, a través de mensajes falsos o perfiles clonados","Solo Facebook","Solo en computadora"],"answer":"Sí, a través de mensajes falsos o perfiles clonados"},
            ],
            # Módulo 3: Privacidad en redes sociales
            [
                {"question":"¿Qué información NO debes publicar en redes sociales?","options":["Tu película favorita","Dirección exacta de tu casa","Un paisaje bonito","Tu equipo de fútbol"],"answer":"Dirección exacta de tu casa"},
                {"question":"¿Qué es la huella digital?","options":["Tu huella dactilar en pantalla","Rastro de datos que dejas en internet","Un tipo de contraseña","Tu firma electrónica"],"answer":"Rastro de datos que dejas en internet"},
                {"question":"¿Qué hacer con perfiles de redes sociales que no reconoces?","options":["Aceptarlos siempre","No aceptarlos y reportarlos","Aceptarlos si tienen foto","Ignorarlos sin reportar"],"answer":"No aceptarlos y reportarlos"},
                {"question":"¿Es recomendable tener el perfil público si eres menor de edad?","options":["Sí, para tener más amigos","No, es más seguro tenerlo privado","Solo en Instagram","Solo con supervisión"],"answer":"No, es más seguro tenerlo privado"},
                {"question":"¿Qué son los permisos de las apps?","options":["Precios de suscripción","Autorizaciones que das a las apps para acceder a tu info","Los términos de uso","Las notificaciones"],"answer":"Autorizaciones que das a las apps para acceder a tu info"},
                {"question":"¿Debes revisar los permisos que piden las apps?","options":["No, son automáticos","Sí, y solo dar los necesarios","Solo en apps de pago","Solo en apps nuevas"],"answer":"Sí, y solo dar los necesarios"},
                {"question":"¿Qué riesgo tiene compartir tu ubicación en tiempo real?","options":["Ninguno","Permite que otros sepan dónde estás en todo momento","Solo gasta batería","Solo gasta datos"],"answer":"Permite que otros sepan dónde estás en todo momento"},
                {"question":"¿Qué es el grooming en internet?","options":["Un tipo de virus","Manipulación de menores por adultos en línea con fines de abuso","Una red social","Un tipo de phishing"],"answer":"Manipulación de menores por adultos en línea con fines de abuso"},
                {"question":"¿Qué hacer si alguien te acosa en línea?","options":["Responder con insultos","Bloquear, reportar y contarle a un adulto de confianza","Ignorarlo siempre","Cerrar tu cuenta"],"answer":"Bloquear, reportar y contarle a un adulto de confianza"},
                {"question":"¿Es seguro conectarse a Wi-Fi público sin protección?","options":["Sí, siempre","No, pueden interceptar tu información","Solo en cafeterías","Solo para redes sociales"],"answer":"No, pueden interceptar tu información"},
            ],
            # Módulo 4: Malware y protección del dispositivo
            [
                {"question":"¿Qué es un malware?","options":["Un programa de diseño","Software malicioso que daña o roba información","Un tipo de red","Un sistema operativo"],"answer":"Software malicioso que daña o roba información"},
                {"question":"¿Qué es un virus informático?","options":["Un malware que se replica y daña archivos","Un tipo de antivirus","Un archivo de texto","Una aplicación de pago"],"answer":"Un malware que se replica y daña archivos"},
                {"question":"¿Qué es un ransomware?","options":["Antivirus gratuito","Malware que cifra tus archivos y pide rescate","Un tipo de correo","Una red privada"],"answer":"Malware que cifra tus archivos y pide rescate"},
                {"question":"¿Qué hace un antivirus?","options":["Acelera el internet","Detecta y elimina software malicioso","Guarda contraseñas","Cifra archivos"],"answer":"Detecta y elimina software malicioso"},
                {"question":"¿Con qué frecuencia actualizar el sistema operativo?","options":["Nunca","Solo una vez al año","Cuando haya actualizaciones de seguridad disponibles","Solo si el equipo va lento"],"answer":"Cuando haya actualizaciones de seguridad disponibles"},
                {"question":"¿Es seguro descargar programas de sitios no oficiales?","options":["Sí, ahorra dinero","No, pueden contener malware","Solo programas pequeños","Solo en computadora"],"answer":"No, pueden contener malware"},
                {"question":"¿Qué es un spyware?","options":["Un tipo de antivirus","Malware que espía tus actividades sin que lo sepas","Un programa de diseño","Una red privada"],"answer":"Malware que espía tus actividades sin que lo sepas"},
                {"question":"¿Qué hacer si tu dispositivo se infecta?","options":["Ignorarlo","Desconectarlo de internet y usar antivirus o buscar ayuda técnica","Formatearlo siempre sin más","Solo reiniciarlo"],"answer":"Desconectarlo de internet y usar antivirus o buscar ayuda técnica"},
                {"question":"¿Las actualizaciones de apps corrigen problemas de seguridad?","options":["No, solo agregan funciones","Sí, incluyen parches de seguridad","Solo en iPhones","Solo en Android"],"answer":"Sí, incluyen parches de seguridad"},
                {"question":"¿Es recomendable hacer respaldos (backups) de tu información?","options":["No, ocupa espacio","Sí, ante pérdida o ataque puedes recuperar tus datos","Solo en empresas","Solo en computadoras"],"answer":"Sí, ante pérdida o ataque puedes recuperar tus datos"},
            ],
            # Módulo 5: Navegación segura y buenas prácticas
            [
                {"question":"¿Qué es una VPN?","options":["Un tipo de antivirus","Red privada virtual que cifra tu conexión a internet","Un navegador web","Un tipo de contraseña"],"answer":"Red privada virtual que cifra tu conexión a internet"},
                {"question":"¿Para qué sirve una VPN?","options":["Para navegar más rápido","Para proteger tu privacidad en redes inseguras","Para descargar más rápido","Para bloquear anuncios"],"answer":"Para proteger tu privacidad en redes inseguras"},
                {"question":"¿Qué es el modo incógnito en un navegador?","options":["Una VPN integrada","No guarda historial local, pero no oculta tu IP del proveedor","Un antivirus integrado","Una forma de navegar anónimamente en internet"],"answer":"No guarda historial local, pero no oculta tu IP del proveedor"},
                {"question":"¿Qué significa HTTPS en una URL?","options":["La página es gratuita","La conexión está cifrada y es más segura","El sitio es oficial","El sitio tiene antivirus"],"answer":"La conexión está cifrada y es más segura"},
                {"question":"¿Qué son las cookies?","options":["Archivos de malware","Pequeños archivos que guardan información de tu navegación","Contraseñas guardadas","Un tipo de antivirus"],"answer":"Pequeños archivos que guardan información de tu navegación"},
                {"question":"¿Es seguro guardar tarjetas de crédito en sitios web de compras?","options":["Sí, es conveniente","Depende del sitio; solo en sitios con HTTPS y reputados","Siempre es inseguro","Solo en apps"],"answer":"Depende del sitio; solo en sitios con HTTPS y reputados"},
                {"question":"¿Qué es el cifrado de datos?","options":["Comprimir archivos","Proceso que convierte datos en código ilegible sin la clave","Eliminar archivos","Hacer copias de seguridad"],"answer":"Proceso que convierte datos en código ilegible sin la clave"},
                {"question":"¿Qué hacer antes de vender o reciclar un dispositivo?","options":["Solo apagarlo","Borrar todos los datos y hacer un restablecimiento de fábrica","Solo quitarle la SIM","Solo formatear la tarjeta SD"],"answer":"Borrar todos los datos y hacer un restablecimiento de fábrica"},
                {"question":"¿La educación en ciberseguridad es responsabilidad de todos?","options":["No, solo de expertos en TI","Sí, todos los usuarios deben conocer buenas prácticas","Solo de empresas","Solo de jóvenes"],"answer":"Sí, todos los usuarios deben conocer buenas prácticas"},
                {"question":"¿Qué es la ingeniería social en ciberseguridad?","options":["Diseño de redes","Manipulación psicológica para obtener información o acceso","Programación de sistemas","Instalación de antivirus"],"answer":"Manipulación psicológica para obtener información o acceso"},
            ],
        ]


MainApp().run()
