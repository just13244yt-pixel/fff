import curses
import os
import shutil
from datetime import datetime

# --- KONFIGURATION & LISTEN ---
color_config = {
    "border": curses.COLOR_BLUE,
    "text": curses.COLOR_CYAN,
    "logo": curses.COLOR_BLUE,
    "bg": curses.COLOR_BLACK
}

HACK_LIST = [
    "aircrack-ng", "wifite", "nmap", "msfconsole", "sqlmap", "hydra", "bettercap", 
    "wireshark", "tshark", "driftnet", "beef-xss", "responder", "setoolkit", 
    "nikto", "gobuster", "hashcat", "crunch", "socat", "john", "macchanger"
]

GAMES_LIST = [
    "nsnake", "ninvaders", "pacman4console", "bastet", "greed", "2048-c"
]

def apply_colors():
    curses.start_color()
    curses.init_pair(1, color_config["logo"], color_config["bg"])   
    curses.init_pair(2, color_config["border"], color_config["bg"]) 
    curses.init_pair(3, color_config["text"], color_config["bg"])   
    curses.init_pair(4, curses.COLOR_GREEN, color_config["bg"])     

def draw_frame(stdscr, title):
    h, w = stdscr.getmaxyx()
    stdscr.bkgd(' ', curses.color_pair(3))
    stdscr.attron(curses.color_pair(2) | curses.A_BOLD)
    stdscr.border()
    stdscr.addstr(0, w//2 - len(title)//2, f" {title.upper()} ")
    status_text = f" NEW CHAT | {datetime.now().strftime('%H:%M:%S')} "
    stdscr.addstr(h-1, w - len(status_text) - 2, status_text, curses.color_pair(4))
    stdscr.attroff(curses.color_pair(2) | curses.A_BOLD)

# --- DATEI MANAGER (MIT EDITOR-FUNKTION) ---
def file_manager(stdscr):
    curr = os.getcwd()
    sel_idx = 0
    stdscr.nodelay(False)
    while True:
        stdscr.clear()
        draw_frame(stdscr, "DATEI-MANAGER")
        h, w = stdscr.getmaxyx()
        try: items = [".. (ZURÜCK)"] + os.listdir(curr)
        except: items = [".. (ZURÜCK)"]
        
        for i, item in enumerate(items[:h-10]):
            attr = curses.A_REVERSE if i == sel_idx else 0
            prefix = "[DIR] " if os.path.isdir(os.path.join(curr, item)) and item != ".. (ZURÜCK)" else "      "
            stdscr.addstr(4+i, 4, f"{prefix}{item[:w-15]}", attr | curses.color_pair(3))

        stdscr.addstr(h-3, 4, "[ENTER] Öffnen/Edit | [N] Neu | [D] Löschen | [Q] Exit", curses.A_BOLD)
        stdscr.refresh()
        k = stdscr.getch()
        
        if k in [ord('q'), ord('Q')]: break
        elif k == curses.KEY_UP and sel_idx > 0: sel_idx -= 1
        elif k == curses.KEY_DOWN and sel_idx < len(items)-1: sel_idx += 1
        elif k in [10, 13]: # ENTER
            path = os.path.join(curr, items[sel_idx])
            if items[sel_idx] == ".. (ZURÜCK)":
                curr = os.path.dirname(curr)
                sel_idx = 0
            elif os.path.isdir(path):
                curr = path
                sel_idx = 0
            else:
                # DATEI ÖFFNEN MIT NANO (für txt, py, etc.)
                curses.endwin()
                os.system(f"nano {path}")
                stdscr = curses.initscr()
                apply_colors()
                curses.curs_set(0)
        elif k in [ord('n'), ord('N')]:
            stdscr.addstr(h-2, 4, "Name der neuen Datei: "); curses.echo()
            name = stdscr.getstr().decode(); curses.noecho()
            if name: open(os.path.join(curr, name), 'a').close()
        elif k in [ord('d'), ord('D')]:
            if sel_idx > 0:
                path = os.path.join(curr, items[sel_idx])
                if os.path.isdir(path): shutil.rmtree(path)
                else: os.remove(path)

# --- LIST LAUNCHER ---
def list_launcher(stdscr, title, items):
    sel_idx = 0
    while True:
        stdscr.clear()
        draw_frame(stdscr, title)
        h, w = stdscr.getmaxyx()
        for i, item in enumerate(items[:h-10]):
            attr = curses.A_REVERSE if i == sel_idx else 0
            stdscr.addstr(4+i, 6, f" > {item} ", attr | curses.color_pair(3))
        stdscr.addstr(h-2, 6, "[ENTER] Starten | [Q] Zurück", curses.A_BOLD)
        stdscr.refresh()
        k = stdscr.getch()
        if k == curses.KEY_UP and sel_idx > 0: sel_idx -= 1
        elif k == curses.KEY_DOWN and sel_idx < len(items)-1: sel_idx += 1
        elif k in [10, 13]:
            curses.endwin()
            os.system(f"{items[sel_idx]} || (echo 'Fehler: {items[sel_idx]} nicht gefunden!' && sleep 2)")
            stdscr = curses.initscr(); apply_colors(); curses.curs_set(0)
        elif k in [ord('q'), ord('Q')]: break

# --- SETTINGS ---
def settings_menu(stdscr):
    opts = ["BORDER", "TEXT", "LOGO", "BG COLOR", "ZURÜCK"]
    colors = {"BLACK": 0, "BLUE": 4, "RED": 1, "GREEN": 2, "YELLOW": 3, "CYAN": 6, "WHITE": 7}
    sel_idx = 0
    while True:
        stdscr.clear()
        draw_frame(stdscr, "SETTINGS")
        for i, o in enumerate(opts):
            attr = curses.A_REVERSE if i == sel_idx else 0
            stdscr.addstr(10+i, 10, f" {o} ", attr)
        k = stdscr.getch()
        if k == curses.KEY_UP and sel_idx > 0: sel_idx -= 1
        elif k == curses.KEY_DOWN and sel_idx < len(opts)-1: sel_idx += 1
        elif k in [10, 13]:
            if sel_idx == 4: break
            c_sel = 0
            c_list = list(colors.keys())
            while True:
                stdscr.clear()
                draw_frame(stdscr, "COLOR")
                for j, c_name in enumerate(c_list):
                    attr = curses.A_REVERSE if j == c_sel else 0
                    stdscr.addstr(8+j, 15, c_name, attr)
                sk = stdscr.getch()
                if sk == curses.KEY_UP and c_sel > 0: c_sel -= 1
                elif sk == curses.KEY_DOWN and c_sel < len(c_list)-1: c_sel += 1
                elif sk in [10, 13]:
                    key = ["border", "text", "logo", "bg"][sel_idx]
                    color_config[key] = colors[c_list[c_sel]]
                    apply_colors(); break
                elif sk == ord('q'): break

# --- MAIN ---
def main(stdscr):
    apply_colors()
    curses.curs_set(0)
    stdscr.keypad(True)
    logo = [
        "      ██╗██╗   ██╗███████╗████████╗",
        "      ██║██║   ██║██╔════╝╚══██╔══╝",
        "      ██║██║   ██║███████╗   ██║   ",
        " ██   ██║██║   ██║╚════██║   ██║   ",
        " ╚██████╔╝╚██████╔╝███████║   ██║   ",
        "  ╚═════╝  ╚═════╝ ╚══════╝   ╚═╝   "
    ]
    menu = ["DATEI-MANAGER", "TERMINAL", "HACKING TOOLS", "GAMES", "SETTINGS"]
    sel = 0
    while True:
        stdscr.clear()
        draw_frame(stdscr, "JUST-OS V21")
        h, w = stdscr.getmaxyx()
        for i, l in enumerate(logo):
            stdscr.addstr(2+i, w//2-20, l, curses.color_pair(1))
        for i, m in enumerate(menu):
            attr = curses.A_REVERSE if i == sel else 0
            stdscr.addstr(10+i*2, w//2-10, f" [[ {m} ]] ", attr | curses.color_pair(3))
        k = stdscr.getch()
        if k == curses.KEY_UP and sel > 0: sel -= 1
        elif k == curses.KEY_DOWN and sel < len(menu)-1: sel += 1
        elif k in [10, 13]:
            if sel == 0: file_manager(stdscr)
            elif sel == 1: 
                curses.endwin()
                os.system("bash")
                stdscr = curses.initscr(); apply_colors(); curses.curs_set(0)
            elif sel == 2: list_launcher(stdscr, "TOOL REPOSITORY", HACK_LIST)
            elif sel == 3: list_launcher(stdscr, "GAMES ARCADE", GAMES_LIST)
            elif sel == 4: settings_menu(stdscr)

if __name__ == "__main__":
    curses.wrapper(main)