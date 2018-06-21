from invoke import task
import pathlib

def run_main(c, dir_path, processdata=False):
    """
    Run `python main.py` in all sub dirs of `dir_path`.
    """
    for directory in dir_path.glob("*"):
        print(directory)
        command = f"cd {directory}; python main.py"
        if processdata:
            command += " process_data"
        c.run(command)

@task
def img(c, processdata=False):
    """
    Create all image assets
    """
    img_path = pathlib.Path("./assets/img")
    run_main(c, img_path, processdata=processdata)

@task
def tex(c):
    """
    Create all tex assets
    """
    tex_path = pathlib.Path("./assets/tex")
    run_main(c, tex_path)

@task
def assets(c, processdata=False):
    """
    Create all assets
    """
    img(c, process_data=process_data)
    tex(c)

@task
def process(c):
    """
    Process all raw data
    """
    for tournament_type in ("std", "noisy", "probend"):
        for player_group in ("full", "stewart_plotkin"):
            directory = "./data/processed/"
            print(tournament_type, player_group)
            c.run(f"cd {directory}; python main.py {tournament_type} {player_group}")

@task
def pdf(c, clean=False):
    """
    Compile the pdf
    """
    if clean:
        c.run("latexmk -c")
    c.run("latexmk --xelatex main.tex")

@task
def build(c):
    """
    Process all data and compile the pdf
    """
    process(c)
    assets(c, processdata=True)
    pdf(c)
