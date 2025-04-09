DISCOUNT_THRESHOLD = 10      # units
DISCOUNT_RATE = 0.10         # 10%
SHIPPING_THRESHOLD = 50.0    # dollars
SHIPPING_FEE = 5.0           # flat rate


def calculate_item_total(price: float, quantity: int) -> float:
    """
    Apply bulk discount if quantity exceeds threshold.
    """
    if quantity >= DISCOUNT_THRESHOLD:
        return price * quantity * (1 - DISCOUNT_RATE)
    return price * quantity


def apply_shipping(subtotal: float) -> float:
    """
    Add flat shipping fee if subtotal is under the threshold.
    """
    return SHIPPING_FEE if subtotal < SHIPPING_THRESHOLD else 0.0


def calculate_order_total(items: list[dict]) -> tuple[float, list[float]]:
    """
    Calculate total for all items and return per-item prices.
    `items` is a list of dicts with 'price' and 'quantity'.
    """
    item_totals = []
    subtotal = 0

    for item in items:
        total = calculate_item_total(item["price"], item["quantity"])
        item_totals.append(total)
        subtotal += total

    shipping = apply_shipping(subtotal)
    total_with_shipping = subtotal + shipping

    return total_with_shipping, item_totals
