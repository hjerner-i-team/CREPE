# This file will keep track of which start the primary dataloop.
from .modus import PrimaryDataLoopModus, PrimaryDataLoopModusEnum
import primary_dataloops.example as PDexample

modus = PrimaryDataLoopModus()

def main():

    print(modus)
    PDexample.main()

if __name__ == "__main__":
    main()
