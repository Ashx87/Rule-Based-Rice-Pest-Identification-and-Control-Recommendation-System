# Rice Pest Identification and Control Recommendation Expert System

A **Rule-Based Expert System** for Malaysian Rice Cultivation using **Forward Chaining** inference with **Certainty Factor** for uncertainty handling.

> **Course:** TES6313 - Expert Systems  
> **Institution:** Multimedia University (MMU)

---

## Overview

This expert system assists farmers and agricultural extension officers in identifying common rice pests based on observed field symptoms and provides comprehensive **Integrated Pest Management (IPM)** control recommendations, including:

- **Chemical Control** - Pesticide applications with dosage guidelines
- **Biological Control** - Natural enemies and parasitoids
- **Cultural Control** - Agricultural practices to reduce pest incidence
- **Mechanical Control** - Physical methods for pest management

### Key Features

- **Forward Chaining Inference Engine** - Data-driven reasoning from symptoms to pest identification
- **Certainty Factor (CF)** - Handles uncertainty in symptom observations and pest identification
- **IPM-Based Recommendations** - Prioritized control methods following sustainable agriculture principles
- **Two Implementation Versions** - Standalone Python and Python + CLIPS
- **Multi-Agent Evaluation** - Automated testing with different user profiles

---

## Pests Covered

The system can identify **5 major rice pests** commonly found in Malaysian rice cultivation:

| Pest | Scientific Name | Primary Damage |
|------|-----------------|----------------|
| Brown Planthopper | *Nilaparvata lugens* | Hopper burn - plants dry up and appear scorched |
| Yellow Stem Borer | *Scirpophaga incertulas* | Dead heart (vegetative) / White head (reproductive) |
| Rice Leaf Folder | *Cnaphalocrocis medinalis* | Reduced photosynthetic area, whitish leaf streaks |
| Rice Gall Midge | *Orseolia oryzae* | Silver shoot - tillers fail to produce panicles |
| Rice Bug | *Leptocorisa oratorius* | Empty/partially filled grains, reduced quality |

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│              (Interactive Symptom Selection)                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    KNOWLEDGE BASE                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │   Symptoms   │  │    Pests     │  │  Control Methods     │  │
│  │  (24 items)  │  │  (5 pests)   │  │  (20+ recommendations)│ │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    INFERENCE ENGINE                             │
│         Forward Chaining + Certainty Factor Combination         │
│                                                                 │
│    CF_combined = CF1 + CF2 × (1 - CF1)    [for CF1, CF2 ≥ 0]   │
│    Final_CF = Average_Symptom_CF × Rule_CF                      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      OUTPUT                                     │
│   Pest Identification + Confidence Level + IPM Recommendations  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Files

| File | Description |
|------|-------------|
| `rice_pest_expert_standalone.py` | Standalone Python version (**recommended**, no external dependencies) |
| `rice_pest_expert.py` | Python + CLIPS version (requires clipspy) |
| `rice_pest_rules.clp` | CLIPS rules file with pest identification rules and control recommendations |
| `rice_pest_multi_agent_eval.py` | Multi-agent simulation evaluator for system testing |
| `requirements.txt` | Python dependencies |

---

## Installation & Usage

### Option 1: Standalone Version (Recommended)

No external dependencies required. Just run:

```bash
python rice_pest_expert_standalone.py
```

### Option 2: CLIPS Version

1. Install the CLIPS Python binding:
   ```bash
   pip install clipspy
   ```

2. Run the expert system:
   ```bash
   python rice_pest_expert.py
   ```

### Option 3: Multi-Agent Evaluation

Run automated testing with 6 different simulated user profiles:

```bash
# Run evaluation
python rice_pest_multi_agent_eval.py

# Run with CSV export
python rice_pest_multi_agent_eval.py --csv eval_results.csv
```

---

## How to Use

1. **Run the program** - Choose either standalone or CLIPS version
2. **View symptoms** - Symptoms are organized by associated pest type for easier reference
3. **Select symptoms** - Enter numbers of observed symptoms (comma-separated)
4. **Provide confidence** - Rate your certainty for each symptom (0-100%)
5. **Get results** - The system will:
   - Execute forward chaining inference
   - Identify the most likely pest(s) with certainty factors
   - Display comprehensive IPM control recommendations

---

## Symptoms Database

The system includes **24 symptoms** across 5 pest categories:

### Brown Planthopper (5 symptoms)
- Hopper burn appearance
- Yellowing and drying from bottom
- Circular patches of dead plants
- Honeydew with sooty mold
- Brown insects at plant base

### Yellow Stem Borer (7 symptoms)
- Dead heart (vegetative stage)
- Central shoot withering
- Stem bore holes with frass
- White head (reproductive stage)
- Empty panicles
- Egg masses on leaves
- Larval feeding marks

### Rice Leaf Folder (5 symptoms)
- Longitudinally folded leaves
- Leaf scraping damage
- Whitish/transparent streaks
- Tubular rolled leaves
- Larvae inside folded leaves

### Rice Gall Midge (5 symptoms)
- Silver shoot/onion shoot
- Onion leaf-like gall
- Stunted tillers
- No panicle emergence
- Elongated pale leaf sheath

### Rice Bug (3 symptoms)
- Foul smell in field
- Empty/partially filled grains
- Discolored grain spots

---

## Inference Rules

