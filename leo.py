"""
╔══════════════════════════════════════════════════════════╗
║        FlexCoach — AI Health Coach App v7                ║
║  FULLY AI-POWERED using Google Gemini (FREE)             ║
║                                                          ║
║  Features:                                               ║
║  • AI Chat — real GPT-powered health coach               ║
║  • AI Meal Plans — unique every time, personalised       ║
║  • AI Workout Plans — personalised per profile           ║
║  • AI Meditation — goal-based guided sessions            ║
║  • AI Calorie Checker — camera + vision AI               ║
║  • Water Tracker, BMI, Medications, Streaks, XP          ║
║  • Aria — AI girl voice coach                            ║
║                                                          ║
║  Setup:                                                  ║
║  1. Get FREE key at https://aistudio.google.com          ║
║  2. Add to Streamlit secrets:                            ║
║       GEMINI_API_KEY = "AIza..."                         ║
║  3. pip install streamlit google-generativeai pillow     ║
║  4. streamlit run health_coach_app.py                    ║
╚══════════════════════════════════════════════════════════╝
"""

import streamlit as st
import streamlit.components.v1 as components
import datetime, math, random, base64, io, re
from collections import Counter

# ── Gemini setup ─────────────────────────────────────────────────────────────
try:
    import google.generativeai as genai
    _KEY = st.secrets.get("GEMINI_API_KEY", "")
    if _KEY:
        genai.configure(api_key=_KEY)
    AI_OK = bool(_KEY)
except Exception:
    AI_OK = False

# ─── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FlexCoach – AI Health Coach",
    page_icon="💪❤️🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Dark mode CSS ───────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600;700&family=Inter:wght@300;400;500;600&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;background:#0d0d0d!important;color:#e0e0e0!important}
