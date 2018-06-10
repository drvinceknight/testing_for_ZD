import axelrod as axl

def main():
    N = len([s for s in axl.strategies if not s.classifier["long_run_time"]])
    with open("main.tex", "w") as f:
        f.write(str(N))


if __name__ == "__main__":
    main()
