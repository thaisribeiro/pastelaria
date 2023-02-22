import click
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

@click.group()
def cli():
    pass

def abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()
        
@click.command()
@click.option('--yes', is_flag=True, callback=abort_if_false,
              expose_value=False,
              prompt='Vamos começar o preparo?\n')
def init():
    name = input("Como posso te chamar? ")
    menu_f = [
        "Escolha seu recheio (framework):",
        "FastAPI",
        "Flask (em construção)",
        "Django (em construção)"
    ]

    menu_db = [
        "Agora um topping (database):",
        "mongoDB",
        "MySQL",
        "PostgreSQL",
        "Nenhum"
    ]

    click.echo(f"{name}, para inciarmos o preparo, informe as informações do cardápio abaixo: \n")
    
    framework = menu_f[cutie.select(menu_f, caption_indices=[0, 4, 4], selected_index=1)]
    database = menu_db[cutie.select(menu_db, caption_indices=[0, 5, 5], selected_index=1)]

    click.echo(framework)
    click.echo(database)


cli.add_command(init)

if __name__ == "__main__":
    print(LOGO)
    print("Cárdapio:")
    print(" init                initialize app")
    print(" --framework         set framework, ex.: FastAPI, Flask ou Django")
    print(" --database          set database, ex.: mongoDB, MySQL, PostgreSQL\n\n\n")

    cli()
