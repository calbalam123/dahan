import re
import time
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
try:
    import pyperclip
except Exception:
    pyperclip = None

try:
    from pywinauto import Desktop
    from pywinauto.keyboard import send_keys
except Exception:
    Desktop = None
    send_keys = None

APP_TITLE = "가국경제봇"
POLL_SECONDS = 1.2
OPENCHAT_RE = re.compile(r"^https?://open\.kakao\.com/o/[A-Za-z0-9_-]+/?$")

HELP = """[ 💰 가국경제봇 ]

├ >도움말
├ >계좌
├ >출석
├ >송금 @닉네임 금액
├ >시장
├ >상품시장
├ >부동산목록 1
├ >공장목록
├ >주식시장
├ >국가목록
└ >인구

[ 🏛️ 국가 ]
├ >국가정보
├ >국고
├ >GDP
├ >경제
├ >세금
├ >예산
├ >재정
├ >정책
└ >세계경제
"""

class Economy:
    def __init__(self):
        self.treasury = 100_000
        self.population = 30_000_000
        self.gdp = 1_500
        self.approval = 70
        self.tax = 18
        self.turn = 1
        self.balances = {}

    def command(self, text, user="플레이어"):
        t = text.strip()
        if not t.startswith(">"):
            return None
        cmd = t[1:].strip()
        low = cmd.lower()
        if low in ("도움말", "도움말 국가", "도움말 경제"):
            return HELP
        if low == "계좌":
            bal = self.balances.get(user, 100_000)
            self.balances.setdefault(user, bal)
            return f"💳 {user}님의 계좌\n━━━━━━━━━━━━━━\n💰 잔액: {bal:,}원"
        if low == "출석":
            self.balances[user] = self.balances.get(user, 100_000) + 10_000
            return f"📅 출석 완료!\n💰 +10,000원\n현재 잔액: {self.balances[user]:,}원"
        if low == "국가정보":
            return self.info()
        if low == "국고":
            return f"💰 대한제국 국고: {self.treasury:,}억 원"
        if low == "인구":
            return f"👥 인구: {self.population:,}명"
        if low == "gdp":
            return f"📈 GDP: {self.gdp:,}조 원"
        if low in ("경제", "경제지표"):
            return f"📊 경제지표\n━━━━━━━━━━━━━━\nGDP {self.gdp:,}조\n성장률 +3.2%\n국고 {self.treasury:,}억\n물가 2.1%\n세율 {self.tax}%"
        if low == "시장":
            return "📈 시장\n━━━━━━━━━━━━━━\nKOSPI형 지수 2,840\n제조업 +1.8%\n건설 +0.7%\nIT +2.4%"
        if low == "상품시장":
            return "🛒 상품시장\n━━━━━━━━━━━━━━\n쌀 4,200원\n철강 820,000원\n석유 1,320원\n전자부품 58,000원"
        if low.startswith("세금 "):
            try:
                value = int(cmd.split()[1])
                if 0 <= value <= 100:
                    self.tax = value
                    return f"🧾 세율 변경\n현재 세율: {self.tax}%"
            except ValueError:
                pass
            return "사용법: >세금 15"
        if low == "정책":
            return "📜 정책\n━━━━━━━━━━━━━━\n>정책 산업육성\n>정책 교육투자\n>정책 인프라"
        if low.startswith("정책 "):
            name = cmd[3:].strip()
            effects = {"산업육성":(-8000,2,0), "교육투자":(-4000,0,3), "인프라":(-5000,1,1)}
            if name in effects:
                money, gdp, approval = effects[name]
                self.treasury += money
                self.gdp += gdp
                self.approval = min(100, self.approval + approval)
                return f"🏛️ 정책 시행: {name}\n국고 {money:+,}억\nGDP {gdp:+}조\n지지율 {approval:+}%"
            return "존재하지 않는 정책입니다. >정책 으로 목록을 확인하세요."
        if low == "세계경제":
            return "🌏 세계경제\n━━━━━━━━━━━━━━\n세계 성장률 +2.8%\n무역지수 114\n원자재지수 103"
        if low == "국가목록":
            return "🌏 국가목록\n━━━━━━━━━━━━━━\n🇰🇷 대한제국\n🏳️ 동해연방\n🏳️ 북방공화국\n🏳️ 태평양연합"
        return "❓ 알 수 없는 명령어입니다.\n>도움말 을 입력하세요."

    def info(self):
        return (f"👑 대한제국 국가정보\n━━━━━━━━━━━━━━\n"
                f"💰 국고 {self.treasury:,}억 원\n👥 인구 {self.population:,}명\n"
                f"📈 GDP {self.gdp:,}조 원\n😊 지지율 {self.approval}%\n"
                f"🧾 세율 {self.tax}%\n📅 {self.turn}년차")

