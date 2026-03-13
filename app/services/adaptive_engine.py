import math


def probability_correct(theta, difficulty):
    return 1 / (1 + math.exp(-(theta - difficulty)))


def update_ability(theta, difficulty, correct, lr=0.1):

    predicted = probability_correct(theta, difficulty)

    actual = 1 if correct else 0

    new_theta = theta + lr * (actual - predicted)

    return max(0.0, min(1.0, new_theta))
