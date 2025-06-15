class BaseballElimination:
    def __init__(self):
        self._teams = []
        self._team_index = {}
        self._wins = []
        self._losses = []
        self._remaining = []
        self._against = []

        n = int(input())
        self._n = n
        self._against = [[0] * n for _ in range(n)]

        for i in range(n):
            data = input().split()
            name = data[0]
            self._teams.append(name)
            self._team_index[name] = i
            self._wins.append(int(data[1]))
            self._losses.append(int(data[2]))
            self._remaining.append(int(data[3]))
            for j in range(n):
                self._against[i][j] = int(data[4 + j])

    def number_of_teams(self):
        return self._n

    def teams(self):
        return list(self._teams)

    def wins(self, team):
        self._validate_team(team)
        return self._wins[self._team_index[team]]

    def losses(self, team):
        self._validate_team(team)
        return self._losses[self._team_index[team]]

    def remaining(self, team):
        self._validate_team(team)
        return self._remaining[self._team_index[team]]

    def against(self, team1, team2):
        self._validate_team(team1)
        self._validate_team(team2)
        i = self._team_index[team1]
        j = self._team_index[team2]
        return self._against[i][j]

    def is_eliminated(self, team):
        self._validate_team(team)
        x = self._team_index[team]
        max_wins = self._wins[x] + self._remaining[x]

        for i in range(self._n):
            if self._wins[i] > max_wins:
                return True
        return False

    def certificate_of_elimination(self, team):
        self._validate_team(team)
        x = self._team_index[team]
        max_wins = self._wins[x] + self._remaining[x]
        R = []

        for i in range(self._n):
            if self._wins[i] > max_wins:
                R.append(self._teams[i])

        return R if R else None

    def _validate_team(self, team):
        if team not in self._team_index:
            raise ValueError(f"Time '{team}' não encontrado na divisão.")

# Exemplo de uso
if __name__ == '__main__':
    be = BaseballElimination()
    for team in be.teams():
        if be.is_eliminated(team):
            R = be.certificate_of_elimination(team)
            print(f"{team} está eliminado pelo subconjunto R = {{ {' '.join(R)} }}")
        else:
            print(f"{team} não está eliminado")
