import os
import json

def get_order_by_id(order_id: str) -> dict:
    """
    Looks up an order in the mock database (data/orders.json) by ID,
    normalizes the ID input, cleans/sanitizes private data, and returns the result.
    """
    orders_path = os.path.join("data", "orders.json")
    if not os.path.exists(orders_path):
        return {"error": "Order database not found."}

    # Normalize order_id: remove spaces, convert to uppercase (e.g., "ord-1001" -> "ORD-1001")
    normalized_id = order_id.strip().upper()

    try:
        with open(orders_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            orders = data.get("orders", [])
    except Exception as e:
        return {"error": f"Failed to read order database: {str(e)}"}

    # Find the order
    found_order = None
    for order in orders:
        if order.get("order_id") == normalized_id:
            found_order = order
            break

    if not found_order:
        return {"error": f"Order {normalized_id} not found."}

    # Sanitization: Extract ONLY customer-safe fields. 
    # NEVER include customer name, email, shipping address, or internal note/risk score.
    sanitized_order = {
        "order_id": found_order.get("order_id"),
        "membership_tier": found_order.get("membership_tier"),
        "placed_at": found_order.get("placed_at"),
        "status": found_order.get("status"),
        "status_updated_at": found_order.get("status_updated_at"),
        "shipped_at": found_order.get("shipped_at"),
        "delivered_at": found_order.get("delivered_at"),
        "carrier": found_order.get("carrier"),
        "tracking_number": found_order.get("tracking_number"),
        "estimated_delivery": found_order.get("estimated_delivery"),
        "customer_safe_message": found_order.get("customer_safe_message"),
        "items": []
    }

    # Extract clean item info (safe fields only)
    for item in found_order.get("items", []):
        sanitized_order["items"].append({
            "name": item.get("name"),
            "quantity": item.get("quantity"),
            "final_sale": item.get("final_sale")
        })

    # Status Precedence Rules (from the data dictionary):
    status = sanitized_order["status"]
    
    # 1. Cancelled or Returned orders: clear stale carrier estimates
    if status in ["cancelled", "returned"]:
        sanitized_order["carrier"] = None
        sanitized_order["tracking_number"] = None
        sanitized_order["estimated_delivery"] = None
        sanitized_order["shipped_at"] = None

    # 2. Shipped but missing delivery estimate
    elif status == "shipped" and not sanitized_order["estimated_delivery"]:
        # Do not calculate or guess a date. Leave it as None.
        pass

    # 3. Exception status requires human handoff
    elif status == "exception":
        sanitized_order["requires_human_handoff"] = True

    return sanitized_order
