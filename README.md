# Rice Pest Identification and Control Recommendation Expert System

A Rule-Based Expert System for Malaysian Rice Cultivation using Forward Chaining inference with Certainty Factor.

## Overview

This expert system helps farmers identify common rice pests based on observed symptoms and provides integrated pest management (IPM) control recommendations including chemical, biological, cultural, and mechanical control methods.

## Pests Covered

1. **Brown Planthopper** (*Nilaparvata lugens*)
2. **Yellow Stem Borer** (*Scirpophaga incertulas*)
3. **Rice Leaf Folder** (*Cnaphalocrocis medinalis*)
4. **Rice Gall Midge** (*Orseolia oryzae*)
5. **Rice Bug** (*Leptocorisa oratorius*)

## Files

- `rice_pest_expert_standalone.py` - Standalone Python version (recommended, no external dependencies)
- `rice_pest_expert.py` - Python + CLIPS version (requires clipspy)
- `rice_pest_rules.clp` - CLIPS rules file
- `requirements.txt` - Python dependencies

## Installation & Usage

### Option 1: Standalone Version (Recommended)

No external dependencies required. Just run:

```bash
python rice_pest_expert_standalone.py
```

### Option 2: CLIPS Version

1. Install clipspy:
   ```bash
   pip install clipspy
   ```

2. Run the expert system:
   ```bash
   python rice_pest_expert.py
   ```

## How to Use

1. Run the program
2. View the symptom checklist organized by pest type
3. Enter the numbers of symptoms you observe (comma-separated)
4. Provide confidence level for each symptom (0-100%)
5. The system will:
   - Run forward chaining inference
   - Identify the most likely pest(s)
   - Display certainty factor for each identification
   - Provide control recommendations

## System Architecture

- **Knowledge Representation**: Rule-based with symptoms, pests, and control recommendations
- **Inference Engine**: Forward chaining (data-driven reasoning)
- **Uncertainty Handling**: Certainty Factor method
- **Control Recommendations**: Integrated Pest Management (IPM) approach

## Example Session

```
Enter observed symptom numbers: 1,2,3
Confidence for 'Plants appear burnt/scorched...' (0-100%, default 80): 90
Confidence for 'Yellowing and drying...' (0-100%, default 80): 85
Confidence for 'Circular patches...' (0-100%, default 80): 80

DIAGNOSIS RESULTS
==================
IDENTIFIED PEST: Brown Planthopper
Scientific Name: Nilaparvata lugens
Confidence Level: 80.8%

CONTROL RECOMMENDATIONS:
[CULTURAL CONTROL]
  Priority 1: Avoid excessive nitrogen application; Use resistant varieties...
[CHEMICAL CONTROL]
  Priority 1: Apply Imidacloprid 17.8 SL at 100-125 ml/ha...
```

## References

Based on research from Malaysian Agricultural Research and Development Institute (MARDI) and Department of Agriculture Malaysia guidelines for rice pest management.
