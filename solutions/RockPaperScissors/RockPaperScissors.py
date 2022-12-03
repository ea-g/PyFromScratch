from random import choice


class RockPaperScissors:
    def __init__(self, wins: int = 0, ties: int = 0, losses: int = 0, record: list[tuple[str, str]] = None):
        self.wins = wins
        self.ties = ties
        self.losses = losses
        self.record = record

    def shoot(self):
        # implement the basic game here!
        user = input("Rock? paper? or scissors?")
        while user.lower() not in ["rock", "paper", "scissors"]:
            user = input("Input MUST BE rock, paper, or scissors! Try again: ")
        computer = choice(["rock", "paper", "scissors"])
        wins = [("rock", "scissors"), ("paper", "rock"), ("scissors", "paper")]
        rec = (user, computer)
        if not self.record:
            self.record = [rec]
        else:
            self.record.append(rec)
        if rec in wins:
            self.wins += 1
        elif user == computer:
            self.ties += 1
        else:
            self.losses += 1

    def results(self):
        N = len(self.record)
        freqs = [self.wins/N, self.ties/N, self.losses/N]
        return freqs

    def play(self):
        print("Welcome to RockPaperScissors+!! w[*_*]w ")
        print("To win, your relative win frequency (num of wins/total games) must be > than random chance (1/3)")
        print("We recommend at least 6 games")
        pa = True
        while pa:
            self.shoot()
            pa = input("Play again? y/n")
            if pa == 'y':
                pa = True
            else:
                pa = False
        freqs = self.results()
        if freqs[0] > 1/3:
            print("You WIN!")
        else:
            print("You LOSE!")
        print(f'Win, tie, and loss frequencies:{freqs}')

if __name__ == "__main__":
    a = RockPaperScissors()
    a.play()
        
