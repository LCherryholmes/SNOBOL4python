# Reading inbox. 901205028 bytes.
# Scanning lines. 12976894 lines.
# Scanning sections. 8259 sections.
# Parsing emails.

# From - Thu Feb 20 20:43:02 2025
# From - Thu Feb 20 20:43:02 2025
# From - Thu Feb 20 20:43:02 2025
# From - Thu Feb 20 20:43:03 2025
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_Account_Key:: yield from (
    r' [a-z]+[0-9]'
   #4: account1
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_UIDL:: yield from (
    r' [A-Z]+[a-z]+[A-Z]+[0-9][A-Z]+[a-z]/[A-Z][a-z]+[0-9]+[a-z][0-9][a-z][A-Z]+'
   #1: ABVlxEIAAC5GRXQn/Ajb40l5eAU
|   r' [A-Z]+[a-z]+[A-Z]+[a-z][A-Z]+[a-z][0-9][A-Z][0-9][A-Z][a-z][A-Z][a-z][A-Z][a-z]+[A-Z]'
   #1: ABBlxEIAABVkRXRs6Q6ThBqYacU
|   r' [A-Z]+[a-z]+[A-Z]+[0-9][a-z][A-Z]+[a-z][A-Z]+[a-z][A-Z]'
   #1: AAxlxEIAAJIJRXR2qQRAFlOTAhE
|   r' [A-Z]+[a-z]+[A-Z]+[0-9][A-Z][a-z][A-Z][a-z]+[A-Z][a-z]+[A-Z]'
   #1: ABhlxEIAAHLNRXR9JwOfywIsljY
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_Mozilla_Status:: yield from (
    r' [0-9]+'
   #3: 0000
   #1: 0011
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_Mozilla_Status2:: yield from (
    r' [0-9]+'
   #4: 00000000
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_Mozilla_Keys:: yield from (
    r'[ ]+'
   #4:                                                                                 
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_Apparently_To:: yield from (
    r' [a-z]+@[a-z]+\.[a-z]+ [a-z]+ [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+; [A-Z][a-z]+, [0-9]+ [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ -[0-9]+'
   #1: lcherryh@yahoo.com via 66.196.101.21; Mon, 04 Dec 2006 05:51:56 -0800
   #1: lcherryh@yahoo.com via 66.196.101.16; Mon, 04 Dec 2006 10:46:01 -0800
   #1: lcherryh@yahoo.com via 66.196.101.12; Mon, 04 Dec 2006 11:27:37 -0800
   #1: lcherryh@yahoo.com via 66.196.101.24; Mon, 04 Dec 2006 11:55:19 -0800
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_Originating_IP:: yield from (
    r' \[[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\]'
   #1: [12.106.87.68]
   #3: [12.106.87.70]
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def Return_Path:: yield from (
    r' <[a-z]+\.[a-z]+@[a-z]+\.[a-z]+>'
   #1: <ken.moses@quest.com>
   #1: <pat.luis@quest.com>
   #1: <lisa.radford@quest.com>
   #1: <keren.kamilian@quest.com>
|   r' [A-Z][a-z]+\.[A-Z][a-z]+@[a-z]+\.[a-z]+'
   #1: Ken.Moses@quest.com
   #1: Lisa.Radford@quest.com
   #1: Keren.Kamilian@quest.com
|   r' [a-z]+\.[a-z]+@[a-z]+\.[a-z]+'
   #1: pat.luis@quest.com
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def Authentication_Results:: yield from (
    r' [a-z]+[0-9]+\.[a-z]+\.[a-z]+\.[a-z]+\.[a-z]+[ ]+[a-z]+=[a-z]+\.[a-z]+; [a-z]+=[a-z]+ \([a-z]+ [a-z]+\)'
   #1: mta526.mail.mud.yahoo.com  from=quest.com; domainkeys=neutral (no sig)
|   r' [a-z]+[0-9]+\.[a-z]+\.[a-z]+[0-9]\.[a-z]+\.[a-z]+[ ]+[a-z]+=[a-z]+\.[a-z]+; [a-z]+=[a-z]+ \([a-z]+ [a-z]+\)'
   #1: mta188.mail.re3.yahoo.com  from=quest.com; domainkeys=neutral (no sig)
   #1: mta224.mail.re4.yahoo.com  from=quest.com; domainkeys=neutral (no sig)
   #1: mta368.mail.re4.yahoo.com  from=quest.com; domainkeys=neutral (no sig)
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def Received:: yield from (
    r' [a-z]+ [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+[ ]+\([A-Z]+ [a-z]+[0-9]+\.[a-z]+\.[a-z]+\) \([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\)\n[ ]+[a-z]+ [a-z]+[0-9]+\.[a-z]+\.[a-z]+\.[a-z]+\.[a-z]+ [a-z]+ [A-Z]+; [A-Z][a-z]+, [0-9]+ [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ -[0-9]+'
   #1: from 12.106.87.68  (EHLO irvbhxw02.quest.com) (12.106.87.68){bslash}n  by mta526.mail.mud.yahoo.com with SMTP; Mon, 04 Dec 2006 05:51:56 -0800
|   r' [a-z]+ [a-z]+[0-9]+\.[a-z]+\.[a-z]+\.[a-z]+ \(\[[0-9]+\.[0-9]\.[0-9]\.[0-9]+\]\) [a-z]+ [a-z]+[0-9]+\.[a-z]+\.[a-z]+ [a-z]+ [A-Z][a-z]+ [A-Z]+\([0-9]\.[0-9]\.[0-9]+\.[0-9]+\);\n\t [A-Z][a-z]+, [0-9] [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ -[0-9]+'
   #1: from alvmbxw02.prod.quest.corp ([10.1.0.209]) by irvbhxw02.quest.com with Microsoft SMTPSVC(6.0.3790.1830);{bslash}n	 Mon, 4 Dec 2006 05:51:56 -0800
|   r' [a-z]+ [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+[ ]+\([A-Z]+ [a-z]+[0-9]+\.[a-z]+\.[a-z]+\) \([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\)\n[ ]+[a-z]+ [a-z]+[0-9]+\.[a-z]+\.[a-z]+[0-9]\.[a-z]+\.[a-z]+ [a-z]+ [A-Z]+; [A-Z][a-z]+, [0-9]+ [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ -[0-9]+'
   #1: from 12.106.87.70  (EHLO irvbhxw03.quest.com) (12.106.87.70){bslash}n  by mta188.mail.re3.yahoo.com with SMTP; Mon, 04 Dec 2006 10:46:01 -0800
   #1: from 12.106.87.70  (EHLO irvbhxw03.quest.com) (12.106.87.70){bslash}n  by mta224.mail.re4.yahoo.com with SMTP; Mon, 04 Dec 2006 11:27:37 -0800
   #1: from 12.106.87.70  (EHLO irvbhxw03.quest.com) (12.106.87.70){bslash}n  by mta368.mail.re4.yahoo.com with SMTP; Mon, 04 Dec 2006 11:55:18 -0800
|   r' [a-z]+ [a-z]+[0-9]+\.[a-z]+\.[a-z]+\.[a-z]+ \(\[[0-9]+\.[0-9]\.[0-9]+\.[0-9]+\]\) [a-z]+ [a-z]+[0-9]+\.[a-z]+\.[a-z]+ [a-z]+ [A-Z][a-z]+ [A-Z]+\([0-9]\.[0-9]\.[0-9]+\.[0-9]+\);\n\t [A-Z][a-z]+, [0-9] [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ -[0-9]+'
   #1: from alvmbxw01.prod.quest.corp ([10.1.50.13]) by irvbhxw03.quest.com with Microsoft SMTPSVC(6.0.3790.1830);{bslash}n	 Mon, 4 Dec 2006 10:46:00 -0800
   #1: from alvmbxw01.prod.quest.corp ([10.1.50.13]) by irvbhxw03.quest.com with Microsoft SMTPSVC(6.0.3790.1830);{bslash}n	 Mon, 4 Dec 2006 11:27:36 -0800
   #1: from alvmbxw01.prod.quest.corp ([10.1.50.13]) by irvbhxw03.quest.com with Microsoft SMTPSVC(6.0.3790.1830);{bslash}n	 Mon, 4 Dec 2006 11:55:17 -0800
|   r' [a-z]+ [a-z]+[0-9]+\.[a-z]+\.[a-z]+\.[a-z]+ \(\[[0-9]+\.[0-9]+\.[0-9]\.[0-9]+\]\) [a-z]+ [a-z]+[0-9]+\.[a-z]+\.[a-z]+\.[a-z]+ [a-z]+ [A-Z][a-z]+ [A-Z]+\([0-9]\.[0-9]\.[0-9]+\.[0-9]+\);\n\t [A-Z][a-z]+, [0-9] [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ -[0-9]+'
   #1: from ukbmbxw01.prod.quest.corp ([10.10.1.34]) by alvmbxw01.prod.quest.corp with Microsoft SMTPSVC(6.0.3790.1830);{bslash}n	 Mon, 4 Dec 2006 11:55:17 -0800
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_MimeOLE:: yield from (
    r' [A-Z][a-z]+ [A-Z][a-z] [A-Z][a-z]+ [A-Z][a-z]+ [A-Z][0-9]\.[0-9]'
   #4: Produced By Microsoft Exchange V6.5
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def Content_class:: yield from (
    r' [a-z]+:[a-z]+-[a-z]+:[a-z]+'
   #4: urn:content-classes:message
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def MIME_Version:: yield from (
    r' [0-9]\.[0-9]'
   #4: 1.0
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def Content_Type:: yield from (
    r' [a-z]+/[a-z]+;\n\t[a-z]+="----_=_[A-Z][a-z]+[A-Z][a-z]+_[0-9]+_[0-9]+[A-Z][0-9]+[A-Z]+\.[0-9][A-Z][0-9]+[A-Z]+"'
   #1: multipart/alternative;{bslash}n	boundary="----_=_NextPart_001_01C717AB.5C51AFDE"
   #1: multipart/alternative;{bslash}n	boundary="----_=_NextPart_001_01C717DA.3F949EDA"
|   r' [a-z]+/[a-z]+;\n\t[a-z]+="----_=_[A-Z][a-z]+[A-Z][a-z]+_[0-9]+_[0-9]+[A-Z][0-9]+[A-Z][0-9]\.[0-9]+[A-Z][0-9]"'
   #1: multipart/alternative;{bslash}n	boundary="----_=_NextPart_001_01C717D4.712756D2"
|   r' [a-z]+/[a-z]+;\n\t[a-z]+="----_=_[A-Z][a-z]+[A-Z][a-z]+_[0-9]+_[0-9]+[A-Z][0-9]+[A-Z]+\.[0-9][A-Z]+[0-9]+[A-Z][0-9]+"'
   #1: multipart/alternative;{bslash}n	boundary="----_=_NextPart_001_01C717DE.1CE62D98"
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def Subject:: yield from (
    r' [A-Z][a-z]+ [a-z]+ [A-Z][a-z]+ [A-Z][a-z]+[A-Z][a-z]+: [A-Z][a-z]+ [a-z]+ [a-z]+!'
   #1: Out of Office AutoReply: Account accidentally disabled!
|   r' [A-Z][a-z]+ [A-Z][a-z]+ - [a-z]+ [a-z]+-[a-z]+'
   #1: Quest Software - account re-activation
|   r' [A-Z]+: [A-Z][a-z]+ [a-z]+ [a-z]+ [a-z]+!'
   #1: RE: Please reactivate my account!
|   r' [A-Z]+: [A-Z][a-z]+ [A-Z][a-z]+ - [a-z]+ [a-z]+-[a-z]+'
   #1: RE: Quest Software - account re-activation
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def Date:: yield from (
    r' [A-Z][a-z]+, [0-9] [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ \+[0-9]+'
   #1: Mon, 4 Dec 2006 21:51:55 +0800
|   r' [A-Z][a-z]+, [0-9] [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ -[0-9]+'
   #1: Mon, 4 Dec 2006 10:46:00 -0800
   #1: Mon, 4 Dec 2006 11:27:33 -0800
   #1: Mon, 4 Dec 2006 19:55:13 -0000
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def Message_ID:: yield from (
    r' <[0-9]+[A-Z]+[0-9]+[A-Z]+[0-9]+[A-Z][0-9][A-Z][0-9][A-Z][0-9][A-Z][0-9][A-Z][0-9]+[A-Z][0-9]+[A-Z][0-9][A-Z][0-9][A-Z]+[0-9]@[A-Z]+[0-9]+\.[a-z]+\.[a-z]+\.[a-z]+>'
   #1: <78CD474EB76D9C4C9E8F03720184A36B0B5BCBF2@ALVMBXW02.prod.quest.corp>
|   r' <[A-Z]+[0-9]+[A-Z][0-9]+[A-Z][0-9]+[A-Z]+[0-9]+[A-Z][0-9][A-Z][0-9][A-Z]+[0-9][A-Z][0-9]+[A-Z]+[0-9][A-Z][0-9]@[a-z]+[0-9]+\.[a-z]+\.[a-z]+\.[a-z]+>'
   #1: <FA13712B13469646A618BC95F7E1BA8F01ABD6E9@alvmbxw01.prod.quest.corp>
|   r' <[0-9]+[A-Z][0-9]+[A-Z][0-9]+[A-Z][0-9]+[A-Z]+[0-9][A-Z][0-9]+[A-Z][0-9]+[A-Z][0-9]+[A-Z][0-9]@[a-z]+[0-9]+\.[a-z]+\.[a-z]+\.[a-z]+>'
   #1: <81B3912B246E23449049CFA9C12D04F6036620A7@alvmbxw01.prod.quest.corp>
|   r' <[A-Z][0-9]+[A-Z][0-9]+[A-Z][0-9]+[A-Z][0-9]+[A-Z]+[0-9]+[A-Z][0-9][A-Z]+[0-9]+[A-Z][0-9][A-Z]@[a-z]+[0-9]+\.[a-z]+\.[a-z]+\.[a-z]+>'
   #1: <E61E658006418E47861A484DE76F4FC507310D8B@ukbmbxw01.prod.quest.corp>
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_MS_Has_Attach:: yield from (
    r' '
   #4: 
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_MS_TNEF_Correlator:: yield from (
    r' '
   #4: 
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def Thread_Topic:: yield from (
    r' [A-Z][a-z]+ [a-z]+ [a-z]+!'
   #1: Account accidentally disabled!
|   r' [A-Z][a-z]+ [A-Z][a-z]+ - [a-z]+ [a-z]+-[a-z]+'
   #2: Quest Software - account re-activation
|   r' [A-Z][a-z]+ [a-z]+ [a-z]+ [a-z]+!'
   #1: Please reactivate my account!
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def Thread_Index:: yield from (
    r' [A-Z][a-z]+[A-Z][a-z][0-9][a-z][A-Z]+[0-9][A-Z][0-9][a-z][A-Z]+/[A-Z][0-9][A-Z]+[a-z]+[A-Z]\+[a-z][A-Z]\+[A-Z]+[a-z]'
   #1: AccXq1xKC7R4pDK/Q6KSUBrhS+yX+QAAAAFe
|   r' [A-Z][a-z]+[A-Z][0-9][A-Z]+[0-9][a-z][A-Z][a-z][A-Z]+[a-z][A-Z][0-9][A-Z][a-z][A-Z][a-z][0-9][A-Z]+[0-9][a-z]+=='
   #1: AccX1HFT7mXxXKMqQ4WfYy2XVAP9zw==
|   r' [A-Z][a-z]+[A-Z][a-z][A-Z][a-z]+[A-Z][a-z][A-Z][a-z]+/[A-Z]+/[0-9][A-Z][a-z]+[A-Z][a-z][A-Z]+[a-z][A-Z][a-z][A-Z]+[a-z][A-Z][a-z]+'
   #1: AccXrCpwUjAvi/HMR/2FvoCaIKuTaAALgIgw
|   r' [A-Z][a-z]+[A-Z][0-9][A-Z]+[0-9][a-z][A-Z][a-z][A-Z]+[a-z][A-Z][0-9][A-Z][a-z][A-Z][a-z][0-9][A-Z]+[0-9][a-z]+[A-Z]+[0-9]'
   #1: AccX1HFT7mXxXKMqQ4WfYy2XVAP9zwACDWR8
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def From:: yield from (
    r' "[A-Z][a-z]+ [A-Z][a-z]+" <[A-Z][a-z]+\.[A-Z][a-z]+@[a-z]+\.[a-z]+>'
   #1: "Ken Moses" <Ken.Moses@quest.com>
   #1: "Lisa Radford" <Lisa.Radford@quest.com>
   #1: "Keren Kamilian" <Keren.Kamilian@quest.com>
|   r' "[A-Z][a-z]+ [A-Z][a-z]+" <[a-z]+\.[a-z]+@[a-z]+\.[a-z]+>'
   #1: "Pat Luis" <pat.luis@quest.com>
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def To:: yield from (
    r' "[A-Z][a-z]+ [A-Z][a-z]+" <[a-z]+@[a-z]+\.[a-z]+>'
   #2: "Lon Cherryholmes" <lcherryh@yahoo.com>
|   r' <[a-z]+@[a-z]+\.[a-z]+>'
   #1: <lcherryh@yahoo.com>
|   r' "[A-Z][a-z]+ [A-Z][a-z]+" <[a-z]+\.[a-z]+@[a-z]+\.[a-z]+>'
   #1: "Pat Luis" <pat.luis@quest.com>
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_OriginalArrivalTime:: yield from (
    r' [0-9]+ [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+\.[0-9]+ \([A-Z]+\) [A-Z]+=\[[0-9][A-Z][0-9][A-Z]+[0-9]+:[0-9]+[A-Z][0-9]+[A-Z]+\]'
   #1: 04 Dec 2006 13:51:56.0083 (UTC) FILETIME=[5C6CD030:01C717AB]
|   r' [0-9]+ [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+\.[0-9]+ \([A-Z]+\) [A-Z]+=\[[0-9]+[A-Z][0-9]+:[0-9]+[A-Z][0-9]+[A-Z][0-9]\]'
   #1: 04 Dec 2006 18:46:00.0912 (UTC) FILETIME=[71900D00:01C717D4]
|   r' [0-9]+ [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+\.[0-9]+ \([A-Z]+\) [A-Z]+=\[[0-9]+[A-Z]+[0-9]+[A-Z][0-9]:[0-9]+[A-Z][0-9]+[A-Z]+\]'
   #1: 04 Dec 2006 19:27:36.0302 (UTC) FILETIME=[40EE58E0:01C717DA]
|   r' [0-9]+ [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+\.[0-9]+ \([A-Z]+\) [A-Z]+=\[[0-9][A-Z]+[0-9]+[A-Z][0-9]+:[0-9]+[A-Z][0-9]+[A-Z]+\]'
   #1: 04 Dec 2006 19:55:17.0081 (UTC) FILETIME=[1ED51C90:01C717DE]
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def Content_Length:: yield from (
    r' [0-9]+'
   #1: 1150
   #1: 7937
   #1: 6054
   #1: 8406
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def Cc:: yield from (
    r' "[A-Z][a-z]+ [A-Z][a-z]+" <[A-Z][a-z]+\.[A-Z][a-z]+@[a-z]+\.[a-z]+>,\n\t"[A-Z][a-z]+ [A-Z][a-z]+" <[A-Z][a-z]+\.[A-Z][a-z]+@[a-z]+\.[a-z]+>'
   #1: "Ken Moses" <Ken.Moses@quest.com>,{bslash}n	"Keren Kamilian" <Keren.Kamilian@quest.com>
|   r' "[A-Z][a-z]+ [A-Z][a-z]+" <[A-Z][a-z]+\.[A-Z][a-z]+@[a-z]+\.[a-z]+>'
   #1: "Mark Wright" <Mark.Wright@quest.com>
|   r' "[A-Z][a-z]+ [A-Z][a-z]+" <[A-Z][a-z]+\.[A-Z][a-z]+@[a-z]+\.[a-z]+>,\n\t"[a-z]+@[a-z]+\.[a-z]+" <'[a-z]+@[a-z]+\.[a-z]+'>'
   #1: "Ken Moses" <Ken.Moses@quest.com>,{bslash}n	"lcherryh@yahoo.com" <'lcherryh@yahoo.com'>
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def In_Reply_To:: yield from (
    r' <[0-9]+\.[0-9]+\.[a-z]+@[a-z]+[0-9]+\.[a-z]+\.[a-z]+[0-9]\.[a-z]+\.[a-z]+>'
   #1: <721514.94331.qm@web59106.mail.re1.yahoo.com>
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def References:: yield from (
    r' <[A-Z]+[0-9]+[A-Z][0-9]+[A-Z][0-9]+[A-Z]+[0-9]+[A-Z][0-9][A-Z][0-9][A-Z]+[0-9][A-Z][0-9]+[A-Z]+[0-9][A-Z][0-9]@[a-z]+[0-9]+\.[a-z]+\.[a-z]+\.[a-z]+>'
   #1: <FA13712B13469646A618BC95F7E1BA8F01ABD6E9@alvmbxw01.prod.quest.corp>
)
{'φ(From_rex) + η()\n + X_Account_Key() + η()\n + X_UIDL() + η()\n + X_Mozilla_Status() + η()\n + X_Mozilla_Status2() + η()\n + X_Mozilla_Keys() + η()\n + X_Apparently_To() + η()\n + X_Originating_IP() + η()\n + Return_Path() + η()\n + Authentication_Results() + η()\n + Received() + η()\n + Received() + η()\n + Received() + η()\n + X_MimeOLE() + η()\n + Content_class() + η()\n + MIME_Version() + η()\n + Content_Type() + η()\n + Subject() + η()\n + Date() + η()\n + Message_ID() + η()\n + X_MS_Has_Attach() + η()\n + X_MS_TNEF_Correlator() + η()\n + Thread_Topic() + η()\n + Thread_Index() + η()\n + References() + η()\n + From() + η()\n + To() + η()\n + Cc() + η()\n + Return_Path() + η()\n + X_OriginalArrivalTime() + η()\n + Content_Length() + η()\n': 1,
 'φ(From_rex) + η()\n + X_Account_Key() + η()\n + X_UIDL() + η()\n + X_Mozilla_Status() + η()\n + X_Mozilla_Status2() + η()\n + X_Mozilla_Keys() + η()\n + X_Apparently_To() + η()\n + X_Originating_IP() + η()\n + Return_Path() + η()\n + Authentication_Results() + η()\n + Received() + η()\n + Received() + η()\n + X_MimeOLE() + η()\n + Content_class() + η()\n + MIME_Version() + η()\n + Content_Type() + η()\n + Subject() + η()\n + Date() + η()\n + Message_ID() + η()\n + In_Reply_To() + η()\n + X_MS_Has_Attach() + η()\n + X_MS_TNEF_Correlator() + η()\n + Thread_Topic() + η()\n + Thread_Index() + η()\n + From() + η()\n + To() + η()\n + Cc() + η()\n + Return_Path() + η()\n + X_OriginalArrivalTime() + η()\n + Content_Length() + η()\n': 1,
 'φ(From_rex) + η()\n + X_Account_Key() + η()\n + X_UIDL() + η()\n + X_Mozilla_Status() + η()\n + X_Mozilla_Status2() + η()\n + X_Mozilla_Keys() + η()\n + X_Apparently_To() + η()\n + X_Originating_IP() + η()\n + Return_Path() + η()\n + Authentication_Results() + η()\n + Received() + η()\n + Received() + η()\n + X_MimeOLE() + η()\n + Content_class() + η()\n + MIME_Version() + η()\n + Content_Type() + η()\n + Subject() + η()\n + Date() + η()\n + Message_ID() + η()\n + X_MS_Has_Attach() + η()\n + X_MS_TNEF_Correlator() + η()\n + Thread_Topic() + η()\n + Thread_Index() + η()\n + From() + η()\n + To() + η()\n + Cc() + η()\n + Return_Path() + η()\n + X_OriginalArrivalTime() + η()\n + Content_Length() + η()\n': 1,
 'φ(From_rex) + η()\n + X_Account_Key() + η()\n + X_UIDL() + η()\n + X_Mozilla_Status() + η()\n + X_Mozilla_Status2() + η()\n + X_Mozilla_Keys() + η()\n + X_Apparently_To() + η()\n + X_Originating_IP() + η()\n + Return_Path() + η()\n + Authentication_Results() + η()\n + Received() + η()\n + Received() + η()\n + X_MimeOLE() + η()\n + Content_class() + η()\n + MIME_Version() + η()\n + Content_Type() + η()\n + Subject() + η()\n + Date() + η()\n + Message_ID() + η()\n + X_MS_Has_Attach() + η()\n + X_MS_TNEF_Correlator() + η()\n + Thread_Topic() + η()\n + Thread_Index() + η()\n + From() + η()\n + To() + η()\n + Return_Path() + η()\n + X_OriginalArrivalTime() + η()\n + Content_Length() + η()\n': 1}
