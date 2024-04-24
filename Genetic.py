import random
import chess

class Genetic:
    def __init__(self, population_size, mutation_rate):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.population = self.initialize_population()

    def initialize_population(self):
        population = []
        for _ in range(self.population_size):
            moves = []
            for _ in range(50):  # 50 moves per sequence
                move = random.choice(list(chess.Board().legal_moves))
                moves.append(move)
            population.append(moves)
        return population

    def evaluate_population(self):
        """ Get the score of the population"""
        scores = []
        for _ in self.population:
            # TODO: Evaluate the board
            scores.append(self.evaluate_board(self.board))
        return scores

    def evaluate_board(self, board):
        """ Get the score of the board"""
        score = 0
        for piece in board.piece_map().values():
            score += piece.piece_type
        return score

    def selection(self, scores):
        """ Select the best population """
        sorted_indices = sorted(range(len(scores)), key=lambda k: scores[k], reverse=True)
        selected_indices = sorted_indices[:self.population_size // 2]
        return [self.population[i] for i in selected_indices]

    def crossover(self, selected_population):
        """ Crossover the population """
        new_population = []
        for _ in range(self.population_size):
            parent1 = random.choice(selected_population)
            parent2 = random.choice(selected_population)
            child = []
            for i in range(len(parent1)):
                if random.random() < 0.5:
                    child.append(parent1[i])
                else:
                    child.append(parent2[i])
            new_population.append(child)
        return new_population

    def mutate(self, population):
        """ Mutate the population """
        for i in range(len(population)):
            for j in range(len(population[i])):
                if random.random() < self.mutation_rate:
                    legal_moves = list(self.board.legal_moves)
                    if legal_moves:
                        population[i][j] = random.choice(legal_moves)
                    else:
                        break 
        return population

    def get_best_moves(self, board):
        """ Return the best moves """
        self.board = board
        for _ in range(10):  # 10 generations
            scores = self.evaluate_population()
            selected_population = self.selection(scores)
            new_population = self.crossover(selected_population)
            self.population = self.mutate(new_population)
        best_moves = max(self.population, key=lambda moves: self.evaluate_board(self.board))
        for i in range(len(best_moves)):
            if not board.is_legal(best_moves[i]):
                best_moves = best_moves[:i]
                break
        return best_moves