The system contains **15 inference rules** with varying certainty factors:

| Rule | Pest | Symptoms Required | Rule CF |
|------|------|-------------------|---------|
| R1 | Brown Planthopper | hopper_burn + yellowing + circular_patches | 0.95 |
| R2 | Brown Planthopper | honeydew + plant_base_insects | 0.75 |
| R3 | Brown Planthopper | hopper_burn + plant_base_insects | 0.85 |
| R4 | Yellow Stem Borer | dead_heart + central_shoot + bore_holes | 0.92 |
| R5 | Yellow Stem Borer | white_head + empty_panicles | 0.88 |
| R6 | Yellow Stem Borer | egg_mass + larval_marks | 0.70 |
| R7 | Yellow Stem Borer | dead_heart + bore_holes | 0.85 |
| R8 | Rice Leaf Folder | folded_leaves + scraping + streaks | 0.93 |
| R9 | Rice Leaf Folder | tubular_leaf + larvae_inside | 0.85 |
| R10 | Rice Leaf Folder | folded_leaves + larvae_inside | 0.90 |
| R11 | Rice Gall Midge | silver_shoot + onion_gall | 0.95 |
| R12 | Rice Gall Midge | stunted + no_panicle + elongated | 0.78 |
| R13 | Rice Gall Midge | silver_shoot + no_panicle | 0.88 |
| R14 | Rice Bug | foul_smell + empty_grains + discolored | 0.85 |
| R15 | Rice Bug | foul_smell + empty_grains | 0.75 |

---

## Multi-Agent Evaluation

The evaluation script simulates **6 different user profiles** across **11 test cases**:

### Agent Profiles
| Agent | Description | CF Behavior |
|-------|-------------|-------------|
| A1 | Novice Farmer | Fixed CF (0.80) |
| A2 | Experienced Farmer | High CF (0.85-0.95) |
| A3 | Extension Officer | Moderate CF (0.70-0.90) |
| A4 | Risk-Averse User | Lower CF (0.50-0.75) |
| A5 | Noisy User | Random + extra symptoms |
| A6 | Chemical-First User | High CF (0.80-0.90) |

### Test Cases
- 10 positive cases (2 per pest type)
- 1 negative case (mixed symptoms, no rule match)

### Scoring Rubric
- **Diagnostic Accuracy** - Correct pest identification
- **CF Reasonableness** - Appropriate certainty factors
- **Recommendation Quality** - Number of control methods provided
- **IPM Completeness** - Coverage of all 4 control categories
- **Clarity** - Output organization

---

## Example Session

```
======================================================================
  RICE PEST IDENTIFICATION AND CONTROL RECOMMENDATION SYSTEM
  Rule-Based Expert System with Forward Chaining & Certainty Factor
  For Malaysian Rice Cultivation
======================================================================

Enter observed symptom numbers: 1,2,3
Confidence for 'Plants appear burnt/scorched...' (0-100%, default 80): 90
Confidence for 'Yellowing and drying...' (0-100%, default 80): 85
Confidence for 'Circular patches...' (0-100%, default 80): 80

======================================================================
RUNNING FORWARD CHAINING INFERENCE ENGINE...
======================================================================

Rules Fired:
  - R1: Identified Brown Planthopper (CF: 80.75%)

======================================================================
DIAGNOSIS RESULTS
======================================================================

************************************************************
IDENTIFIED PEST: Brown Planthopper
Scientific Name: Nilaparvata lugens
Confidence Level: 80.8%
************************************************************

Description: Small brown sucking insect that feeds on plant sap
Damage Type: Causes hopper burn - plants dry up and appear scorched
Favorable Conditions: High humidity, excessive nitrogen use, continuous flooding
Affected Stage: All growth stages, especially tillering to heading

--- CONTROL RECOMMENDATIONS (IPM Approach) ---

[CULTURAL CONTROL]
  Priority 1: Avoid excessive nitrogen application; Use resistant varieties like MR219, MR220

[MECHANICAL CONTROL]
  Priority 2: Use light traps (15W bulb) to monitor and reduce adult population

[BIOLOGICAL CONTROL]
  Priority 1: Conserve natural enemies: Cyrtorhinus lividipennis, Lycosa pseudoannulata

[CHEMICAL CONTROL]
  Priority 1: Apply Imidacloprid 17.8 SL at 100-125 ml/ha
  Priority 2: Apply Buprofezin 25 SC at 1.5-2.0 ml/L for nymph control
```

---

## Technical Details

### Certainty Factor Calculation

The system uses the standard CF combination formula:

**For combining evidence (CF1, CF2 ≥ 0):**
```
CF_combined = CF1 + CF2 × (1 - CF1)
```

**For rule application:**
```
Final_CF = Average_Symptom_CF × Rule_CF
```

### Forward Chaining Process

1. User asserts symptoms with confidence levels
2. Inference engine matches symptoms against rule antecedents
3. When all required symptoms are present, rule fires
4. Multiple rules can fire, CFs are combined for same pest
5. Results sorted by confidence level

---

## References

- Malaysian Agricultural Research and Development Institute (MARDI) guidelines
- Department of Agriculture Malaysia rice pest management protocols
- International Rice Research Institute (IRRI) pest identification resources
- CLIPS Expert System Shell documentation

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

Developed as part of the TES6313 Expert Systems course at Multimedia University (MMU), Malaysia.
