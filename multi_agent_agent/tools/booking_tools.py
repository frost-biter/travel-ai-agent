from typing import Dict, Any, Optional
from datetime import datetime

def simulate_booking(
    flight_id: Optional[str] = None,
    hotel_id: Optional[str] = None,
    guests: int = 1,
    payment_method: str = "credit_card"
) -> Dict[str, Any]:
    """
    Simulate a travel booking process.
    
    Args:
        flight_id: Optional flight offer ID to book
        hotel_id: Optional hotel offer ID to book
        guests: Number of guests (default: 1)
        payment_method: Payment method to simulate (default: credit_card)
        
    Returns:
        Dictionary containing booking simulation results
    """
    booking_ref = f"BK{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    booking_items = []
    total_price = 0.0
    
    if flight_id:
        flight_price = 500.00  # Simulated price
        booking_items.append({
            "type": "flight",
            "id": flight_id,
            "price": flight_price,
            "guests": guests
        })
        total_price += flight_price * guests
    
    if hotel_id:
        hotel_price = 200.00  # Simulated price per night
        nights = 1  # Simulated duration
        booking_items.append({
            "type": "hotel",
            "id": hotel_id,
            "price_per_night": hotel_price,
            "nights": nights,
            "guests": guests
        })
        total_price += hotel_price * nights * guests
    
    return {
        "booking_reference": booking_ref,
        "status": "confirmed",
        "items": booking_items,
        "total_price": total_price,
        "currency": "USD",
        "guests": guests,
        "payment": {
            "method": payment_method,
            "status": "simulated",
            "amount": total_price
        },
        "note": "(This is a simulated booking - no actual reservations or charges were made)"
    } 