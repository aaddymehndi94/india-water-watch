# 15 · Outlook and prediction contract

## Four different products

1. **Observed:** a measurement with observation period and source.
2. **Official/research forecast:** the named provider's forecast, issue date, validity, geography, target variable, probability if actually provided, and known limits.
3. **Scenario:** conditional reasoning from explicit assumptions. It is not a prediction or probability.
4. **Long-term projection:** a model result under a stated climate/demographic/economic scenario, not a dated near-term warning.

Do not join these with one continuous unlabeled line. Do not imply an LLM forecast is scientific because it is numerically precise.

## Launch default

Publish reviewed official forecasts with attribution and expiry. Build a conditional scenario explorer where grounded in understandable physical/resource assumptions. No new machine-learned drought model is required for launch. A clear explanation of forecast uncertainty is more valuable than an unvalidated prediction layer.

## Official outlook records

Provider, exact bulletin, issue/valid-from/valid-to, target period, region/version, variable/unit, categories and any probability, model/ensemble information if supplied, skill/caveat, evidence record and source link. An all-India seasonal category cannot be assigned to every district. A probability for below-normal rainfall is not the probability of taps running dry.

Expire highlight status automatically at the appropriate date; archive the record. Forecasts must remain recognizable as historical forecasts after the event occurs. Do not quietly rewrite them to match the outcome.

## Conditional severe-outcome explorer

Each branch needs a bounded geography and time horizon, starting observations, assumptions, causal pathways, supporting evidence, possible buffers, recovery/reversal signals, and what data would be required to quantify it. Show at least a recovery branch alongside sustained-stress and compounded-stress branches when appropriate. These are scenarios, not three probabilities summing to 100.

Example design questions, not asserted outcomes: How could successive weak rainy periods interact with observed low storage? How would documented irrigation restrictions affect a particular crop calendar? Which supply-chain dependencies are shared across income groups? What observations would show that concern is easing?

Do not invent numbers for deaths, displaced people, crop losses, food prices or water-exhaustion dates. A numeric scenario must use unit-consistent inputs and a reviewed model. A qualitative branch is preferable to false precision. A worst conceivable apocalypse is not a useful scenario; use plausible bounded conditions that can be checked.

## Water-balance models, only if feasible

A reservoir model needs `next_storage = storage + inflow − allocated releases − evaporation − other losses`, with consistent time units and capacity/operating constraints. Explain how inputs are estimated, treatment/dead-storage limits, allocation priorities and sensitivity. Do not derive inflow by equating it to rainfall over an arbitrary area. Do not double-count connected reservoirs or transfers.

A household cost illustration needs an actual tariff/price source, volume assumptions, geography/date and clear exclusions. It is not a measured household spending survey.

## New prediction-model gate

Only after adequate data exist: define outcome and horizon before fitting; use time-ordered training/backtesting; prevent look-ahead/data revision leakage; compare with climatology/persistence; report calibration and relevant scoring/interval coverage; evaluate geography and regime transfer; document missingness and uncertainty; obtain independent hydrological/model review. Publish a model card and archived forecasts. If evidence of useful skill is absent, withhold the model and retain official outlooks/scenarios.

Never produce risk probabilities merely to make the dashboard interactive. No political/election forecasting belongs in this product.
