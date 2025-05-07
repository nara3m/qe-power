# Turbo Pump Voltage-Current Dashboard

This script processes a TSV file containing date-time and measurement data, then generates an interactive Bokeh dashboard with scatter plots for voltage and current data.

## Features

- Reads and preprocesses a TSV file.
- Extracts datetime and two numeric columns (6th and 7th).
- Cleans data by removing rows with invalid datetime or numeric values.
- Optionally removes outliers using the IQR method (commented out in the script).
- Generates two scatter plots (datetime vs. voltage and datetime vs. current).
- Adds interactive hover tools and zoom/pan functionality.
- Saves the resulting dashboard as a standalone HTML file.

## File Requirements

- Input `.tsv` file must:
  - Use tab (`\t`) as delimiter.
  - Include a `DateTime` column.
  - Have at least 7 columns (uses 6th and 7th columns for plots).

## Output

- `processed_volt_current.tsv`: Cleaned version of the input data.
- `2025_TurboPump_Power_VoltxCurr_Log_NM.html`: Bokeh dashboard with interactive plots.

## Usage

1. Place your input `.tsv` file in the script directory.
2. Edit the script to set the correct `input_file` and `output_html` names.
3. Run the script:
   ```bash
   python power.py
   ```
4. Open the generated `.html` file in a browser to explore the plots.

## Dependencies

- `pandas`
- `bokeh`

Install required packages with:
```bash
pip install pandas bokeh
```

## Notes

- Outlier removal using IQR is available via the `remove_outliers()` function, currently commented out.
- The 6th and 7th columns in the TSV file are assumed to be voltage and current or similar numeric metrics.
