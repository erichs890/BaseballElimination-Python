import networkx as nx

class BaseballElimination:
    def __init__(self, filename):
        self.teams = []
        self.team_index = {}
        self.wins = []
        self.losses = []
        self.remaining = []
        self.against = []

        with open(filename) as f:
            n = int(f.readline())
            self.n = n
            self.against = [[0]*n for _ in range(n)]
            for i in range(n):
                data = f.readline().split()
                name = data[0]
                self.teams.append(name)
                self.team_index[name] = i
                self.wins.append(int(data[1]))
                self.losses.append(int(data[2]))
                self.remaining.append(int(data[3]))
                for j in range(n):
                    self.against[i][j] = int(data[4 + j])

    def is_eliminated(self, team):
        x = self.team_index[team]
        max_wins = self.wins[x] + self.remaining[x]

        # Eliminação trivial
        for i in range(self.n):
            if self.wins[i] > max_wins:
                return True

        # Eliminação não trivial
        G = nx.DiGraph()
        s = 's'
        t = 't'

        game_nodes = []
        team_nodes = []

        total_capacity = 0

        # Criar nós de jogos
        for i in range(self.n):
            for j in range(i+1, self.n):
                if i == x or j == x:
                    continue
                game = f'game_{i}_{j}'
                game_nodes.append(game)
                G.add_edge(s, game, capacity=self.against[i][j])
                total_capacity += self.against[i][j]

                G.add_edge(game, f'team_{i}', capacity=float('inf'))
                G.add_edge(game, f'team_{j}', capacity=float('inf'))

        # Criar nós de times
        for i in range(self.n):
            if i == x:
                continue
            cap = max_wins - self.wins[i]
            G.add_edge(f'team_{i}', t, capacity=max(0, cap))
            team_nodes.append(f'team_{i}')

        # Rodar fluxo máximo
        flow_value, flow_dict = nx.maximum_flow(G, s, t)

        return flow_value < total_capacity

    def certificate_of_elimination(self, team):
        if not self.is_eliminated(team):
            return None
        x = self.team_index[team]
        max_wins = self.wins[x] + self.remaining[x]

        # Repetir a construção do grafo como acima
        G = nx.DiGraph()
        s = 's'
        t = 't'

        for i in range(self.n):
            for j in range(i+1, self.n):
                if i == x or j == x:
                    continue
                game = f'game_{i}_{j}'
                G.add_edge(s, game, capacity=self.against[i][j])
                G.add_edge(game, f'team_{i}', capacity=float('inf'))
                G.add_edge(game, f'team_{j}', capacity=float('inf'))

        for i in range(self.n):
            if i == x:
                continue
            cap = max_wins - self.wins[i]
            G.add_edge(f'team_{i}', t, capacity=max(0, cap))

        cut_value, partition = nx.minimum_cut(G, s, t)
        reachable, non_reachable = partition
        R = []

        for node in reachable:
            if node.startswith("team_"):
                i = int(node.split("_")[1])
                R.append(self.teams[i])

        return R

if __name__ == '__main__':
    arquivo = input("Digite o nome do arquivo:\n")
    be = BaseballElimination(arquivo)
    print("")
    for team in be.teams:
        if be.is_eliminated(team):
            R = be.certificate_of_elimination(team)
            print(f"{team} está eliminado pelo subconjunto R = {{ {' '.join(R)} }}")
        else:
            print(f"{team} não está eliminado")
