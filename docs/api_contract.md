# API Contract — Wallet-to-VASP Risk Attribution

This is the shared data contract agreed in Step 0 of the build workflow. All three duos build
against this shape — Model (Duo A), Backend (Duo B), and UI (Duo C). If a field needs to change,
update it here first and re-sync with the other duos before changing code.

## Endpoint

```
GET /score/{wallet_id}
```

Returns the risk score and VASP attribution for a single wallet (transaction ID) from the
Elliptic dataset.

## Response shape

```json
{
  "wallet_address": "string",
  "risk_score": 0.0,
  "risk_label": "illicit / licit / uncertain",
  "graph_hops_to_nearest_vasp": 3,
  "nearest_vasp_name": "string or 'unidentified'",
  "attribution_confidence": "high / medium / low",
  "top_features": ["feature1", "feature2", "feature3"]
}
```

## Field reference

| Field | Type | Description |
|---|---|---|
| `wallet_address` | string | The transaction/wallet ID that was queried. |
| `risk_score` | float (0–1) | Probability of "illicit", from `model.predict_proba`, rounded to 3 decimals. |
| `risk_label` | string | `"illicit"` if `risk_score > 0.5`, else `"licit"`. |
| `graph_hops_to_nearest_vasp` | int or null | BFS shortest-path hop count to the nearest known VASP node. `null` if no path exists. |
| `nearest_vasp_name` | string | Name of nearest VASP, or `"unidentified"` if none reachable. |
| `attribution_confidence` | string | `"high"` if hops ≤ 2, `"medium"` if hops ≤ 5, `"low"` otherwise (including unidentified). |
| `top_features` | array of strings | Top 3 features by `model.feature_importances_` for this prediction. |

## Error handling

- Wallet ID not found in the dataset → **404** with a clear error message (not a raw stack trace).

## Known limitations (state these honestly if asked during the demo)

- `nearest_vasp_name` values are placeholder labels (`known_vasp_1`, `known_vasp_2`, ...) — the
  Elliptic dataset doesn't ship real labeled exchange addresses.
- Graph-feature improvements over the baseline model were marginal in testing (see `model/`
  notebooks) — this is disclosed, not hidden.
- This prototype does not perform real-world identity attribution. Linking a wallet to an actual
  VASP account would require a legal request to the exchange — that is out of scope here.

## Source

Defined in `03_graph_features.ipynb` / `04_vasp_attribution.ipynb` (Duo A) and implemented in
`backend/main.py` (Duo B). Consumed by `ui/app.py` (Duo C).
