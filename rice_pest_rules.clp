;;;======================================================
;;; Rice Pest Identification and Control Recommendation
;;; Expert System using Forward Chaining with Certainty Factor
;;; For Malaysian Rice Cultivation
;;;======================================================

;;; Define templates for symptoms
(deftemplate symptom
   (slot name (type SYMBOL))
   (slot present (type SYMBOL) (allowed-symbols yes no unknown) (default unknown))
   (slot cf (type FLOAT) (range 0.0 1.0) (default 0.0)))

;;; Define template for pest identification
(deftemplate pest
   (slot name (type STRING))
   (slot scientific-name (type STRING))
   (slot cf (type FLOAT) (range 0.0 1.0) (default 0.0))
   (slot identified (type SYMBOL) (allowed-symbols yes no) (default no)))

;;; Define template for control recommendations
(deftemplate control-recommendation
   (slot pest-name (type STRING))
   (slot control-type (type SYMBOL) (allowed-symbols chemical biological cultural mechanical))
   (slot recommendation (type STRING))
   (slot priority (type INTEGER) (range 1 5)))

;;;======================================================
;;; INITIAL FACTS - Control Recommendations Knowledge Base
;;;======================================================

(deffacts control-methods
   ;; Brown Planthopper Control
   (control-recommendation (pest-name "Brown Planthopper") (control-type chemical) 
      (recommendation "Apply Imidacloprid 17.8 SL at 100-125 ml/ha or Thiamethoxam 25 WG at 100g/ha") (priority 1))
   (control-recommendation (pest-name "Brown Planthopper") (control-type chemical)
      (recommendation "Apply Buprofezin 25 SC at 1.5-2.0 ml/L for nymph control") (priority 2))
   (control-recommendation (pest-name "Brown Planthopper") (control-type biological)
      (recommendation "Conserve natural enemies: Cyrtorhinus lividipennis (mirid bug), Lycosa pseudoannulata (wolf spider)") (priority 1))
   (control-recommendation (pest-name "Brown Planthopper") (control-type cultural)
      (recommendation "Avoid excessive nitrogen application; Use resistant varieties like MR219, MR220") (priority 1))
   (control-recommendation (pest-name "Brown Planthopper") (control-type mechanical)
      (recommendation "Use light traps (15W bulb) to monitor and reduce adult population") (priority 2))
   
   ;; Yellow Stem Borer Control
   (control-recommendation (pest-name "Yellow Stem Borer") (control-type chemical)
      (recommendation "Apply Cartap hydrochloride 4G at 25 kg/ha or Chlorantraniliprole 18.5 SC at 150 ml/ha") (priority 1))
   (control-recommendation (pest-name "Yellow Stem Borer") (control-type chemical)
      (recommendation "Spray Fipronil 5 SC at 1.5-2.0 ml/L at tillering stage") (priority 2))
   (control-recommendation (pest-name "Yellow Stem Borer") (control-type biological)
      (recommendation "Release Trichogramma japonicum egg parasitoid at 100,000/ha at weekly intervals") (priority 1))
   (control-recommendation (pest-name "Yellow Stem Borer") (control-type biological)
      (recommendation "Conserve predators: Conocephalus longipennis, Anaxipha longipennis") (priority 2))
   (control-recommendation (pest-name "Yellow Stem Borer") (control-type cultural)
      (recommendation "Remove and destroy stubbles after harvest; Synchronize planting in the area") (priority 1))
   (control-recommendation (pest-name "Yellow Stem Borer") (control-type mechanical)
      (recommendation "Use pheromone traps (5/ha) for monitoring; Collect and destroy egg masses") (priority 1))
   
   ;; Rice Leaf Folder Control
   (control-recommendation (pest-name "Rice Leaf Folder") (control-type chemical)
      (recommendation "Apply Chlorantraniliprole 18.5 SC at 150 ml/ha or Flubendiamide 39.35 SC at 50 ml/ha") (priority 1))
   (control-recommendation (pest-name "Rice Leaf Folder") (control-type chemical)
      (recommendation "Spray Quinalphos 25 EC at 2 ml/L when damage exceeds economic threshold") (priority 2))
   (control-recommendation (pest-name "Rice Leaf Folder") (control-type biological)
      (recommendation "Release Trichogramma chilonis at 50,000/ha; Conserve Apanteles spp. parasitoids") (priority 1))
   (control-recommendation (pest-name "Rice Leaf Folder") (control-type cultural)
      (recommendation "Avoid excessive nitrogen; Maintain field sanitation; Remove grassy weeds") (priority 1))
   (control-recommendation (pest-name "Rice Leaf Folder") (control-type mechanical)
      (recommendation "Use light traps to attract and kill adult moths") (priority 2))
   
   ;; Rice Gall Midge Control
   (control-recommendation (pest-name "Rice Gall Midge") (control-type chemical)
      (recommendation "Apply Carbofuran 3G at 25-30 kg/ha in nursery or Fipronil 0.3G at 25 kg/ha") (priority 1))
   (control-recommendation (pest-name "Rice Gall Midge") (control-type chemical)
      (recommendation "Seed treatment with Thiamethoxam 70 WS at 3g/kg seed") (priority 2))
   (control-recommendation (pest-name "Rice Gall Midge") (control-type biological)
      (recommendation "Conserve Platygaster oryzae parasitoid; Maintain spider population in fields") (priority 1))
   (control-recommendation (pest-name "Rice Gall Midge") (control-type cultural)
      (recommendation "Use resistant varieties; Early and synchronous planting; Destroy ratoon and volunteer plants") (priority 1))
   (control-recommendation (pest-name "Rice Gall Midge") (control-type mechanical)
      (recommendation "Pull out and destroy affected tillers (silver shoots)") (priority 1))
   
   ;; Rice Bug Control
   (control-recommendation (pest-name "Rice Bug") (control-type chemical)
      (recommendation "Apply Carbaryl 85 WP at 1.5 kg/ha or Lambda-cyhalothrin 5 EC at 300 ml/ha") (priority 1))
   (control-recommendation (pest-name "Rice Bug") (control-type biological)
      (recommendation "Conserve egg parasitoids Gryon nixoni and Ooencyrtus spp.") (priority 1))
   (control-recommendation (pest-name "Rice Bug") (control-type cultural)
      (recommendation "Remove weeds around bunds; Synchronize planting to avoid staggered harvesting") (priority 1))
   (control-recommendation (pest-name "Rice Bug") (control-type mechanical)
      (recommendation "Collect bugs using sweep nets during early morning when less active") (priority 2))
)

