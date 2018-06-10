from invoke import task
import pathlib

def run_main(c, dir_path):
    """
    Run `python main.py` in all sub dirs of `dir_path`.
    """
    for directory in dir_path.glob("*"):
        print(directory)
        c.run(f"cd {directory}; python main.py")

@task
def img(c):
    """
    Create all image assets
    """
    img_path = pathlib.Path("./assets/img")
    run_main(c, img_path)

@task
def tex(c):
    """
    Create all tex assets
    """
    tex_path = pathlib.Path("./assets/tex")
    run_main(c, tex_path)

@task
def assets(c):
    """
    Create all assets
    """
    img(c)
    tex(c)

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
    assets(c)
    pdf(c)


# TODO Add task for processing data
