import streamlit as st
import random
import time

st.set_page_config(page_title="MURDER", layout="centered")

# -----------------------------
# Initialisierung
# -----------------------------
if "state" not in st.session_state:
    st.session_state.state = "servant"
    st.session_state.distance = 100
    st.session_state.difficulty = 1
    st.session_state.assassin_side = None
    st.session_state.attack_time = None

st.title("🗡️ MURDER")

# -----------------------------
# DIENER-PHASE
# -----------------------------
if st.session_state.state == "servant":
    st.subheader("Du bist ein Diener.")
    st.write("Schleiche dich an den König heran.")
    
    st.session_state.distance -= random.randint(5, 15)
    st.progress(max(0, 100 - st.session_state.distance))

    if st.button("🗡️ Mordversuch"):
        if st.session_state.distance <= 20:
            st.session_state.state = "king"
            st.session_state.difficulty = 1
            st.success("Der Mord gelingt. Du bist jetzt König.")
            st.rerun()
        else:
            st.session_state.state = "dead"
            st.rerun()

    st.caption("Je näher du bist, desto besser dein Timing.")

# -----------------------------
# KÖNIGS-PHASE
# -----------------------------
elif st.session_state.state == "king":
    st.subheader("👑 Du bist König.")
    st.write(f"Schwierigkeit: {st.session_state.difficulty}")

    # Neuen Attentäter erzeugen
    if st.session_state.assassin_side is None:
        st.session_state.assassin_side = random.choice(["links", "rechts"])
        st.session_state.attack_time = time.time()

    reaction_window = max(0.6, 2.0 - st.session_state.difficulty * 0.15)

    st.warning(f"⚠️ Ein Attentäter nähert sich von **{st.session_state.assassin_side.upper()}**!")
    st.caption(f"Reaktionszeit: {reaction_window:.2f} Sekunden")

    col1, col2 = st.columns(2)

    def defend(side):
        now = time.time()
        if (
            side == st.session_state.assassin_side
            and now - st.session_state.attack_time <= reaction_window
        ):
            st.session_state.difficulty += 1
            st.session_state.assassin_side = None
            st.success("Angriff abgewehrt!")
            st.rerun()
        else:
            st.session_state.state = "dead"
            st.rerun()

    with col1:
        if st.button("⬅️ Links abwehren"):
            defend("links")

    with col2:
        if st.button("➡️ Rechts abwehren"):
            defend("rechts")

    # Zu langsam = Tod
    if time.time() - st.session_state.attack_time > reaction_window:
        st.session_state.state = "dead"
        st.rerun()

# -----------------------------
# TOD
# -----------------------------
elif st.session_state.state == "dead":
    st.error("☠️ DU BIST TOT")
    st.write("Macht ist vergänglich.")
    if st.button("🔄 Neustart"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