h1,h2,h3{font-family:'Orbitron',sans-serif;color:#00e676!important}
h4,h5,p,span,div,label{color:#e0e0e0}
header{visibility:hidden}
.main,.block-container{background:#0d0d0d!important}
.fc-card{background:#161625;border:1px solid #252545;border-radius:16px;padding:1.4rem;
         box-shadow:0 4px 24px rgba(0,230,118,.07);margin-bottom:1rem;color:#e0e0e0}
.onboard{max-width:660px;margin:1.5rem auto;background:#161625;border:1px solid #252545;
         border-radius:24px;padding:2.5rem 2.8rem;box-shadow:0 4px 40px rgba(0,230,118,.12)}
.xpbar-bg{background:rgba(255,255,255,.07);border-radius:999px;height:10px;margin:6px 0 2px;overflow:hidden}
.xpbar-fill{height:100%;border-radius:999px;background:linear-gradient(90deg,#00c853,#00e676);
            box-shadow:0 0 8px rgba(0,230,118,.5)}
.lvl-lbl{font-size:.75rem;letter-spacing:.06em;opacity:.7;margin-bottom:2px;color:#00e676!important}
.badge-grid{display:flex;flex-wrap:wrap;gap:10px;margin:.6rem 0}
.badge-pill{border-radius:999px;padding:5px 14px;font-size:.82rem;font-weight:600;
            display:inline-flex;align-items:center;gap:5px}
.badge-on{background:#0d2818;color:#00e676;border:1.5px solid #00e676}
.badge-off{background:#161625;color:#444;border:1.5px solid #252545}
.toast{background:linear-gradient(135deg,#0a1f10,#0d2615);border-left:4px solid #00e676;
       border-radius:12px;padding:1rem 1.3rem;margin:.6rem 0;
       box-shadow:0 2px 20px rgba(0,230,118,.18);color:#e0e0e0}
.chal-card{background:linear-gradient(135deg,#0a1a10,#0d2015);border:1.5px solid #00e676;
           border-radius:16px;padding:1.2rem 1.5rem;margin-bottom:1rem;color:#e0e0e0}
.streak-pill{display:inline-flex;align-items:center;gap:5px;background:#1f1200;color:#ffab40;
             border-radius:999px;padding:4px 14px;font-weight:600;font-size:.82rem;
             border:1.5px solid #ffab40}
.stat-row{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:1rem}
.stat-box{flex:1;min-width:88px;background:#161625;border:1px solid #252545;
          border-radius:12px;padding:.8rem 1rem;text-align:center}
.stat-box .val{font-size:1.25rem;font-weight:700;color:#00e676!important}
.stat-box .lbl{font-size:.7rem;color:#666!important;margin-top:2px}
.bmi-badge{display:inline-block;border-radius:999px;padding:3px 14px;font-weight:600;font-size:.82rem}
.bmi-u{background:#0a1530;color:#82b1ff}
.bmi-n{background:#0a2015;color:#00e676}
.bmi-ow{background:#1f1500;color:#ffab40}
.bmi-ob{background:#200a0a;color:#ff5252}
.user-bub{background:#0d2015;border-radius:16px 16px 4px 16px;padding:.8rem 1.1rem;
          margin:.4rem 0;max-width:80%;margin-left:auto;font-size:.95rem;
          color:#e0e0e0!important;border:1px solid #00e676}
.coach-bub{background:#161625;border-left:3px solid #00e676;border-radius:4px 16px 16px 16px;
           padding:.8rem 1.1rem;margin:.4rem 0;max-width:88%;font-size:.95rem;
           color:#e0e0e0!important;box-shadow:0 2px 12px rgba(0,230,118,.08)}
.drop{font-size:1.8rem}.empty{filter:grayscale(1) opacity(.18)}
[data-testid="stSidebar"]{background:#090912!important;border-right:1px solid #1a1a30}
[data-testid="stSidebar"] *{color:#e0e0e0!important}
[data-testid="stSidebar"] h2{color:#00e676!important;font-size:1.1rem!important}
.stButton>button{border-radius:999px;background:linear-gradient(90deg,#00c853,#00e676)!important;
                 color:#0a0a0a!important;font-weight:700;border:none;padding:.5rem 1.6rem;
                 box-shadow:0 0 14px rgba(0,230,118,.3);transition:all .2s}
.stButton>button:hover{box-shadow:0 0 22px rgba(0,230,118,.55);transform:translateY(-1px)}
.stTextInput input,.stNumberInput input,.stTextArea textarea{background:#161625!important;
  color:#e0e0e0!important;border:1px solid #252545!important;border-radius:8px!important}
.stTextInput input:focus,.stTextArea textarea:focus{border-color:#00e676!important;
  box-shadow:0 0 8px rgba(0,230,118,.25)!important}
div[data-baseweb="select"]>div{background:#161625!important;border-color:#252545!important;color:#e0e0e0!important}
.stProgress>div>div>div{background:linear-gradient(90deg,#00c853,#00e676)!important}
[data-testid="stExpander"]{background:#161625!important;border:1px solid #252545!important;border-radius:12px!important}
[data-testid="stForm"]{background:#161625!important;border:1px solid #252545!important;border-radius:12px;padding:1rem}
hr{border-color:#252545!important}
.stSuccess{background:#0a2015!important;border-color:#00e676!important}
.stInfo{background:#0a1525!important;border-color:#448aff!important}
.stError{background:#200a0a!important;border-color:#ff5252!important}
.stWarning{background:#1f1500!important;border-color:#ffab40!important}
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ════════════════════════════════════════════════════════════════════════════
LEVELS = [
    (0,"🌱 Seedling",100),(100,"🌿 Sprout",250),(250,"🌳 Grower",500),
    (500,"💪 Vitalist",900),(900,"⚡ Energiser",1400),(1400,"🔥 Igniter",2000),
    (2000,"🏅 Champion",3000),(3000,"🌟 Elite",5000),
    (5000,"🦁 Master",8000),(8000,"👑 Grandmaster",99999),
]
BADGES = [
    ("💧","Hydration Hero","Drink full water goal in a day","water_goal"),
    ("🥗","Meal Planner","Generate first AI meal plan","meal_done"),
    ("🧘","Zen Seeker","Complete first AI meditation","med_done"),
    ("💪","Workout Warrior","Generate first AI workout plan","wkt_done"),
    ("💊","Med Master","Mark all meds taken in a day","meds_all"),
    ("📊","BMI Tracker","Log BMI","bmi_done"),
    ("💬","Chatterbox","Send 10 AI chat messages","chat10"),
    ("🔥","7-Day Streak","Use app 7 days in a row","streak7"),
    ("🌟","Centurion","Earn 500 XP","xp500"),
    ("🏆","FlexCoach Legend","Earn 2000 XP","xp2000"),
    ("🌅","Early Bird","Open before 8 AM","earlybird"),
    ("🎯","Goal Getter","Complete 5 daily challenges","chal5"),
    ("🍽️","Calorie Counter","Use AI Calorie Checker","cal_done"),
]
DAILY_CHALLENGES = [
    ("💧","Drink 3 glasses of water before noon","water_count",3),
    ("🧘","Complete an AI meditation session","med_done",True),
    ("💬","Send 3 messages to AI coach","chat_count",3),
    ("💊","Mark all medications as taken","meds_all_today",True),
    ("📊","Log your BMI today","bmi_today",True),
    ("🥗","Generate a personalised AI meal plan","meal_done",True),
    ("💪","Generate a personalised AI workout plan","wkt_done",True),
    ("💧","Hit your full daily water goal","water_goal_today",True),
    ("🍽️","Use AI Calorie Checker to log a meal","cal_done",True),
]
XP = {"chat":10,"water":5,"water_goal":50,"meal":30,"meditation":25,
      "workout":30,"bmi":20,"med":15,"meds_all":40,"challenge":60,
      "login":20,"streak":10,"calorie":15}
QUOTES = [
    '"The groundwork of all happiness is health." — Leigh Hunt',
    '"Take care of your body. It\'s the only place you have to live." — Jim Rohn',
    '"A healthy outside starts from the inside." — Robert Urich',
    '"Your body can stand almost anything. It\'s your mind you have to convince."',
    '"Wellness is not a destination, it\'s a way of travelling."',
]
GOAL_OPTIONS   = ["General wellness","Weight loss","Muscle gain","Improve fitness",
                  "Stress management","Better sleep","Manage a health condition",
                  "Increase energy levels"]
GENDER_OPTIONS = ["Male","Female","Other / Prefer not to say"]

# ════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ════════════════════════════════════════════════════════════════════════════
def _init():
    D = {
        "profile_done":False,"user_name":"","user_age":25,"user_gender":"Male",
        "user_height":170.0,"user_weight":70.0,"user_goal":"General wellness",
        "user_activity":"Moderately active",
        "messages":[],"water_count":0,"water_date":"","bmi_history":[],
        "medications":[],"xp":0,"badges":[],"streak":0,"last_login":"",
        "chat_count":0,"challenges_done":0,"chal_date":"","chal_done":False,
        "chal_idx":0,"reward":None,"bmi_today":False,"meal_done":False,
        "med_done":False,"wkt_done":False,"meds_all_today":False,
        "water_goal_today":False,"cal_done":False,"earlybird_done":False,
        "cal_log":[],"cal_date":"","cal_total":0,
        "voice_on":True,"voice_speed":0.92,"voice_pitch":1.25,
    }
    for k,v in D.items():
        if k not in st.session_state:
            st.session_state[k] = v
_init()

# ════════════════════════════════════════════════════════════════════════════
# HELPERS
# ════════════════════════════════════════════════════════════════════════════
def bmi_val():
    h = st.session_state.user_height/100
    return round(st.session_state.user_weight/(h**2),1) if h>0 else 0.0

def bmi_cat(b):
    if b<=0:    return "Unknown","bmi-n"
    if b<18.5:  return "Underweight","bmi-u"
    elif b<25:  return "Normal","bmi-n"
    elif b<30:  return "Overweight","bmi-ow"
    else:       return "Obese","bmi-ob"

def water_goal():
    return max(6,min(math.ceil(st.session_state.user_weight*35/250),14))

def bmr():
    w,h,a=st.session_state.user_weight,st.session_state.user_height,st.session_state.user_age
    return (10*w+6.25*h-5*a+5) if st.session_state.user_gender=="Male" else (10*w+6.25*h-5*a-161)

def kcal_goal():
    return int(bmr()*1.4)

def get_level(xp):
    cur=LEVELS[0]
    for l in LEVELS:
        if xp>=l[0]: cur=l
        else: break
    return cur

def xp_pct(xp):
    l=get_level(xp); i=LEVELS.index(l)
    if i+1>=len(LEVELS): return 100.0
    n=LEVELS[i+1]; s=n[0]-l[0]
    return min(((xp-l[0])/s)*100,100) if s>0 else 100.0

def profile_str():
    b=bmi_val(); bc,_=bmi_cat(b)
    return (f"Name:{st.session_state.user_name}, Age:{st.session_state.user_age}, "
            f"Gender:{st.session_state.user_gender}, Height:{st.session_state.user_height}cm, "
            f"Weight:{st.session_state.user_weight}kg, BMI:{b}({bc}), "
            f"Activity:{st.session_state.get('user_activity','Moderate')}, "
            f"Goal:{st.session_state.user_goal}, Daily kcal target:~{kcal_goal()}")

def award(amount, badge_key=None):
    old=get_level(st.session_state.xp)
    st.session_state.xp+=amount
    new=get_level(st.session_state.xp)
    lvl_up=new[0]!=old[0]
    new_badge=None
    if badge_key and badge_key not in st.session_state.badges:
        st.session_state.badges.append(badge_key); new_badge=badge_key
    for thr,key in [(500,"xp500"),(2000,"xp2000")]:
        if st.session_state.xp>=thr and key not in st.session_state.badges:
            st.session_state.badges.append(key); new_badge=new_badge or key
    if st.session_state.streak>=7 and "streak7" not in st.session_state.badges:
        st.session_state.badges.append("streak7"); new_badge=new_badge or "streak7"
    icon="🎊" if lvl_up else ("🏅" if new_badge else "✨")
    msg=f"**+{amount} XP**"
    if lvl_up: msg+=f" 🚀 **Level up! {new[1]}**"
    if new_badge:
        b=next((x for x in BADGES if x[3]==new_badge),None)
        if b: msg+=f" 🏅 **Badge: {b[0]} {b[1]}**"
    st.session_state.reward={"icon":icon,"msg":msg}

def check_chal(key):
    if st.session_state.chal_done: return
    ch=DAILY_CHALLENGES[st.session_state.chal_idx]
    if ch[2]!=key: return
    cur=st.session_state.get(key,0)
    thr=ch[3]
    met=bool(cur) if isinstance(thr,bool) else (cur if isinstance(cur,(int,float)) else 0)>=thr
    if met:
        st.session_state.chal_done=True
        st.session_state.challenges_done+=1
        award(XP["challenge"],"chal5" if st.session_state.challenges_done>=5 else None)

def show_reward():
    r=st.session_state.get("reward")
    if not r: return
    st.markdown(f'<div class="toast"><span style="font-size:1.3rem">{r["icon"]}</span> {r["msg"]}</div>',
                unsafe_allow_html=True)
    st.session_state.reward=None

# ════════════════════════════════════════════════════════════════════════════
# AI ENGINE — Google Gemini (Free)
# ════════════════════════════════════════════════════════════════════════════
SYSTEM = """You are FlexCoach, a warm, motivating, expert AI health coach.
Always personalise responses using the user profile provided.
Be encouraging, science-backed, concise and practical.
Always end with a short motivating sentence for the user.
Never diagnose medical conditions. Recommend consulting a doctor for medical issues."""

def ai_text(prompt: str, history: list = None) -> str:
    """Call Gemini text model. Returns response string."""
    if not AI_OK:
        return ("⚠️ AI not configured. Please add your free GEMINI_API_KEY to Streamlit secrets. "
                "Get a free key at https://aistudio.google.com")
    try:
        model = genai.GenerativeModel(
            "gemini-1.5-flash",
            system_instruction=SYSTEM + "\n\nUser profile: " + profile_str()
        )
        if history:
            chat = model.start_chat(history=history)
            resp = chat.send_message(prompt)
        else:
            resp = model.generate_content(prompt)
        return resp.text.strip()
    except Exception as e:
        return f"⚠️ AI error: {e}"

def ai_vision(image_bytes: bytes, prompt: str) -> str:
    """Call Gemini vision model with an image."""
    if not AI_OK:
        return ("⚠️ AI not configured. Add GEMINI_API_KEY to Streamlit secrets.")
    try:
        import PIL.Image
        img = PIL.Image.open(io.BytesIO(image_bytes))
        model = genai.GenerativeModel("gemini-1.5-flash")
        resp = model.generate_content([prompt, img])
        return resp.text.strip()
    except Exception as e:
        return f"⚠️ Vision error: {e}"

# ════════════════════════════════════════════════════════════════════════════
# ARIA VOICE
# ════════════════════════════════════════════════════════════════════════════
def speak(text:str, force:bool=False):
    """Speak via Web Speech API — female voice."""
    try:
        if not st.session_state.get("voice_on",True) and not force: return
        if not text or len(str(text).strip())<3: return
        import re as _r
        c=str(text)
        c=_r.sub(r'\*\*(.*?)\*\*',r'\1',c)
        c=_r.sub(r'\*(.*?)\*',r'\1',c)
        c=_r.sub(r'#{1,6}\s*',' ',c)
        c=_r.sub(r'[_`>~|\[\]()]',' ',c)
        c=_r.sub(r'https?://\S+',' ',c)
        c=_r.sub('[' +
            '\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF'
            '\U0001F1E0-\U0001F1FF\U00002700-\U000027BF\U000024C2-\U0001F251'
            '\U0001F900-\U0001F9FF\U00002500-\U00002BEF]+',' ',c,flags=_r.UNICODE)
        c=_r.sub(r'\s+',' ',c).strip()
        if not c or len(c)<3: return
        if len(c)>300:
            t=c[:300]; s=max(t.rfind('. '),t.rfind('! '),t.rfind('? '))
            c=t[:s+1] if s>80 else t.rsplit(' ',1)[0]+'.'
        spd=float(st.session_state.get("voice_speed",0.92))
        pit=float(st.session_state.get("voice_pitch",1.25))
        safe=c.replace('\\',' ').replace('\n',' ').replace("'"," ").replace('"',' ').replace('`',' ')
        js=f"""<script>
(function(){{try{{
  if(!window.speechSynthesis)return;
  window.speechSynthesis.cancel();
  var u=new SpeechSynthesisUtterance('{safe}');
  u.rate={spd};u.pitch={pit};u.volume=1.0;u.lang='en-US';
  function pick(){{
    var vv=window.speechSynthesis.getVoices();if(!vv||!vv.length)return;
    var p=["samantha","karen","victoria","moira","tessa","fiona","allison","ava",
           "susan","zira","aria","hazel","eva","google uk english female",
           "microsoft zira","microsoft aria","google us english"];
    var ch=null;
    for(var n of p){{ch=vv.find(function(v){{return v.name.toLowerCase().indexOf(n)!==-1&&v.lang.indexOf('en')===0;}});if(ch)break;}}
    if(!ch)ch=vv.find(function(v){{return v.lang==='en-US'||v.lang==='en-GB';}});
    if(!ch&&vv.length)ch=vv[0];
    if(ch)u.voice=ch;
  }}
  if(window.speechSynthesis.getVoices().length>0){{pick();window.speechSynthesis.speak(u);}}
  else{{window.speechSynthesis.onvoiceschanged=function(){{pick();window.speechSynthesis.speak(u);}};}}
}}catch(e){{console.warn('Aria:',e);}}}}
)();
</script>"""
        components.html(js,height=0,scrolling=False)
    except Exception: pass

def aria_say(key:str):
    n=st.session_state.get("user_name","champion")
    msgs={
        "login":[f"Welcome back {n}! Ready to crush today?",
                 f"Hey {n}! So great to see you. Let's make today count!"],
        "streak":[f"Wow {n}, your streak is on fire! Consistency is your superpower!",
                  f"Look at you {n}! Every day you show up for yourself!"],
        "water":[f"Hydration hero mode, {n}! Your body loves you for this!",
                 f"Every sip counts {n}! Keep going!"],
        "water_goal":[f"You hit your water goal {n}! That is absolutely incredible!"],
        "meal":[f"Your AI meal plan is ready {n}! Fuel your best days!"],
        "workout":[f"Let's go {n}! Your personalised workout plan is ready!"],
        "meditation":[f"Beautiful choice {n}. Taking time to breathe is true strength."],
        "bmi":[f"Smart tracking {n}! Knowledge is the first step to change!"],
        "med":[f"Consistency is your superpower {n}! Every dose matters!"],
        "meds_all":[f"All medications taken {n}! You are absolutely crushing it!"],
        "calorie":[f"Calories logged {n}! You're so disciplined — love that!"],
        "challenge":[f"Daily challenge complete {n}! You are absolutely legendary!"],
        "level_up":[f"Level up {n}! All your hard work is paying off!"],
        "badge":[f"New badge unlocked {n}! You earned every bit of this!"],
    }
    pool=msgs.get(key,[f"You're doing amazing {n}! Keep going!"])
    speak(random.choice(pool))

def voice_panel():
    n=st.session_state.get("user_name","friend")
    en=st.session_state.get("voice_on",True)
    col=("#00e676" if en else "#444"); status=("LIVE" if en else "OFF")
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0a1f10,#0d2a18);border:1.5px solid {col};
                border-radius:16px;padding:1rem 1.1rem;margin:.5rem 0 .8rem;text-align:center">
      <div style="font-size:2.2rem;margin-bottom:4px">👩</div>
      <div style="font-size:.95rem;font-weight:700;color:#00e676;letter-spacing:.05em">ARIA</div>
      <div style="font-size:.72rem;color:#aaa;margin-bottom:6px">Your AI Girl Coach</div>
      <span style="background:{col};color:#0d0d0d;border-radius:999px;padding:2px 10px;font-size:.7rem;font-weight:700">{status}</span>
    </div>""", unsafe_allow_html=True)
    enabled=st.toggle("🎙️ Aria Voice",value=en,key="aria_toggle")
    st.session_state.voice_on=enabled
    if enabled:
        c1,c2=st.columns(2)
        with c1:
            spd=st.slider("Spd",.6,1.4,float(st.session_state.get("voice_speed",.92)),.05,
                          key="spd_sl",label_visibility="collapsed")
        with c2:
            pit=st.slider("Pit",.8,1.8,float(st.session_state.get("voice_pitch",1.25)),.05,
                          key="pit_sl",label_visibility="collapsed")
        st.session_state.voice_speed=spd; st.session_state.voice_pitch=pit
        st.caption("← Speed · Pitch →")
        c1,c2=st.columns(2)
        with c1:
            if st.button("👋 Meet Aria",key="meet_aria"):
                speak(f"Hey {n}! I am Aria, your personal FlexCoach AI girl coach. "
                      f"I am here to celebrate every win, cheer you on every step, "
                      f"and remind you how amazing you are. Let us build the "
                      f"healthiest version of you together!",force=True)
        with c2:
            if st.button("🔇 Stop",key="stop_aria"):
                components.html("<script>window.speechSynthesis&&window.speechSynthesis.cancel();</script>",height=0)
        if st.button("💚 Compliment Me!",key="aria_comp"):
            comps=[
                f"Hey {n}, you are doing better than you think! Every healthy choice moves you forward.",
                f"{n}, I see you showing up every day. That is what champions are made of!",
                f"You are building something incredible {n}. Your dedication inspires me!",
                f"Progress is progress {n}, no matter how small. You are growing every single day!",
                f"Your body is working so hard for you {n}. Give it all the love it deserves!",
            ]
            speak(random.choice(comps),force=True)
    else:
        st.caption("Turn on to hear Aria! 🎙️")

# ════════════════════════════════════════════════════════════════════════════
# DAILY RESET & LOGIN
# ════════════════════════════════════════════════════════════════════════════
today=str(datetime.date.today())

# Daily reset
if st.session_state.water_date!=today:
    st.session_state.water_date=today; st.session_state.water_count=0
    for k in ["bmi_today","meal_done","med_done","wkt_done",
              "meds_all_today","water_goal_today","cal_done"]:
        st.session_state[k]=False
    for m in st.session_state.medications: m["taken"]=False

if st.session_state.cal_date!=today:
    st.session_state.cal_date=today; st.session_state.cal_log=[]; st.session_state.cal_total=0

# Login streak + XP
if st.session_state.profile_done and st.session_state.last_login!=today:
    yest=str(datetime.date.today()-datetime.timedelta(days=1))
    st.session_state.streak=(st.session_state.streak+1
                              if st.session_state.last_login==yest else 1)
    st.session_state.last_login=today
    st.session_state.chal_date=today; st.session_state.chal_done=False
    st.session_state.chal_idx=abs(hash(today))%len(DAILY_CHALLENGES)
    bonus=XP["login"]
    if st.session_state.streak>1: bonus+=XP["streak"]*min(st.session_state.streak,7)
    st.session_state.xp+=bonus
    msg_pool=["login"] if st.session_state.streak<3 else ["streak"]
    aria_say(msg_pool[0])
    st.session_state.reward={"icon":"🌿","msg":f"**+{bonus} XP** for showing up today! 🌿"}

# Early bird
if (st.session_state.profile_done and not st.session_state.earlybird_done
        and datetime.datetime.now().hour<8):
    st.session_state.earlybird_done=True
    if "earlybird" not in st.session_state.badges:
        st.session_state.badges.append("earlybird")

# ════════════════════════════════════════════════════════════════════════════
# ONBOARDING
# ════════════════════════════════════════════════════════════════════════════
if not st.session_state.profile_done:
    st.markdown("""
    <div style='text-align:center;padding:2rem 0 .5rem'>
      <span style='font-size:3.5rem'>💪❤️🌿</span>
      <h1 style='margin:0;color:#00e676'>FlexCoach</h1>
      <p style='color:#666;margin-top:.2rem'>Your fully AI-powered health companion — 100% Free</p>
    </div>""", unsafe_allow_html=True)
    st.markdown('<div class="onboard">', unsafe_allow_html=True)
    st.markdown("### 👋 Set up your profile")
    st.markdown("Fill in your details — AI personalises everything just for you. No API key needed from you!")
    st.divider()
    st.markdown("**🪪 About You**")
    c1,c2=st.columns(2)
    with c1: name=st.text_input("Full name *",placeholder="e.g. Alex Johnson",key="ob_name")
    with c2: gender=st.selectbox("Gender *",GENDER_OPTIONS,key="ob_gender")
    st.markdown("**📏 Body Stats**")
    c1,c2,c3=st.columns(3)
    with c1: age=st.number_input("Age *",10,100,25,key="ob_age")
    with c2: height=st.number_input("Height (cm) *",100.0,250.0,170.0,.5,key="ob_height")
    with c3: weight=st.number_input("Weight (kg) *",30.0,300.0,70.0,.5,key="ob_weight")
    if height>0 and weight>0:
        pb=round(weight/((height/100)**2),1); pc,pcs=bmi_cat(pb)
        st.markdown(f'<p style="color:#aaa;font-size:.88rem">📊 BMI preview: <strong>{pb}</strong> <span class="bmi-badge {pcs}">{pc}</span></p>',unsafe_allow_html=True)
    st.markdown("**🎯 Goals**")
    c1,c2=st.columns(2)
    with c1: goal=st.selectbox("Primary goal *",GOAL_OPTIONS,key="ob_goal")
    with c2: activity=st.select_slider("Activity level",
        ["Sedentary","Lightly active","Moderately active","Very active","Athlete"],
        value="Moderately active",key="ob_activity")
    st.markdown("<br>",unsafe_allow_html=True)
    if st.button("Start my health journey 🚀",use_container_width=True,key="ob_start"):
        if not name.strip(): st.error("Please enter your name.")
        else:
            bv=round(float(weight)/((float(height)/100)**2),1); cv,_=bmi_cat(bv)
            st.session_state.update({
                "profile_done":True,"user_name":name.strip(),"user_age":int(age),
                "user_gender":gender,"user_height":float(height),"user_weight":float(weight),
                "user_goal":goal,"user_activity":activity,
            })
            st.session_state.bmi_history.append({"date":today,"bmi":bv,"cat":cv})
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    if not AI_OK:
        st.warning("⚠️ **AI features need setup:** Add `GEMINI_API_KEY` to Streamlit secrets. "
                   "Get a FREE key at https://aistudio.google.com — it takes 2 minutes!")
    st.stop()

# ════════════════════════════════════════════════════════════════════════════
# MAIN APP
# ════════════════════════════════════════════════════════════════════════════
WG  = water_goal()
CL  = get_level(st.session_state.xp)
XPC = xp_pct(st.session_state.xp)

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 💪❤️🌿 FlexCoach")
    gi="👨" if st.session_state.user_gender=="Male" else "👩" if st.session_state.user_gender=="Female" else "🧑"
    st.markdown(f"""
    <div style='background:rgba(255,255,255,.1);border-radius:14px;padding:.9rem 1rem;margin-bottom:.5rem'>
      <div style='font-size:1.1rem;font-weight:600'>{gi} {st.session_state.user_name}</div>
      <div class='lvl-lbl'>{CL[1]}</div>
      <div class='xpbar-bg'><div class='xpbar-fill' style='width:{XPC:.0f}%'></div></div>
      <div style='font-size:.72rem;opacity:.75'>{st.session_state.xp} XP · {len(st.session_state.badges)} badges</div>
    </div>""", unsafe_allow_html=True)
    if st.session_state.streak>0:
        st.markdown(f'<div style="margin-bottom:.6rem"><span class="streak-pill">🔥 {st.session_state.streak}-day streak</span></div>',unsafe_allow_html=True)
    bs=bmi_val(); bc,_=bmi_cat(bs)
    st.markdown(f"""
    <div style='font-size:.82rem;line-height:2;opacity:.9'>
      <b>Age:</b> {st.session_state.user_age} | {st.session_state.user_gender}<br>
      <b>Height:</b> {st.session_state.user_height}cm | <b>Weight:</b> {st.session_state.user_weight}kg<br>
      <b>BMI:</b> {bs} · {bc} | <b>Goal:</b> {st.session_state.user_goal}
    </div>""", unsafe_allow_html=True)
    if not AI_OK:
        st.warning("⚠️ Add GEMINI_API_KEY to secrets for AI features!")
    st.divider()
    PAGE=st.radio("Navigate",[
        "🏠 Dashboard","💬 AI Chat","🥗 Meal Plan","🧘 Meditation",
        "🏋️ Workout","💧 Water Tracker","📊 BMI Tracker",
        "🍽️ Calorie Checker","💊 Medications","👤 My Profile",
    ],label_visibility="collapsed",key="nav_radio")
    st.divider()
    voice_panel()
    st.divider()
    if st.button("🔄 Edit Profile",key="edit_profile_btn"):
        st.session_state.profile_done=False; st.rerun()
    st.caption("Not a substitute for medical advice.")

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("# 💪❤️🌿 FlexCoach")
hr=datetime.datetime.now().hour
gw="Good morning" if hr<12 else "Good afternoon" if hr<17 else "Good evening"
st.markdown(f"**{gw}, {st.session_state.user_name}! 👋** Your AI health coach is ready.")
show_reward()

# Greet via Aria once per page per day
_gk=f"greeted_{today}_{PAGE}"
if not st.session_state.get(_gk):
    st.session_state[_gk]=True
    speak(f"{gw} {st.session_state.user_name}! Welcome back to FlexCoach. "
          f"Every time you open this app you are choosing your health. Let us make today amazing!")
st.divider()

# ════════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ════════════════════════════════════════════════════════════════════════════
if PAGE=="🏠 Dashboard":
    st.subheader("🏠 Your Dashboard")
    li=LEVELS.index(CL); nl=LEVELS[min(li+1,len(LEVELS)-1)]
    need=max(nl[0]-st.session_state.xp,0)
    st.markdown(f"""
    <div class='fc-card' style='border-left:4px solid #00e676'>
      <div style='display:flex;justify-content:space-between;align-items:center'>
        <div><div style='font-size:1.05rem;font-weight:700'>{CL[1]}</div>
             <div style='font-size:.82rem;color:#888'>{st.session_state.xp} XP · {need} to next level</div></div>
        <div style='font-size:2rem'>{CL[1].split()[0]}</div>
      </div>
      <div style='background:#252545;border-radius:999px;height:10px;margin-top:.8rem;overflow:hidden'>
        <div style='height:100%;width:{XPC:.0f}%;background:linear-gradient(90deg,#00c853,#00e676);border-radius:999px'></div>
      </div>
    </div>""", unsafe_allow_html=True)
    tm=sum(1 for m in st.session_state.medications if m.get("taken",False))
    tt=len(st.session_state.medications)
    st.markdown(f"""
    <div class='stat-row'>
      <div class='stat-box'><div class='val'>{st.session_state.xp}</div><div class='lbl'>Total XP</div></div>
      <div class='stat-box'><div class='val'>{st.session_state.streak}🔥</div><div class='lbl'>Streak</div></div>
      <div class='stat-box'><div class='val'>{len(st.session_state.badges)}</div><div class='lbl'>Badges</div></div>
      <div class='stat-box'><div class='val'>{st.session_state.water_count}/{WG}</div><div class='lbl'>Water</div></div>
      <div class='stat-box'><div class='val'>{f"{tm}/{tt}" if tt else "—"}</div><div class='lbl'>Meds</div></div>
      <div class='stat-box'><div class='val'>{st.session_state.challenges_done}</div><div class='lbl'>Challenges</div></div>
    </div>""", unsafe_allow_html=True)
    ch=DAILY_CHALLENGES[st.session_state.chal_idx]; cd=st.session_state.chal_done
    st.markdown(f"""
    <div class='chal-card' style='border-color:{"#00e676" if cd else "#ff9800"}'>
      <h4>{ch[0]} Today's Challenge</h4>
      <p style='font-size:1rem;font-weight:500;margin:.3rem 0 .2rem'>{ch[1]}</p>
      <p style='font-size:.8rem;opacity:.75'>{"✅ Completed! +60 XP" if cd else "📌 Complete to earn +60 XP"}</p>
    </div>""", unsafe_allow_html=True)
    st.markdown("#### 🏅 Badges")
    st.markdown('<div class="badge-grid">'+"".join(
        f'<span class="badge-pill {"badge-on" if b[3] in st.session_state.badges else "badge-off"}" title="{b[2]}">{b[0]} {b[1]}</span>'
        for b in BADGES)+'</div>', unsafe_allow_html=True)
    if not st.session_state.badges: st.caption("Complete actions to earn your first badge!")
    st.markdown(f"""
    <div class='fc-card' style='text-align:center;padding:1.2rem'>
      <span style='font-size:1.5rem'>💭</span>
      <p style='color:#aaa;font-style:italic;margin:.5rem 0 0'>{random.choice(QUOTES)}</p>
    </div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# AI CHAT
# ════════════════════════════════════════════════════════════════════════════
elif PAGE=="💬 AI Chat":
    st.subheader("💬 AI Health Coach Chat")
    st.caption(f"Powered by Google Gemini AI · {st.session_state.user_name} · {st.session_state.user_age}y · {st.session_state.user_goal}")

    QUICK={
        "💪 Workout Plan":"Create a personalised workout plan for me based on my profile",
        "🥗 Meal Plan":"Give me a personalised 7-day meal plan for my goal",
        "🧘 Meditate":"Guide me through a personalised meditation session",
        "💧 Water Tip":"Give me personalised hydration tips for my weight",
        "😴 Sleep":"Give me personalised sleep improvement tips",
    }
    cols=st.columns(len(QUICK))
    for col,(lbl,prompt) in zip(cols,QUICK.items()):
        if col.button(lbl,key=f"qk_{lbl}"):
            st.session_state.messages.append({"role":"user","content":prompt})
            st.rerun()

    for msg in st.session_state.messages:
        if msg["role"]=="user":
            st.markdown(f'<div class="user-bub">🧑 {msg["content"]}</div>',unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="coach-bub">💪❤️🌿 {msg["content"]}</div>',unsafe_allow_html=True)

    if st.session_state.messages and st.session_state.messages[-1]["role"]=="user":
        with st.spinner("AI Coach is thinking…"):
            # Build Gemini history
            history=[]
            for m in st.session_state.messages[:-1]:
                role="user" if m["role"]=="user" else "model"
                history.append({"role":role,"parts":[m["content"]]})
            reply=ai_text(st.session_state.messages[-1]["content"],history=history)
            st.session_state.messages.append({"role":"assistant","content":reply})
            st.session_state.chat_count+=1
            award(XP["chat"],"chat10" if st.session_state.chat_count>=10 else None)
            check_chal("chat_count")
        # Aria speaks first clean sentence
        clean=[l.strip() for l in reply.split("\n")
               if l.strip() and not l.strip().startswith(("#","-","*","•")) and len(l.strip())>20]
        if clean: speak(clean[0])
        st.rerun()

    with st.form("chat_form",clear_on_submit=True):
        ui=st.text_input("Ask your AI health coach anything…",label_visibility="collapsed",
                         placeholder="e.g. What should I eat after a workout?",key="chat_input")
        sb=st.form_submit_button("Send 💚")
    if sb and ui.strip():
        st.session_state.messages.append({"role":"user","content":ui.strip()}); st.rerun()
    if st.button("🗑️ Clear Chat",key="clear_chat"):
        st.session_state.messages=[]; st.rerun()

# ════════════════════════════════════════════════════════════════════════════
# AI MEAL PLAN
# ════════════════════════════════════════════════════════════════════════════
elif PAGE=="🥗 Meal Plan":
    st.subheader("🥗 AI-Powered Personalised Meal Plan")
    st.caption("Every plan is unique — generated fresh by AI based on your profile")
    c1,c2,c3=st.columns(3)
    with c1: diet=st.selectbox("Diet type",["Balanced","Vegetarian","Vegan","Keto",
                                             "Mediterranean","Low-carb","High-protein","Paleo"],key="meal_diet")
    with c2: dur=st.selectbox("Duration",["1 day","3 days","7 days"],key="meal_duration_sel")
    with c3: cals=st.number_input("Calories/day",1000,5000,kcal_goal(),50,key="meal_cals")
    extra=st.text_input("Allergies or restrictions",placeholder="e.g. lactose intolerant, nut allergy",key="meal_extra")
    pref=st.text_input("Favourite foods or cuisine (optional)",placeholder="e.g. Asian food, love pasta",key="meal_pref")

    if st.button("🥦 Generate My AI Meal Plan",use_container_width=True,key="gen_meal"):
        prompt=(f"Create a UNIQUE, detailed {dur} {diet} meal plan targeting ~{cals} kcal/day "
                f"for this person. Make it completely different from any generic plan — "
                f"include local and international variety, seasonal ingredients, and practical recipes. "
                f"{'Restrictions: '+extra+'.' if extra else ''} "
                f"{'Favourite foods: '+pref+'.' if pref else ''} "
                f"For EACH day include: Breakfast, Mid-morning snack, Lunch, Afternoon snack, Dinner, Evening snack. "
                f"For each meal give: meal name, key ingredients, quick prep note (1 sentence), and calories. "
                f"End with a 3-tip nutrition advice section personalised to the user's goal.")
        with st.spinner("🥗 AI is crafting your unique meal plan…"):
            reply=ai_text(prompt)
        st.markdown(f'<div class="fc-card">{reply}</div>',unsafe_allow_html=True)
        if not st.session_state.meal_done:
            st.session_state.meal_done=True
            award(XP["meal"],"meal_done"); check_chal("meal_done"); show_reward()
        aria_say("meal")

# ════════════════════════════════════════════════════════════════════════════
# AI MEDITATION
# ════════════════════════════════════════════════════════════════════════════
elif PAGE=="🧘 Meditation":
    st.subheader("🧘 AI-Guided Meditation Session")
    st.caption("Personalised to your goal and current state of mind")
    c1,c2=st.columns(2)
    with c1: tech=st.selectbox("Technique",["Box Breathing","Body Scan","Mindfulness",
                                              "Visualisation","Progressive Muscle Relaxation",
                                              "Loving-Kindness","Energising Breath","Sleep Meditation"],
                                key="med_tech")
    with c2: dur_m=st.selectbox("Duration",["3 min","5 min","10 min","15 min","20 min"],key="med_duration_sel")
    concern=st.text_input("What are you dealing with right now?",
                          placeholder="e.g. work stress, poor sleep, low energy, anxiety",key="med_concern")

    if st.button("🕯️ Start My AI Meditation",use_container_width=True,key="start_med"):
        prompt=(f"Guide me through a personalised {dur_m} {tech} meditation session. "
                f"{'I am currently dealing with: '+concern+'.' if concern else ''} "
                f"Format as numbered steps with timing for each step. "
                f"Make it vivid, calming, and deeply personal to my goal. "
                f"Include: what to do, what to visualise or feel, breathing instructions. "
                f"End with the science behind why this technique works for my situation "
                f"and a personal motivating message.")
        with st.spinner("🧘 AI is preparing your session…"):
            reply=ai_text(prompt)
        st.markdown(f'<div class="fc-card">{reply}</div>',unsafe_allow_html=True)
        if not st.session_state.med_done:
            st.session_state.med_done=True
            award(XP["meditation"],"med_done"); check_chal("med_done"); show_reward()
        aria_say("meditation")

# ════════════════════════════════════════════════════════════════════════════
# AI WORKOUT
# ════════════════════════════════════════════════════════════════════════════
elif PAGE=="🏋️ Workout":
    st.subheader("🏋️ AI-Powered Personalised Workout Plan")
    st.caption("Every plan is unique — generated fresh by AI for your exact profile")
    c1,c2,c3=st.columns(3)
    with c1: lvl=st.selectbox("Fitness level",["Beginner","Intermediate","Advanced"],key="wkt_lvl")
    with c2: wtype=st.selectbox("Type",["Strength","Cardio","HIIT","Yoga/Flexibility",
                                         "Weight loss","Muscle gain","Full body","Calisthenics"],key="wkt_type")
    with c3: days=st.selectbox("Days/week",[2,3,4,5,6],key="wkt_days")
    equip=st.multiselect("Equipment available",["No equipment","Dumbbells","Barbell","Resistance bands",
                                                  "Pull-up bar","Gym machines","Kettlebell","Yoga mat"],key="wkt_equip")
    wgoal=st.text_input("Specific goal",placeholder="e.g. lose 5kg, run 5K, build chest",key="wkt_goal")
    injury=st.text_input("Any injuries or limitations?",placeholder="e.g. bad knees, shoulder pain",key="wkt_injury")

    if st.button("💪 Generate My AI Workout Plan",use_container_width=True,key="gen_wkt"):
        eq=", ".join(equip) if equip else "no equipment"
        prompt=(f"Create a UNIQUE, detailed {days}-day/week {wtype} workout plan for a {lvl} "
                f"using {eq}. Make it completely personalised and different from generic plans. "
                f"{'Specific goal: '+wgoal+'.' if wgoal else ''} "
                f"{'Injuries/limitations: '+injury+' — modify exercises accordingly.' if injury else ''} "
                f"For each training day provide: warm-up (5 min), main exercises with sets/reps/rest, "
                f"cool-down (5 min). Include progression tips for weeks 2, 3, 4. "
                f"Add a rest day recommendation and recovery advice. "
                f"End with 3 personalised tips to maximise results for this person's goal.")
        with st.spinner("💪 AI is building your unique workout plan…"):
            reply=ai_text(prompt)
        st.markdown(f'<div class="fc-card">{reply}</div>',unsafe_allow_html=True)
        if not st.session_state.wkt_done:
            st.session_state.wkt_done=True
            award(XP["workout"],"wkt_done"); check_chal("wkt_done"); show_reward()
        aria_say("workout")

# ════════════════════════════════════════════════════════════════════════════
# WATER TRACKER
# ════════════════════════════════════════════════════════════════════════════
elif PAGE=="💧 Water Tracker":
    st.subheader("💧 Daily Water Tracker")
    st.markdown(f"Your goal: **{WG} glasses/day** ({WG*250}ml) — based on {st.session_state.user_weight}kg body weight")
    cnt=st.session_state.water_count; rem=max(0,WG-cnt); prog=min(cnt/WG,1.0)
    drops="".join(f'<span class="drop {"" if i<cnt else "empty"}">💧</span>' for i in range(WG))
    st.markdown(f'<div class="fc-card" style="text-align:center"><h3>Today\'s intake</h3>{drops}'
                f'<p style="margin-top:.8rem;font-size:1.1rem"><strong>{cnt}</strong> / {WG} glasses</p></div>',
                unsafe_allow_html=True)
    st.progress(prog)
    c1,c2,c3=st.columns(3)
    if c1.button("➕ Add glass",key="water_add"):
        if st.session_state.water_count<WG:
            st.session_state.water_count+=1
            award(XP["water"]); check_chal("water_count"); aria_say("water")
            if st.session_state.water_count>=WG and not st.session_state.water_goal_today:
                st.session_state.water_goal_today=True
                award(XP["water_goal"],"water_goal"); check_chal("water_goal_today")
                aria_say("water_goal")
        st.rerun()
    if c2.button("➖ Remove",key="water_rem"):
        if st.session_state.water_count>0: st.session_state.water_count-=1
        st.rerun()
    if c3.button("🔄 Reset",key="water_rst"):
        st.session_state.water_count=0; st.rerun()
    if cnt>=WG: st.success("🎉 Daily water goal smashed! You're a hydration hero!")
    elif rem==1: st.info("🌊 Just 1 more glass — almost there!")
    else: st.info(f"💦 {rem} more glasses to go. You've got this!")
    if st.button("💡 AI Hydration Tip",key="water_tip"):
        with st.spinner(""):
            tip=ai_text(f"Give me one creative, practical hydration tip personalised to my weight and goal. 2-3 sentences max.")
        st.markdown(f'<div class="fc-card">{tip}</div>',unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# BMI TRACKER
# ════════════════════════════════════════════════════════════════════════════
elif PAGE=="📊 BMI Tracker":
    st.subheader("📊 BMI Tracker")
    c1,c2,c3=st.columns(3)
    with c1: w=st.number_input("Weight (kg)",30.0,300.0,float(st.session_state.user_weight),.5,key="bmi_weight_input")
    with c2: h=st.number_input("Height (cm)",100.0,250.0,float(st.session_state.user_height),.5,key="bmi_height_input")
    with c3: st.markdown("<br>",unsafe_allow_html=True); calc=st.button("Calculate & Save",key="bmi_calc")
    if calc and h>0:
        b=round(w/((h/100)**2),1); cat,css=bmi_cat(b)
        st.session_state.user_weight=w; st.session_state.user_height=h
        st.session_state.bmi_history.append({"date":today,"bmi":b,"cat":cat})
        st.markdown(f"""
        <div class='fc-card' style='text-align:center'>
          <h2>Your BMI</h2>
          <div style='font-size:3rem;font-weight:700;color:#00e676'>{b}</div>
          <span class='bmi-badge {css}'>{cat}</span>
          <p style='margin-top:1rem;color:#aaa'>Healthy range: <strong>18.5–24.9</strong></p>
        </div>""", unsafe_allow_html=True)
        with st.spinner("Getting AI advice…"):
            adv=ai_text(f"My BMI is {b} ({cat}), weight {w}kg, height {h}cm. "
                        f"Give me 3 specific, encouraging, actionable tips tailored to my full profile.")
        st.markdown(f'<div class="fc-card">{adv}</div>',unsafe_allow_html=True)
        if not st.session_state.bmi_today:
            st.session_state.bmi_today=True
            award(XP["bmi"],"bmi_done"); check_chal("bmi_today"); show_reward()
        aria_say("bmi")
    if st.session_state.bmi_history:
        st.markdown("#### History")
        for e in reversed(st.session_state.bmi_history[-10:]):
            _,css=bmi_cat(e["bmi"])
            st.markdown(f'<div style="display:flex;justify-content:space-between;padding:.5rem 0;border-bottom:1px solid #252545">'
                        f'<span>{e["date"]}</span><strong>{e["bmi"]}</strong>'
                        f'<span class="bmi-badge {css}">{e["cat"]}</span></div>',unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# AI CALORIE CHECKER WITH CAMERA
# ════════════════════════════════════════════════════════════════════════════
elif PAGE=="🍽️ Calorie Checker":
    st.subheader("🍽️ AI Calorie Checker")
    st.caption("Snap a photo or describe your food — AI identifies it and estimates calories instantly")

    # Daily progress bar
    cg=kcal_goal(); ct=st.session_state.cal_total; cp=min(ct/cg,1.0) if cg else 0
    bc_color=("#00e676" if cp<.85 else ("#ffab40" if cp<1.0 else "#ff5252"))
    st.markdown(f"""
    <div class='fc-card'>
      <div style='display:flex;justify-content:space-between;margin-bottom:6px'>
        <span style='font-weight:600;color:#00e676'>🔥 Today's Calories</span>
        <span style='color:#aaa;font-size:.85rem'>Goal: {cg} kcal</span>
      </div>
      <div style='font-size:2rem;font-weight:700;color:{bc_color}'>{ct} kcal</div>
      <div style='background:#252545;border-radius:999px;height:10px;margin-top:8px;overflow:hidden'>
        <div style='height:100%;width:{cp*100:.0f}%;background:{bc_color};border-radius:999px'></div>
      </div>
      <div style='font-size:.78rem;color:#888;margin-top:4px'>
        {max(0,cg-ct)} kcal remaining · {len(st.session_state.cal_log)} items logged today
      </div>
    </div>""", unsafe_allow_html=True)

    tab1,tab2=st.tabs(["📷 Camera / Photo","⌨️ Type Food"])

    # ── TAB 1: Camera with AI Vision ─────────────────────────────────────────
    with tab1:
        st.markdown("#### 📷 Snap Your Food — AI Will Identify It!")
        st.info("📸 Take a photo of your meal and the AI will identify the food and estimate calories automatically!")

        photo=st.camera_input("Point camera at your food and snap 📸",key="food_cam")

        if photo is not None:
            img_bytes=photo.read()
            st.image(photo,caption="Your food photo",use_column_width=True)
            st.markdown("---")
            with st.spinner("🤖 AI is analysing your food photo…"):
                vision_prompt=(
                    f"You are a nutrition expert AI. Analyse this food photo carefully.\n"
                    f"The user's profile: {profile_str()}\n\n"
                    f"Please provide:\n"
                    f"1. **Food Identified**: List every food item you can see\n"
                    f"2. **Calorie Estimate**: For each item and total\n"
                    f"3. **Portion Size**: Estimate serving size\n"
                    f"4. **Macros**: Approximate protein, carbs, fat in grams\n"
                    f"5. **Health Rating**: 1-10 scale for this meal based on the user's goal\n"
                    f"6. **Personalised Tip**: One tip about this meal for this user's specific goal\n"
                    f"Format clearly with headers. Be specific with calorie numbers."
                )
                ai_result=ai_vision(img_bytes,vision_prompt)

            st.markdown(f'<div class="fc-card">{ai_result}</div>',unsafe_allow_html=True)

            # Extract total calories from AI response to log
            st.markdown("---")
            st.markdown("**📝 Log this meal:**")
            c1,c2=st.columns(2)
            with c1: food_name=st.text_input("Food description",placeholder="e.g. Grilled chicken with rice",key="cam_food_name")
            with c2: est_cal=st.number_input("Estimated calories (from AI above)",0,5000,0,10,key="cam_cal_est")
            meal_type_cam=st.selectbox("Meal type",["🌅 Breakfast","🌞 Lunch","🌙 Dinner","🍎 Snack"],key="cam_meal_type")

            if st.button("✅ Log This Meal",key="cam_log_btn",use_container_width=True):
                if food_name.strip() and est_cal>0:
                    st.session_state.cal_log.append({
                        "time":datetime.datetime.now().strftime("%H:%M"),
                        "food":food_name.strip(),"calories":est_cal,
                        "source":"📷 Camera AI","meal":meal_type_cam,
                    })
                    st.session_state.cal_total+=est_cal
                    if not st.session_state.cal_done:
                        st.session_state.cal_done=True
                        award(XP["calorie"],"cal_done"); check_chal("cal_done"); show_reward()
                    aria_say("calorie")
                    speak(f"Logged {food_name} for {est_cal} calories. Great tracking {st.session_state.user_name}!")
                    st.success(f"✅ Logged **{food_name}** — **{est_cal} kcal**")
                    st.rerun()
                else:
                    st.warning("Please enter food name and calorie estimate above.")

            # Option to upload photo instead of camera
            st.markdown("---")
            st.markdown("**Or upload a photo from your device:**")
            uploaded=st.file_uploader("Upload food photo",type=["jpg","jpeg","png","webp"],key="food_upload")
            if uploaded:
                img_bytes_up=uploaded.read()
                st.image(uploaded,caption="Uploaded food",use_column_width=True)
                if st.button("🔍 Analyse Uploaded Photo",key="analyse_upload"):
                    with st.spinner("🤖 AI analysing…"):
                        result_up=ai_vision(img_bytes_up,vision_prompt)
                    st.markdown(f'<div class="fc-card">{result_up}</div>',unsafe_allow_html=True)

    # ── TAB 2: Type Food ──────────────────────────────────────────────────────
    with tab2:
        st.markdown("#### ⌨️ Describe Your Food — AI Calculates Calories")
        food_desc=st.text_area(
            "What did you eat?",
            placeholder="e.g. 2 scrambled eggs, 2 slices whole grain toast, 1 cup orange juice\nor: large plate of pasta with tomato sauce and mozzarella",
            height=100,key="type_food_input")
        meal_type_txt=st.selectbox("Meal type",["🌅 Breakfast","🌞 Lunch","🌙 Dinner","🍎 Snack"],key="txt_meal_type")

        if st.button("🔍 Calculate Calories with AI",use_container_width=True,key="calc_cal_btn"):
            if food_desc.strip():
                prompt=(f"As a nutrition expert, calculate the calories for this meal: '{food_desc}'\n"
                        f"User profile: {profile_str()}\n\n"
                        f"Provide:\n"
                        f"1. **Item-by-item breakdown**: Each food with calories\n"
                        f"2. **Total calories** for the meal\n"
                        f"3. **Macronutrients**: Protein, Carbs, Fat (grams)\n"
                        f"4. **Health Score**: 1-10 for this user's goal\n"
                        f"5. **Personalised feedback**: How this meal fits their {st.session_state.user_goal} goal\n"
                        f"6. **Swap suggestion**: One healthier swap if applicable\n"
                        f"Be precise with numbers. Format with clear headers.")
                with st.spinner("🤖 AI calculating…"):
                    cal_result=ai_text(prompt)
                st.markdown(f'<div class="fc-card">{cal_result}</div>',unsafe_allow_html=True)

                # Quick log
                st.markdown("---")
                c1,c2=st.columns(2)
                with c1: log_name=st.text_input("Meal name to log",value=food_desc[:50],key="txt_log_name")
                with c2: log_cal=st.number_input("Total calories (from AI above)",0,5000,0,10,key="txt_log_cal")
                if st.button("✅ Log this meal",key="txt_log_btn",use_container_width=True):
                    if log_name.strip() and log_cal>0:
                        st.session_state.cal_log.append({
                            "time":datetime.datetime.now().strftime("%H:%M"),
                            "food":log_name.strip(),"calories":log_cal,
                            "source":"⌨️ AI Analysis","meal":meal_type_txt,
                        })
                        st.session_state.cal_total+=log_cal
                        if not st.session_state.cal_done:
                            st.session_state.cal_done=True
                            award(XP["calorie"],"cal_done"); check_chal("cal_done"); show_reward()
                        aria_say("calorie")
                        speak(f"Meal logged! {log_cal} calories tracked. You are doing brilliantly {st.session_state.user_name}!")
                        st.success(f"✅ Logged — **{log_cal} kcal**")
                        st.rerun()
            else:
                st.info("Please describe what you ate above.")

    # ── Today's Log ───────────────────────────────────────────────────────────
    st.divider()
    st.markdown("### 📋 Today's Food Log")
    if not st.session_state.cal_log:
        st.info("No food logged yet. Use Camera or Type Food above!")
    else:
        for entry in reversed(st.session_state.cal_log):
            bp=min(entry["calories"]/cg*100,100) if cg else 0
            st.markdown(f"""
            <div class='fc-card' style='padding:.8rem 1rem;margin-bottom:.4rem'>
              <div style='display:flex;justify-content:space-between;align-items:center'>
                <div>
                  <span style='font-weight:600'>{entry["food"].title()}</span>
                  <span style='color:#888;font-size:.78rem'> · {entry.get("source","—")} · {entry["time"]} · {entry.get("meal","")}</span>
                </div>
                <div style='font-size:1.2rem;font-weight:700;color:#00e676;white-space:nowrap;margin-left:1rem'>
                  {entry["calories"]} kcal
                </div>
              </div>
              <div style='background:#1a1a2e;border-radius:999px;height:4px;margin-top:6px;overflow:hidden'>
                <div style='height:100%;width:{bp:.0f}%;background:#00e676;border-radius:999px'></div>
              </div>
            </div>""", unsafe_allow_html=True)
        c1,c2,c3=st.columns(3)
        c1.metric("Total today",f"{ct} kcal"); c2.metric("Daily goal",f"{cg} kcal")
        c3.metric("Remaining",f"{max(0,cg-ct)} kcal")
        if ct>=cg:
            st.warning(f"⚠️ You've hit your daily calorie goal of {cg} kcal. Consider lighter options for the rest of the day.")
        if st.button("🗑️ Clear log",key="clear_cal_log"):
            st.session_state.cal_log=[]; st.session_state.cal_total=0; st.rerun()

# ════════════════════════════════════════════════════════════════════════════
# MEDICATIONS
# ════════════════════════════════════════════════════════════════════════════
elif PAGE=="💊 Medications":
    st.subheader("💊 Medication Reminders")
    with st.expander("➕ Add medication",expanded=not st.session_state.medications):
        with st.form("med_form",clear_on_submit=True):
            c1,c2,c3=st.columns(3)
            with c1: mn=st.text_input("Name",placeholder="e.g. Vitamin D",key="med_name_input")
            with c2: mt=st.time_input("Time",datetime.time(8,0),key="med_time_input")
            with c3: md=st.text_input("Dose",placeholder="e.g. 1 tablet",key="med_dose_input")
            if st.form_submit_button("Add Medication") and mn.strip():
                st.session_state.medications.append({"name":mn.strip(),"time":mt.strftime("%H:%M:%S"),"dose":md.strip(),"taken":False})
                st.rerun()
    now=datetime.datetime.now().time()
    if not st.session_state.medications:
        st.info("No medications added yet.")
    else:
        for i,med in enumerate(st.session_state.medications):
            try: mtt=datetime.time.fromisoformat(med["time"])
            except: mtt=datetime.time(0,0)
            overdue=not med.get("taken",False) and mtt<now
            icon="✅" if med.get("taken") else ("⚠️" if overdue else "⏰")
            col=("#00e676" if med.get("taken") else ("#ff5252" if overdue else "#ffab40"))
            st.markdown(f"""
            <div class='fc-card' style='border-left:4px solid {col}'>
              <strong>{icon} {med["name"]}</strong>
              {"<span style='color:#888;font-size:.85rem'> · "+med['dose']+"</span>" if med.get('dose') else ""}
              <br><span style='color:#888;font-size:.82rem'>⏱ {med["time"]}</span>
              {"<span style='color:#ff5252;font-size:.82rem'> · Overdue!</span>" if overdue else ""}
            </div>""", unsafe_allow_html=True)
            cc1,cc2,cc3=st.columns([2,1,1])
            with cc2:
                if st.button("Mark taken ✅" if not med.get("taken") else "Undo ↩️",key=f"med_tog_{i}"):
                    st.session_state.medications[i]["taken"]=not med.get("taken",False)
                    if st.session_state.medications[i]["taken"]:
                        award(XP["med"]); aria_say("med")
                        if all(m.get("taken") for m in st.session_state.medications) and not st.session_state.meds_all_today:
                            st.session_state.meds_all_today=True
                            award(XP["meds_all"],"meds_all"); check_chal("meds_all_today"); aria_say("meds_all")
                    st.rerun()
            with cc3:
                if st.button("Remove 🗑️",key=f"med_del_{i}"):
                    st.session_state.medications.pop(i); st.rerun()
    if st.session_state.medications:
        tk=sum(1 for m in st.session_state.medications if m.get("taken",False))
        tt=len(st.session_state.medications)
        st.progress(tk/tt); st.markdown(f"**{tk}/{tt}** taken today.")
        if tk==tt>0: st.success("🎉 All medications taken — you're crushing it!")
    if st.button("💡 AI Adherence Tips",key="med_tips"):
        with st.spinner(""):
            tip=ai_text("Give me 3 practical, personalised tips to remember taking my medications on time every day.")
        st.markdown(f'<div class="fc-card">{tip}</div>',unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# MY PROFILE
# ════════════════════════════════════════════════════════════════════════════
elif PAGE=="👤 My Profile":
    st.subheader("👤 My Health Profile")
    bv=bmi_val(); bc,css=bmi_cat(bv)
    st.markdown(f"""
    <div class='stat-row'>
      <div class='stat-box'><div class='val'>{st.session_state.user_age}</div><div class='lbl'>Age</div></div>
      <div class='stat-box'><div class='val'>{st.session_state.user_gender[0]}</div><div class='lbl'>Gender</div></div>
      <div class='stat-box'><div class='val'>{st.session_state.user_height}cm</div><div class='lbl'>Height</div></div>
      <div class='stat-box'><div class='val'>{st.session_state.user_weight}kg</div><div class='lbl'>Weight</div></div>
      <div class='stat-box'><div class='val'>{bv}</div><div class='lbl'>BMI <span class='bmi-badge {css}'>{bc}</span></div></div>
      <div class='stat-box'><div class='val'>{int(bmr())} kcal</div><div class='lbl'>BMR</div></div>
      <div class='stat-box'><div class='val'>{WG}💧</div><div class='lbl'>Water goal</div></div>
    </div>""", unsafe_allow_html=True)
    st.divider()
    st.markdown("#### 🏆 Achievements")
    earned=[b for b in BADGES if b[3] in st.session_state.badges]
    if earned:
        st.markdown('<div class="badge-grid">'+"".join(f'<span class="badge-pill badge-on">{b[0]} {b[1]}</span>' for b in earned)+'</div>',unsafe_allow_html=True)
    else: st.caption("No badges yet — start using the app to earn them!")
    st.markdown(f"""
    <div class='stat-row' style='margin-top:.5rem'>
      <div class='stat-box'><div class='val'>{st.session_state.xp}</div><div class='lbl'>Total XP</div></div>
      <div class='stat-box'><div class='val'>{CL[1]}</div><div class='lbl'>Level</div></div>
      <div class='stat-box'><div class='val'>{st.session_state.streak}🔥</div><div class='lbl'>Streak</div></div>
      <div class='stat-box'><div class='val'>{st.session_state.challenges_done}</div><div class='lbl'>Challenges</div></div>
      <div class='stat-box'><div class='val'>{st.session_state.chat_count}</div><div class='lbl'>AI Chats</div></div>
    </div>""", unsafe_allow_html=True)
    st.divider()
    st.markdown("#### ✏️ Edit Profile")
    with st.form("profile_edit_form"):
        c1,c2=st.columns(2)
        with c1:
            nn=st.text_input("Name",st.session_state.user_name,key="profile_name_input")
            na=st.number_input("Age",10,100,st.session_state.user_age,key="profile_age_input")
            nh=st.number_input("Height (cm)",100.0,250.0,st.session_state.user_height,.5,key="profile_height_input")
        with c2:
            ng=st.selectbox("Gender",GENDER_OPTIONS,index=GENDER_OPTIONS.index(st.session_state.user_gender) if st.session_state.user_gender in GENDER_OPTIONS else 0,key="profile_gender_input")
            nw=st.number_input("Weight (kg)",30.0,300.0,st.session_state.user_weight,.5,key="profile_weight_input")
            ngl=st.selectbox("Goal",GOAL_OPTIONS,index=GOAL_OPTIONS.index(st.session_state.user_goal) if st.session_state.user_goal in GOAL_OPTIONS else 0,key="profile_goal_input")
        if st.form_submit_button("Save ✅"):
            st.session_state.update({"user_name":nn,"user_age":int(na),"user_gender":ng,
                                     "user_height":float(nh),"user_weight":float(nw),"user_goal":ngl})
            st.success("Profile updated! AI now uses your new stats. 💪❤️🌿"); st.rerun()
    st.divider()
    if st.button("💡 AI Health Summary",key="health_sum"):
        with st.spinner(""):
            s=ai_text("Give me a concise personalised health summary: current status, top 3 priorities, and one powerful motivating message tailored to me.")
        st.markdown(f'<div class="fc-card">{s}</div>',unsafe_allow_html=True)

# ─── Footer ──────────────────────────────────────────────────────────────────
st.divider()
st.caption("💪❤️🌿 FlexCoach · Powered by Google Gemini AI (Free) · Not a substitute for medical advice.")
