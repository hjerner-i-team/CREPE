# This file will keep track of which start the primary dataloop.
from .modus import PrimaryDataLoopModus, PrimaryDataLoopModusEnum

def main():
    m = PrimaryDataLoopModus()
    print(m)    
if __name__ == "__main__":
    main()
