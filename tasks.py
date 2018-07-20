from invoke import task
import pathlib

def run_main(c, dir_path, processdata=False):
    """
    Run `python main.py` in all sub dirs of `dir_path`.
    """
    for directory in dir_path.glob("*"):
        print(directory)
        if (directory / "main.py").is_file():
            command = f"cd {directory}; python main.py"
        else:
            command =  f"cd {directory}; latexmk --xelatex main.tex"
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
def tex(c, processdata=False):
    """
    Create all tex assets
    """
    tex_path = pathlib.Path("./assets/tex")
    run_main(c, tex_path, processdata=processdata)

@task
def pdf(c):
    """
    Create all pdf assets
    """
    tex_path = pathlib.Path("./assets/pdf")
    run_main(c, tex_path)

@task
def assets(c, processdata=False):
    """
    Create all assets
    """
    img(c, processdata=processdata)
    tex(c, processdata=processdata)
    pdf(c)

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
def main(c, clean=False):
    """
    Compile the main pdf
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
    main(c)

@task
def unpack(c):
    """
    Unpack downloaded `raw.tar.gz` file
    """
    c.run("tar -xzf raw.tar.gz --directory data")

@task
def get(c):
    """
    Download the data from the online archive
    """
    c.run("wget https://zenodo.org/record/1317619/files/raw.tar.gz?download=1 -O raw.tar.gz")

@task
def data(c):
    """
    Download and unpack data from online archive
    """
    print("Downloading data")
    get(c)
    print("Unpacking data")
    unpack(c)

@task
def test(c):
    """
    Test all packaged code and notebooks
    """
    c.run("pytest --nbval --current-env")
