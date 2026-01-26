"""
Multi-Agent Simulation Evaluator for Rice Pest Expert System (CLIPSpy)
---------------------------------------------------------------------
Adds:
- Detailed results table (agent x test case)
- Summary table (overall)
- Summary table by agent
- Optional CSV export

Run:
  python rice_pest_multi_agent_eval.py
Optional:
  python rice_pest_multi_agent_eval.py --csv eval_results.csv
"""

from __future__ import annotations

import argparse
import csv
import random
from statistics import mean

# --- Update this import if your main file name is different ---
try:
    from rice_pest_expert import RicePestExpertSystem  # change if needed
except Exception as e:
    raise ImportError(
        "Could not import RicePestExpertSystem. Make sure:\n"
        "1) This evaluator file is in the same folder as your main script.\n"
        "2) Your main script is named 'rice_pest_expert.py' OR update the import.\n"
        f"Original import error: {e}"
    )


def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


# -------------------------
# Rubric scoring functions
# -------------------------
def score_diagnostic(predicted: str, expected: str) -> int:
    # 5 = correct, 2 = wrong but some output, 1 = no output
    if predicted == expected:
        return 5
    return 2 if predicted and predicted != "No pest identified" else 1


def score_cf_reasonableness(cf_value: float | None, agent_name: str) -> int:
    """
    Simple heuristic:
    - Risk-averse agents should generally produce lower CF.
    - Experienced/chemical-first agents should generally produce higher CF.
    """
    if cf_value is None:
        return 1

    if "Risk-Averse" in agent_name:
        return 5 if cf_value <= 0.75 else 3
    if "Experienced" in agent_name or "Chemical-First" in agent_name:
        return 5 if cf_value >= 0.70 else 3
    return 4 if 0.50 <= cf_value <= 0.90 else 3


def score_recommendations(recs: dict) -> int:
    total = sum(len(v) for v in recs.values())
    return 5 if total >= 4 else 4 if total >= 2 else 2 if total == 1 else 1


def score_ipm_completeness(recs: dict) -> int:
    cats = sum(1 for k in ["cultural", "mechanical", "biological", "chemical"] if recs.get(k))
    return 5 if cats == 4 else 4 if cats == 3 else 3 if cats == 2 else 2 if cats == 1 else 1


def score_clarity() -> int:
    # CLI output is structured and grouped; keep constant for simulation
    return 5


# -------------------------
# Agents + Test Cases
# -------------------------
def build_agents(seed: int = 42):
    random.seed(seed)
    return [
        {"name": "A1 Novice Farmer", "cf_fn": lambda: 0.80, "add_noise": False},
        {"name": "A2 Experienced Farmer", "cf_fn": lambda: clamp(random.uniform(0.85, 0.95)), "add_noise": False},
        {"name": "A3 Extension Officer", "cf_fn": lambda: clamp(random.uniform(0.70, 0.90)), "add_noise": False},
        {"name": "A4 Risk-Averse User", "cf_fn": lambda: clamp(random.uniform(0.50, 0.75)), "add_noise": False},
        {"name": "A5 Noisy/Mixed-Symptoms User", "cf_fn": lambda: clamp(random.uniform(0.60, 0.90)), "add_noise": True},
        {"name": "A6 Chemical-First User", "cf_fn": lambda: clamp(random.uniform(0.80, 0.90)), "add_noise": False},
    ]


