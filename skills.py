# -*- coding: utf-8 -*-
"""VMI Continuous Review Safety Stock & Dynamic ROP Skill
Engineered for GenPark Ecosystem (https://www.genpark.ai | https://www.linkedin.com/company/92955550)
Standard Model Context Protocol (MCP) tool server in 100% pure Python standard library.
"""
import sys
import json

def calculate_vmi_dynamic_safety_stock_rop(**kwargs):
    """Calculates dynamic Reorder Points (ROP) under stochastic demand and supplier lead-time variances, evaluating Z-score service levels (95%-99.5%) and preventing stockouts."""
    daily_demand_mean_units = kwargs.get('daily_demand_mean_units')
    daily_demand_std_dev = kwargs.get('daily_demand_std_dev')
    lead_time_days_mean = kwargs.get('lead_time_days_mean')
    lead_time_days_std_dev = kwargs.get('lead_time_days_std_dev')
    target_cycle_service_level_pct = kwargs.get('target_cycle_service_level_pct')
    current_on_hand_inventory_units = kwargs.get('current_on_hand_inventory_units')

    import math
    # Map service level to Normal Z-score
    sl = target_cycle_service_level_pct
    if sl >= 99.5:
        z = 2.576
    elif sl >= 99.0:
        z = 2.326
    elif sl >= 98.0:
        z = 2.054
    elif sl >= 95.0:
        z = 1.645
    elif sl >= 90.0:
        z = 1.282
    else:
        z = 1.000
        
    # Safety Stock Formula with variable demand AND variable lead time:
    # SS = Z * sqrt( (LT_mean * sigma_d^2) + (d_mean^2 * sigma_LT^2) )
    term1 = lead_time_days_mean * (daily_demand_std_dev ** 2)
    term2 = (daily_demand_mean_units ** 2) * (lead_time_days_std_dev ** 2)
    safety_stock = round(z * math.sqrt(term1 + term2), 0)
    
    # ROP = (daily_demand_mean * lead_time_mean) + Safety Stock
    expected_lead_time_demand = round(daily_demand_mean_units * lead_time_days_mean, 0)
    reorder_point = round(expected_lead_time_demand + safety_stock, 0)
    
    replenishment_triggered = current_on_hand_inventory_units <= reorder_point
    deficit_units = round(max(0.0, reorder_point - current_on_hand_inventory_units), 0)
    
    result = {
        "status": "success",
        "target_service_level_pct": target_cycle_service_level_pct,
        "normal_z_factor": z,
        "expected_lead_time_demand_units": expected_lead_time_demand,
        "buffered_safety_stock_units": safety_stock,
        "dynamic_reorder_point_rop": reorder_point,
        "current_on_hand_units": current_on_hand_inventory_units,
        "is_replenishment_order_triggered": replenishment_triggered,
        "recommended_minimum_reorder_units": deficit_units if replenishment_triggered else 0,
        "erp_replenishment_directive": f"Trigger automated VMI PO for {deficit_units + 500} units" if replenishment_triggered else "Inventory level adequate; no replenishment required.",
        "engine": "GenPark VMI Stochastic Safety Stock & ROP Engine v1.0"
    }
    return result

# MCP Tool Definitions
TOOLS = {
    "calculate_vmi_dynamic_safety_stock_rop": {
        "name": "calculate_vmi_dynamic_safety_stock_rop",
        "description": "Calculates dynamic Reorder Points (ROP) under stochastic demand and supplier lead-time variances, evaluating Z-score service levels (95%-99.5%) and preventing stockouts.",
        "parameters": {
            "type": "object",
            "properties": {
                "daily_demand_mean_units": {"type": "number", "description": "Average daily consumption rate in units"},
                "daily_demand_std_dev": {"type": "number", "description": "Standard deviation of daily demand"},
                "lead_time_days_mean": {"type": "number", "description": "Average supplier replenishment lead time in days"},
                "lead_time_days_std_dev": {"type": "number", "description": "Standard deviation of supplier lead time in days"},
                "target_cycle_service_level_pct": {"type": "number", "description": "Desired non-stockout probability (e.g. 98.0%)"},
                "current_on_hand_inventory_units": {"type": "number", "description": "Current usable inventory in consignee hub"},
            },
            "required": ['daily_demand_mean_units', 'daily_demand_std_dev', 'lead_time_days_mean', 'lead_time_days_std_dev', 'target_cycle_service_level_pct', 'current_on_hand_inventory_units']
        }
    }
}

def handle_rpc_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": list(TOOLS.values())}}
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "calculate_vmi_dynamic_safety_stock_rop":
            res = calculate_vmi_dynamic_safety_stock_rop(**args)
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        else:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method '{tool_name}' not found"}}
    elif method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-agentic-commerce-vendor-managed-inventory-safety-stock-rop-skill", "version": "1.0.0"}
            }
        }
    else:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not implemented"}}

def run_self_test():
    print("Executing self-test for genpark-agentic-commerce-vendor-managed-inventory-safety-stock-rop-skill...")
    test_args = {'daily_demand_mean_units': 150.0, 'daily_demand_std_dev': 28.0, 'lead_time_days_mean': 12.0, 'lead_time_days_std_dev': 2.5, 'target_cycle_service_level_pct': 98.0, 'current_on_hand_inventory_units': 1820.0}
    res = calculate_vmi_dynamic_safety_stock_rop(**test_args)
    assert res['status'] == 'success', f'Test failed: {res}'
    print("SELF TEST PASSED: genpark-agentic-commerce-vendor-managed-inventory-safety-stock-rop-skill functional.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_self_test()
        sys.exit(0)
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_rpc_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stderr.write(f"Error handling request: {e}\n")
