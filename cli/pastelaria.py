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
        seu boilerplate de API é montado na
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

    switcher = {
        'fastapi': handle_fast_api,
        'flask': handle_flask,
        'django': django
    }
    
    try:
        switcher[framework.lower()](database)
    except:
        click.echo('Framework não suportado, tente novamente com um destes: FastAPI, Flask ou Django')

def handle_fast_api(db):
    from frameworks.fastapi.framework import FastApiFramework
    fastapi = FastApiFramework()
    
    fastapi.create_fastapi_architecture(db)

def handle_flask(db):
    click.echo("Oh não! Essa é uma receita nova e ainda está sendo construída, logo mais no cardápio")

def django(db):
    click.echo("Oh não! Essa é uma receita nova e ainda está sendo construída, logo mais no cardápio")
    

cli.add_command(init)

if __name__ == "__main__":
    print(LOGO)
    print("Cárdapio:")
    print(" init                  initialize app")
    cli()
