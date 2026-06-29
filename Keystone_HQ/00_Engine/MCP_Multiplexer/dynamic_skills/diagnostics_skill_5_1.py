
def get_preservation_threshold(weight_lbs: float, training_intensity: float) -> dict:
    # empirical protein material calculations
    base_protein = weight_lbs * 1.0 # 1g per lb of body weight
    if training_intensity > 0.8:
        base_protein += 45.0 # extra material for Angiogenesis recovery
    return {"threshold_lbs": base_protein}