;;;======================================================
;;; RULES FOR PEST IDENTIFICATION WITH CERTAINTY FACTOR
;;;======================================================

;;; Brown Planthopper (Nilaparvata lugens) Identification Rules
(defrule identify-brown-planthopper-strong
   (symptom (name hopper-burn) (present yes) (cf ?cf1))
   (symptom (name yellowing-drying) (present yes) (cf ?cf2))
   (symptom (name circular-patches) (present yes) (cf ?cf3))
   =>
   (bind ?combined-cf (* (+ ?cf1 ?cf2 ?cf3) 0.333 0.95))
   (assert (pest (name "Brown Planthopper") (scientific-name "Nilaparvata lugens") 
                 (cf ?combined-cf) (identified yes))))

(defrule identify-brown-planthopper-moderate
   (symptom (name honeydew-sooty-mold) (present yes) (cf ?cf1))
   (symptom (name plant-base-insects) (present yes) (cf ?cf2))
   =>
   (bind ?combined-cf (* (+ ?cf1 ?cf2) 0.5 0.75))
   (assert (pest (name "Brown Planthopper") (scientific-name "Nilaparvata lugens")
                 (cf ?combined-cf) (identified yes))))

;;; Yellow Stem Borer (Scirpophaga incertulas) Identification Rules
(defrule identify-yellow-stem-borer-deadheart
   (symptom (name dead-heart) (present yes) (cf ?cf1))
   (symptom (name central-shoot-withered) (present yes) (cf ?cf2))
   (symptom (name stem-bore-holes) (present yes) (cf ?cf3))
   =>
   (bind ?combined-cf (* (+ ?cf1 ?cf2 ?cf3) 0.333 0.92))
   (assert (pest (name "Yellow Stem Borer") (scientific-name "Scirpophaga incertulas")
                 (cf ?combined-cf) (identified yes))))

