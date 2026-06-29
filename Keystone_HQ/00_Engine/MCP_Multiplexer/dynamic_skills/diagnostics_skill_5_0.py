
def get_acoustic_layers(tempo: int, frequency: float) -> dict:
    # Stoic builder sonic layout mapping
    if tempo < 120:
        return {"layers": ["ambient_solfeggio_396hz"]}
    layers = ["tech_house_bass", "solfeggio_528hz_layer"]
    if frequency > 400.0:
        layers.append("progressive_middle_eastern_lead")
    return {"layers": layers}
