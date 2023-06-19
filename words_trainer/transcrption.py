import eng_to_ipa as ipa
from g2p_en import G2p


word = "obnoxious"
transcription = ipa.convert(word)
print(transcription)


g2p = G2p()
word = "obnoxious"
transcription = g2p(word)
print(transcription)
