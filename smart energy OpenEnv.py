"""
⚡ Smart Energy OpenEnv (Single File Version)
Python 3.11 Compatible
"""

import random
from typing import Dict, Tuple

# =========================
# 🌍 ENVIRONMENT
# =========================
class EnergyEnv:
    def __init__(self, seed: int = 42):
        random.seed(seed)
        self.max_steps = 50
        self.reset()

    def reset(self) -> Dict:
        self.battery = random.uniform(40, 60)
        self.solar = random.uniform(20, 80)
        self.load = random.uniform(30, 70)
        self.price = random.uniform(3, 8)
        self.steps = 0
        return self.state()

    def state(self) -> Dict:
        return {
            "battery": round(self.battery, 2),
            "solar": round(self.solar, 2),
            "load": round(self.load, 2),
            "price": round(self.price, 2),
            "step": self.steps
        }

    def step(self, action: str) -> Tuple[Dict, float, bool, Dict]:
        reward = 0.0

        # Dynamic changes
        self.solar = max(0, self.solar + random.uniform(-10, 10))
        self.load = max(0, self.load + random.uniform(-10, 10))
        self.price = max(1, self.price + random.uniform(-1, 1))

        if action == "use_solar":
            used = min(self.solar, self.load)
            reward += used * 0.05

        elif action == "use_battery":
            used = min(self.battery, self.load)
            self.battery -= used
            reward += used * 0.04

        elif action == "use_grid":
            cost = self.load * self.price * 0.02
            reward -= cost

        elif action == "store_energy":
            stored = min(self.solar, 10)
            self.battery = min(100, self.battery + stored)
            reward += stored * 0.02

        # Penalty
        if self.battery < 10:
            reward -= 2

        self.steps += 1
        done = self.steps >= self.max_steps

        return self.state(), round(reward, 3), done, {}


# =========================
# 🎯 TASKS
# =========================
def run_easy():
    env = EnergyEnv()
    state = env.reset()
    total_reward = 0

    for _ in range(20):
        action = "use_solar"
        state, reward, done, _ = env.step(action)
        total_reward += reward

    return total_reward


def run_medium():
    env = EnergyEnv()
    state = env.reset()
    total_reward = 0

    for _ in range(30):
        if state["solar"] > 50:
            action = "use_solar"
        elif state["battery"] > 40:
            action = "use_battery"
        else:
            action = "use_grid"

        state, reward, done, _ = env.step(action)
        total_reward += reward

    return total_reward


def run_hard():
    env = EnergyEnv()
    state = env.reset()
    total_reward = 0

    for _ in range(50):
        if state["price"] > 6:
            action = "use_battery"
        elif state["solar"] > state["load"]:
            action = "store_energy"
        else:
            action = "use_grid"

        state, reward, done, _ = env.step(action)
        total_reward += reward

    return total_reward


# =========================
# 📊 GRADER
# =========================
def grade(score: float, max_score: float = 100) -> float:
    normalized = score / max_score
    return max(0.0, min(1.0, normalized))


# =========================
# 🤖 BASELINE AGENT
# =========================
def policy(state):
    if state["solar"] > state["load"]:
        return "store_energy"
    elif state["battery"] > 30:
        return "use_battery"
    else:
        return "use_grid"


def run_baseline():
    env = EnergyEnv()
    state = env.reset()
    total_reward = 0

    while True:
        action = policy(state)
        state, reward, done, _ = env.step(action)
        total_reward += reward

        if done:
            break

    return total_reward


# =========================
# 🧾 OPENENV YAML (STRING)
# =========================
openenv_yaml = """
name: energy-management-env
description: Smart energy optimization environment

observation_space:
  battery: float
  solar: float
  load: float
  price: float
  step: int

action_space:
  type: discrete
  values:
    - use_solar
    - use_battery
    - use_grid
    - store_energy

tasks:
  - easy
  - medium
  - hard
"""


# =========================
# 🌐 SIMPLE CLI INTERFACE
# =========================
def main():
    print("⚡ Smart Energy OpenEnv")
    print("1. Run Easy Task")
    print("2. Run Medium Task")
    print("3. Run Hard Task")
    print("4. Run Baseline Agent")

    choice = input("Enter choice: ")

    if choice == "1":
        score = run_easy()
        print("Easy Score:", score, "Grade:", grade(score))

    elif choice == "2":
        score = run_medium()
        print("Medium Score:", score, "Grade:", grade(score))

    elif choice == "3":
        score = run_hard()
        print("Hard Score:", score, "Grade:", grade(score))

    elif choice == "4":
        score = run_baseline()
        print("Baseline Score:", score, "Grade:", grade(score))

    else:
        print("Invalid choice")


# =========================
# ▶️ RUN
# =========================
if __name__ == "__main__":
    main()
