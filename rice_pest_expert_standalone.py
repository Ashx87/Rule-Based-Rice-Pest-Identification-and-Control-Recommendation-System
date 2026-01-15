"""
Rule-Based Rice Pest Identification and Control Recommendation System
For Malaysian Rice Cultivation
Standalone Python Implementation with Forward Chaining and Certainty Factor

This version does not require CLIPS installation.

Author: Expert System Project - TES6313
"""


class Symptom:
    """Represents a symptom with certainty factor"""

    def __init__(self, name, description, pest_hint, present=False, cf=0.0):
        self.name = name
        self.description = description
        self.pest_hint = pest_hint
        self.present = present
        self.cf = cf  # Certainty Factor (0.0 to 1.0)


class Pest:
    """Represents a pest with identification confidence"""

    def __init__(
        self,
        name,
        scientific_name,
        description,
        damage_type,
        favorable_conditions,
        affected_stage,
    ):
        self.name = name
        self.scientific_name = scientific_name
        self.description = description
        self.damage_type = damage_type
        self.favorable_conditions = favorable_conditions
        self.affected_stage = affected_stage


class ControlRecommendation:
    """Represents a control recommendation"""

    def __init__(self, pest_name, control_type, recommendation, priority):
        self.pest_name = pest_name
        self.control_type = control_type  # chemical, biological, cultural, mechanical
        self.recommendation = recommendation
        self.priority = priority  # 1 = highest priority


class Rule:
    """Represents an inference rule for pest identification"""

    def __init__(self, rule_id, pest_name, required_symptoms, rule_cf):
        self.rule_id = rule_id
        self.pest_name = pest_name
        self.required_symptoms = required_symptoms  # List of symptom names
        self.rule_cf = rule_cf  # Rule confidence factor


