import torch
import random
from collections import deque
from modell_pytorch import Linear_QNet, QTrainer

MAX_MEM = 100_000
BATCH_SIZE = 1000


class Agent:

    def __init__(self, epsilon, learning_rate, epsilon_verfall_spiele, gamma):
        self.n_games = 0
        self.epsilon = epsilon
        self.epsilon_verfall_spiele = epsilon_verfall_spiele
        self.epsilon_verfall = epsilon / epsilon_verfall_spiele
        self.gamma = gamma
        self.memory = deque(maxlen=MAX_MEM) # popleft
        self.modell = Linear_QNet(11, 256, 3)
        self.trainer = QTrainer(self.modell, lr=learning_rate, gamma=self.gamma)

    def sichere_erinnerungen(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def trainiere_langzeit_gedaechtnis(self):
        if len(self.memory) > BATCH_SIZE:
            stichprobe = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            stichprobe = self.memory

        zustaende, aktionen, belohnungen, naechste_zustaende, game_over = zip(*stichprobe)
        self.trainer.trainingsschritt(zustaende, aktionen, belohnungen, naechste_zustaende, game_over)

    def trainiere_kurzzeit_gedaechtnis(self, zustand, aktion, belohnung, naechster_zustand, game_over):
        self.trainer.trainingsschritt(zustand, aktion, belohnung, naechster_zustand, game_over)

    def naechste_aktion(self, zustand):
        # random moves: tradeoff exploration / exploitation

        print("naechst_aktion-----")

        naechste_aktion = [0, 0, 0]
        if random.random() < self.epsilon:
            auswahl = random.randint(0, 2)
            naechste_aktion[auswahl] = 1

        else:
            zustand0 = torch.tensor(zustand, dtype = torch.float)
            vorhersage = self.modell(zustand0)
            auswahl = torch.argmax(vorhersage).item()
            naechste_aktion[auswahl] = 1

        return naechste_aktion
