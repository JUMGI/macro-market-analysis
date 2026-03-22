def log_panel(panel, assets, families, alignment):

    n_rows, n_cols = panel.shape
    nan_pct = panel.isna().mean().mean() * 100

    print("\n=== PANEL BUILT ===")
    print(f"Assets: {assets}")
    print(f"Families: {families}")
    print(f"Shape: {n_rows} x {n_cols}")
    print(f"Date range: {panel.index.min()} → {panel.index.max()}")
    print(f"NaN %: {nan_pct:.2f}%")
    print(f"Alignment: {alignment}")
    print("====================\n")