class KakaoBridge:
    def __init__(self, target):
        self.target = target
        self.window = None

    def connect(self):
        if Desktop is None:
            raise RuntimeError("pywinauto가 설치되지 않았습니다.")
        wins = Desktop(backend="uia").windows(title_re=".*카카오톡.*")
        if not wins:
            raise RuntimeError("카카오톡 PC가 실행 중인지 확인하세요.")
        self.window = wins[0]
        self.window.set_focus()
        return True

    def open_room(self):
        if not self.window:
            self.connect()
        if OPENCHAT_RE.match(self.target):
            webbrowser.open(self.target)
            time.sleep(2.5)
            self.window.set_focus()
            time.sleep(0.8)
            return
        send_keys("^f")
        time.sleep(.4)
        send_keys("^a")
        if pyperclip is None:
            raise RuntimeError("클립보드 모듈이 없습니다.")
        pyperclip.copy(self.target)
        send_keys("^v")
        time.sleep(.8)
        send_keys("{ENTER}")
        time.sleep(.8)

    def send(self, message):
        if not self.window:
            self.connect()
        self.window.set_focus()
        if pyperclip is None:
            raise RuntimeError("클립보드 모듈이 없습니다.")
        pyperclip.copy(message)
        send_keys("^v")
        send_keys("{ENTER}")
        time.sleep(0.15)
        return True

    def visible_text(self):
        if not self.window:
            self.connect()
        texts = []
        seen = set()
        try:
            for c in self.window.descendants():
                try:
                    s = c.window_text().strip()
                except Exception:
                    continue
                if s and s not in seen:
                    seen.add(s)
                    texts.append(s)
        except Exception:
            pass
        return texts

    def command_messages(self):
        found = []
        for value in self.visible_text():
            for line in value.splitlines():
                line = line.strip()
                if line.startswith(">"):
                    found.append(line)
        result = []
        seen = set()
        for cmd in found:
            if cmd not in seen:
                seen.add(cmd)
                result.append(cmd)
        return result

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("920x650")
        self.minsize(760, 560)
        self.configure(bg="#0b1422")
        self.bot = Economy()
        self.bridge = None
        self.running = False
        self.last_seen = set()
        self.build()

    def build(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background="#0b1422")
        style.configure("TLabel", background="#0b1422", foreground="#e9eef5")
        style.configure("TButton", padding=8)
        style.configure("Header.TLabel", font=("Malgun Gothic", 18, "bold"), foreground="#e6c679")

        top = ttk.Frame(self); top.pack(fill="x", padx=18, pady=15)
        ttk.Label(top, text="💰 가국경제봇", style="Header.TLabel").pack(side="left")
        self.status = ttk.Label(top, text="● 연결 안 됨")
        self.status.pack(side="right")

        config = ttk.Frame(self); config.pack(fill="x", padx=18)
        ttk.Label(config, text="카카오톡 오픈채팅 URL:").pack(side="left")
        self.room = ttk.Entry(config)
        self.room.pack(side="left", fill="x", expand=True, padx=8)
        self.room.insert(0, "https://open.kakao.com/o/...")
        ttk.Button(config, text="오픈채팅 열기", command=self.connect).pack(side="left")
        ttk.Button(config, text="봇 시작/중지", command=self.toggle).pack(side="left", padx=5)

        self.log = tk.Text(self, bg="#101c2d", fg="#dce6f2", insertbackground="white",
                           relief="flat", font=("Consolas", 10), wrap="word")
        self.log.pack(fill="both", expand=True, padx=18, pady=15)
        self.log.insert("end", "가국경제봇 준비 완료.\n오픈채팅 URL을 입력한 뒤 [오픈채팅 열기]를 누르세요.\n")
        self.log.configure(state="disabled")

        bottom = ttk.Frame(self); bottom.pack(fill="x", padx=18, pady=(0,15))
        self.manual = ttk.Entry(bottom)
        self.manual.pack(side="left", fill="x", expand=True)
        self.manual.bind("<Return>", lambda e: self.manual_send())
        ttk.Button(bottom, text="카톡으로 보내기", command=self.manual_send).pack(side="left", padx=8)

    def write_log(self, text):
        self.log.configure(state="normal")
        self.log.insert("end", text + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def connect(self):
        target = self.room.get().strip()
        if not OPENCHAT_RE.match(target):
            messagebox.showerror("URL 오류", "카카오톡 오픈채팅 URL을 입력하세요.\n예: https://open.kakao.com/o/gLC22zPi")
            return
        try:
            self.bridge = KakaoBridge(target)
            self.bridge.connect()
            self.bridge.open_room()
            self.status.configure(text="● 오픈채팅 연결됨")
            self.write_log(f"오픈채팅 열기 완료: {target}")
        except Exception as e:
            messagebox.showerror("연결 실패", str(e))
            self.write_log("연결 실패: " + str(e))

    def manual_send(self):
        text = self.manual.get().strip()
        if not text:
            return
        try:
            if not self.bridge:
                self.connect()
            self.bridge.send(text)
            self.write_log("보냄: " + text)
            self.manual.delete(0, "end")
        except Exception as e:
            self.write_log("전송 실패: " + str(e))

    def toggle(self):
        if self.running:
            self.running = False
            self.status.configure(text="● 중지됨")
            self.write_log("봇 중지")
            return
        try:
            if not self.bridge:
                self.connect()
            self.running = True
            self.status.configure(text="● 봇 실행 중")
            self.write_log("봇 실행 시작")
            threading.Thread(target=self.loop, daemon=True).start()
        except Exception as e:
            messagebox.showerror("시작 실패", str(e))

    def loop(self):
        while self.running:
            try:
                candidates = self.bridge.command_messages()
                for cmd in candidates[-8:]:
                    if cmd in self.last_seen:
                        continue
                    self.last_seen.add(cmd)
                    reply = self.bot.command(cmd)
                    if reply:
                        self.bridge.send(reply)
                        self.after(0, self.write_log, f"수신: {cmd}\n응답: {reply}")
                if len(self.last_seen) > 300:
                    self.last_seen = set(list(self.last_seen)[-100:])
            except Exception as e:
                self.after(0, self.write_log, "자동수신 오류: " + str(e))
            time.sleep(POLL_SECONDS)

if __name__ == "__main__":
    App().mainloop()
