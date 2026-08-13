# Copilot Context — MLOps Zoomcamp Learning Journey

> This file exists so that any AI assistant session picks up exactly where the user left off.
> Read this first before helping with anything in this repo.

## Who is the user & what do they want?

- Has a solid **Machine Learning background** already (models, metrics, sklearn, etc.).
- Does **NOT** have prior MLOps/DevOps/infra experience — learning it fresh, step by step.
- Following the official course: [DataTalksClub/mlops-zoomcamp](https://github.com/DataTalksClub/mlops-zoomcamp), in order, module by module.
- Wants to learn in an **educational, guided way**:
  - Explain concepts, don't just hand over finished code.
  - When something is foundational/important, give **exercises or small challenges** instead of the answer immediately.
  - Confirm understanding by asking the user to report back findings (e.g. "go check the MLflow UI and tell me X").
- Alongside the course, is separately learning **practical bash/terminal skills**
  (`cat`, `grep`, pipes `|`, redirects `>`/`>>`, heredocs, `$PATH`, env vars, `.bashrc`, etc.)
  and keeping notes as markdown files in the repo root (see `bash_essentials.md`).
- Wants all such learning notes/summaries saved as **markdown files**, not just chat answers.

## Ground rules for the assistant

1. Don't dump full solutions immediately — teach step by step, Socratic style when appropriate.
2. When a concept is important to internalize (e.g. hyperopt objective functions, MLflow tracking URI vs artifact store, model registry aliases vs stages), give a short exercise before or instead of just fixing it.
3. Keep a running mental model of course progress (see below) and always relate new questions back to "where we are in the course."
4. Save conceptual explanations as markdown notes in the repo (like `bash_essentials.md`, `hyperopt_explanation.txt`) when the user is learning a reusable concept — future note files should follow the `<topic>_notes.md` naming style and live at repo root or inside the relevant module folder.
5. Never touch/modify things outside what's being discussed unless asked.
6. When fixing bugs in notebooks, explain *why* it broke (e.g. sklearn API changes) — this is a teaching moment, not just a patch.
7. **PRACTICAL-ONLY teaching (user's explicit request, Aug 2026):** Do NOT clutter notes/notebooks with "the course said X but it's now deprecated" history. The user does not care what deprecated APIs looked like. Teach only the **current, real-world, practical** way. A brief one-liner that a modern replacement exists is fine ONLY if it helps solve a real problem; otherwise omit deprecated content entirely. Focus on skills that help debug/solve *new* unsolved problems, not memorization.

## Course structure (official repo, for reference)

- `01-intro/` — Intro to MLOps ✅ **DONE** by user (`homework.ipynb` completed).
- `02-experiment-tracking/` — 🔶 **IN PROGRESS** (current focus)
  - 2.1 Experiment tracking intro
  - 2.2 Getting started with MLflow
  - 2.3 Experiment tracking with MLflow
  - 2.4 Model management
  - 2.5 Model registry (⚠️ course note: stage-based transitions like `transition_model_version_stage` are **deprecated** — use aliases via `set_registered_model_alias` instead)
  - 2.6 MLflow in practice
  - 2.7 MLflow: benefits/limitations/alternatives + Homework
- `03-orchestration/` — not started
- `04-deployment/` — not started
- `05-monitoring/` — not started
- `06-best-practices/` — not started
- `07-project/` — not started

## Where the user currently is (Module 2 — Experiment Tracking)

Working notebook: `02-experiment-tracking/duration-prediction.ipynb`

What's been done so far in the notebook:
- Loaded NYC green taxi trip data (Jan/Feb 2021), built `read_dataframe()` preprocessing.
- Feature engineering: `PU_DO` combined categorical feature + `DictVectorizer`.
- Trained baseline `LinearRegression`, pickled model to `models/lin_reg.bin`.
- Set up MLflow tracking (`sqlite:///mlflow.db` backend store, experiment `nyc-taxi-experiment`).
- Logged a manual `Lasso` run with params/metrics/artifact.
- Learned **Hyperopt** concepts separately (see `02-experiment-tracking/hyperopt_explanation.txt`):
  TPE sampler, `fmin`, search space `hp.*`, `Trials`, objective function contract, `DMatrix`.
- Used Hyperopt + XGBoost (`xgb.train` + `DMatrix`) to tune hyperparameters, each trial logged as an MLflow run.
- Logged best XGBoost model via `mlflow.xgboost.log_model(...)` (model logging, not just artifact logging).
- Ran an autologged sweep (`mlflow.sklearn.autolog()`) across RandomForest, GradientBoosting, ExtraTrees, LinearSVR.

Known bugs identified but **not yet fixed in the NOTEBOOK** (already fixed in the .py script):
1. `mean_squared_error` used in 3 cells but never imported (only `root_mean_squared_error` is imported).
2. `squared=False` kwarg no longer exists in current sklearn — needs to switch to `root_mean_squared_error(y_val, y_pred)` directly.
3. `!mlflow ui --backend` cell is incomplete/blocking — should run `mlflow ui --backend-store-uri sqlite:///mlflow.db` from a terminal, not inside a notebook cell.

### Environment / infra facts learned
- Codespace: ~4.7 GB free RAM, 2 cores. Memory-constrained.
- The combined `PU_DO` feature = ~13,221 one-hot columns -> densifies to ~7.8 GB -> OOM
  (exit 143 / SIGTERM). Fixed with "Option A": use `PULocationID` + `DOLocationID`
  separately (~few hundred columns). See `oom_debugging_playbook.md` at repo root.
- `mlflow.set_tracking_uri("sqlite:///mlflow.db")` MUST be set or MLflow falls back to a
  broken `./mlruns` file store (was throwing "could not find experiment with id 0" /
  missing `meta.yaml`). The broken file store was moved to `mlruns_broken_filestore_backup/`.

## Next steps (not yet done)

1. User was asked to run `mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5000` in a terminal,
   explore the UI, and report back: best run's RMSE/run ID, whether XGBoost or an autologged sklearn model won,
   and which columns MLflow autologged automatically. **Awaiting their findings.**
2. Fix the 3 known bugs above (offered to do it for them or let them fix it as practice — undecided which they chose).
3. Introduce **Model Registry** (`model-registry.ipynb` from the course, which user does not yet have locally) —
   using modern **aliases** (`set_registered_model_alias`) instead of deprecated stage transitions.
4. Explain artifact store vs backend store distinction concretely using their own `mlruns/` + `mlflow.db` setup.
5. Eventually: Module 2 homework, then move to Module 3 (Orchestration).

## Separate parallel learning track: Bash/Terminal

File: `bash_essentials.md` (repo root). Topics already covered:
core concepts (`bash`, `cat`, `grep`), redirection (`|`, `>`, `>>`), `~/.bashrc`, heredocs,
env vars & `export`, process hierarchy, `$PATH`, and virtual env activation mechanics (`conda activate`).
Continue adding topics here as the user asks about new bash/terminal concepts, don't mix this into MLOps module notes.
