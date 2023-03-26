import os
import azure.cognitiveservices.speech as speechsdk
import openai
import gradio as gr
import hashlib

speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), 
                                       region=os.environ.get('SPEECH_REGION')
                                       )
tts_output_file = "output.wav"
audio_config = speechsdk.audio.AudioOutputConfig(filename=tts_output_file)

openai.api_key = os.environ.get('OPENAI_KEY')

voices = ['af-ZA-AdriNeural', 'af-ZA-WillemNeural', 'am-ET-AmehaNeural', 'am-ET-MekdesNeural', 'ar-AE-FatimaNeural', 'ar-AE-HamdanNeural', 'ar-BH-AliNeural', 'ar-BH-LailaNeural', 'ar-DZ-AminaNeural', 'ar-DZ-IsmaelNeural', 'ar-EG-SalmaNeural', 'ar-EG-ShakirNeural', 'ar-IQ-BasselNeural', 'ar-IQ-RanaNeural', 'ar-JO-SanaNeural', 'ar-JO-TaimNeural', 'ar-KW-FahedNeural', 'ar-KW-NouraNeural', 'ar-LB-LaylaNeural', 'ar-LB-RamiNeural', 'ar-LY-ImanNeural', 'ar-LY-OmarNeural', 'ar-MA-JamalNeural', 'ar-MA-MounaNeural', 'ar-OM-AbdullahNeural', 'ar-OM-AyshaNeural', 'ar-QA-AmalNeural', 'ar-QA-MoazNeural', 'ar-SA-HamedNeural', 'ar-SA-ZariyahNeural', 'ar-SY-AmanyNeural', 'ar-SY-LaithNeural', 'ar-TN-HediNeural', 'ar-TN-ReemNeural', 'ar-YE-MaryamNeural', 'ar-YE-SalehNeural', 'az-AZ-BabekNeural', 'az-AZ-BanuNeural', 'bg-BG-BorislavNeural', 'bg-BG-KalinaNeural', 'bn-BD-NabanitaNeural', 'bn-BD-PradeepNeural', 'bn-IN-BashkarNeural', 'bn-IN-TanishaaNeural', 'bs-BA-GoranNeural', 'bs-BA-VesnaNeural', 'ca-ES-AlbaNeural', 'ca-ES-EnricNeural', 'ca-ES-JoanaNeural', 'cs-CZ-AntoninNeural', 'cs-CZ-VlastaNeural', 'cy-GB-AledNeural', 'cy-GB-NiaNeural', 'da-DK-ChristelNeural', 'da-DK-JeppeNeural', 'de-AT-IngridNeural', 'de-AT-JonasNeural', 'de-CH-JanNeural', 'de-CH-LeniNeural', 'de-DE-AmalaNeural', 'de-DE-BerndNeural', 'de-DE-ChristophNeural', 'de-DE-ConradNeural', 'de-DE-ElkeNeural', 'de-DE-GiselaNeural', 'de-DE-KasperNeural', 'de-DE-KatjaNeural', 'de-DE-KillianNeural', 'de-DE-KlarissaNeural', 'de-DE-KlausNeural', 'de-DE-LouisaNeural', 'de-DE-MajaNeural', 'de-DE-RalfNeural', 'de-DE-TanjaNeural', 'el-GR-AthinaNeural', 'el-GR-NestorasNeural', 'en-AU-AnnetteNeural', 'en-AU-CarlyNeural', 'en-AU-DarrenNeural', 'en-AU-DuncanNeural', 'en-AU-ElsieNeural', 'en-AU-FreyaNeural', 'en-AU-JoanneNeural', 'en-AU-KenNeural', 'en-AU-KimNeural', 'en-AU-NatashaNeural', 'en-AU-NeilNeural', 'en-AU-TimNeural', 'en-AU-TinaNeural', 'en-AU-WilliamNeural', 'en-CA-ClaraNeural', 'en-CA-LiamNeural', 'en-GB-AbbiNeural', 'en-GB-AlfieNeural', 'en-GB-BellaNeural', 'en-GB-ElliotNeural', 'en-GB-EthanNeural', 'en-GB-HollieNeural', 'en-GB-LibbyNeural', 'en-GB-MaisieNeural', 'en-GB-NoahNeural', 'en-GB-OliverNeural', 'en-GB-OliviaNeural', 'en-GB-RyanNeural', 'en-GB-SoniaNeural', 'en-GB-ThomasNeural', 'en-HK-SamNeural', 'en-HK-YanNeural', 'en-IE-ConnorNeural', 'en-IE-EmilyNeural', 'en-IN-NeerjaNeural', 'en-IN-PrabhatNeural', 'en-KE-AsiliaNeural', 'en-KE-ChilembaNeural', 'en-NG-AbeoNeural', 'en-NG-EzinneNeural', 'en-NZ-MitchellNeural', 'en-NZ-MollyNeural', 'en-PH-JamesNeural', 'en-PH-RosaNeural', 'en-SG-LunaNeural', 'en-SG-WayneNeural', 'en-TZ-ElimuNeural', 'en-TZ-ImaniNeural', 'en-US-AIGenerateNeural', 'en-US-AIGenerateNeural', 'en-US-AmberNeural', 'en-US-AnaNeural', 'en-US-AriaNeural', 'en-US-AshleyNeural', 'en-US-BrandonNeural', 'en-US-ChristopherNeural', 'en-US-CoraNeural', 'en-US-DavisNeural', 'en-US-ElizabethNeural', 'en-US-EricNeural', 'en-US-GuyNeural', 'en-US-JacobNeural', 'en-US-JaneNeural', 'en-US-JasonNeural', 'en-US-JennyMultilingualNeural', 'en-US-JennyNeural', 'en-US-MichelleNeural', 'en-US-MonicaNeural', 'en-US-NancyNeural', 'en-US-RogerNeural', 'en-US-SaraNeural', 'en-US-SteffanNeural', 'en-US-TonyNeural', 'en-ZA-LeahNeural', 'en-ZA-LukeNeural', 'es-AR-ElenaNeural', 'es-AR-TomasNeural', 'es-BO-MarceloNeural', 'es-BO-SofiaNeural', 'es-CL-CatalinaNeural', 'es-CL-LorenzoNeural', 'es-CO-GonzaloNeural', 'es-CO-SalomeNeural', 'es-CR-JuanNeural', 'es-CR-MariaNeural', 'es-CU-BelkysNeural', 'es-CU-ManuelNeural', 'es-DO-EmilioNeural', 'es-DO-RamonaNeural', 'es-EC-AndreaNeural', 'es-EC-LuisNeural', 'es-ES-AbrilNeural', 'es-ES-AlvaroNeural', 'es-ES-ArnauNeural', 'es-ES-DarioNeural', 'es-ES-EliasNeural', 'es-ES-ElviraNeural', 'es-ES-EstrellaNeural', 'es-ES-IreneNeural', 'es-ES-LaiaNeural', 'es-ES-LiaNeural', 'es-ES-NilNeural', 'es-ES-SaulNeural', 'es-ES-TeoNeural', 'es-ES-TrianaNeural', 'es-ES-VeraNeural', 'es-GQ-JavierNeural', 'es-GQ-TeresaNeural', 'es-GT-AndresNeural', 'es-GT-MartaNeural', 'es-HN-CarlosNeural', 'es-HN-KarlaNeural', 'es-MX-BeatrizNeural', 'es-MX-CandelaNeural', 'es-MX-CarlotaNeural', 'es-MX-CecilioNeural', 'es-MX-DaliaNeural', 'es-MX-GerardoNeural', 'es-MX-JorgeNeural', 'es-MX-LarissaNeural', 'es-MX-LibertoNeural', 'es-MX-LucianoNeural', 'es-MX-MarinaNeural', 'es-MX-NuriaNeural', 'es-MX-PelayoNeural', 'es-MX-RenataNeural', 'es-MX-YagoNeural', 'es-NI-FedericoNeural', 'es-NI-YolandaNeural', 'es-PA-MargaritaNeural', 'es-PA-RobertoNeural', 'es-PE-AlexNeural', 'es-PE-CamilaNeural', 'es-PR-KarinaNeural', 'es-PR-VictorNeural', 'es-PY-MarioNeural', 'es-PY-TaniaNeural', 'es-SV-LorenaNeural', 'es-SV-RodrigoNeural', 'es-US-AlonsoNeural', 'es-US-PalomaNeural', 'es-UY-MateoNeural', 'es-UY-ValentinaNeural', 'es-VE-PaolaNeural', 'es-VE-SebastianNeural', 'et-EE-AnuNeural', 'et-EE-KertNeural', 'eu-ES-AinhoaNeural', 'eu-ES-AnderNeural', 'fa-IR-DilaraNeural', 'fa-IR-FaridNeural', 'fi-FI-HarriNeural', 'fi-FI-NooraNeural', 'fi-FI-SelmaNeural', 'fil-PH-AngeloNeural', 'fil-PH-BlessicaNeural', 'fr-BE-CharlineNeural', 'fr-BE-GerardNeural', 'fr-CA-AntoineNeural', 'fr-CA-JeanNeural', 'fr-CA-SylvieNeural', 'fr-CH-ArianeNeural', 'fr-CH-FabriceNeural', 'fr-FR-AlainNeural', 'fr-FR-BrigitteNeural', 'fr-FR-CelesteNeural', 'fr-FR-ClaudeNeural', 'fr-FR-CoralieNeural', 'fr-FR-DeniseNeural', 'fr-FR-EloiseNeural', 'fr-FR-HenriNeural', 'fr-FR-JacquelineNeural', 'fr-FR-JeromeNeural', 'fr-FR-JosephineNeural', 'fr-FR-MauriceNeural', 'fr-FR-YvesNeural', 'fr-FR-YvetteNeural', 'ga-IE-ColmNeural', 'ga-IE-OrlaNeural', 'gl-ES-RoiNeural', 'gl-ES-SabelaNeural', 'gu-IN-DhwaniNeural', 'gu-IN-NiranjanNeural', 'he-IL-AvriNeural', 'he-IL-HilaNeural', 'hi-IN-MadhurNeural', 'hi-IN-SwaraNeural', 'hr-HR-GabrijelaNeural', 'hr-HR-SreckoNeural', 'hu-HU-NoemiNeural', 'hu-HU-TamasNeural', 'hy-AM-AnahitNeural', 'hy-AM-HaykNeural', 'id-ID-ArdiNeural', 'id-ID-GadisNeural', 'is-IS-GudrunNeural', 'is-IS-GunnarNeural', 'it-IT-BenignoNeural', 'it-IT-CalimeroNeural', 'it-IT-CataldoNeural', 'it-IT-DiegoNeural', 'it-IT-ElsaNeural', 'it-IT-FabiolaNeural', 'it-IT-FiammaNeural', 'it-IT-GianniNeural', 'it-IT-ImeldaNeural', 'it-IT-IrmaNeural', 'it-IT-IsabellaNeural', 'it-IT-LisandroNeural', 'it-IT-PalmiraNeural', 'it-IT-PierinaNeural', 'it-IT-RinaldoNeural', 'ja-JP-AoiNeural', 'ja-JP-DaichiNeural', 'ja-JP-KeitaNeural', 'ja-JP-MayuNeural', 'ja-JP-NanamiNeural', 'ja-JP-NaokiNeural', 'ja-JP-ShioriNeural', 'jv-ID-DimasNeural', 'jv-ID-SitiNeural', 'ka-GE-EkaNeural', 'ka-GE-GiorgiNeural', 'kk-KZ-AigulNeural', 'kk-KZ-DauletNeural', 'km-KH-PisethNeural', 'km-KH-SreymomNeural', 'kn-IN-GaganNeural', 'kn-IN-SapnaNeural', 'ko-KR-BongJinNeural', 'ko-KR-GookMinNeural', 'ko-KR-InJoonNeural', 'ko-KR-JiMinNeural', 'ko-KR-SeoHyeonNeural', 'ko-KR-SoonBokNeural', 'ko-KR-SunHiNeural', 'ko-KR-YuJinNeural', 'lo-LA-ChanthavongNeural', 'lo-LA-KeomanyNeural', 'lt-LT-LeonasNeural', 'lt-LT-OnaNeural', 'lv-LV-EveritaNeural', 'lv-LV-NilsNeural', 'mk-MK-AleksandarNeural', 'mk-MK-MarijaNeural', 'ml-IN-MidhunNeural', 'ml-IN-SobhanaNeural', 'mn-MN-BataaNeural', 'mn-MN-YesuiNeural', 'mr-IN-AarohiNeural', 'mr-IN-ManoharNeural', 'ms-MY-OsmanNeural', 'ms-MY-YasminNeural', 'mt-MT-GraceNeural', 'mt-MT-JosephNeural', 'my-MM-NilarNeural', 'my-MM-ThihaNeural', 'nb-NO-FinnNeural', 'nb-NO-IselinNeural', 'nb-NO-PernilleNeural', 'ne-NP-HemkalaNeural', 'ne-NP-SagarNeural', 'nl-BE-ArnaudNeural', 'nl-BE-DenaNeural', 'nl-NL-ColetteNeural', 'nl-NL-FennaNeural', 'nl-NL-MaartenNeural', 'pl-PL-AgnieszkaNeural', 'pl-PL-MarekNeural', 'pl-PL-ZofiaNeural', 'ps-AF-GulNawazNeural', 'ps-AF-LatifaNeural', 'pt-BR-AntonioNeural', 'pt-BR-BrendaNeural', 'pt-BR-DonatoNeural', 'pt-BR-ElzaNeural', 'pt-BR-FabioNeural', 'pt-BR-FranciscaNeural', 'pt-BR-GiovannaNeural', 'pt-BR-HumbertoNeural', 'pt-BR-JulioNeural', 'pt-BR-LeilaNeural', 'pt-BR-LeticiaNeural', 'pt-BR-ManuelaNeural', 'pt-BR-NicolauNeural', 'pt-BR-ValerioNeural', 'pt-BR-YaraNeural', 'pt-PT-DuarteNeural', 'pt-PT-FernandaNeural', 'pt-PT-RaquelNeural', 'ro-RO-AlinaNeural', 'ro-RO-EmilNeural', 'ru-RU-DariyaNeural', 'ru-RU-DmitryNeural', 'ru-RU-SvetlanaNeural', 'si-LK-SameeraNeural', 'si-LK-ThiliniNeural', 'sk-SK-LukasNeural', 'sk-SK-ViktoriaNeural', 'sl-SI-PetraNeural', 'sl-SI-RokNeural', 'so-SO-MuuseNeural', 'so-SO-UbaxNeural', 'sq-AL-AnilaNeural', 'sq-AL-IlirNeural', 'sr-RS-NicholasNeural', 'sr-RS-SophieNeural', 'su-ID-JajangNeural', 'su-ID-TutiNeural', 'sv-SE-HilleviNeural', 'sv-SE-MattiasNeural', 'sv-SE-SofieNeural', 'sw-KE-RafikiNeural', 'sw-KE-ZuriNeural', 'sw-TZ-DaudiNeural', 'sw-TZ-RehemaNeural', 'ta-IN-PallaviNeural', 'ta-IN-ValluvarNeural', 'ta-LK-KumarNeural', 'ta-LK-SaranyaNeural', 'ta-MY-KaniNeural', 'ta-MY-SuryaNeural', 'ta-SG-AnbuNeural', 'ta-SG-VenbaNeural', 'te-IN-MohanNeural', 'te-IN-ShrutiNeural', 'th-TH-AcharaNeural', 'th-TH-NiwatNeural', 'th-TH-PremwadeeNeural', 'tr-TR-AhmetNeural', 'tr-TR-EmelNeural', 'uk-UA-OstapNeural', 'uk-UA-PolinaNeural', 'ur-IN-GulNeural', 'ur-IN-SalmanNeural', 'ur-PK-AsadNeural', 'ur-PK-UzmaNeural', 'uz-UZ-MadinaNeural', 'uz-UZ-SardorNeural', 'vi-VN-HoaiMyNeural', 'vi-VN-NamMinhNeural', 'wuu-CN-XiaotongNeural,', 'wuu-CN-YunzheNeural,', 'yue-CN-XiaoMinNeural,', 'yue-CN-YunSongNeural,', 'zh-CN-XiaochenNeural', 'zh-CN-XiaohanNeural', 'zh-CN-XiaomengNeural', 'zh-CN-XiaomoNeural', 'zh-CN-XiaoqiuNeural', 'zh-CN-XiaoruiNeural', 'zh-CN-XiaoshuangNeural', 'zh-CN-XiaoxiaoNeural', 'zh-CN-XiaoxuanNeural', 'zh-CN-XiaoyanNeural', 'zh-CN-XiaoyiNeural', 'zh-CN-XiaoyouNeural', 'zh-CN-XiaozhenNeural', 'zh-CN-YunfengNeural', 'zh-CN-YunhaoNeural', 'zh-CN-YunjianNeural', 'zh-CN-YunxiNeural', 'zh-CN-YunxiaNeural', 'zh-CN-YunyangNeural', 'zh-CN-YunyeNeural', 'zh-CN-YunzeNeural', 'zh-CN-henan', 'zh-CN-henan-YundengNeural', 'zh-CN-liaoning', 'zh-CN-liaoning-XiaobeiNeural,', 'zh-CN-shaanxi', 'zh-CN-shaanxi-XiaoniNeural,', 'zh-CN-shandong', 'zh-CN-shandong-YunxiangNeural', 'zh-CN-sichuan', 'zh-CN-sichuan-YunxiNeural,', 'zh-HK-HiuGaaiNeural', 'zh-HK-HiuMaanNeural', 'zh-HK-WanLungNeural', 'zh-TW-HsiaoChenNeural', 'zh-TW-HsiaoYuNeural', 'zh-TW-YunJheNeural', 'zu-ZA-ThandoNeural', 'zu-ZA-ThembaNeural']
language_names = ['Afrikaans (South Africa)','Amharic (Ethiopia)','Arabic (United Arab Emirates)','Arabic (Bahrain)','Arabic (Algeria)','Arabic (Egypt)','Arabic (Iraq)','Arabic (Jordan)','Arabic (Kuwait)','Arabic (Lebanon)','Arabic (Libya)','Arabic (Morocco)','Arabic (Oman)','Arabic (Qatar)','Arabic (Saudi Arabia)','Arabic (Syria)','Arabic (Tunisia)','Arabic (Yemen)','Azerbaijani (Latin, Azerbaijan)','Bulgarian (Bulgaria)','Bangla (Bangladesh)','Bengali (India)','Bosnian (Bosnia and Herzegovina)','Catalan (Spain)','Czech (Czechia)','Welsh (United Kingdom)','Danish (Denmark)','German (Austria)','German (Switzerland)','German (Germany)','Greek (Greece)','English (Australia)','English (Canada)','English (United Kingdom)','English (Hong Kong SAR)','English (Ireland)','English (India)','English (Kenya)','English (Nigeria)','English (New Zealand)','English (Philippines)','English (Singapore)','English (Tanzania)','English (United States)','English (South Africa)','Spanish (Argentina)','Spanish (Bolivia)','Spanish (Chile)','Spanish (Colombia)','Spanish (Costa Rica)','Spanish (Cuba)','Spanish (Dominican Republic)','Spanish (Ecuador)','Spanish (Spain)','Spanish (Equatorial Guinea)','Spanish (Guatemala)','Spanish (Honduras)','Spanish (Mexico)','Spanish (Nicaragua)','Spanish (Panama)','Spanish (Peru)','Spanish (Puerto Rico)','Spanish (Paraguay)','Spanish (El Salvador)','Spanish (United States)','Spanish (Uruguay)','Spanish (Venezuela)','Estonian (Estonia)','Basque','Persian (Iran)','Finnish (Finland)','Filipino (Philippines)','French (Belgium)','French (Canada)','French (Switzerland)','French (France)','Irish (Ireland)','Galician','Gujarati (India)','Hebrew (Israel)','Hindi (India)','Croatian (Croatia)','Hungarian (Hungary)','Armenian (Armenia)','Indonesian (Indonesia)','Icelandic (Iceland)','Italian (Italy)','Japanese (Japan)','Javanese (Latin, Indonesia)','Georgian (Georgia)','Kazakh (Kazakhstan)','Khmer (Cambodia)','Kannada (India)','Korean (Korea)','Lao (Laos)','Lithuanian (Lithuania)','Latvian (Latvia)','Macedonian (North Macedonia)','Malayalam (India)','Mongolian (Mongolia)','Marathi (India)','Malay (Malaysia)','Maltese (Malta)','Burmese (Myanmar)','Norwegian Bokmål (Norway)','Nepali (Nepal)','Dutch (Belgium)','Dutch (Netherlands)','Polish (Poland)','Pashto (Afghanistan)','Portuguese (Brazil)','Portuguese (Portugal)','Romanian (Romania)','Russian (Russia)','Sinhala (Sri Lanka)','Slovak (Slovakia)','Slovenian (Slovenia)','Somali (Somalia)','Albanian (Albania)','Serbian (Cyrillic, Serbia)','Sundanese (Indonesia)','Swedish (Sweden)','Swahili (Kenya)','Swahili (Tanzania)','Tamil (India)','Tamil (Sri Lanka)','Tamil (Malaysia)','Tamil (Singapore)','Telugu (India)','Thai (Thailand)','Turkish (Turkey)','Ukrainian (Ukraine)','Urdu (India)','Urdu (Pakistan)','Uzbek (Latin, Uzbekistan)','Vietnamese (Vietnam)','Chinese (Wu, Simplified)','Chinese (Cantonese, Simplified)','Chinese (Mandarin, Simplified)','Chinese (Zhongyuan Mandarin Henan, Simplified)','Chinese (Northeastern Mandarin, Simplified)','Chinese (Zhongyuan Mandarin Shaanxi, Simplified)','Chinese (Jilu Mandarin, Simplified)','Chinese (Southwestern Mandarin, Simplified)','Chinese (Cantonese, Traditional)','Chinese (Taiwanese Mandarin, Traditional)','Zulu (South Africa)']
language_codes = ['af-ZA', 'am-ET', 'ar-AE', 'ar-BH', 'ar-DZ', 'ar-EG', 'ar-IQ', 'ar-JO', 'ar-KW', 'ar-LB', 'ar-LY', 'ar-MA', 'ar-OM', 'ar-QA', 'ar-SA', 'ar-SY', 'ar-TN', 'ar-YE', 'az-AZ', 'bg-BG', 'bn-BD', 'bn-IN', 'bs-BA', 'ca-ES', 'cs-CZ', 'cy-GB', 'da-DK', 'de-AT', 'de-CH', 'de-DE', 'el-GR', 'en-AU', 'en-CA', 'en-GB', 'en-HK', 'en-IE', 'en-IN', 'en-KE', 'en-NG', 'en-NZ', 'en-PH', 'en-SG', 'en-TZ', 'en-US', 'en-ZA', 'es-AR', 'es-BO', 'es-CL', 'es-CO', 'es-CR', 'es-CU', 'es-DO', 'es-EC', 'es-ES', 'es-GQ', 'es-GT', 'es-HN', 'es-MX', 'es-NI', 'es-PA', 'es-PE', 'es-PR', 'es-PY', 'es-SV', 'es-US', 'es-UY', 'es-VE', 'et-EE', 'eu-ES', 'fa-IR', 'fi-FI', 'fil-PH', 'fr-BE', 'fr-CA', 'fr-CH', 'fr-FR', 'ga-IE', 'gl-ES', 'gu-IN', 'he-IL', 'hi-IN', 'hr-HR', 'hu-HU', 'hy-AM', 'id-ID', 'is-IS', 'it-IT', 'ja-JP', 'jv-ID', 'ka-GE', 'kk-KZ', 'km-KH', 'kn-IN', 'ko-KR', 'lo-LA', 'lt-LT', 'lv-LV', 'mk-MK', 'ml-IN', 'mn-MN', 'mr-IN', 'ms-MY', 'mt-MT', 'my-MM', 'nb-NO', 'ne-NP', 'nl-BE', 'nl-NL', 'pl-PL', 'ps-AF', 'pt-BR', 'pt-PT', 'ro-RO', 'ru-RU', 'si-LK', 'sk-SK', 'sl-SI', 'so-SO', 'sq-AL', 'sr-RS', 'su-ID', 'sv-SE', 'sw-KE', 'sw-TZ', 'ta-IN', 'ta-LK', 'ta-MY', 'ta-SG', 'te-IN', 'th-TH', 'tr-TR', 'uk-UA', 'ur-IN', 'ur-PK', 'uz-UZ', 'vi-VN', 'wuu-CN', 'yue-CN', 'zh-CN', 'zh-HK', 'zh-TW', 'zu-ZA']

