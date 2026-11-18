from services.ai_service import LANGUAGE_NAMES, _call_gemini
from services.schemes_data import LAST_VERIFIED, SCHEMES, TIPS


def _scheme_text(s: dict) -> str:
    parts = [
        f"યોજના: {s['name']} ({s['tag']})",
        f"ટૂંકમાં: {s['summary']}",
        f"લાભ: {s['benefit']}",
        "કોણ પાત્ર: " + "; ".join(s["who"]),
        "અરજી કેવી રીતે: " + "; ".join(s["how"]),
        "દસ્તાવેજો: " + "; ".join(s["docs"]),
        f"સત્તાવાર લિંક: {s['link']}",
    ]
    if s.get("helpline"):
        parts.append(f"હેલ્પલાઇન: {s['helpline']}")
    if s.get("caution"):
        parts.append(f"સાવચેતી: {s['caution']}")
    return "\n".join(parts)


def answer_scheme_question(question: str, language: str = "gu", scheme_id: str = "") -> str:
    """ચકાસેલી યાદીના આધારે જ યોજનાનો જવાબ આપે છે."""
    lang = LANGUAGE_NAMES.get(language, "ગુજરાતી")
    chosen = [s for s in SCHEMES if s["id"] == scheme_id] or SCHEMES
    data = "\n\n".join(_scheme_text(s) for s in chosen)

    prompt = (
        f"નીચે સરકારી યોજનાઓની ચકાસેલી માહિતી છે (ચકાસણી: {LAST_VERIFIED}).\n\n"
        f"{data}\n\n"
        "સામાન્ય સૂચના: " + " ".join(TIPS) + "\n\n"
        "નિયમો: ફક્ત ઉપરની માહિતીના આધારે જવાબ આપો. આ માહિતીમાં ન હોય તેવી રકમ, તારીખ, "
        "પાત્રતા કે યોજનાનું નામ બનાવશો નહીં. પ્રશ્ન કોઈ બીજી યોજના વિશે હોય તો કહો કે મારી પાસે તેની "
        "ચકાસેલી માહિતી નથી, અને ikhedut.gujarat.gov.in, myscheme.gov.in કે તાલુકા ખેતી કચેરી/ગ્રામ સેવકનો "
        "સંપર્ક કરવા કહો. ખેડૂતને પાત્ર હોવાની ખાતરી ન આપો; 'સામાન્ય રીતે પાત્ર હોઈ શકે' કહી સત્તાવાર "
        "પોર્ટલ પર ચકાસવા કહો. ખેડૂત પાસે આધાર, OTP કે બેંકની વિગત માગશો નહીં, અને આવી વિગત કોઈને ન "
        "આપવા સલાહ આપો. જવાબ સરળ અને ટૂંકા મુદ્દાઓમાં આપો, અને અંતે સત્તાવાર લિંક કે હેલ્પલાઇન જણાવો. "
        f"જવાબ {lang} ભાષામાં આપો.\n\n"
        f"ખેડૂતનો પ્રશ્ન: {question}"
    )
    return _call_gemini(prompt)