"""
Rule-Based Rice Pest Identification and Control Recommendation System
For Malaysian Rice Cultivation
Using Python with CLIPSpy for Forward Chaining Inference

Author: Expert System Project - TES6313
"""

import clips
import os
import sys


class RicePestExpertSystem:
    """Expert System for Rice Pest Identification and Control Recommendations"""

    def __init__(self):
        self.env = clips.Environment()
        self.symptoms_db = self._initialize_symptoms_database()
        self.pests_info = self._initialize_pests_info()
        self._load_rules()

    def _initialize_symptoms_database(self):
        """Initialize the symptom database with descriptions"""
        return {
            # Brown Planthopper symptoms
            "hopper-burn": {
                "description": "Plants appear burnt/scorched in circular patches (hopper burn)",
                "pest_hint": "Brown Planthopper",
            },
            "yellowing-drying": {
                "description": "Yellowing and drying of plants from bottom upwards",
                "pest_hint": "Brown Planthopper",
            },
            "circular-patches": {
                "description": "Circular patches of dead/dying plants in the field",
                "pest_hint": "Brown Planthopper",
            },
            "honeydew-sooty-mold": {
                "description": "Honeydew secretion with black sooty mold on plants",
                "pest_hint": "Brown Planthopper",
            },
            "plant-base-insects": {
                "description": "Small brown insects visible at the base of plants",
                "pest_hint": "Brown Planthopper",
            },
            # Yellow Stem Borer symptoms
            "dead-heart": {
                "description": "Central shoot/tiller dies and turns brown (dead heart) - vegetative stage",
                "pest_hint": "Yellow Stem Borer",
            },
            "central-shoot-withered": {
                "description": "Central leaf whorl unfolds incompletely and withers",
                "pest_hint": "Yellow Stem Borer",
            },
            "stem-bore-holes": {
                "description": "Visible bore holes at the stem base with frass",
                "pest_hint": "Yellow Stem Borer",
            },
            "white-head": {
                "description": "White/empty panicles that can be easily pulled out (white head) - reproductive stage",
                "pest_hint": "Yellow Stem Borer",
            },
            "empty-panicles": {
                "description": "Panicles are chaffy/empty with no grain filling",
                "pest_hint": "Yellow Stem Borer",
            },
            "egg-mass-on-leaves": {
                "description": "Yellowish-brown hairy egg masses on leaf blades",
                "pest_hint": "Yellow Stem Borer",
            },
            "larval-feeding-marks": {
                "description": "Larvae feeding marks on leaf sheath before boring",
                "pest_hint": "Yellow Stem Borer",
            },
            # Rice Leaf Folder symptoms
            "folded-leaves": {
                "description": "Leaves are folded longitudinally with silk threads",
                "pest_hint": "Rice Leaf Folder",
            },
            "leaf-scraping": {
                "description": "Scraping damage on leaf surface (green tissue removed)",
                "pest_hint": "Rice Leaf Folder",
            },
            "whitish-streaks": {
                "description": "Whitish/transparent streaks on damaged leaves",
                "pest_hint": "Rice Leaf Folder",
            },
            "tubular-folded-leaf": {
                "description": "Leaf rolled into a tubular structure",
                "pest_hint": "Rice Leaf Folder",
            },
            "larvae-inside-leaf": {
                "description": "Green caterpillar/larvae found inside folded leaves",
                "pest_hint": "Rice Leaf Folder",
            },
            # Rice Gall Midge symptoms
            "silver-shoot": {
                "description": "Silver-white hollow tillers (silver shoot/onion shoot)",
                "pest_hint": "Rice Gall Midge",
            },
            "onion-leaf-gall": {
                "description": "Gall formation with onion leaf-like appearance",
                "pest_hint": "Rice Gall Midge",
            },
            "stunted-tillers": {
                "description": "Stunted growth of affected tillers",
                "pest_hint": "Rice Gall Midge",
            },
            "no-panicle-emergence": {
                "description": "Affected tillers fail to produce panicles",
                "pest_hint": "Rice Gall Midge",
            },
            "elongated-leaf-sheath": {
                "description": "Elongated and pale green leaf sheath",
                "pest_hint": "Rice Gall Midge",
            },
            # Rice Bug symptoms
            "foul-smell": {
                "description": "Strong foul/unpleasant smell in the field",
                "pest_hint": "Rice Bug",
            },
            "empty-grains": {
                "description": "Empty or partially filled grains at maturity",
                "pest_hint": "Rice Bug",
            },
            "discolored-grains": {
                "description": "Discolored spots on grains (feeding marks)",
                "pest_hint": "Rice Bug",
            },
        }

    def _initialize_pests_info(self):
        """Initialize pest information database"""
        return {
            "Brown Planthopper": {
                "scientific_name": "Nilaparvata lugens",
                "description": "Small brown sucking insect that feeds on plant sap at the base of rice plants",
                "damage_type": "Causes hopper burn - plants dry up and appear scorched",
                "favorable_conditions": "High humidity, excessive nitrogen use, continuous flooding",
                "affected_stage": "All growth stages, especially tillering to heading",
            },
            "Yellow Stem Borer": {
                "scientific_name": "Scirpophaga incertulas",
                "description": "Larvae bore into rice stems causing dead hearts and white heads",
                "damage_type": "Dead heart in vegetative stage, White head in reproductive stage",
                "favorable_conditions": "Staggered planting, presence of stubbles, high nitrogen",
                "affected_stage": "Tillering (dead heart) and heading (white head) stages",
            },
            "Rice Leaf Folder": {
                "scientific_name": "Cnaphalocrocis medinalis",
                "description": "Caterpillar folds leaves and feeds on green tissue inside",
                "damage_type": "Reduces photosynthetic area, whitish streaks on leaves",
                "favorable_conditions": "High humidity, shaded/dense canopy, excessive nitrogen",
                "affected_stage": "Vegetative to reproductive stages",
            },
            "Rice Gall Midge": {
                "scientific_name": "Orseolia oryzae",
                "description": "Maggot causes gall formation producing silver shoots",
                "damage_type": "Silver shoot/onion leaf - tillers become tubular and fail to produce panicles",
                "favorable_conditions": "Cloudy weather, high humidity, late planting",
                "affected_stage": "Seedling to tillering stages",
            },
            "Rice Bug": {
                "scientific_name": "Leptocorisa oratorius",
                "description": "Slender green/brown bug that sucks sap from developing grains",
                "damage_type": "Empty/partially filled grains, reduced grain quality",
                "favorable_conditions": "Weedy fields, staggered harvesting, presence of wild grasses",
                "affected_stage": "Flowering to grain filling stages",
            },
        }

    def _load_rules(self):
        """Load CLIPS rules from file"""
        rules_file = os.path.join(os.path.dirname(__file__), "rice_pest_rules.clp")
        if os.path.exists(rules_file):
            self.env.load(rules_file)
        else:
            print(f"Warning: Rules file not found at {rules_file}")
            print("Creating rules from embedded knowledge base...")
            self._create_embedded_rules()

    def _create_embedded_rules(self):
        """Create rules directly if CLP file not found"""
        self.env.build("""
        (deftemplate symptom
           (slot name (type SYMBOL))
           (slot present (type SYMBOL) (allowed-symbols yes no unknown) (default unknown))
           (slot cf (type FLOAT) (range 0.0 1.0) (default 0.0)))
        """)

        self.env.build("""
        (deftemplate pest
           (slot name (type STRING))
           (slot scientific-name (type STRING))
           (slot cf (type FLOAT) (range 0.0 1.0) (default 0.0))
           (slot identified (type SYMBOL) (allowed-symbols yes no) (default no)))
        """)

    def reset_system(self):
        """Reset the expert system for a new consultation"""
        self.env.reset()

    def assert_symptom(self, symptom_name, present=True, certainty=0.8):
        """Assert a symptom fact with certainty factor"""
        present_val = "yes" if present else "no"
        cf = min(1.0, max(0.0, certainty))
        fact_str = f"(symptom (name {symptom_name}) (present {present_val}) (cf {cf}))"
        self.env.assert_string(fact_str)

    def run_inference(self):
        """Run the inference engine"""
        self.env.run()

    def get_identified_pests(self):
        """Get all identified pests from facts"""
        pests = []
        for fact in self.env.facts():
            if str(fact.template.name) == "pest":
                pest_data = {}
                for slot in fact.template.slots:
                    pest_data[slot.name] = fact[slot.name]
                if pest_data.get("identified") == clips.Symbol("yes"):
                    pests.append(pest_data)
        return sorted(pests, key=lambda x: x.get("cf", 0), reverse=True)

    def get_control_recommendations(self, pest_name):
        """Get control recommendations for a specific pest"""
        recommendations = {
            "chemical": [],
            "biological": [],
            "cultural": [],
            "mechanical": [],
        }

        for fact in self.env.facts():
            if str(fact.template.name) == "control-recommendation":
                if fact["pest-name"] == pest_name:
                    control_type = str(fact["control-type"])
                    rec = {
                        "recommendation": fact["recommendation"],
                        "priority": fact["priority"],
                    }
                    if control_type in recommendations:
                        recommendations[control_type].append(rec)

        for key in recommendations:
            recommendations[key] = sorted(
                recommendations[key], key=lambda x: x["priority"]
            )

        return recommendations

    def display_symptoms_menu(self):
        """Display symptoms menu for user selection"""
        print("\n" + "=" * 70)
        print("RICE PEST SYMPTOM CHECKLIST")
        print("=" * 70)

        symptom_groups = {}
        for sym_id, sym_info in self.symptoms_db.items():
            hint = sym_info["pest_hint"]
            if hint not in symptom_groups:
                symptom_groups[hint] = []
            symptom_groups[hint].append((sym_id, sym_info["description"]))

        idx = 1
        symptom_list = []
        for pest, symptoms in symptom_groups.items():
            print(f"\n--- Symptoms often associated with {pest} ---")
            for sym_id, desc in symptoms:
                print(f"  [{idx}] {desc}")
                symptom_list.append(sym_id)
                idx += 1

        return symptom_list

    def interactive_diagnosis(self):
        """Run interactive diagnosis session"""
        print("\n" + "=" * 70)
        print("  RICE PEST IDENTIFICATION AND CONTROL RECOMMENDATION SYSTEM")
        print("  Rule-Based Expert System for Malaysian Rice Cultivation")
        print("=" * 70)

        symptom_list = self.display_symptoms_menu()

        print("\n" + "-" * 70)
        print("INSTRUCTIONS:")
        print("- Enter symptom numbers separated by commas (e.g., 1,3,5)")
        print("- For each symptom, you'll be asked for confidence level (0-100%)")
        print("- Enter 'q' to quit, 'r' to restart")
        print("-" * 70)

        while True:
            user_input = input(
                "\nEnter observed symptom numbers (or 'q' to quit): "
            ).strip()

            if user_input.lower() == "q":
                print("\nThank you for using the Rice Pest Expert System. Goodbye!")
                break
            elif user_input.lower() == "r":
                self.reset_system()
                print("\nSystem reset. Starting new consultation...")
                continue

            try:
                selections = [int(x.strip()) for x in user_input.split(",")]
            except ValueError:
                print("Invalid input. Please enter numbers separated by commas.")
                continue

            self.reset_system()

            observed_symptoms = []
            for sel in selections:
                if 1 <= sel <= len(symptom_list):
                    symptom_id = symptom_list[sel - 1]

                    cf_input = input(
                        f"Confidence for '{self.symptoms_db[symptom_id]['description'][:50]}...' (0-100%, default 80): "
                    ).strip()

                    try:
                        cf = float(cf_input.replace("%", "")) / 100 if cf_input else 0.8
                        cf = min(1.0, max(0.0, cf))
                    except ValueError:
                        cf = 0.8

                    self.assert_symptom(symptom_id, present=True, certainty=cf)
                    observed_symptoms.append((symptom_id, cf))
                else:
                    print(f"Invalid symptom number: {sel}")

            if not observed_symptoms:
                print("No valid symptoms selected. Please try again.")
                continue

            print("\n" + "=" * 70)
            print("RUNNING INFERENCE ENGINE...")
            print("=" * 70)

            self.run_inference()

            identified_pests = self.get_identified_pests()

            if identified_pests:
                print("\n" + "=" * 70)
                print("DIAGNOSIS RESULTS")
                print("=" * 70)

                for pest in identified_pests:
                    pest_name = pest.get("name", "Unknown")
                    sci_name = pest.get("scientific-name", "")
                    cf = pest.get("cf", 0)

                    print(f"\n{'*' * 60}")
                    print(f"IDENTIFIED PEST: {pest_name}")
                    print(f"Scientific Name: {sci_name}")
                    print(f"Confidence Level: {cf * 100:.1f}%")
                    print(f"{'*' * 60}")

                    if pest_name in self.pests_info:
                        info = self.pests_info[pest_name]
                        print(f"\nDescription: {info['description']}")
                        print(f"Damage Type: {info['damage_type']}")
                        print(f"Favorable Conditions: {info['favorable_conditions']}")
                        print(f"Affected Stage: {info['affected_stage']}")

                    print("\n--- CONTROL RECOMMENDATIONS ---")
                    recs = self.get_control_recommendations(pest_name)

                    for control_type in [
                        "cultural",
                        "mechanical",
                        "biological",
                        "chemical",
                    ]:
                        if recs[control_type]:
                            print(f"\n[{control_type.upper()} CONTROL]")
                            for rec in recs[control_type]:
                                print(
                                    f"  Priority {rec['priority']}: {rec['recommendation']}"
                                )

                    print(f"\n{'*' * 60}")
            else:
                print("\n" + "-" * 70)
                print("NO PEST COULD BE IDENTIFIED")
                print("-" * 70)
                print(
                    "The symptoms you described do not match any known pest patterns."
                )
                print("Suggestions:")
                print("  1. Observe more symptoms and try again")
                print("  2. Check if the symptoms are due to diseases instead of pests")
                print("  3. Consult with local agricultural extension officers")

            print("\n" + "-" * 70)
            cont = (
                input("Do you want to perform another diagnosis? (y/n): ")
                .strip()
                .lower()
            )
            if cont != "y":
                print("\nThank you for using the Rice Pest Expert System. Goodbye!")
                break


def main():
    """Main function to run the expert system"""
    print("\n" + "#" * 70)
    print("#" + " " * 68 + "#")
    print("#    RULE-BASED RICE PEST IDENTIFICATION AND CONTROL SYSTEM" + " " * 8 + "#")
    print("#    Expert System for Malaysian Rice Cultivation" + " " * 18 + "#")
    print("#" + " " * 68 + "#")
    print("#" * 70)

    try:
        expert_system = RicePestExpertSystem()
        expert_system.interactive_diagnosis()
    except Exception as e:
        print(f"\nError initializing expert system: {e}")
        print("\nMake sure you have clipspy installed:")
        print("  pip install clipspy")
        sys.exit(1)


if __name__ == "__main__":
    main()
