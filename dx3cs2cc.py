import requests
import pyperclip
import json
import sys
import os
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

def cs2cc(vgm_url):
    html_text = requests.get(vgm_url).text
    soup = BeautifulSoup(html_text, 'html.parser')

    # character_name
    character_name = soup.find('input', {'name': 'data_title'})

    # 能力値・HP
    NP1 = soup.find('input', {'name': 'NP1'}) # 肉体
    NP2 = soup.find('input', {'name': 'NP2'}) # 感覚
    NP3 = soup.find('input', {'name': 'NP3'}) # 精神
    NP4 = soup.find('input', {'name': 'NP4'}) # 社会
    NP5 = soup.find('input', {'name': 'NP5'}) # HP
    NP6 = soup.find('input', {'name': 'NP6'}) # 侵蝕
    NP7 = soup.find('input', {'name': 'NP7'}) # 行動
    NP8 = soup.find('input', {'name': 'NP8'}) # 移動

    # ライフパス
    works_name = soup.find('input', {'name': 'works_name'})
    cover_name = soup.find('input', {'name': 'cover_name'})
    birth_name = soup.find('input', {'name': 'birth_name'})
    think_name = soup.find('input', {'name': 'think_name'})
    shutuji_name = soup.find('input', {'name': 'shutuji_name'})
    keiken_name = soup.find('input', {'name': 'keiken_name'})
    kaikou_name = soup.find('input', {'name': 'kaikou_name'})

    # 技能
    skill_total = soup.find_all('input',{'name': 'skill_total[]'})
    skill_memo = soup.find_all('input',{'name': 'skill_memo[]'})
    skill_list = ['白兵','回避','運転','射撃','知覚','芸術','RC','意志','知識','交渉','調達','情報']

    # パーソナルデータ
    pc_name = soup.find('input', {'name': 'pc_name'})
    pc_codename = soup.find('input', {'name': 'pc_codename'})
    shuzoku = soup.find('input', {'name': 'shuzoku'})
    age = soup.find('input', {'name': 'age'})
    sex = soup.find('input', {'name': 'sex'})

    # create_memo
    memo = ''
    if len(works_name.get('value')) != 0:
        memo += works_name.get('value') + "\n"
    if len(cover_name.get('value')) != 0:
        memo += cover_name.get('value') + "\n"
    if len(birth_name.get('value')) != 0:
        memo += birth_name.get('value') + "\n"
    if len(think_name.get('value')) != 0:
        memo += think_name.get('value') + "\n"
    if len(shutuji_name.get('value')) != 0:
        memo += shutuji_name.get('value') + "\n"
    if len(keiken_name.get('value')) != 0:
        memo += keiken_name.get('value') + "\n"
    if len(kaikou_name.get('value')) != 0:
        memo += kaikou_name.get('value') + "\n"

    # エフェクト
    # effect_name
    effect_name = soup.find_all('input', {'name': 'effect_name[]'})

    # effect_timing
    effect_timing = soup.find_all('input', {'name': 'effect_timing[]'})

    # effect_cost
    effect_cost = soup.find_all('input', {'name': 'effect_cost[]'})

    # effect_memo
    effect_memo = soup.find_all('input', {'name': 'effect_memo[]'})

    # 戦闘・武器・防具
    # arms_name
    arms_name = soup.find_all('input', {'name': 'arms_name[]'})
    # print(arms_name)

    # arms_hit
    arms_hit = soup.find_all('input', {'name': 'arms_hit[]'})
    # print(arms_hit)

    # arms_power
    arms_power = soup.find_all('input', {'name': 'arms_power[]'})
    # print(arms_power)

    command = ''

    command += "#シーン登場時に使用してください\n"
    command += "1d10\n　(入力例 :侵蝕率+7)\n"
    command += "#適宜使用して下さい\n"
    command += ":HP-\n:侵蝕率+\n:侵蝕DB+\n:ﾀﾞｲｽ修正+\n:達成修正+\n:攻撃修正+\n\n"

    command += "\n#技能判定\n"
    for list,total,skill_memo in zip(skill_list,skill_total,skill_memo):
        ginou = "(" + total.get('value').split("r")[0] + "+{侵蝕DB})dx10" + total.get('value').split("r")[1] + "　【" + list
        if len(skill_memo.get('value')) != 0:
            ginou += ":" + skill_memo.get('value')
        ginou += "】\n"
        command += ginou

    command += "#コンボ\n"
    for item1, item2 in zip(arms_name, arms_hit):
        command += "(" + item2.get('value').split("r")[0] + "+{侵蝕DB})dx{C値}" + item2.get('value').split("r")[1] + "　【" + item1.get('value') + "】\n"

    # ココフォリア
    chara_data = {
        "kind":"character",
        "data":{
            "name": character_name.get('value'),
            "memo": memo,
            "initiative": int(NP7.get('value')),
            "externalUrl": vgm_url,
            "status": [
                {"label": "HP","value": NP5.get('value'),"max": NP5.get('value')},
                {"label": "侵蝕率","value": NP6.get('value'),"max": 0},
                {"label": "侵蝕DB","value": 0,"max": 0},
                {"label": "C値","value": 8,"max": 0},
                {"label": "ﾀﾞｲｽ修正","value": 0,"max": 0},
                {"label": "達成修正","value": 0,"max": 0},
                {"label": "攻撃修正","value": 0,"max": 0},
                {"label": "ﾛｲｽ","value": 7,"max": 7},
            ],
            "params": [
                {"label": "肉体","value": NP1.get('value')},
                {"label": "感覚","value": NP2.get('value')},
                {"label": "精神","value": NP3.get('value')},
                {"label": "社会","value": NP4.get('value')},
            ],
            "commands": command
        }
    }

    pyperclip.copy(str(json.dumps(chara_data)))
    messagebox.showinfo('確認', 'クリップボードにコピーしました')

def temp_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

root = Tk()
root.title('キャラクター保管所 ココフォリアキャラコマ出力')
iconfile = temp_path('dx3.ico')
root.iconbitmap(default=iconfile)
root.resizable(False, False)
frame1 = ttk.Frame(root, padding=(32))
frame1.grid()

label1 = ttk.Label(frame1, text='URL', padding=(5, 2))
label1.grid(row=0, column=0, sticky=E)


# Username Entry
csurl = StringVar()
csurl_entry = ttk.Entry(
    frame1,
    textvariable=csurl,
    width=60)
csurl_entry.grid(row=0, column=1)

frame2 = ttk.Frame(frame1, padding=(0, 5))
frame2.grid(row=2, column=1, sticky=W)

button1 = ttk.Button(
    frame2, text='OK',
    command=lambda: cs2cc(csurl.get())
    )
button1.pack(side=LEFT)

button2 = ttk.Button(
    frame2, text='Cancel',
    command=lambda: sys.exit())
button2.pack(side=LEFT)

root.mainloop()