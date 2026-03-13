import streamlit as st
import pandas as pd
import os
from streamlit.components.v1 import html as st_html

st.set_page_config(page_title="TN Slang Translator - Voice", page_icon="🎙️", layout="wide")

st.title("🎙️ Tamil Nadu COMPLETE Slang Translator — Voice Edition")
st.markdown("**ALL 38 Districts | Voice Input | Text-to-Speech | Dual Tamil/English**")

# ── Load CSV data ──────────────────────────────────────────────────────────────
DISTRICTS = [
    "Chennai", "Cuddalore", "Dharmapuri", "Kanchipuram", "Kanyakumari", "Karur",
    "Krishnagiri", "Madurai", "Mayiladuthurai", "Nagapattinam", "Namakkal", "Nilgiris",
    "Perambalur", "Pudukottai", "Ramanathapuram", "Ranipet", "Salem", "Sivaganga",
    "Tenkasi", "Thanjavur", "Theni", "Thoothukudi", "Tiruchirappalli", "Tirunelveli",
    "Tirupattur", "Tiruppur", "Tiruvallur", "Tiruvannamalai", "Tiruvarur", "Vellore",
    "Viluppuram", "Virudhunagar", "Coimbatore", "Dindigul", "Erode"
]

@st.cache_data
def load_district_slang():
    result = {}
    csv_folder = os.path.join(os.path.dirname(__file__), "slang_data")
    for district in DISTRICTS:
        csv_file = os.path.join(csv_folder, f"{district.lower()}.csv")
        if os.path.exists(csv_file):
            df = pd.read_csv(csv_file)
            slang_dict = {}
            for _, row in df.iterrows():
                slang_dict[str(row['slang'])] = {
                    'tamil':       str(row.get('tamil', '')),
                    'english':     str(row.get('english', '')),
                    'description': str(row.get('description', ''))
                }
            result[district] = slang_dict
        else:
            result[district] = {}
    return result

DISTRICT_SLANG = load_district_slang()

# ── Voice Input Component ───────────────────────────────────────────────────────
VOICE_JS = """
<div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:16px;">
  <button id="micBtn" onclick="toggleVoice()" style="
      width:56px;height:56px;border-radius:50%;border:none;cursor:pointer;
      background:linear-gradient(135deg,#ff6b6b,#ee5a24);color:white;
      font-size:24px;display:flex;align-items:center;justify-content:center;
      box-shadow:0 4px 15px rgba(238,90,36,0.4);transition:all 0.3s;">🎙️</button>

  <div id="voiceStatus" style="
      flex:1;background:#f8f9fa;border:1px solid #e0e0e0;border-radius:8px;
      padding:10px 14px;font-size:14px;color:#555;min-width:160px;">
    Click the mic to speak…
  </div>

  <select id="voiceLang" style="
      padding:8px 12px;border:2px solid #e0e0e0;border-radius:8px;
      font-size:13px;background:white;cursor:pointer;">
    <option value="ta-IN">Tamil (India)</option>
    <option value="en-IN">English (India)</option>
    <option value="en-US">English (US)</option>
  </select>
</div>

<style>
@keyframes pulse{
  0%,100%{transform:scale(1);box-shadow:0 0 0 0 rgba(255,0,0,0.4);}
  50%{transform:scale(1.08);box-shadow:0 0 0 14px rgba(255,0,0,0);}
}
@keyframes ripple{
  0%{transform:scale(0.8);opacity:1;}
  100%{transform:scale(2.4);opacity:0;}
}
#micBtn.recording{animation:pulse 1.2s infinite;background:linear-gradient(135deg,#e74c3c,#c0392b)!important;}
</style>

<script>
var recognition=null,isRecording=false;
var SR=window.SpeechRecognition||window.webkitSpeechRecognition;

if(!SR){
  document.getElementById('micBtn').disabled=true;
  document.getElementById('micBtn').style.opacity='0.4';
  document.getElementById('voiceStatus').textContent='⚠️ Voice not supported in this browser (use Chrome/Edge)';
} else {
  recognition=new SR();
  recognition.continuous=false;
  recognition.interimResults=true;

  recognition.onstart=function(){
    isRecording=true;
    document.getElementById('micBtn').classList.add('recording');
    document.getElementById('micBtn').textContent='⏹️';
    document.getElementById('voiceStatus').textContent='🔴 Listening… speak now';
    document.getElementById('voiceStatus').style.color='#e74c3c';
  };

  recognition.onresult=function(e){
    var interim='',final='';
    for(var i=e.resultIndex;i<e.results.length;i++){
      var t=e.results[i][0].transcript;
      if(e.results[i].isFinal) final+=t; else interim+=t;
    }
    var heard=final||interim;
    if(final){
      document.getElementById('voiceStatus').textContent='✅ Heard: "'+final.trim()+'"';
      document.getElementById('voiceStatus').style.color='#155724';
      // Push to Streamlit via query param trick
      var url=new URL(window.parent.location.href);
      url.searchParams.set('voice_input',final.trim());
      window.parent.history.replaceState(null,'',url);
    }
  };

  recognition.onerror=function(e){
    isRecording=false;
    document.getElementById('micBtn').classList.remove('recording');
    document.getElementById('micBtn').textContent='🎙️';
    document.getElementById('voiceStatus').textContent='Error: '+e.error+'. Try again.';
    document.getElementById('voiceStatus').style.color='#856404';
  };

  recognition.onend=function(){
    isRecording=false;
    document.getElementById('micBtn').classList.remove('recording');
    document.getElementById('micBtn').textContent='🎙️';
  };
}

function toggleVoice(){
  if(!recognition){alert('Voice recognition not supported. Use Chrome or Edge.');return;}
  if(isRecording){recognition.stop();isRecording=false;}
  else{recognition.lang=document.getElementById('voiceLang').value;recognition.start();}
}
</script>
"""

