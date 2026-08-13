# Diagnosing Out-of-Memory (OOM) / Process Kills — A Data Scientist's Playbook

> Real-world skill: when a training job dies with no Python traceback, it was almost
> always **killed by the operating system for using too much memory**. Here's how to
> confirm it, quantify it, and fix it — the exact method used to debug the NYC taxi
> `PU_DO` feature blowup in `4_ML_Models.py`.

---

## 1. Read the Exit Code First
Exit codes **above 128** mean "killed by a signal". The signal number is `exit_code - 128`:

| Exit code | Signal | Meaning |
| --------- | ------ | ------- |
| `137` | 9 (SIGKILL) | Hard-killed — classic **OOM killer** |
| `143` | 15 (SIGTERM) | Terminated — usually **OOM** or a shutdown request |
| `130` | 2 (SIGINT) | You pressed `Ctrl+C` |

**Golden rule:** exit `137`/`143` **with no Python traceback** = out of memory.
A genuine code bug gives you a Python traceback (e.g. `ValueError`), not a bare `Terminated`.

---

## 2. Check the Machine's Actual Limits
```bash
free -h    # RAM: look at the "available" / "free" column
nproc      # number of CPU cores
```
This gives you a **budget** to compare your data size against.
(Example Codespace: ~4.7 GB free, 2 cores.)

---

## 3. Compute the WORST-CASE (Densified) Size of Your Data
The trap: a **sparse** matrix looks tiny, but many models silently convert it to
**dense**, exploding memory. Always compute the dense size:

$$\text{dense bytes} = \text{rows} \times \text{cols} \times 8 \quad (\text{float64} = 8\ \text{bytes})$$

```python
X.shape                               # e.g. (73908, 13221)
X.shape[0] * X.shape[1] * 8 / 1e9     # 7.82  -> GB if densified
```
If that number **exceeds available RAM**, the kill is guaranteed. That inequality
*is* the diagnosis. (7.82 GB needed vs 4.7 GB free -> dead.)

Measure the **true sparse** footprint for comparison:
```python
X.data.nbytes + X.indices.nbytes + X.indptr.nbytes   # bytes actually used while sparse
```

---

## 4. Know Which Algorithms Force Dense (memorize this)
| Handles sparse natively (safe) | Forces dense (danger) |
| ------------------------------ | --------------------- |
| RandomForest, ExtraTrees | **GradientBoostingRegressor** |
| Linear models (Ridge/Lasso/SGD) | SVMs with some kernels |
| XGBoost / LightGBM | anything calling `np.asarray(X)` |

In the taxi case, `GradientBoostingRegressor` was the main culprit: it densified the
13k-column matrix to 7.8 GB instantly.

---

## 5. Attack the Biggest Multiplier
The size formula has three levers: `rows × cols × bytes`. Find the abnormal one.
- Here `cols = 13,221` was abnormal — caused by a **high-cardinality** categorical
  feature (`PU_DO` = pickup_dropoff pair -> ~13k unique combos -> ~13k one-hot columns).
- Fix ("Option A"): use `PULocationID` and `DOLocationID` **separately** (~few hundred
  columns) instead of the combined pair. Dropped dense size from 7.8 GB to ~0.3 GB.

Other valid fixes:
- **Drop** the dense-forcing model (e.g. remove GradientBoosting).
- **Subsample** rows (fewer `rows`).
- **Dimensionality reduction / hashing** to cut `cols`.
- Get a bigger machine (last resort — fix the data first).

---

## 6. Watch Memory Live (see the kill happen)
```bash
watch -n 1 free -m        # refresh every second; watch "available" fall toward 0
```
Run this in a second terminal next to any heavy job for visceral proof.

---

## 7. Quick Mental Checklist
1. Exit code 137/143 + no traceback? -> suspect OOM.
2. `free -h` / `nproc` -> what's my budget?
3. `rows * cols * 8` -> does dense size exceed budget?
4. Which model densifies? Which feature inflated `cols`?
5. Cut the biggest multiplier (usually high-cardinality columns).

---

## Bonus lesson from the same run: silent model failure
`LinearSVR` "succeeded" but produced RMSE ~900 (garbage) with a
`ConvergenceWarning: Liblinear failed to converge`. Lesson: **a run finishing without
crashing does NOT mean the model is good.** Always sanity-check the metric magnitude;
absurd values often mean non-convergence or unscaled features (SVMs need feature scaling).
