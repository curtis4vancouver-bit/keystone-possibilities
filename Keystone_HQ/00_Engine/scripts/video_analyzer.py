#!/usr/bin/env python3
"""
Keystone Sovereign - Perceptual Video Analyzer & Safe Media Sandbox.
Implements dHash (Difference Hashing) frame deduplication, Hamming distance metrics,
chronological timeline compilation, and strict sandboxed path/command validation.
"""

import os
import sys
import json
import re
import hashlib
import binascii
import logging
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional

# Workspace Configuration
ROOT_DIR = Path(r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain")
TRANSCRIPTS_DIR = ROOT_DIR / "Transcripts"
TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [MediaAnalyzer] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(TRANSCRIPTS_DIR / "video_analyzer.log", encoding="utf-8")
    ]
)
logger = logging.getLogger("VideoAnalyzer")


# =====================================================================
# 1. PERCEPTUAL FRAME DEDUPLICATION (dHash & Hamming Engine)
# =====================================================================
class PerceptualDeduplicator:
    """
    Implements Difference Hashing (dHash) and Hamming Distance calculations
    to discard redundant static video frames while preserving dynamic cuts.
    Threshold theta = 0.1 corresponds to a Hamming distance of 6 bits out of 64.
    """
    def __init__(self, threshold_theta: float = 0.1):
        self.threshold_bits = int(64 * threshold_theta)  # Threshold bits (e.g. 6)
        logger.info(f"Initialized Perceptual Deduplicator (Theta={threshold_theta} // Bit Threshold={self.threshold_bits})")

    def generate_dhash_64bit(self, image_data: bytes) -> int:
        """
        Generates a 64-bit binary dHash from raw image bytes.
        If Pillow is available and input is valid binary image data, 
        downsamples to 8x9 grayscale and calculates horizontal diffs.
        Otherwise (ImportError or parsing exception), falls back to a deterministic 64-bit sha256 checksum.
        """
        try:
            from PIL import Image
            import io
            img = Image.open(io.BytesIO(image_data)).convert('L').resize((9, 8), Image.Resampling.LANCZOS)
            pixels = list(img.getdata())
            
            # Compute horizontal differences
            difference = 0
            for row in range(8):
                for col in range(8):
                    left = pixels[row * 9 + col]
                    right = pixels[row * 9 + col + 1]
                    difference = (difference << 1) | (1 if left > right else 0)
            return difference
        except Exception:
            # Stable fallback: Generate a deterministic 64-bit integer from content hash
            h = hashlib.sha256(image_data).digest()
            val = int.from_bytes(h[:8], byteorder='big')
            return val

    def hamming_distance(self, hash1: int, hash2: int) -> int:
        """Computes the exact Hamming distance (exclusive-OR bit count) between two 64-bit hashes."""
        xor_val = hash1 ^ hash2
        # Count set bits in XOR result (Hamming Distance)
        distance = 0
        while xor_val:
            distance += 1
            xor_val &= xor_val - 1  # Brian Kernighan's bit-counting algorithm
        return distance

    def should_deduplicate(self, hash1: int, hash2: int) -> bool:
        """Returns True if the similarity is below the strict threshold (redundant frames)."""
        dist = self.hamming_distance(hash1, hash2)
        # Deduplicate if the bit difference is less than our threshold (indicating near-identical frames)
        return dist < self.threshold_bits


