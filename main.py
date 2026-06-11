import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.network.urlrequest import UrlRequest
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
import ssl

def calcular_1x2(id_casa, id_fora):
    f_casa = ((int(id_casa) % 7) + 1.0) * 0.70 * 1.10
    f_fora = ((int(id_fora) % 7) + 1.0) * 0.70
    peso = f_casa + f_fora + 1.0 
    return {"casa": int((f_casa / peso) * 100), "empate": int((1.0 / peso) * 100), "fora": int((f_fora / peso) * 100)}

class PredictorHome(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.lista_jogos_global = []
        with self.canvas.before:
            Color(0.02, 0.08, 0.2, 1)
            self.bg = RoundedRectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.atualizar_bg, size=self.atualizar_bg)
        
        self.btn_sync = Button(text="🔄 CARREGAR JOGOS", size_hint_y=None, height=dp(60), background_color=(0, 0.5, 0.8, 1))
        self.btn_sync.bind(on_press=self.sincronizar_tudo)
        self.add_widget(self.btn_sync)
        
        self.scroll = ScrollView()
        self.container = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(10), padding=dp(10))
        self.container.bind(minimum_height=self.container.setter('height'))
        self.scroll.add_widget(self.container)
        self.add_widget(self.scroll)

    def atualizar_bg(self, *args):
        self.bg.pos, self.bg.size = self.pos, self.size

    def sincronizar_tudo(self, *args):
        headers = {'x-rapidapi-host': 'v3.football.api-sports.io', 'x-rapidapi-key': 'cb68bec4ddaf9f52abed04e245718776'}
        UrlRequest("https://v3.football.api-sports.io/fixtures?date=2026-06-11", req_headers=headers, on_success=self.processar_lista, verify=False)

    def processar_lista(self, req, resultado):
        self.lista_jogos_global = resultado.get('response', [])
        self.renderizar_lista_ligas()

    def renderizar_lista_ligas(self):
        self.container.clear_widgets()
        ligas = sorted(list(set([j['league']['name'] for j in self.lista_jogos_global])))
        for liga in ligas:
            btn = Button(text=liga, size_hint_y=None, height=dp(60), background_color=(0.1, 0.3, 0.5, 1))
            btn.bind(on_press=lambda x, l=liga: self.renderizar_jogos_da_liga(l))
            self.container.add_widget(btn)

    def renderizar_jogos_da_liga(self, nome_liga):
        self.container.clear_widgets()
        btn_voltar = Button(text="⬅️ VOLTAR", size_hint_y=None, height=dp(50), background_color=(0.8, 0.2, 0.2, 1))
        btn_voltar.bind(on_press=lambda x: self.renderizar_lista_ligas())
        self.container.add_widget(btn_voltar)
        for j in [j for j in self.lista_jogos_global if j['league']['name'] == nome_liga]:
            el = j['fixture']['status']['elapsed']
            gc, gf = j['goals']['home'] or 0, j['goals']['away'] or 0
            st = j['fixture']['status']['short']
            if st in ["1H", "2H"]: info = f"[color=ffff00]LIVE {el}'[/color] | {gc}-{gf}"
            elif st == "FT": info = f"[color=ff3333]FIM[/color] | {gc}-{gf}"
            else: info = f"[color=00ccff]{j['fixture']['date'].split('T')[1][:5]}[/color]"
            p = calcular_1x2(j['teams']['home']['id'], j['teams']['away']['id'])
            
            card = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(90))
            with card.canvas.before:
                Color(0.05, 0.15, 0.35, 1)
                self.rect = RoundedRectangle(pos=card.pos, size=card.size, radius=[10])
            card.add_widget(Label(text=f"{j['teams']['home']['name']} vs {j['teams']['away']['name']}\n{info}\n[color=88ccff]C:{p['casa']}% | E:{p['empate']}% | F:{p['fora']}%[/color]", markup=True))
            self.container.add_widget(card)

class PredictorApp(App):
    def build(self): return PredictorHome()

if __name__ == '__main__': PredictorApp().run()
