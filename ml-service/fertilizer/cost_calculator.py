"""
KisanAI Fertilizer Cost Calculator

This module calculates the estimated cost of a fertilizer
quantity using the fertilizer's stored prototype price.

Important:
- Prices are prototype values stored in fertilizer_database.py.
- They are NOT guaranteed to represent current market prices.
"""


def calculate_cost(quantity_kg, price_per_kg):
    """
    Calculate the estimated fertilizer cost.

    Formula:
        cost = quantity_kg × price_per_kg
    """

    if quantity_kg < 0:
        raise ValueError("Fertilizer quantity cannot be negative.")

    if price_per_kg < 0:
        raise ValueError("Fertilizer price cannot be negative.")

    cost = quantity_kg * price_per_kg

    return round(cost, 2)


if __name__ == "__main__":
    print("=" * 60)
    print("KISANAI FERTILIZER COST CALCULATOR")
    print("=" * 60)

    quantity = 86.96
    price = 25

    cost = calculate_cost(quantity, price)

    print(f"\nFertilizer quantity: {quantity} kg")
    print(f"Price per kg: ₹{price}")
    print(f"Estimated cost: ₹{cost}")