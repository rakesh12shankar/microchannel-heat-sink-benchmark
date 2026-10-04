# Figure 7 digitization

These are approximate readings from the supplied PDF, not author-provided raw data.

The PDF's ninth page was rendered at 4x scale. The Figure 7a crop used full-image pixel bounds (300,950)-(1080,1370); Figure 7b used (1120,950)-(1960,1390). In crop coordinates:

- Figure 7a vertical calibration: T=0 C at y=405; T=140 C at y=54.
- Figure 7b vertical calibration: T=0 C at y=404; T=180 C at y=53.
- Experimental symbols were read at the four tabulated sensor x locations. Assigned reading uncertainty: +/-1 C, separate from the paper's thermocouple uncertainty.
- Published numerical curves were sampled approximately 10 pixels on either side of each sensor marker to avoid the symbol, then averaged. Figure 7b's third sensor has text obscuring part of the two lower curves; their right-hand continuation was used with a small local-slope allowance. Assigned reading uncertainty for numerical curves: +/-1.5 C. Pixel y selections are retained in `paper_numerical_digitized.csv`.

The two comparisons answer different questions. Agreement with experimental symbols assesses physical prediction, while agreement with the paper's numerical curves assesses reproduction of its numerical model. Neither should be silently substituted for the other. The published curves themselves differ from some experimental points by several degrees.