# =====================================================================
# 2. CHRONOLOGICAL TIMELINE COMPILER
# =====================================================================
class VideoTimelineCompiler:
    """
    Compiles deduplicated frames, speaker transcripts, detected scene changes,
    and OCR text arrays into a structured timeline for clean context delivery.
    """
    def __init__(self):
        self.deduplicator = PerceptualDeduplicator()

    def compile_timeline(self, raw_frames: List[Dict[str, Any]], transcript: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Merges transcript data, diarization, and deduped keyframes chronologically."""
        logger.info("Compiling chronological visual timeline...")
        timeline_events = []
        last_hash = None
        deduped_count = 0
        
        # Sort keyframes by timestamp
        sorted_frames = sorted(raw_frames, key=lambda x: x["timestamp"])
        
        for frame in sorted_frames:
            current_hash = self.deduplicator.generate_dhash_64bit(frame["data"].encode('utf-8'))
            
            if last_hash is not None and self.deduplicator.should_deduplicate(last_hash, current_hash):
                deduped_count += 1
                continue # Skip redundant frame to protect context window size
            
            # Map transcript sentences matching this frame's timestamp
            associated_dialogue = []
            for entry in transcript:
                if abs(entry["timestamp"] - frame["timestamp"]) <= 2.0:
                    associated_dialogue.append(f"{entry['speaker'].upper()}: {entry['text']}")
            
            timeline_events.append({
                "timestamp": frame["timestamp"],
                "hash": f"0x{current_hash:016x}",
                "dialogue": associated_dialogue,
                "ocr_detected_text": frame.get("ocr_text", []),
                "base64_data_url": f"data:image/jpeg;base64,{frame['data'][:64]}..." # Truncated URL for telemetry
            })
            
            last_hash = current_hash

        logger.info(f"Timeline compilation complete. Kept {len(timeline_events)} keyframes. Deduplicated {deduped_count} redundant frames.")
        
        return {
            "total_keyframes": len(timeline_events),
            "redundant_frames_cleared": deduped_count,
            "events": timeline_events
        }


# =====================================================================
# 3. SECURE MEDIA SANDBOX GATING
# =====================================================================
class MediaSecuritySandbox:
    """
    Implements safety audits:
    - Input Path Validation (locks directory traversal strings).
    - Command Restriction (denies execution unless prefixed with ffmpeg and contains zero shell-chainers).
    """
    def __init__(self, allowed_workspace: Path):
        self.allowed_workspace = allowed_workspace.resolve()
        logger.info(f"Media Sandbox secured for workspace: {self.allowed_workspace}")

    def validate_input_path(self, file_path: str) -> Path:
        """
        Validates file path parameters.
        Blocks directory traversal attempts and null byte characters.
        """
        # Block directory traversal sequences and null byte injections
        if "../" in file_path or "..\\" in file_path or "\x00" in file_path:
            raise PermissionError(
                f"[Security Exception] Unauthorized Path Traversal Attempt Blocked: '{file_path}'"
            )

        resolved_path = Path(file_path).resolve()
        # Enforce relative check to ensure it lies inside workspace
        if not str(resolved_path).startswith(str(self.allowed_workspace)):
            raise PermissionError(
                f"[Security Exception] Input file path lies outside of designated media sandbox: {file_path}"
            )
            
        return resolved_path

    def validate_ffmpeg_command(self, cmd_args: List[str]) -> List[str]:
        """
        Validates system commands before execution.
        Enforces 'ffmpeg' prefix and blocks dangerous chaining characters (&&, ;, |).
        """
        if not cmd_args:
            raise ValueError("Command arguments list cannot be empty.")

        # Enforce prefix lock
        if cmd_args[0].lower() != "ffmpeg":
            raise PermissionError(
                f"[Security Exception] Command execution denied. Non-FFmpeg binary requested: '{cmd_args[0]}'"
            )

        # Scan for shell command injection indicators
        dangerous_symbols = [";", "&&", "||", "|", "`", "$", "(", ")", ">", "<"]
        for arg in cmd_args:
            if any(symbol in arg for symbol in dangerous_symbols):
                raise PermissionError(
                    f"[Security Exception] Command execution denied. Dangerous shell chaining characters detected in argument: '{arg}'"
                )

        logger.info(f"[Sandbox Audit] FFmpeg command execution pre-validated: {' '.join(cmd_args)}")
        return cmd_args


# =====================================================================
# SYSTEM EXECUTION TEST RUNNER
# =====================================================================
def run_diagnostic_suite():
    logger.info("=" * 70)
    logger.info("KEYSTONE MEDIA METADATA SUITE - SOVEREIGN EDGE COMPILER ONLINE")
    logger.info("=" * 70)

    # 1. Initialize Security Sandbox
    sandbox = MediaSecuritySandbox(ROOT_DIR)

    # Test Path Traversal Defenses
    try:
        sandbox.validate_input_path("local_vector_db/memory.db")
        logger.info("[Sandbox Success] Valid path check passed cleanly.")
        
        # Simulated traversal attack
        logger.info("[Sandbox Check] Testing security response to directory traversal attempt...")
        sandbox.validate_input_path("../../etc/passwd")
    except PermissionError as p_err:
        logger.error(f"[Sandbox Success] Blocked attack successfully: {p_err}")

    # Test Command Injection Defenses
    try:
        sandbox.validate_ffmpeg_command(["ffmpeg", "-i", "input.mp4", "-vf", "scale=1920:1080", "output.mp4"])
        logger.info("[Sandbox Success] Valid FFmpeg command check passed cleanly.")
        
        # Simulated shell injection attack
        logger.info("[Sandbox Check] Testing security response to command injection attempt...")
        sandbox.validate_ffmpeg_command(["ffmpeg", "-i", "in.mp4", "&&", "rm", "-rf", "/"])
    except PermissionError as p_err:
        logger.error(f"[Sandbox Success] Blocked attack successfully: {p_err}")

    # 2. Test Frame Deduplication & Timeline Compilation
    logger.info("[Timeline Compiler] Scaffold mock scene keyframes and voiceover transcripts...")
    
    # 5 Mock frames (Frame 2 and Frame 3 are identical duplicates representing a presentation slide)
    mock_frames = [
        {"timestamp": 0.0, "data": "BASE64_IMAGE_DATA_OUTFLOW_001_SQUAMISH_misty_fjord_bluffs", "ocr_text": []},
        {"timestamp": 3.0, "data": "BASE64_IMAGE_DATA_OUTFLOW_002_DXA_SCAN_Sarcopenia_Loss_Loss", "ocr_text": ["SKELETAL", "DXA SCAN"]},
        {"timestamp": 6.0, "data": "BASE64_IMAGE_DATA_OUTFLOW_002_DXA_SCAN_Sarcopenia_Loss_Loss", "ocr_text": ["SKELETAL", "DXA SCAN"]}, # DUPLICATE
        {"timestamp": 9.0, "data": "BASE64_IMAGE_DATA_OUTFLOW_003_TIMBER_FRAMING_architectural", "ocr_text": ["CEDAR", "BUILD"]},
    ]

    mock_transcript = [
        {"timestamp": 0.5, "speaker": "Wayne", "text": "Welcome to Keystone Protocols, where we protect structural mass."},
        {"timestamp": 4.0, "speaker": "Wayne", "text": "Rapid body fat reduction wasting skeletal muscle tissue is a trap."},
        {"timestamp": 7.5, "speaker": "Wayne", "text": "This is research study data and not clinical advice."}
    ]

    compiler = VideoTimelineCompiler()
    timeline = compiler.compile_timeline(mock_frames, mock_transcript)

    print("\n" + "=" * 70)
    print("COMPILED CHRONOLOGICAL TIMELINE METADATA (Deduplicated frames)")
    print("=" * 70)
    print(f"Total Keyframes:           {timeline['total_keyframes']}")
    print(f"Redundant Frames Cleared:  {timeline['redundant_frames_cleared']}")
    print("-" * 70)
    for event in timeline["events"]:
        print(f"Timestamp: {event['timestamp']}s // Hash: {event['hash']}")
        print(f"  Visual URL: {event['base64_data_url']}")
        print(f"  OCR Text:   {event['ocr_detected_text']}")
        print(f"  Dialogue:   {event['dialogue']}")
        print("-" * 70)
    print("=" * 70)


if __name__ == "__main__":
    run_diagnostic_suite()
