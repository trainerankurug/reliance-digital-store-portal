---
description: Reliance Digital Inventory Monitoring Workflow
on:
  workflow_dispatch:
permissions:
  contents: none
  copilot-requests: write
imports:
  - .github/agents/reliance-digital-inventory-monitoring.agent.md
safe-outputs:
  create-issue:
    title-prefix: "[inventory] "
    max: 1
checkout: false
tools:
  bash: false
  cli-proxy: false
  edit: false
  github: false
jobs:
  inventory_processing:
    name: Process inventory aggregates
    runs-on: ubuntu-latest
    permissions:
      contents: read
    outputs:
      total_product_count: ${{ steps.aggregate.outputs.total_product_count }}
      low_stock_product_count: ${{ steps.aggregate.outputs.low_stock_product_count }}
      out_of_stock_product_count: ${{ steps.aggregate.outputs.out_of_stock_product_count }}
      normal_stock_product_count: ${{ steps.aggregate.outputs.normal_stock_product_count }}
      stock_threshold: ${{ steps.aggregate.outputs.stock_threshold }}
    steps:
      - name: Check out repository for local inventory processing
        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1
      - name: Install backend dependencies
        working-directory: backend
        run: python -m pip install -r requirements.txt
      - name: Calculate and expose only aggregate counts
        id: aggregate
        working-directory: backend
        run: |
          python - <<'PY'
          import os

          from app.agents.inventory_monitoring_agent import run_inventory_monitoring

          report = run_inventory_monitoring()
          values = {
              "total_product_count": report.total_product_count,
              "low_stock_product_count": report.low_stock_count,
              "out_of_stock_product_count": report.out_of_stock_count,
              "normal_stock_product_count": report.normal_stock_count,
              "stock_threshold": 5,
          }
          with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as output:
              for key, value in values.items():
                  output.write(f"{key}={value}\n")
          PY
  agent:
    needs:
      - inventory_processing
    permissions:
      contents: none
      copilot-requests: write
---

# Reliance Digital Inventory Monitoring Workflow

Use the imported Reliance Digital Inventory Monitoring Agent instructions in workflow mode. Analyze only the following sanitized values produced by the separate Python processing job:

- Total product count: `${{ needs.inventory_processing.outputs.total_product_count }}`
- Low-stock product count: `${{ needs.inventory_processing.outputs.low_stock_product_count }}`
- Out-of-stock product count: `${{ needs.inventory_processing.outputs.out_of_stock_product_count }}`
- Normal-stock product count: `${{ needs.inventory_processing.outputs.normal_stock_product_count }}`
- Stock threshold: `${{ needs.inventory_processing.outputs.stock_threshold }}`

Prepare a concise inventory report using only these values. State stock conditions and recommend manager review when low-stock or out-of-stock counts are nonzero. Do not invent missing information or identify individual products. Request one GitHub issue using the safe issue output with the aggregate report. Never modify inventory, prices, transactions, or purchase orders, and perform no financial operations.