language_code_dict = dict(zip(language_codes,language_names))


#with open('dialog.txt','w') as textfile:
#  print(textfile.write(base_prompt))

def clear_chat():
    filename = f'''dialog.txt'''
    os.remove(filename)

def querybot(audio_file, voice_choice, request: gr.Request):


    language_choice = language_code_dict['-'.join(voice_choice.split('-')[:2])].split()[0]

    guidance_prompt = f'''
You are a {language_choice} conversation bot named Robotto, talking to a student who is an intermediate learner in the {language_choice} language. 
You should only use the {language_choice.lower()} language when answering. The user will talk to you in {language_choice}. The user likes it when Robotto gives long answers.
'''

    os.rename(audio_file, audio_file + '.wav')
    audio_file+='.wav'
    if request:
        ip_address = request.client.host
        user_id = hashlib.md5(ip_address.encode()).hexdigest()
        filename = f'''dialog.txt'''

    if not os.path.isfile(filename):
        with open(filename,'w') as textfile:
            base_prompt = f'''
Conversation Start
'''
#            base_prompt = f'''
#You are a {language_choice} conversation bot named Robotto, talking to a student who is an intermediate learner in the {language_choice} language. 
#You should only use the {language_choice.lower()} language when answering. The user will talk to you in {language_choice}. The user likes it when Robotto gives long answers.
#'''
            textfile.write(base_prompt)    

    with open(audio_file,'rb') as audio_source:
        prompt = openai.Audio.transcribe("whisper-1",audio_source)['text']

    with open(filename,'r') as textfile:
      base_prompt = textfile.readlines()
      numlines = len(base_prompt)
      num_context_lines = 20
      base_prompt = base_prompt[:3] + base_prompt[3:][-num_context_lines:]
      base_prompt = ''.join(base_prompt)
    full_prompt = base_prompt+'\nUser:'+prompt+'\nRobotto:'

    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo", 
      messages=[{"role": "system", "content": guidance_prompt},
                {"role": "user", "content": full_prompt}
                ]
    )

    output = response['choices'][0]['message']['content'] 

    with open(filename,'w') as textfile:
      print(textfile.write(full_prompt+output)) 

    output = output.replace('Robotto:','').strip()


    tts_output_file = "output.wav"
    audio_config = speechsdk.audio.AudioOutputConfig(filename=tts_output_file)
    speech_config.speech_synthesis_voice_name=voice_choice.split()[0]

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, 
                                                    audio_config=audio_config
                                                    )

    text = output

    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

    return tts_output_file, output

app = gr.Blocks()

with app:
    gr.Markdown('Powered by: OpenAI Whisper, OpenAI GPT-3.5, Azure TTS')
    with gr.Tabs():
      with gr.Column():
          tts_input1 = gr.Audio(source="microphone", type="filepath")
          tts_input2 = gr.Dropdown(voices, value=voices[0], label="Robotto voice")
          with gr.Row():
              tts_submit = gr.Button("Generate", variant="primary")
              chat_delete = gr.Button("Clear chat", variant="primary")

          tts_output1 = gr.Audio(label="Output Audio")
          tts_output2 = gr.Textbox(label = 'What does the bot say?')

          tts_submit.click(querybot, [tts_input1, tts_input2],
                            [tts_output1, tts_output2])
          chat_delete.click(clear_chat)

app.queue(concurrency_count=3).launch(show_api=False, share=False)
