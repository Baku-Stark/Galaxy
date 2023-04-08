import os

try:
    from rich import print as rprint

except ModuleNotFoundError:
    os.system('pip install rich')

def message():
    rprint(
        """
        [blue] ___          _     _[/blue]                 
        [blue]| _ \  _  _  | |_  | |_    ___   _ _[/blue]  
        [blue]|  _/ | || | |  _| | ' \  / _ \ | ' \ [/blue] 
        [blue]|_|    \_, |  \__| |_||_| \___/ |_||_|[/blue]
        [blue]        |__/          [/blue]

        [blue] _  __  _[/blue]      
        [blue]| |/ / (_) __ __  _  _ [/blue]
        [blue]| ' <  | | \ V / | || |[/blue]
        [blue]|_|\_\ |_|  \_/   \_, |[/blue]
        [blue]                |__/[/blue]
        """
    )

def sucess():
    status_title = "[ON-MODE]"
    status_message = "[bold green]KIVY[/bold green] application successfully created!"
    rprint(f'[on white] [black] {status_title} [/black] [/on white][on blue] [bold]{status_message}[/bold] [/on blue]')

def error(message: str):
    status_title = "[ERROR]"
    status_message = f"[bold green]KIVY[/bold green] {message}"
    rprint(f'[on white] [black] {status_title} [/black] [/on white][on blue] [bold]{status_message}[/bold] [/on blue]')
    rprint(f'[on white] [black] {status_title} [/black] [/on white][on red] [bold]{status_message}[/bold] [/on red]')
