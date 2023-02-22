import sys
import os
import cutie

LOGO = """
        ──────────────────────────────────
        ──────────────────────────────────
        ──────────────────────────────────
        ──────────█▀▀▀▀▀▀▀▀▀▀▀▀█──────────
        ──────────█ PASTELARIA █──────────
        ─────▒▒▒▒▒▒▒▒▒▒▒▒██▒▒██▒▒██▒▒██───
        ─────▒▒▒▒▒▒▒▒▒▒▒▒██▒▒██▒▒██▒▒██───
        ─────███┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼▐─────
        ─────███░███████▌░░▐▀▀▀▀▀▀▀█▐─────
        ─────███░▌░░▐░░░▌░░▐═══════█▐─────
        ─────███░▌░░▐░░░▌░░▐═══════█▐─────
        ─────███░███████▌░░▐═══════█▐─────
        ─────███░░░░░░░░░░░▐▀▀▀▀▀▀▀█▐─────
        ─────███░░░░░░░░░░░▐═══════█▐─────
        ─────███░░░░░░░░░░░▐═══════█▐─────
        ────▄████████████████████████▄────
        ──────────────────────────────────
        ──────────────────────────────────
        ──────────────────────────────────

        Bem-vindes a pastelaria, aqui 
        seu boilerplate é montado na
        hora!
"""


def help():
    print("Cárdapio:")
    print(" init                initialize app")
    print(" --framework         set framework, ex.: flask, django ou fastapi")
    print(" --database          set database")

def menu():
    print(LOGO)
    help()
    if cutie.prompt_yes_or_no("Vamos iniciar?"):
        name = input('Como posso te chamar? ')
        menu_f = [
            "Escolha o seu recheio (framework):",
            "FastApi",
            "Flask",
            "Django"
        ]
        
        menu_db = [
            "Agora um topping (database):",
            "mongodb",
            "mysql",
            "postgress"
        ]
        
        print(f'{name}, para iniciar informe as opções do cardápio abaixo: \n')
        framework = menu_f[cutie.select(menu_f, caption_indices=[0, 4, 4], selected_index=1)]
        database = menu_db[cutie.select(menu_db, caption_indices=[0, 4, 4], selected_index=1)]

        

run()