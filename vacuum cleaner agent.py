import time

class VacuumEnvironment:
    def __init__(self, status_a, status_b, initial_location):
        # Environment state: 'Clean' or 'Dirty'
        self.locations = {
            'A': status_a,
            'B': status_b
        }
        self.agent_location = initial_location
        self.performance_score = 0

    def get_percept(self):
        """Returns what the agent currently senses (Location, Status)."""
        current_loc = self.agent_location
        status = self.locations[current_loc]
        return current_loc, status

    def execute_action(self, action):
        """Modifies the environment based on the agent's action decision."""
        print(f"🤖 Agent Action: {action}")
        
        if action == "SUCK":
            if self.locations[self.agent_location] == "Dirty":
                self.locations[self.agent_location] = "Clean"
                self.performance_score += 10  # Reward points for cleaning
                print(f"🧹 Cleaned Location {self.agent_location}!")
            else:
                self.performance_score -= 1  # Penalty for wasting energy sucking air
                
        elif action == "RIGHT":
            if self.agent_location == 'A':
                self.agent_location = 'B'
            self.performance_score -= 1  # Movement cost
            
        elif action == "LEFT":
            if self.agent_location == 'B':
                self.agent_location = 'A'
            self.performance_score -= 1  # Movement cost

    def is_completely_clean(self):
        """Checks if all locations in the environment are Clean."""
        return self.locations['A'] == "Clean" and self.locations['B'] == "Clean"

    def display_state(self):
        """Prints the current layout status of the rooms."""
        print("\n--- Current Environment Status ---")
        for loc, status in self.locations.items():
            agent_marker = " <- [VACUUM HERE]" if self.agent_location == loc else ""
            print(f"  Location {loc}: {status}{agent_marker}")
        print(f"  Current Performance Score: {self.performance_score}")
        print("----------------------------------")


class ReflexVacuumAgent:
    def __init__(self):
        pass

    def decide_action(self, percept):
        """Simple Reflex Rule-Base: Map percept directly to an action choice."""
        location, status = percept
        
        # Rule 1: If the room is dirty, clean it immediately!
        if status == "Dirty":
            return "SUCK"
        # Rule 2: If clean and at Room A, move right to look for more dirt
        elif location == 'A':
            return "RIGHT"
        # Rule 3: If clean and at Room B, move left to check Room A
        elif location == 'B':
            return "LEFT"


# --- MAIN EXECUTION LOOP ---
if __name__ == "__main__":
    print("==============================================")
    print("        AI Reflex Vacuum Agent Simulator      ")
    print("==============================================")
    
    # Get initial settings from user inputs
    print("Set status for rooms (Type 'D' for Dirty, 'C' for Clean):")
    status_input_a = "Dirty" if input("  Status of Location A: ").strip().upper() == 'D' else "Clean"
    status_input_b = "Dirty" if input("  Status of Location B: ").strip().upper() == 'D' else "Clean"
    
    start_loc = input("Where should the vacuum start? (A/B): ").strip().upper()
    if start_loc not in ['A', 'B']:
        start_loc = 'A' # Default fallback state

    # Initialize Environment and Agent instances
    env = VacuumEnvironment(status_input_a, status_input_b, start_loc)
    agent = ReflexVacuumAgent()
    
    # Execution Simulation Loop
    step = 1
    max_steps = 5  # Prevention cap loop safety limit
    
    env.display_state()
    
    while step <= max_steps:
        print(f"\n▶️ SIMULATION STEP {step}")
        time.sleep(0.8) # 800ms pacing delay for legibility in IDLE console
        
        # 1. Agent senses the current state (Perception phase)
        current_percept = env.get_percept()
        print(f"👀 Agent Senses: Location={current_percept[0]}, Status={current_percept[1]}")
        
        # 2. Agent processes rule criteria matrix (Decision phase)
        chosen_action = agent.decide_action(current_percept)
        
        # 3. Environment changes state according to choice (Action phase)
        env.execute_action(chosen_action)
        
        # Render visual readout update
        env.display_state()
        
        # Performance check exit gate
        if env.is_completely_clean():
            print("\n🎉 Mission Accomplished! Both rooms are entirely clean.")
            break
            
        step += 1
    else:
        print("\n⏳ Simulation reached max processing step threshold cap limits.")
        
    print(f"🌟 Final Agent Efficiency Evaluation Score: {env.performance_score}")