def build_test_cases():
    # Derived from your rule base + 1 negative case
    return [
        {"id": "TC-A1", "name": "BPH strong",
         "symptoms": ["hopper-burn", "yellowing-drying", "circular-patches"], "expected_pest": "Brown Planthopper"},
        {"id": "TC-A2", "name": "BPH moderate",
         "symptoms": ["honeydew-sooty-mold", "plant-base-insects"], "expected_pest": "Brown Planthopper"},
        {"id": "TC-A3", "name": "YSB deadheart (veg)",
         "symptoms": ["dead-heart", "central-shoot-withered", "stem-bore-holes"], "expected_pest": "Yellow Stem Borer"},
        {"id": "TC-A4", "name": "YSB whitehead (rep)",
         "symptoms": ["white-head", "empty-panicles"], "expected_pest": "Yellow Stem Borer"},
        {"id": "TC-A5", "name": "YSB egg/larva signs",
         "symptoms": ["egg-mass-on-leaves", "larval-feeding-marks"], "expected_pest": "Yellow Stem Borer"},
        {"id": "TC-A6", "name": "Leaf folder strong",
         "symptoms": ["folded-leaves", "leaf-scraping", "whitish-streaks"], "expected_pest": "Rice Leaf Folder"},
        {"id": "TC-A7", "name": "Leaf folder moderate",
         "symptoms": ["tubular-folded-leaf", "larvae-inside-leaf"], "expected_pest": "Rice Leaf Folder"},
        {"id": "TC-A8", "name": "Gall midge strong",
         "symptoms": ["silver-shoot", "onion-leaf-gall"], "expected_pest": "Rice Gall Midge"},
        {"id": "TC-A9", "name": "Gall midge moderate",
         "symptoms": ["stunted-tillers", "no-panicle-emergence", "elongated-leaf-sheath"], "expected_pest": "Rice Gall Midge"},
        {"id": "TC-A10", "name": "Rice bug strong",
         "symptoms": ["foul-smell", "empty-grains", "discolored-grains"], "expected_pest": "Rice Bug"},
        {"id": "TC-A11", "name": "Negative (mixed, no rule match)",
         "symptoms": ["folded-leaves", "foul-smell"], "expected_pest": "No pest identified"},
    ]


# -------------------------
# Printing helpers
# -------------------------
def print_table(headers, rows):
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))

    def fmt_row(r):
        return "  ".join(str(r[i]).ljust(col_widths[i]) for i in range(len(headers)))

    print(fmt_row(headers))
    print("-" * len(fmt_row(headers)))
    for r in rows:
        print(fmt_row(r))


# -------------------------
# Main simulation
# -------------------------
def run_multi_agent_simulation(seed: int = 42):
    es = RicePestExpertSystem()

    # Optional: if your CLIPS file prints a lot, you can redirect output to file when running:
    # python rice_pest_multi_agent_eval.py > eval_results.txt

    agents = build_agents(seed=seed)
    test_cases = build_test_cases()
    all_symptoms = list(es.symptoms_db.keys())

    results = []

    for agent in agents:
        for tc in test_cases:
            es.reset_system()
            chosen_symptoms = list(tc["symptoms"])

            # Noisy agent adds one extra random symptom not in the test case
            if agent["add_noise"]:
                noise_candidates = [s for s in all_symptoms if s not in chosen_symptoms]
                if noise_candidates:
                    chosen_symptoms.append(random.choice(noise_candidates))

            # Assert symptoms with agent-specific CF
            for s in chosen_symptoms:
                es.assert_symptom(s, present=True, certainty=agent["cf_fn"]())

            es.run_inference()

            identified = es.get_identified_pests()
            if identified:
                top = identified[0]
                pred_pest = str(top.get("name", ""))
                pred_cf = float(top.get("cf", 0.0))
            else:
                pred_pest = "No pest identified"
                pred_cf = None

            # Recommendations only if a real pest is identified
            recs = (
                es.get_control_recommendations(pred_pest)
                if pred_pest != "No pest identified"
                else {"chemical": [], "biological": [], "cultural": [], "mechanical": []}
            )

            diag_score = score_diagnostic(pred_pest, tc["expected_pest"])
            cf_score = score_cf_reasonableness(pred_cf, agent["name"])
            rec_score = score_recommendations(recs)
            ipm_score = score_ipm_completeness(recs)
            clarity_score = score_clarity()
            overall = round(mean([diag_score, cf_score, rec_score, ipm_score, clarity_score]), 2)

            correct = (pred_pest == tc["expected_pest"])

            results.append(
                {
                    "agent": agent["name"],
                    "test_case": tc["id"],
                    "expected": tc["expected_pest"],
                    "predicted": pred_pest,
                    "cf_percent": None if pred_cf is None else round(pred_cf * 100, 1),
                    "overall": overall,
                    "correct": correct,
                }
            )

    return results