(defrule identify-yellow-stem-borer-whitehead
   (symptom (name white-head) (present yes) (cf ?cf1))
   (symptom (name empty-panicles) (present yes) (cf ?cf2))
   =>
   (bind ?combined-cf (* (+ ?cf1 ?cf2) 0.5 0.88))
   (assert (pest (name "Yellow Stem Borer") (scientific-name "Scirpophaga incertulas")
                 (cf ?combined-cf) (identified yes))))

(defrule identify-yellow-stem-borer-egg-mass
   (symptom (name egg-mass-on-leaves) (present yes) (cf ?cf1))
   (symptom (name larval-feeding-marks) (present yes) (cf ?cf2))
   =>
   (bind ?combined-cf (* (+ ?cf1 ?cf2) 0.5 0.70))
   (assert (pest (name "Yellow Stem Borer") (scientific-name "Scirpophaga incertulas")
                 (cf ?combined-cf) (identified yes))))

;;; Rice Leaf Folder (Cnaphalocrocis medinalis) Identification Rules
(defrule identify-leaf-folder-strong
   (symptom (name folded-leaves) (present yes) (cf ?cf1))
   (symptom (name leaf-scraping) (present yes) (cf ?cf2))
   (symptom (name whitish-streaks) (present yes) (cf ?cf3))
   =>
   (bind ?combined-cf (* (+ ?cf1 ?cf2 ?cf3) 0.333 0.93))
   (assert (pest (name "Rice Leaf Folder") (scientific-name "Cnaphalocrocis medinalis")
                 (cf ?combined-cf) (identified yes))))

(defrule identify-leaf-folder-moderate
   (symptom (name tubular-folded-leaf) (present yes) (cf ?cf1))
   (symptom (name larvae-inside-leaf) (present yes) (cf ?cf2))
   =>
   (bind ?combined-cf (* (+ ?cf1 ?cf2) 0.5 0.85))
   (assert (pest (name "Rice Leaf Folder") (scientific-name "Cnaphalocrocis medinalis")
                 (cf ?combined-cf) (identified yes))))

;;; Rice Gall Midge (Orseolia oryzae) Identification Rules
(defrule identify-gall-midge-strong
   (symptom (name silver-shoot) (present yes) (cf ?cf1))
   (symptom (name onion-leaf-gall) (present yes) (cf ?cf2))
   =>
   (bind ?combined-cf (* (+ ?cf1 ?cf2) 0.5 0.95))
   (assert (pest (name "Rice Gall Midge") (scientific-name "Orseolia oryzae")
                 (cf ?combined-cf) (identified yes))))

(defrule identify-gall-midge-moderate
   (symptom (name stunted-tillers) (present yes) (cf ?cf1))
   (symptom (name no-panicle-emergence) (present yes) (cf ?cf2))
   (symptom (name elongated-leaf-sheath) (present yes) (cf ?cf3))
   =>
   (bind ?combined-cf (* (+ ?cf1 ?cf2 ?cf3) 0.333 0.78))
   (assert (pest (name "Rice Gall Midge") (scientific-name "Orseolia oryzae")
                 (cf ?combined-cf) (identified yes))))

;;; Rice Bug (Leptocorisa oratorius) Identification Rules
(defrule identify-rice-bug
   (symptom (name foul-smell) (present yes) (cf ?cf1))
   (symptom (name empty-grains) (present yes) (cf ?cf2))
   (symptom (name discolored-grains) (present yes) (cf ?cf3))
   =>
   (bind ?combined-cf (* (+ ?cf1 ?cf2 ?cf3) 0.333 0.85))
   (assert (pest (name "Rice Bug") (scientific-name "Leptocorisa oratorius")
                 (cf ?combined-cf) (identified yes))))

;;;======================================================
;;; DISPLAY RULES
;;;======================================================

(defrule display-pest-identification
   (pest (name ?name) (scientific-name ?sci-name) (cf ?cf) (identified yes))
   =>
   (printout t crlf "*** PEST IDENTIFIED ***" crlf)
   (printout t "Pest Name: " ?name crlf)
   (printout t "Scientific Name: " ?sci-name crlf)
   (printout t "Certainty Factor: " (round (* ?cf 100)) "%" crlf))

(defrule display-control-recommendations
   (pest (name ?name) (identified yes))
   (control-recommendation (pest-name ?name) (control-type ?type) (recommendation ?rec) (priority ?pri))
   =>
   (printout t crlf "Control Recommendation (" ?type ", Priority: " ?pri "):" crlf)
   (printout t "  -> " ?rec crlf))