TTS_TMPL = """
<script>
(function(){{
  if(!window.speechSynthesis){{console.warn('TTS not supported');return;}}
  window.speechSynthesis.cancel();
  var u=new SpeechSynthesisUtterance({text!r});
  u.lang={lang!r};u.rate=0.9;u.pitch=1;
  window.speechSynthesis.speak(u);
}})();
</script>
"""

# ── UI Layout ───────────────────────────────────────────────────────────────────
col_input, col_quick = st.columns([3, 1])

with col_input:
    st.header("🎙️ Voice or Type a Slang")
    st_html(VOICE_JS, height=90)

    # Read voice input from query params if set
    params = st.query_params
    default_text = params.get("voice_input", "")
    input_text   = st.text_area("Slang word:", value=default_text, height=80, key="slang_box")
    selected_district = st.selectbox("➜ Show Slangs From:", DISTRICTS)

with col_quick:
    st.header("🔍 Quick Tests")
    for word in ["machan", "da", "ayya", "thambi", "koothu"]:
        if st.button(word, key=f"quick_{word}"):
            st.query_params["voice_input"] = word
            st.rerun()
    if st.button("🗑️ Clear", key="clear_btn"):
        st.query_params.clear()
        st.rerun()

# ── Search Logic ───────────────────────────────────────────────────────────────
def find_matches(text, slangs):
    text_lower = text.lower()
    return [(s, t) for s, t in slangs.items()
            if text_lower in s.lower() or s.lower() in text_lower][:10]

def render_card(slang, trans):
    with st.expander(f"**{slang}** — {trans.get('english', 'N/A')}"):
        c1, c2 = st.columns(2)
        c1.markdown(f"**🇮🇳 Tamil:** {trans.get('tamil', 'N/A')}")
        c2.markdown(f"**🇺🇸 English:** {trans.get('english', 'N/A')}")
        desc = trans.get('description', '').strip()
        if desc and desc.lower() not in ('nan', ''):
            st.markdown(f"**📝 Description:** {desc}")
        else:
            st.caption("Description coming soon…")
        # TTS button
        if st.button(f"🔊 Speak '{slang}'", key=f"tts_{slang}_{id(trans)}"):
            st_html(TTS_TMPL.format(text=slang, lang="ta-IN"), height=0)

if st.button("🚀 FIND & DISPLAY", type="primary"):
    if input_text.strip():
        matches = find_matches(input_text.strip(), DISTRICT_SLANG[selected_district])
        if matches:
            st.success(f"**Found {len(matches)} match(es) in {selected_district}**")
            st.divider()
            for slang, trans in matches:
                render_card(slang, trans)
        else:
            st.warning(f"No matches for '{input_text}' in {selected_district}")
    else:
        st.info("Please enter or speak a slang word first.")

# ── District Browser ────────────────────────────────────────────────────────────
st.header("📍 Browse All Districts")
cols = st.columns(6)
for i, district in enumerate(DISTRICTS):
    with cols[i % 6]:
        if st.button(district[:12], key=f"browse_{i}"):
            st.session_state.current_district = district
            st.rerun()

if 'current_district' in st.session_state:
    d = st.session_state.current_district
    st.markdown(f"### 🔥 **{d} Slang Library**")
    slangs = DISTRICT_SLANG.get(d, {})
    if slangs:
        for slang, trans in list(slangs.items())[:30]:
            render_card(slang, trans)
    else:
        st.info(f"No slangs loaded for {d}. Add CSV data.")

st.markdown("---")
st.markdown("*🎙️ Voice-Enabled | ALL 38 Tamil Nadu Districts | Rich Slang Heritage*")
