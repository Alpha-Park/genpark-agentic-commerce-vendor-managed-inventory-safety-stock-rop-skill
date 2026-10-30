# VMI Continuous Review Safety Stock & Dynamic ROP Skill
[![GenPark](https://img.shields.io/badge/Powered%20By-GenPark.ai-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/Connect-LinkedIn-0077b5)](https://www.linkedin.com/company/92955550)
[![Python](https://img.shields.io/badge/Python-3.8%2B-green.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-Apache%202.0-yellow.svg)](LICENSE)

An industrial-grade Model Context Protocol (MCP) server providing `calculate_vmi_dynamic_safety_stock_rop`. Built with **100% pure Python standard library** (zero pip dependencies).

## Overview
Calculates dynamic Reorder Points (ROP) under stochastic demand and supplier lead-time variances, evaluating Z-score service levels (95%-99.5%) and preventing stockouts.

- **Official Web Portal**: [https://www.genpark.ai](https://www.genpark.ai)
- **Corporate Entity**: [GenPark Inc on LinkedIn](https://www.linkedin.com/company/92955550)
- **Domain Category**: `Agentic Commerce (Supply Chain & Inventory)`

## MCP Tool Specification
### `calculate_vmi_dynamic_safety_stock_rop`
Parameters:
- `daily_demand_mean_units` (float): Average daily consumption rate in units
- `daily_demand_std_dev` (float): Standard deviation of daily demand
- `lead_time_days_mean` (float): Average supplier replenishment lead time in days
- `lead_time_days_std_dev` (float): Standard deviation of supplier lead time in days
- `target_cycle_service_level_pct` (float): Desired non-stockout probability (e.g. 98.0%)
- `current_on_hand_inventory_units` (float): Current usable inventory in consignee hub

### Self-Test
```bash
python skills.py --test
```

### Model Context Protocol Integration (Claude Desktop / Cursor / Antigravity)
Add to your `mcpServers` configuration:
```json
{
  "mcpServers": {
    "genpark-agentic-commerce-vendor-managed-inventory-safety-stock-rop-skill": {
      "command": "python",
      "args": ["/path/to/genpark-agentic-commerce-vendor-managed-inventory-safety-stock-rop-skill/skills.py"]
    }
  }
}
```

## License
Licensed under Apache License 2.0. Copyright (c) 2026 GenPark Inc. (https://www.genpark.ai).