def summarize_results(results: list[dict]):
    # Overall summary
    total_runs = len(results)
    accuracy_all = round(sum(1 for r in results if r["correct"]) / total_runs * 100, 1)

    pest_runs = [r for r in results if r["expected"] != "No pest identified"]
    neg_runs = [r for r in results if r["expected"] == "No pest identified"]

    accuracy_pest = round(sum(1 for r in pest_runs if r["correct"]) / len(pest_runs) * 100, 1) if pest_runs else 0.0
    accuracy_neg = round(sum(1 for r in neg_runs if r["correct"]) / len(neg_runs) * 100, 1) if neg_runs else 0.0

    avg_overall = round(mean(r["overall"] for r in results), 2)

    cf_vals = [r["cf_percent"] for r in pest_runs if r["cf_percent"] is not None]
    avg_cf_pest = round(mean(cf_vals), 1) if cf_vals else None

    overall_summary = {
        "Total runs": total_runs,
        "Accuracy (all cases) %": accuracy_all,
        "Accuracy (pest cases only) %": accuracy_pest,
        "Negative-case correctness %": accuracy_neg,
        "Average overall score (1–5)": avg_overall,
        "Average CF % (pest cases)": avg_cf_pest,
    }

    # Summary by agent
    agents = sorted(set(r["agent"] for r in results))
    per_agent = []
    for a in agents:
        r_a = [r for r in results if r["agent"] == a]
        acc_a = round(sum(1 for r in r_a if r["correct"]) / len(r_a) * 100, 1)

        r_a_pest = [r for r in r_a if r["expected"] != "No pest identified"]
        cf_a_vals = [r["cf_percent"] for r in r_a_pest if r["cf_percent"] is not None]
        avg_cf_a = round(mean(cf_a_vals), 1) if cf_a_vals else None

        avg_overall_a = round(mean(r["overall"] for r in r_a), 2)
        per_agent.append((a, len(r_a), acc_a, "—" if avg_cf_a is None else avg_cf_a, avg_overall_a))

    return overall_summary, per_agent


def print_results(results: list[dict]):
    print("\n" + "=" * 90)
    print("MULTI-AGENT SIMULATION EVALUATION RESULTS")
    print("=" * 90)

    # Detailed table
    detailed_headers = ["Agent", "TC", "Expected", "Predicted", "CF%", "Overall"]
    detailed_rows = []
    for r in results:
        cf_txt = "—" if r["cf_percent"] is None else f"{r['cf_percent']:.1f}"
        detailed_rows.append([
            r["agent"][:26],
            r["test_case"],
            r["expected"][:20],
            r["predicted"][:22],
            cf_txt,
            f"{r['overall']:.2f}",
        ])

    print("\nDetailed Results Table (All Runs)")
    print_table(detailed_headers, detailed_rows)

    # Summary tables
    overall_summary, per_agent = summarize_results(results)

    print("\nSummary Table (Overall)")
    summary_headers = ["Metric", "Value"]
    summary_rows = [(k, v if v is not None else "—") for k, v in overall_summary.items()]
    print_table(summary_headers, summary_rows)

    print("\nSummary Table (By Agent)")
    agent_headers = ["Agent", "Runs", "Accuracy %", "Avg CF % (pest)", "Avg Overall"]
    agent_rows = [(a, runs, acc, cf, avg) for (a, runs, acc, cf, avg) in per_agent]
    print_table(agent_headers, agent_rows)

    print("\n" + "-" * 90)


def save_csv(results: list[dict], csv_path: str):
    fields = ["agent", "test_case", "expected", "predicted", "cf_percent", "overall", "correct"]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for r in results:
            writer.writerow(r)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility.")
    parser.add_argument("--csv", type=str, default="", help="Optional: output CSV file path (e.g., eval_results.csv).")
    args = parser.parse_args()

    results = run_multi_agent_simulation(seed=args.seed)
    print_results(results)

    if args.csv:
        save_csv(results, args.csv)
        print(f"Saved CSV to: {args.csv}")


if __name__ == "__main__":
    main()
