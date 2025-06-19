"""Streamlit interface for managing workflow blueprints.

Run with:
    streamlit run src/workflow_ui.py
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any

import streamlit as st

from src.config import settings

WORKFLOWS_DIR = Path(settings.WORKFLOWS_DIR)
WORKFLOWS_DIR.mkdir(exist_ok=True)

st.title("Workflow Manager")

existing = [p.stem for p in WORKFLOWS_DIR.glob("*.json")]
selected = st.selectbox("Existing workflows", ["<new>"] + existing)

name = st.text_input("Name", value="" if selected == "<new>" else selected)

content: str = ""
if selected != "<new>" and (WORKFLOWS_DIR / f"{selected}.json").exists():
    content = (WORKFLOWS_DIR / f"{selected}.json").read_text()

blueprint_text = st.text_area("Blueprint JSON", value=content, height=300)

col1, col2 = st.columns(2)

with col1:
    if st.button("Load") and selected != "<new>":
        st.experimental_rerun()

with col2:
    if st.button("Save"):
        if not name:
            st.error("Name is required")
        else:
            try:
                data: Dict[str, Any] = json.loads(blueprint_text or "{}")
            except json.JSONDecodeError as exc:
                st.error(f"Invalid JSON: {exc}")
            else:
                path = WORKFLOWS_DIR / f"{Path(name).stem}.json"
                path.write_text(json.dumps(data, indent=2))
                st.success(f"Saved to {path}")
                st.experimental_rerun()
