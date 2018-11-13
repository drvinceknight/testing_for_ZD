from invoke import task


@task
def unpack(c):
    """
    Unpack downloaded `raw.tar.gz` file
    """
    c.run("tar -xzf raw.tar.gz --directory .")


@task
def get(c):
    """
    Download the data from the online archive
    """
    c.run(
        "wget https://zenodo.org/record/1040129/files/data.tar.gz?download=1 -O raw.tar.gz"
    )


@task
def data(c):
    """
    Download fixation probability data.
    """
    print("Downloading data")
    get(c)
    print("Unpacking data")
    unpack(c)
