import streamlit as st
import requests
import time

# --- 1. DESIGN N'ISHUSHO YA WEBSITE (UI CONFIG) ---
st.set_page_config(
    page_title="AECGI Free AI Engine", 
    page_icon="🎬", 
    layout="wide"
)

# Isura ya Kinyamwuga
st.title("🎬 AECGI FREE AI VIDEO ENGINE v11.0")
st.subheader("Hollywood-Grade Animation Studio (Free Tier Node)")
st.write("Urubuga rwa Kinyamwuga rwo Gukora Video z'Ubuntu Ukoresheje AI Idasaba Credit")

st.markdown("---")

# --- 2. SIDEBAR CONFIGURATIONS (API KEY MANAGEMENT) ---
st.sidebar.header("⚙️ AECGI Core Settings")
st.sidebar.write("Umutekano n'Imiyoborere ya System")
replicate_key = st.sidebar.text_input("Shyiramo Replicate API Key:", type="password")

st.sidebar.markdown("---")
st.sidebar.info(
    "ℹ️ Iyi Engine ikorana na Modeli z'ubuntu (Free Open-Source Models) "
    "kuri Replicate, zikora amavidiyo nta kiguzi basabye kuri konti yawe."
)

# --- 3. THE MAIN VIDEO ENGINE ---
st.header("🎞️ Generator & Prompt Studio")
st.write("Andika Prompt (Ibisobanuro), uheze ukande buto ngo AI iguhe video handles.")

# Umwanya wo kwandika prompt
ai_editing_prompt = st.text_area(
    "Andika Prompt ya Video hano (Mu Cyongereza):",
    placeholder="Urugero: A high-speed sports car racing through Kigali streets, photorealistic, cinematic lighting, 4k resolution..."
)

st.markdown("###")

# --- 4. TANGIRA GUKORA VIDEO ---
if st.button("🚀 Tangira Gukora Video") and ai_editing_prompt:
    if not replicate_key:
        st.error("⚠️ Ugomba gushyiramo Replicate API Key mu ruhande (Sidebar) ngo iyi Engine ifungure umuyoboro!")
    else:
        with st.spinner("AECGI Free Core iri gukorana na Server za Replicate... Tegereza gato..."):
            try:
                headers = {
                    "Authorization": f"Token {replicate_key}",
                    "Content-Type": "application/json"
                }
                
                # Iyi ni Modeli y'ubuntu (Stable Video Diffusion cyangwa AnimateDiff) idasaba credit ku masegonda ya mbere
                data = {
                    "version": "392f6699127431114346340426d7b21efc163a1211bc99734a1d831b26551b74", 
                    "input": {
                        "prompt": ai_editing_prompt,
                        "num_frames": 14,
                        "fps": 6
                    }
                }
                
                # Kohereza Itegeko kuri Replicate
                response = requests.post("https://api.replicate.com/v1/predictions", headers=headers, json=data)
                res_json = response.json()
                
                prediction_id = res_json.get("id")
                
                if prediction_id:
                    status = "starting"
                    ai_video_url = ""
                    
                    # Gukurikiranira hafi niba video yuzuye (Polling loop)
                    while status not in ["succeeded", "failed"]:
                        time.sleep(4)
                        check_res = requests.get(f"https://api.replicate.com/v1/predictions/{prediction_id}", headers=headers)
                        status = check_res.json().get("status")
                        
                        if status == "succeeded":
                            ai_video_url = check_res.json().get("output")
                            break
                        elif status == "failed":
                            break
                    
                    if ai_video_url:
                        st.success("✅ Video yawe y'ubuntu iruzuye neza kandi irarangiye!")
                        
                        # Kwerekana Video yuzuye kuri Website
                        if isinstance(ai_video_url, list):
                            st.video(ai_video_url[0])
                        else:
                            st.video(ai_video_url)
                            
                        st.balloons()
                    else:
                        st.error("⚠️ Server yanze gupfunda video. Ongera ugerageze gato.")
                else:
                    st.error("⚠️ API Key yawe harimo akamenyetso kashizwemo nabi. Kora Copy-Paste neza.")
            except Exception as e:
                st.error(f"⚠️ Haza ikosa mu mivugururire: {e}")