class RicePestExpertSystem:
    """Forward Chaining Expert System for Rice Pest Identification"""

    def __init__(self):
        self.symptoms = {}
        self.pests = {}
        self.rules = []
        self.control_recommendations = []
        self.identified_pests = {}  # pest_name -> combined CF
        self._initialize_knowledge_base()

    def _initialize_knowledge_base(self):
        """Initialize the knowledge base with symptoms, pests, rules, and recommendations"""
        self._init_symptoms()
        self._init_pests()
        self._init_rules()
        self._init_control_recommendations()

    def _init_symptoms(self):
        """Initialize symptom database"""
        symptom_data = [
            # Brown Planthopper symptoms
            (
                "hopper_burn",
                "Plants appear burnt/scorched in circular patches (hopper burn)",
                "Brown Planthopper",
            ),
            (
                "yellowing_drying",
                "Yellowing and drying of plants from bottom upwards",
                "Brown Planthopper",
            ),
            (
                "circular_patches",
                "Circular patches of dead/dying plants in the field",
                "Brown Planthopper",
            ),
            (
                "honeydew_sooty_mold",
                "Honeydew secretion with black sooty mold on plants",
                "Brown Planthopper",
            ),
            (
                "plant_base_insects",
                "Small brown insects visible at the base of plants",
                "Brown Planthopper",
            ),
            # Yellow Stem Borer symptoms
            (
                "dead_heart",
                "Central shoot/tiller dies and turns brown (dead heart) - vegetative stage",
                "Yellow Stem Borer",
            ),
            (
                "central_shoot_withered",
                "Central leaf whorl unfolds incompletely and withers",
                "Yellow Stem Borer",
            ),
            (
                "stem_bore_holes",
                "Visible bore holes at the stem base with frass",
                "Yellow Stem Borer",
            ),
            (
                "white_head",
                "White/empty panicles that can be easily pulled out (white head) - reproductive stage",
                "Yellow Stem Borer",
            ),
            (
                "empty_panicles",
                "Panicles are chaffy/empty with no grain filling",
                "Yellow Stem Borer",
            ),
            (
                "egg_mass_on_leaves",
                "Yellowish-brown hairy egg masses on leaf blades",
                "Yellow Stem Borer",
            ),
            (
                "larval_feeding_marks",
                "Larvae feeding marks on leaf sheath before boring",
                "Yellow Stem Borer",
            ),
            # Rice Leaf Folder symptoms
            (
                "folded_leaves",
                "Leaves are folded longitudinally with silk threads",
                "Rice Leaf Folder",
            ),
            (
                "leaf_scraping",
                "Scraping damage on leaf surface (green tissue removed)",
                "Rice Leaf Folder",
            ),
            (
                "whitish_streaks",
                "Whitish/transparent streaks on damaged leaves",
                "Rice Leaf Folder",
            ),
            (
                "tubular_folded_leaf",
                "Leaf rolled into a tubular structure",
                "Rice Leaf Folder",
            ),
            (
                "larvae_inside_leaf",
                "Green caterpillar/larvae found inside folded leaves",
                "Rice Leaf Folder",
            ),
            # Rice Gall Midge symptoms
            (
                "silver_shoot",
                "Silver-white hollow tillers (silver shoot/onion shoot)",
                "Rice Gall Midge",
            ),
            (
                "onion_leaf_gall",
                "Gall formation with onion leaf-like appearance",
                "Rice Gall Midge",
            ),
            (
                "stunted_tillers",
                "Stunted growth of affected tillers",
                "Rice Gall Midge",
            ),
            (
                "no_panicle_emergence",
                "Affected tillers fail to produce panicles",
                "Rice Gall Midge",
            ),
            (
                "elongated_leaf_sheath",
                "Elongated and pale green leaf sheath",
                "Rice Gall Midge",
            ),
            # Rice Bug symptoms
            ("foul_smell", "Strong foul/unpleasant smell in the field", "Rice Bug"),
            (
                "empty_grains",
                "Empty or partially filled grains at maturity",
                "Rice Bug",
            ),
            (
                "discolored_grains",
                "Discolored spots on grains (feeding marks)",
                "Rice Bug",
            ),
        ]

        for name, desc, hint in symptom_data:
            self.symptoms[name] = Symptom(name, desc, hint)

    def _init_pests(self):
        """Initialize pest database"""
        pest_data = [
            (
                "Brown Planthopper",
                "Nilaparvata lugens",
                "Small brown sucking insect that feeds on plant sap at the base of rice plants",
                "Causes hopper burn - plants dry up and appear scorched",
                "High humidity, excessive nitrogen use, continuous flooding",
                "All growth stages, especially tillering to heading",
            ),
            (
                "Yellow Stem Borer",
                "Scirpophaga incertulas",
                "Larvae bore into rice stems causing dead hearts and white heads",
                "Dead heart in vegetative stage, White head in reproductive stage",
                "Staggered planting, presence of stubbles, high nitrogen",
                "Tillering (dead heart) and heading (white head) stages",
            ),
            (
                "Rice Leaf Folder",
                "Cnaphalocrocis medinalis",
                "Caterpillar folds leaves and feeds on green tissue inside",
                "Reduces photosynthetic area, whitish streaks on leaves",
                "High humidity, shaded/dense canopy, excessive nitrogen",
                "Vegetative to reproductive stages",
            ),
            (
                "Rice Gall Midge",
                "Orseolia oryzae",
                "Maggot causes gall formation producing silver shoots",
                "Silver shoot/onion leaf - tillers become tubular and fail to produce panicles",
                "Cloudy weather, high humidity, late planting",
                "Seedling to tillering stages",
            ),
            (
                "Rice Bug",
                "Leptocorisa oratorius",
                "Slender green/brown bug that sucks sap from developing grains",
                "Empty/partially filled grains, reduced grain quality",
                "Weedy fields, staggered harvesting, presence of wild grasses",
                "Flowering to grain filling stages",
            ),
        ]

        for name, sci, desc, damage, cond, stage in pest_data:
            self.pests[name] = Pest(name, sci, desc, damage, cond, stage)

    def _init_rules(self):
        """Initialize inference rules with certainty factors"""
        self.rules = [
            # Brown Planthopper rules
            Rule(
                "R1",
                "Brown Planthopper",
                ["hopper_burn", "yellowing_drying", "circular_patches"],
                0.95,
            ),
            Rule(
                "R2",
                "Brown Planthopper",
                ["honeydew_sooty_mold", "plant_base_insects"],
                0.75,
            ),
            Rule(
                "R3", "Brown Planthopper", ["hopper_burn", "plant_base_insects"], 0.85
            ),
            # Yellow Stem Borer rules
            Rule(
                "R4",
                "Yellow Stem Borer",
                ["dead_heart", "central_shoot_withered", "stem_bore_holes"],
                0.92,
            ),
            Rule("R5", "Yellow Stem Borer", ["white_head", "empty_panicles"], 0.88),
            Rule(
                "R6",
                "Yellow Stem Borer",
                ["egg_mass_on_leaves", "larval_feeding_marks"],
                0.70,
            ),
            Rule("R7", "Yellow Stem Borer", ["dead_heart", "stem_bore_holes"], 0.85),
            # Rice Leaf Folder rules
            Rule(
                "R8",
                "Rice Leaf Folder",
                ["folded_leaves", "leaf_scraping", "whitish_streaks"],
                0.93,
            ),
            Rule(
                "R9",
                "Rice Leaf Folder",
                ["tubular_folded_leaf", "larvae_inside_leaf"],
                0.85,
            ),
            Rule(
                "R10", "Rice Leaf Folder", ["folded_leaves", "larvae_inside_leaf"], 0.90
            ),
            # Rice Gall Midge rules
            Rule("R11", "Rice Gall Midge", ["silver_shoot", "onion_leaf_gall"], 0.95),
            Rule(
                "R12",
                "Rice Gall Midge",
                ["stunted_tillers", "no_panicle_emergence", "elongated_leaf_sheath"],
                0.78,
            ),
            Rule(
                "R13", "Rice Gall Midge", ["silver_shoot", "no_panicle_emergence"], 0.88
            ),
            # Rice Bug rules
            Rule(
                "R14",
                "Rice Bug",
                ["foul_smell", "empty_grains", "discolored_grains"],
                0.85,
            ),
            Rule("R15", "Rice Bug", ["foul_smell", "empty_grains"], 0.75),
        ]

    def _init_control_recommendations(self):
        """Initialize control recommendations database"""
        rec_data = [
            # Brown Planthopper
            (
                "Brown Planthopper",
                "chemical",
                "Apply Imidacloprid 17.8 SL at 100-125 ml/ha or Thiamethoxam 25 WG at 100g/ha",
                1,
            ),
            (
                "Brown Planthopper",
                "chemical",
                "Apply Buprofezin 25 SC at 1.5-2.0 ml/L for nymph control",
                2,
            ),
            (
                "Brown Planthopper",
                "biological",
                "Conserve natural enemies: Cyrtorhinus lividipennis (mirid bug), Lycosa pseudoannulata (wolf spider)",
                1,
            ),
            (
                "Brown Planthopper",
                "cultural",
                "Avoid excessive nitrogen application; Use resistant varieties like MR219, MR220",
                1,
            ),
            (
                "Brown Planthopper",
                "mechanical",
                "Use light traps (15W bulb) to monitor and reduce adult population",
                2,
            ),
            # Yellow Stem Borer
            (
                "Yellow Stem Borer",
                "chemical",
                "Apply Cartap hydrochloride 4G at 25 kg/ha or Chlorantraniliprole 18.5 SC at 150 ml/ha",
                1,
            ),
            (
                "Yellow Stem Borer",
                "chemical",
                "Spray Fipronil 5 SC at 1.5-2.0 ml/L at tillering stage",
                2,
            ),
            (
                "Yellow Stem Borer",
                "biological",
                "Release Trichogramma japonicum egg parasitoid at 100,000/ha at weekly intervals",
                1,
            ),
            (
                "Yellow Stem Borer",
                "biological",
                "Conserve predators: Conocephalus longipennis, Anaxipha longipennis",
                2,
            ),
            (
                "Yellow Stem Borer",
                "cultural",
                "Remove and destroy stubbles after harvest; Synchronize planting in the area",
                1,
            ),
            (
                "Yellow Stem Borer",
                "mechanical",
                "Use pheromone traps (5/ha) for monitoring; Collect and destroy egg masses",
                1,
            ),
            # Rice Leaf Folder
            (
                "Rice Leaf Folder",
                "chemical",
                "Apply Chlorantraniliprole 18.5 SC at 150 ml/ha or Flubendiamide 39.35 SC at 50 ml/ha",
                1,
            ),
            (
                "Rice Leaf Folder",
                "chemical",
                "Spray Quinalphos 25 EC at 2 ml/L when damage exceeds economic threshold",
                2,
            ),
            (
                "Rice Leaf Folder",
                "biological",
                "Release Trichogramma chilonis at 50,000/ha; Conserve Apanteles spp. parasitoids",
                1,
            ),
            (
                "Rice Leaf Folder",
                "cultural",
                "Avoid excessive nitrogen; Maintain field sanitation; Remove grassy weeds",
                1,
            ),
            (
                "Rice Leaf Folder",
                "mechanical",
                "Use light traps to attract and kill adult moths",
                2,
            ),
            # Rice Gall Midge
            (
                "Rice Gall Midge",
                "chemical",
                "Apply Carbofuran 3G at 25-30 kg/ha in nursery or Fipronil 0.3G at 25 kg/ha",
                1,
            ),
            (
                "Rice Gall Midge",
                "chemical",
                "Seed treatment with Thiamethoxam 70 WS at 3g/kg seed",
                2,
            ),
            (
                "Rice Gall Midge",
                "biological",
                "Conserve Platygaster oryzae parasitoid; Maintain spider population in fields",
                1,
            ),
            (
                "Rice Gall Midge",
                "cultural",
                "Use resistant varieties; Early and synchronous planting; Destroy ratoon and volunteer plants",
                1,
            ),
            (
                "Rice Gall Midge",
                "mechanical",
                "Pull out and destroy affected tillers (silver shoots)",
                1,
            ),
            # Rice Bug
            (
                "Rice Bug",
                "chemical",
                "Apply Carbaryl 85 WP at 1.5 kg/ha or Lambda-cyhalothrin 5 EC at 300 ml/ha",
                1,
            ),
            (
                "Rice Bug",
                "biological",
                "Conserve egg parasitoids Gryon nixoni and Ooencyrtus spp.",
                1,
            ),
            (
                "Rice Bug",
                "cultural",
                "Remove weeds around bunds; Synchronize planting to avoid staggered harvesting",
                1,
            ),
            (
                "Rice Bug",
                "mechanical",
                "Collect bugs using sweep nets during early morning when less active",
                2,
            ),
        ]

        for pest, ctype, rec, pri in rec_data:
            self.control_recommendations.append(
                ControlRecommendation(pest, ctype, rec, pri)
            )

    def reset(self):
        """Reset the system for a new consultation"""
        for symptom in self.symptoms.values():
            symptom.present = False
            symptom.cf = 0.0
        self.identified_pests = {}

    def set_symptom(self, symptom_name, present=True, cf=0.8):
        """Set a symptom as present with a certainty factor"""
        if symptom_name in self.symptoms:
            self.symptoms[symptom_name].present = present
            self.symptoms[symptom_name].cf = min(1.0, max(0.0, cf))
            return True
        return False

    def combine_cf(self, cf1, cf2):
        """Combine two certainty factors using the standard formula"""
        if cf1 >= 0 and cf2 >= 0:
            return cf1 + cf2 * (1 - cf1)
        elif cf1 < 0 and cf2 < 0:
            return cf1 + cf2 * (1 + cf1)
        else:
            return (cf1 + cf2) / (1 - min(abs(cf1), abs(cf2)))

    def forward_chain(self):
        """Execute forward chaining inference"""
        self.identified_pests = {}
        fired_rules = []

        for rule in self.rules:
            all_present = True
            symptom_cfs = []

            for sym_name in rule.required_symptoms:
                if sym_name in self.symptoms and self.symptoms[sym_name].present:
                    symptom_cfs.append(self.symptoms[sym_name].cf)
                else:
                    all_present = False
                    break

            if all_present and symptom_cfs:
                avg_symptom_cf = sum(symptom_cfs) / len(symptom_cfs)
                final_cf = avg_symptom_cf * rule.rule_cf

                if rule.pest_name in self.identified_pests:
                    existing_cf = self.identified_pests[rule.pest_name]
                    self.identified_pests[rule.pest_name] = self.combine_cf(
                        existing_cf, final_cf
                    )
                else:
                    self.identified_pests[rule.pest_name] = final_cf

                fired_rules.append((rule.rule_id, rule.pest_name, final_cf))

        return fired_rules

    def get_recommendations(self, pest_name):
        """Get control recommendations for a pest"""
        recs = {"chemical": [], "biological": [], "cultural": [], "mechanical": []}

        for rec in self.control_recommendations:
            if rec.pest_name == pest_name:
                recs[rec.control_type].append(
                    {"recommendation": rec.recommendation, "priority": rec.priority}
                )

        for key in recs:
            recs[key] = sorted(recs[key], key=lambda x: x["priority"])

        return recs

    def display_symptoms_menu(self):
        """Display symptoms organized by pest hint"""
        print("\n" + "=" * 70)
        print("RICE PEST SYMPTOM CHECKLIST")
        print("=" * 70)

        groups = {}
        for sym in self.symptoms.values():
            if sym.pest_hint not in groups:
                groups[sym.pest_hint] = []
            groups[sym.pest_hint].append(sym)

        idx = 1
        symptom_list = []
        for pest_hint in sorted(groups.keys()):
            print(f"\n--- Symptoms often associated with {pest_hint} ---")
            for sym in groups[pest_hint]:
                print(f"  [{idx:2d}] {sym.description}")
                symptom_list.append(sym.name)
                idx += 1

        return symptom_list

    def run_interactive(self):
        """Run interactive consultation session"""
        print("\n" + "=" * 70)
        print("  RICE PEST IDENTIFICATION AND CONTROL RECOMMENDATION SYSTEM")
        print("  Rule-Based Expert System with Forward Chaining & Certainty Factor")
        print("  For Malaysian Rice Cultivation")
        print("=" * 70)

        while True:
            symptom_list = self.display_symptoms_menu()

            print("\n" + "-" * 70)
            print("INSTRUCTIONS:")
            print("- Enter symptom numbers separated by commas (e.g., 1,3,5)")
            print("- For each symptom, you'll be asked for confidence level (0-100%)")
            print("- Enter 'q' to quit")
            print("-" * 70)

            user_input = input(
                "\nEnter observed symptom numbers (or 'q' to quit): "
            ).strip()

            if user_input.lower() == "q":
                print("\nThank you for using the Rice Pest Expert System. Goodbye!")
                break

            try:
                selections = [
                    int(x.strip()) for x in user_input.split(",") if x.strip()
                ]
            except ValueError:
                print("Invalid input. Please enter numbers separated by commas.")
                continue

            self.reset()
            observed = []

            for sel in selections:
                if 1 <= sel <= len(symptom_list):
                    sym_name = symptom_list[sel - 1]
                    sym = self.symptoms[sym_name]

                    cf_input = input(
                        f"Confidence for '{sym.description[:50]}...' (0-100%, default 80): "
                    ).strip()

                    try:
                        cf = float(cf_input.replace("%", "")) / 100 if cf_input else 0.8
                        cf = min(1.0, max(0.0, cf))
                    except ValueError:
                        cf = 0.8

                    self.set_symptom(sym_name, True, cf)
                    observed.append((sym_name, cf))
                else:
                    print(f"Invalid symptom number: {sel}")

            if not observed:
                print("No valid symptoms selected. Please try again.")
                continue

            print("\n" + "=" * 70)
            print("RUNNING FORWARD CHAINING INFERENCE ENGINE...")
            print("=" * 70)

            fired_rules = self.forward_chain()

            if fired_rules:
                print("\nRules Fired:")
                for rule_id, pest, cf in fired_rules:
                    print(f"  - {rule_id}: Identified {pest} (CF: {cf:.2%})")

            if self.identified_pests:
                print("\n" + "=" * 70)
                print("DIAGNOSIS RESULTS")
                print("=" * 70)

                sorted_pests = sorted(
                    self.identified_pests.items(), key=lambda x: x[1], reverse=True
                )

                for pest_name, cf in sorted_pests:
                    pest = self.pests.get(pest_name)

                    print(f"\n{'*' * 60}")
                    print(f"IDENTIFIED PEST: {pest_name}")
                    if pest:
                        print(f"Scientific Name: {pest.scientific_name}")
                    print(f"Confidence Level: {cf:.1%}")
                    print(f"{'*' * 60}")

                    if pest:
                        print(f"\nDescription: {pest.description}")
                        print(f"Damage Type: {pest.damage_type}")
                        print(f"Favorable Conditions: {pest.favorable_conditions}")
                        print(f"Affected Stage: {pest.affected_stage}")

                    print("\n--- CONTROL RECOMMENDATIONS (IPM Approach) ---")
                    recs = self.get_recommendations(pest_name)

                    for control_type in [
                        "cultural",
                        "mechanical",
                        "biological",
                        "chemical",
                    ]:
                        if recs[control_type]:
                            print(f"\n[{control_type.upper()} CONTROL]")
                            for r in recs[control_type]:
                                print(
                                    f"  Priority {r['priority']}: {r['recommendation']}"
                                )
            else:
                print("\n" + "-" * 70)
                print("NO PEST COULD BE IDENTIFIED")
                print("-" * 70)
                print(
                    "The symptoms you described do not match any known pest patterns."
                )
                print("Suggestions:")
                print("  1. Observe more symptoms and try again")
                print("  2. Check if symptoms are due to diseases instead of pests")
                print("  3. Consult with local agricultural extension officers")

            print("\n" + "-" * 70)
            cont = input("Perform another diagnosis? (y/n): ").strip().lower()
            if cont != "y":
                print("\nThank you for using the Rice Pest Expert System. Goodbye!")
                break


def main():
    """Main entry point"""
    print("\n" + "#" * 70)
    print("#" + " " * 68 + "#")
    print("#    RULE-BASED RICE PEST IDENTIFICATION AND CONTROL SYSTEM" + " " * 8 + "#")
    print(
        "#    Expert System using Forward Chaining with Certainty Factor"
        + " " * 4
        + "#"
    )
    print("#    For Malaysian Rice Cultivation" + " " * 31 + "#")
    print("#" + " " * 68 + "#")
    print("#" * 70)

    expert_system = RicePestExpertSystem()
    expert_system.run_interactive()


if __name__ == "__main__":
    main()
