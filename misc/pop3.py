# Reading inbox. 901205028 bytes.
# Scanning lines. 12976894 lines.
# Scanning sections. 8259 sections.
# Parsing emails.

# From - Thu Feb 20 20:43:02 2025
# From - Thu Feb 20 20:43:02 2025
# From - Thu Feb 20 20:43:02 2025
# From - Thu Feb 20 20:43:03 2025
# From - Thu Feb 20 20:43:03 2025
# From - Thu Feb 20 20:43:04 2025
# From - Thu Feb 20 20:43:04 2025
# From - Thu Feb 20 20:43:05 2025
# From - Thu Feb 20 20:43:05 2025
# From - Thu Feb 20 20:43:07 2025
# From - Thu Feb 20 20:43:08 2025
# From - Thu Feb 20 20:43:08 2025
# From - Thu Feb 20 20:43:09 2025
# From - Thu Feb 20 20:43:09 2025
# From - Thu Feb 20 20:43:10 2025
# From - Thu Feb 20 20:43:10 2025
# From - Thu Feb 20 20:43:10 2025
# From - Thu Feb 20 20:43:11 2025
# From - Thu Feb 20 20:43:11 2025
# From - Thu Feb 20 20:43:12 2025
# From - Thu Feb 20 20:43:12 2025
# From - Thu Feb 20 20:43:14 2025
# From - Thu Feb 20 20:43:15 2025
# From - Thu Feb 20 20:43:15 2025
# From - Thu Feb 20 20:43:16 2025
# From - Thu Feb 20 20:43:16 2025
# From - Thu Feb 20 20:43:17 2025
# From - Thu Feb 20 20:43:18 2025
# From - Thu Feb 20 20:43:18 2025
# From - Thu Feb 20 20:43:19 2025
# From - Thu Feb 20 20:43:19 2025
# From - Thu Feb 20 20:43:19 2025
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def Accept_Language(): yield from (
    φ(r'<[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}>')
     #1:<E52BA26B1940E24FAF1E0BD9F876E23847F2D468@UKBXMBW01.prod.quest.corp>
     #1:<E52BA26B1940E24FAF1E0BD9F876E23847F2D4BE@UKBXMBW01.prod.quest.corp>
     #1:<E52BA26B1940E24FAF1E0BD9F876E23847F2D4BF@UKBXMBW01.prod.quest.corp>
     #1:<E52BA26B1940E24FAF1E0BD9F876E23847F2D4C1@UKBXMBW01.prod.quest.corp>
     #1:<65BB6DF6A76DAF4984F1B08936F2FC34A68B2119@UKBXMBW01.prod.quest.corp>
     #1:<65BB6DF6A76DAF4984F1B08936F2FC34A6B4B6D5@UKBXMBW01.prod.quest.corp>
|   φ(r'\ en\-US')
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def Authentication_Results(): yield from (
    φ(r'(?:(?:[A-Za-z0-9-]+\\.)+[A-Za-z]{2,}|localhost|(?:\d{1,3}\\.){3}\d{1,3})[ ]{2}[a-z]{4}=(?:(?:[A-Za-z0-9-]+\\.)+[A-Za-z]{2,}|localhost|(?:\d{1,3}\\.){3}\d{1,3}); [a-z]{10}=[a-z]{7} \([a-z]{2} [a-z]{3}\)')
     #1:mta526.mail.mud.yahoo.com  from=quest.com; domainkeys=neutral (no sig)
     #1:mta188.mail.re3.yahoo.com  from=quest.com; domainkeys=neutral (no sig)
     #1:mta224.mail.re4.yahoo.com  from=quest.com; domainkeys=neutral (no sig)
     #1:mta368.mail.re4.yahoo.com  from=quest.com; domainkeys=neutral (no sig)
     #1:mta305.mail.re4.yahoo.com  from=quest.com; domainkeys=neutral (no sig)
     #1:mta179.mail.re4.yahoo.com  from=VentiSolutions.com; domainkeys=neutral (no sig)
     #1:mta416.mail.mud.yahoo.com  from=austin.rr.com; domainkeys=neutral (no sig)
     #1:mta191.mail.re3.yahoo.com  from=database-brothers.com; domainkeys=neutral (no sig)
     #1:mta199.mail.re4.yahoo.com  from=quest.com; domainkeys=neutral (no sig)
     #1:mta312.mail.mud.yahoo.com  from=quest.com; domainkeys=neutral (no sig)
     #2:mta303.mail.mud.yahoo.com  from=quest.com; domainkeys=neutral (no sig)
     #1:mta219.mail.mud.yahoo.com  from=quest.com; domainkeys=neutral (no sig)
     #1:mta233.mail.re4.yahoo.com  from=hotmail.com; domainkeys=neutral (no sig)
     #1:mta253.mail.mud.yahoo.com  from=hotmail.com; domainkeys=neutral (no sig)
     #1:mta203.mail.mud.yahoo.com  from=hotmail.com; domainkeys=neutral (no sig)
     #1:mta186.mail.re4.yahoo.com  from=quest.com; domainkeys=neutral (no sig)
     #1:mta188.mail.mud.yahoo.com  from=alcoa.com; domainkeys=neutral (no sig)
     #1:mta268.mail.re4.yahoo.com  from=austin.rr.com; domainkeys=neutral (no sig)
     #1:mta243.mail.re4.yahoo.com  from=riverranchradiology.com; domainkeys=neutral (no sig)
     #1:mta544.mail.mud.yahoo.com  from=peoplepc.com; domainkeys=neutral (no sig)
     #1:mta173.mail.re2.yahoo.com  from=austin.rr.com; domainkeys=neutral (no sig)
     #1:mta294.mail.re4.yahoo.com  from=mw-ar.com; domainkeys=neutral (no sig)
     #1:mta215.mail.mud.yahoo.com  from=aol.com; domainkeys=neutral (no sig)
|   φ(r'(?:(?:[A-Za-z0-9-]+\\.)+[A-Za-z]{2,}|localhost|(?:\d{1,3}\\.){3}\d{1,3})[ ]{2}[a-z]{4}=(?:(?:[A-Za-z0-9-]+\\.)+[A-Za-z]{2,}|localhost|(?:\d{1,3}\\.){3}\d{1,3}); [a-z]{10}=[a-z]{4} \([a-z]{2}\)')
     #1:mta243.mail.re4.yahoo.com  from=yahoogroups.com; domainkeys=pass (ok)
     #1:mta234.mail.re3.yahoo.com  from=yahoo.com; domainkeys=pass (ok)
     #1:mta233.mail.mud.yahoo.com  from=yahoo.com; domainkeys=pass (ok)
     #1:mta499.mail.mud.yahoo.com  from=yahoo.com; domainkeys=pass (ok)
     #1:mta352.mail.mud.yahoo.com  from=yahoo.com; domainkeys=pass (ok)
     #1:mta159.mail.re4.yahoo.com  from=yahoo.com; domainkeys=pass (ok)
     #1:mta230.mail.re4.yahoo.com  from=yahoo.com; domainkeys=pass (ok)
     #1:mta500.mail.mud.yahoo.com  from=yahoo.com; domainkeys=pass (ok)
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def Cc(): yield from (
    φ(r'"[A-Z][a-z]{2} [A-Z][a-z]{4}" <(?:(?:[A-Za-z0-9-]+\\.)+[A-Za-z]{2,}|localhost|(?:\d{1,3}\\.){3}\d{1,3})@(?:(?:[A-Za-z0-9-]+\\.)+[A-Za-z]{2,}|localhost|(?:\d{1,3}\\.){3}\d{1,3})>,\n\t"[A-Z][a-z]{4} [A-Z][a-z]{7}" <(?:(?:[A-Za-z0-9-]+\\.)+[A-Za-z]{2,}|localhost|(?:\d{1,3}\\.){3}\d{1,3})@(?:(?:[A-Za-z0-9-]+\\.)+[A-Za-z]{2,}|localhost|(?:\d{1,3}\\.){3}\d{1,3})>')
     #1:"Ken Moses" <Ken.Moses@quest.com>,\n	"Keren Kamilian" <Keren.Kamilian@quest.com>
|   φ(r'"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z] [A-Z][a-z]{5}" <(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)(?:(?:[A-Za-z0-9-]+\\.)+[A-Za-z]{2,}|localhost|(?:\d{1,3}\\.){3}\d{1,3})@(?:(?:[A-Za-z0-9-]+\\.)+[A-Za-z]{2,}|localhost|(?:\d{1,3}\\.){3}\d{1,3})>')
     #1:"Mark Wright" <Mark.Wright@quest.com>
|   φ(r'"[A-Z][a-z]{2} [A-Z][a-z]{4}" <(?:(?:[A-Za-z0-9-]+\\.)+[A-Za-z]{2,}|localhost|(?:\d{1,3}\\.){3}\d{1,3})@(?:(?:[A-Za-z0-9-]+\\.)+[A-Za-z]{2,}|localhost|(?:\d{1,3}\\.){3}\d{1,3})>,\n\t"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}" <\'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}\'>')
     #1:"Ken Moses" <Ken.Moses@quest.com>,\n	"lcherryh@yahoo.com" <'lcherryh@yahoo.com'>
|   φ(r'"[A-Z][a-z]{4} [A-Z][a-z]{5} \- [A-Z][a-z]{4} [A-Z][a-z]{4} [A-Z][a-z]{8}" <[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}>')
     #1:"Angie Garcia - River Ranch Radiology" <agarcia@riverranchradiology.com>
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def Comment(): yield from (
    φ(r'[A-Z][a-z]{5}[A-Z][a-z]{3}\? [A-Z][a-z]{2} (?:(?:https?|ftp)://)(?:\S+(?::\S*)?@)?(?:(?:[A-Za-z0-9-]+\\.)+[A-Za-z]{2,}|localhost|(?:\d{1,3}\\.){3}\d{1,3})(?::\d+)?(?:/\S*)?')
     #1:DomainKeys? See http://antispam.yahoo.com/domainkeys
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def Content_Language(): yield from (
    φ(r'<[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}>')
     #1:<E52BA26B1940E24FAF1E0BD9F876E23847F2D468@UKBXMBW01.prod.quest.corp>
     #1:<E52BA26B1940E24FAF1E0BD9F876E23847F2D4BE@UKBXMBW01.prod.quest.corp>
     #1:<E52BA26B1940E24FAF1E0BD9F876E23847F2D4BF@UKBXMBW01.prod.quest.corp>
     #1:<E52BA26B1940E24FAF1E0BD9F876E23847F2D4C1@UKBXMBW01.prod.quest.corp>
     #1:<65BB6DF6A76DAF4984F1B08936F2FC34A68B2119@UKBXMBW01.prod.quest.corp>
     #1:<65BB6DF6A76DAF4984F1B08936F2FC34A6B4B6D5@UKBXMBW01.prod.quest.corp>
|   φ(r'\ en\-US')
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def Content_Length(): yield from (
    φ(r'1150')
|   φ(r'7937')
|   φ(r'6054')
|   φ(r'8406')
|   φ(r'5286')
|   φ(r'286450')
|   φ(r'7732')
|   φ(r'1216')
|   φ(r'18240')
|   φ(r'3275573')
|   φ(r'16011')
|   φ(r'10432')
|   φ(r'19338')
|   φ(r'6492')
|   φ(r'1672')
|   φ(r'2749')
|   φ(r'2285')
|   φ(r'2308')
|   φ(r'3094')
|   φ(r'1256')
|   φ(r'5341')
|   φ(r'5368575')
|   φ(r'1562')
|   φ(r'130401')
|   φ(r'193837')
|   φ(r'2595')
|   φ(r'3889')
|   φ(r'602608')
|   φ(r'1971')
|   φ(r'1858')
|   φ(r'5492')
|   φ(r'9145')
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def Content_Transfer_Encoding(): yield from (
    φ(r'7bit')
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def Content_Type(): yield from (
    φ(r'multipart/mixed;\n\ \ boundary="PytmzYxs55LzQoiEiE\-9nUgfn6JY6oCyUsXFY9Y"')
|   φ(r'multipart/mixed;\n\tboundary="\-\-\-\-_=_NextPart_001_01C7E8C6\.62989397"')
|   φ(r'multipart/alternative;\n\tboundary="\-\-\-\-=_NextPart_000_007D_01C7EF12\.9C5AE1C0"')
|   φ(r'multipart/alternative;\n\tboundary="\-\-\-\-=_NextPart_000_02C9_01C7F830\.FDE88060"')
|   φ(r'multipart/related;\n\tboundary="\-\-\-\-=_NextPart_000_0055_01C81248\.792D0D00"')
|   φ(r'multipart/mixed;\n\tboundary="_004_E52BA26B1940E24FAF1E0BD9F876E23847F2D468UKBXMBW01prodqu_"')
|   φ(r'multipart/alternative;\n\tboundary="_000_E52BA26B1940E24FAF1E0BD9F876E23847F2D4BEUKBXMBW01prodqu_"')
|   φ(r'multipart/alternative;\n\tboundary="_000_E52BA26B1940E24FAF1E0BD9F876E23847F2D4BFUKBXMBW01prodqu_"')
|   φ(r'multipart/alternative;\n\tboundary="_000_E52BA26B1940E24FAF1E0BD9F876E23847F2D4C1UKBXMBW01prodqu_"')
|   φ(r'multipart/alternative;\n\tboundary="_000_65BB6DF6A76DAF4984F1B08936F2FC34A68B2119UKBXMBW01prodqu_"')
|   φ(r'multipart/alternative;\n\tboundary="_064391a5\-c6c4\-496d\-b5d3\-d646e45f8071_"')
|   φ(r'multipart/mixed;\ boundary="0\-169234684\-1199209661=:95298"\nContent\-Transfer\-Encoding:\ 8bit')
|   φ(r'multipart/alternative;\n\tboundary="_e71c60b7\-934e\-495d\-8ca5\-68d022d0756b_"')
|   φ(r'multipart/alternative;\ boundary="0\-1690936920\-1199262114=:23902"\nContent\-Transfer\-Encoding:\ 8bit')
|   φ(r'multipart/mixed;\ boundary="0\-1242512665\-1199285010=:51156"\nContent\-Transfer\-Encoding:\ 8bit')
|   φ(r'multipart/alternative;\n\tboundary="_05c4e171\-16e4\-433e\-b2a4\-4f1cce49c8a5_"')
|   φ(r'multipart/mixed;\ boundary="0\-1957197243\-1199790550=:98701"\nContent\-Transfer\-Encoding:\ 8bit')
|   φ(r'multipart/mixed;\n\tboundary="_005_65BB6DF6A76DAF4984F1B08936F2FC34A6B4B6D5UKBXMBW01prodqu_"')
|   φ(r'multipart/alternative;\ boundary="0\-1728457870\-1199890176=:36147"\nContent\-Transfer\-Encoding:\ 8bit')
|   φ(r'multipart/mixed;\ boundary="0\-237260743\-1199989036=:89358"\nContent\-Transfer\-Encoding:\ 8bit')
|   φ(r'multipart/mixed;\n\tboundary="\-\-\-\-_=_NextPart_001_01C85598\.D0B82877"')
|   φ(r'multipart/alternative;\n\tboundary="\-\-\-\-=_NextPart_000_003F_01C8568B\.A7A9DFF0"')
|   φ(r'multipart/mixed;\ boundary="0\-282327629\-1200330844=:6022"\nContent\-Transfer\-Encoding:\ 8bit')
|   φ(r'multipart/mixed;\n\tboundary="\-\-\-\-_=_NextPart_001_01C856F1\.CAFCB0E2"')
|   φ(r'multipart/alternative;\n\tboundary="\-\-\-\-=_NextPart_000_0024_01C8574E\.8A6FD6B0"')
|   φ(r'multipart/alternative;\n\tboundary="\-\-\-\-=_NextPart_000_00BC_01C8577E\.C8509840"')
|   φ(r'multipart/alternative;\n\tboundary="\-\-\-\-=_NextPart_000_015F_01C857CE\.43B00DF0"')
|   φ(r'multipart/alternative;\ boundary="\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-1200488544"\nX\-Mailer:\ 9\.0\ SE\ for\ Windows\ sub\ 5004')
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def Date(): yield from (
    φ(r'(Sun|Mon|Tue|Wed|Thu|Fri|Sat), [0-9] (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2} \+[0-9]{4}')
     #1:Mon, 4 Dec 2006 21:51:55 +0800
     #1:Wed, 9 Jan 2008 11:30:43 +0000
|   φ(r'(Sun|Mon|Tue|Wed|Thu|Fri|Sat), [0-9] (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2} \-[0-9]{4}')
     #1:Mon, 4 Dec 2006 10:46:00 -0800
     #1:Mon, 4 Dec 2006 11:27:33 -0800
     #1:Mon, 4 Dec 2006 19:55:13 -0000
     #1:Tue, 4 Sep 2007 16:42:31 -0600
     #1:Tue, 1 Jan 2008 19:00:50 -0600
     #1:Thu, 3 Jan 2008 19:25:27 -0600
|   φ(r'[0-9] (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2} \-[0-9]{4}')
     #1:6 May 2007 13:14:56 -0000
|   φ(r'(Sun|Mon|Tue|Wed|Thu|Fri|Sat), [0-9]{2} (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2} \-[0-9]{4}')
     #1:Mon, 27 Aug 2007 09:20:57 -0700
     #1:Sun, 16 Sep 2007 07:12:50 -0500
     #1:Fri, 19 Oct 2007 12:06:25 -0500
     #1:Sun, 30 Dec 2007 17:56:16 -0600
     #1:Sat, 12 Jan 2008 23:00:19 -0500
     #1:Mon, 14 Jan 2008 08:58:39 -0600
     #1:Mon, 14 Jan 2008 15:09:47 -0600
     #1:Tue, 15 Jan 2008 08:13:42 -0600
     #1:Tue, 15 Jan 2008 13:59:01 -0600
     #1:Tue, 15 Jan 2008 23:27:59 -0600
|   φ(r'(Sun|Mon|Tue|Wed|Thu|Fri|Sat), [0-9]{2} (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2} \+[0-9]{4}')
     #1:Thu, 27 Dec 2007 13:48:30 +0000
     #1:Thu, 27 Dec 2007 14:09:12 +0000
     #1:Thu, 27 Dec 2007 14:09:22 +0000
     #1:Thu, 27 Dec 2007 14:09:46 +0000
     #1:Thu, 27 Dec 2007 16:35:15 +0000
|   φ(r'(Sun|Mon|Tue|Wed|Thu|Fri|Sat), [0-9] (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2} -[0-9]{4} \([A-Z]{3}\)')
     #1:Tue, 1 Jan 2008 09:47:41 -0800 (PST)
     #1:Wed, 2 Jan 2008 00:21:54 -0800 (PST)
     #1:Wed, 2 Jan 2008 06:43:30 -0800 (PST)
     #1:Tue, 8 Jan 2008 03:09:10 -0800 (PST)
     #1:Wed, 9 Jan 2008 06:49:36 -0800 (PST)
|   φ(r'(Sun|Mon|Tue|Wed|Thu|Fri|Sat), [0-9]{2} (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2} -[0-9]{4} \([A-Z]{3}\)')
     #1:Thu, 10 Jan 2008 10:17:16 -0800 (PST)
     #1:Mon, 14 Jan 2008 09:14:04 -0800 (PST)
|   φ(r'(Sun|Mon|Tue|Wed|Thu|Fri|Sat), [0-9]{2} (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2} [A-Z]{3}')
     #1:Wed, 16 Jan 2008 08:02:24 EST
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def DomainKey_Signature(): yield from (
    φ(r'[a-z]=[a-z]{3}\-[a-z]{3}[0-9]; [a-z]=[a-z]{3}; [a-z]=[a-z]{5}; [a-z]=[a-z]{4}; [a-z]=(?:(?:[A-Za-z0-9-]+\\.)+[A-Za-z]{2,}|localhost|(?:\d{1,3}\\.){3}\d{1,3});\n\t[a-z]=[a-z]{3}[0-9][a-z][A-Z][a-z]{2}[A-Z]{2}[a-z]{2}[0-9][a-z][0-9]\+[A-Z]{5}[a-z]{4}[A-Z][a-z][A-Z][0-9][A-Z]{2}[a-z][A-Z]{2}[0-9][A-Z][a-z]/[A-Z]{4}[a-z]{3}[A-Z]{2}[0-9][a-z][0-9][a-z][A-Z][0-9][A-Z]{2}[a-z][A-Z][a-z][A-Z]{6}[a-z]{3}[A-Z]{2}/[A-Z]{2}[a-z]{6}[A-Z]/[a-z][0-9]{2}[a-z][A-Z][a-z][A-Z][a-z][A-Z][a-z][A-Z]{3}[a-z]{2}/[A-Z]{2}[a-z][A-Z][a-z]{2}[A-Z][0-9][A-Z][a-z][A-Z][a-z]\+[A-Z]{2}[0-9][A-Z][a-z][A-Z]{2}\+[a-z]{3}[0-9]{3}[A-Z][a-z][0-9][a-z][A-Z];')
     #1:a=rsa-sha1; q=dns; c=nofws; s=lima; d=yahoogroups.com;\n	b=nce6rTvfJLmw6r7+SDFNRbllvIiA8ZMhRY0Hj/XSTWwxkPG1z0lS3OHfTlVSRJLKtxwEE/HLdaoimnN/d19uSvWuKmSZLwt/JTfWwoO8SgSw+RD6HaXY+wkf196Vz2dP;
|   φ(r'[a-z]=[a-z]{3}\-[a-z]{3}[0-9]; [a-z]=[a-z]{3}; [a-z]=[a-z]{5};\n[ ]{2}[a-z]=[a-z][0-9]{4}; [a-z]=(?:(?:[A-Za-z0-9-]+\\.)+[A-Za-z]{2,}|localhost|(?:\d{1,3}\\.){3}\d{1,3});')
     #7:a=rsa-sha1; q=dns; c=nofws;\n  s=s1024; d=yahoo.com;
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def From(): yield from (
    φ(r'"Ken\ Moses"\ <Ken\.Moses@quest\.com>')
|   φ(r'"Pat\ Luis"\ <pat\.luis@quest\.com>')
|   φ(r'"Lisa\ Radford"\ <Lisa\.Radford@quest\.com>')
|   φ(r'"Keren\ Kamilian"\ <Keren\.Kamilian@quest\.com>')
|   φ(r'Yahoo!\ Groups\ <notify@yahoogroups\.com>')
|   φ(r'"Lon\ Cherryholmes"\ <Lon\.Cherryholmes@quest\.com>')
|   φ(r'"Tony\ DeLollis"\ <Tony\.DeLollis@VentiSolutions\.com>')
|   φ(r'"Rusty\ Bullerman"\ <rbullerman@austin\.rr\.com>')
|   φ(r'"Jeff\ Omo"\ <jeff\.omo@database\-brothers\.com>')
|   φ(r'Lon\ Cherryholmes\ <Lon\.Cherryholmes@quest\.com>')
|   φ(r'Adi\ Izhar\ <adi\.izhar@quest\.com>')
|   φ(r'Leslie\ Cherryholmes\ <lesliecherryholmes@hotmail\.com>')
|   φ(r'"Lon\ T\.\ Cherryholmes"\ <ness_78759@yahoo\.com>')
|   φ(r'Lon\ Cherryholmes\ <lcherryh@yahoo\.com>')
|   φ(r'"Sheets,\ Chris\ A\ \\\(T\&K\\\)"\ <Chris\.Sheets@alcoa\.com>')
|   φ(r'"DeAtley\ Tile\ \&\ Stone"\ <tdeatley@austin\.rr\.com>')
|   φ(r'"Becky\ Thompson\ \ \-\ River\ Ranch\ Radiology"\ <bthompson@riverranchradiology\.com>')
|   φ(r'"Elizabeth\ Flowers"\ <shalomyaall@peoplepc\.com>')
|   φ(r'"midwest\ auto\ recycling"\ <parts@mw\-ar\.com>')
|   φ(r'CMONEYMAKER72@aol\.com')
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def In_Reply_To(): yield from (
    φ(r'<(?:(?:[A-Za-z0-9-]+\\.)+[A-Za-z]{2,}|localhost|(?:\d{1,3}\\.){3}\d{1,3})@(?:(?:[A-Za-z0-9-]+\\.)+[A-Za-z]{2,}|localhost|(?:\d{1,3}\\.){3}\d{1,3})>')
     #1:<721514.94331.qm@web59106.mail.re1.yahoo.com>
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def Message_ID(): yield from (
    φ(r'<[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}>')
     #1:<78CD474EB76D9C4C9E8F03720184A36B0B5BCBF2@ALVMBXW02.prod.quest.corp>
     #1:<FA13712B13469646A618BC95F7E1BA8F01ABD6E9@alvmbxw01.prod.quest.corp>
     #1:<81B3912B246E23449049CFA9C12D04F6036620A7@alvmbxw01.prod.quest.corp>
     #1:<E61E658006418E47861A484DE76F4FC507310D8B@ukbmbxw01.prod.quest.corp>
     #1:<1178457296.118.80517.m48@yahoogroups.com>
     #1:<23D8DB429EF0494783E86044C51F865903DB9CEB@ALVMBXW02.prod.quest.corp>
     #1:<E52BA26B1940E24FAF1E0BD9F876E23847F2D468@UKBXMBW01.prod.quest.corp>
     #1:<E52BA26B1940E24FAF1E0BD9F876E23847F2D4BE@UKBXMBW01.prod.quest.corp>
     #1:<E52BA26B1940E24FAF1E0BD9F876E23847F2D4BF@UKBXMBW01.prod.quest.corp>
     #1:<E52BA26B1940E24FAF1E0BD9F876E23847F2D4C1@UKBXMBW01.prod.quest.corp>
     #1:<65BB6DF6A76DAF4984F1B08936F2FC34A68B2119@UKBXMBW01.prod.quest.corp>
     #1:<BAY124-W3489E28ECAB87E6AF5089AD2570@phx.gbl>
     #1:<BAY124-W459446EDB4502DFA58F5CD2520@phx.gbl>
     #1:<BAY124-W746E761573BD76BDEF3EED24C0@phx.gbl>
     #1:<65BB6DF6A76DAF4984F1B08936F2FC34A6B4B6D5@UKBXMBW01.prod.quest.corp>
     #1:<9BDA6601615804418B799762F41EA1D7021D166D@NOANDC-MXU24.NOA.Alcoa.com>
     #1:<B9307879C62717418BD7CB1FF0E256730315BB29@server.RiverRanchRadiology.local>
     #1:<bcd.1d0cad8e.34bf5a60@aol.com>
|   φ(r'<[0-9]{3}[a-z][0-9]{2}[a-z][0-9][a-z]{2}[0-9]{2}\$[a-z][0-9][a-z][0-9]{3}[a-z][0-9]\$[0-9]{4}[a-z][0-9][a-z][0-9]@[A-Z][a-z]{4}[A-Z]{2}>')
     #1:<007c01c7ef44$e6f551c0$6501a8c0@VentiRD>
|   φ(r'<[0-9]{2}[A-Z][0-9]{5}[A-Z][0-9][A-Z]{2}[0-9]{3}[A-Z]{3}[0-9]{3}[A-Z][0-9][A-Z][0-9][A-Z][0-9]{2}[A-Z][0-9]{3}@[a-z]{5}[A-Z]{2}>')
     #1:<07E41628A4DA494AAA597D2D0C85A834@ownerPC>
|   φ(r'<[0-9]{6}[a-z][0-9]{5}\$[0-9]{8}\$[a-z]{2}[0-9][a-z][0-9]{2}[a-z]{2}@[a-z]{10}>')
     #1:<005401c81272$62031500$ea0a14ac@jomolaptop>
|   φ(r'<(?:(?:[A-Za-z0-9-]+\\.)+[A-Za-z]{2,}|localhost|(?:\d{1,3}\\.){3}\d{1,3})@(?:(?:[A-Za-z0-9-]+\\.)+[A-Za-z]{2,}|localhost|(?:\d{1,3}\\.){3}\d{1,3})>')
     #1:<851320.95298.qm@web52611.mail.re2.yahoo.com>
     #1:<600240.23902.qm@web52601.mail.re2.yahoo.com>
     #1:<364748.51156.qm@web52604.mail.re2.yahoo.com>
     #1:<482054.98701.qm@web52605.mail.re2.yahoo.com>
     #1:<659587.36147.qm@web52610.mail.re2.yahoo.com>
     #1:<454556.89358.qm@web59107.mail.re1.yahoo.com>
     #1:<467603.6022.qm@web52605.mail.re2.yahoo.com>
|   φ(r'<[0-9]{6}[a-z][0-9]{3}[a-z]{2}\$[a-z][0-9][a-z]{3}[0-9][a-z][0-9]\$[a-z][0-9]{7}@[A-Z][a-z][A-Z][a-z]{4}[A-Z][a-z]{4}>')
     #1:<004201c856bd$f2aad9f0$a9557046@DeAtleyFloor>
|   φ(r'<[0-9]{6}[a-z][0-9]{5}\$[a-z][0-9]{5}[a-z][0-9]\$[0-9][a-z][0-9]{2}[a-z][0-9]{3}@[a-z]{4}[0-9]{2}[a-z][0-9]{4}[a-z][0-9]{2}>')
     #1:<002701c85780$d64510a0$7d90e604@your27e1513d96>
|   φ(r'<[0-9]{2}[a-z]{2}[0-9]{2}[a-z][0-9]{3}[a-z][0-9]\$[0-9]{8}\$[a-z][0-9]{7}@[A-Z][a-z][A-Z][a-z]{4}[A-Z][a-z]{4}>')
     #1:<00bf01c857b1$13458450$a9557046@DeAtleyFloor>
|   φ(r'<[0-9]{6}[a-z][0-9]{5}\$[0-9][a-z][0-9][a-z]{2}[0-9]{3}\$[0-9]{4}[a-z][0-9][a-z][0-9]@[A-Z]{6}[0-9][A-Z][0-9][A-Z][0-9][A-Z]{3}>')
     #1:<016401c85800$8e8ae250$6701a8c0@VALUED2D4C2DDC>
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def References(): yield from (
    φ(r'<[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}>')
     #1:<FA13712B13469646A618BC95F7E1BA8F01ABD6E9@alvmbxw01.prod.quest.corp>
|   φ(r'<(?:(?:[A-Za-z0-9-]+\\.)+[A-Za-z]{2,}|localhost|(?:\d{1,3}\\.){3}\d{1,3})@(?:(?:[A-Za-z0-9-]+\\.)+[A-Za-z]{2,}|localhost|(?:\d{1,3}\\.){3}\d{1,3})>')
     #1:<20080116033202.6569.qmail@outbound.qualityautoparts.com>
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def Reply_To(): yield from (
    φ(r'<[0-9]{6}[a-z][0-9]{5}\$[a-z][0-9]{5}[a-z][0-9]\$[0-9][a-z][0-9]{2}[a-z][0-9]{3}@[a-z]{4}[0-9]{2}[a-z][0-9]{4}[a-z][0-9]{2}>')
     #1:<002701c85780$d64510a0$7d90e604@your27e1513d96>
|   φ(r'\ "Elizabeth\ Flowers"\ <shalomyaall@peoplepc\.com>')
|   φ(r'<[0-9]{6}[a-z][0-9]{5}\$[0-9][a-z][0-9][a-z]{2}[0-9]{3}\$[0-9]{4}[a-z][0-9][a-z][0-9]@[A-Z]{6}[0-9][A-Z][0-9][A-Z][0-9][A-Z]{3}>')
     #1:<016401c85800$8e8ae250$6701a8c0@VALUED2D4C2DDC>
|   φ(r'\ "midwest\ auto\ recycling"\ <parts@mw\-ar\.com>')
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def Return_Path(): yield from (
    φ(r'(?:(?:[A-Za-z0-9-]+\\.)+[A-Za-z]{2,}|localhost|(?:\d{1,3}\\.){3}\d{1,3})@(?:(?:[A-Za-z0-9-]+\\.)+[A-Za-z]{2,}|localhost|(?:\d{1,3}\\.){3}\d{1,3})')
     #1:Ken.Moses@quest.com
     #1:pat.luis@quest.com
     #1:Lisa.Radford@quest.com
     #1:Keren.Kamilian@quest.com
     #4:Lon.Cherryholmes@quest.com
     #2:adi.izhar@quest.com
     #1:Chris.Sheets@alcoa.com
|   φ(r'<>')
     #1:<>
|   φ(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}')
     #3:lesliecherryholmes@hotmail.com
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def Thread_Index(): yield from (
    φ(r'[A-Z][a-z]{2}[A-Z][0-9][A-Z]{3}[0-9][a-z][A-Z][a-z][A-Z]{3}[a-z][A-Z][0-9][A-Z][a-z][A-Z][a-z][0-9][A-Z]{4}[0-9][a-z]{2}==')
     #1:AccX1HFT7mXxXKMqQ4WfYy2XVAP9zw==
|   φ(r'[A-Z][a-z]{3}[A-Z]{3}[a-z]{3}[A-Z][a-z]{4}[A-Z]{2}[a-z][0-9][a-z]{2}[A-Z]{6}[a-z]{3}==')
     #1:AcfvRODlxbBswqcURw6mlUYZAKBweg==
|   φ(r'[A-Z][a-z]{2}[A-Z][a-z]{2}[A-Z][0-9][A-Z]{3}[a-z][A-Z][a-z][0-9][a-z][A-Z]{2}[a-z]{2}[0-9]{2}[A-Z]/[A-Z][a-z][A-Z][a-z][A-Z][a-z]==')
     #1:AcgScmE6LBBfMi0bTIap03W/RkVbJg==
|   φ(r'[A-Z][a-z]{2}[A-Z][a-z]{5}[A-Z]{3}[a-z][A-Z]{2}[0-9][A-Z][a-z][A-Z][a-z][A-Z][a-z][A-Z]{3}[0-9][a-z][A-Z]{3}==')
     #1:AchIjypdoDOCeFK0ReOoChMXS6xNCQ==
|   φ(r'[A-Z][a-z]{2}[A-Z][a-z]{2}[A-Z]{2}[0-9][A-Z][a-z][0-9][a-z][A-Z]{2}[a-z][A-Z]{2}[0-9][A-Z][a-z]{3}[0-9][a-z]{2}[A-Z]/[A-Z]{2}==')
     #1:AchIpnXL8Ol6iCZlSV2Acxm1jfU/DA==
|   φ(r'[A-Z][a-z]{2}[A-Z][a-z]{2}[A-Z]{2}[a-z]{2}[A-Z][a-z][0-9][a-z][A-Z][a-z][A-Z][a-z]{4}\+[a-z]{7}[A-Z]==')
     #1:AchSsxJDtbUm7pYaTdyke+uzwwtfkQ==
|   φ(r'[A-Z][a-z]{2}[A-Z][a-z][A-Z]{3}[0-9][a-z][0-9][A-Z]{3}[a-z][A-Z]{2}[a-z]\+[A-Z]{3}[a-z]{3}[A-Z]{3}\+[A-Z]==')
     #1:AchVmNAQ2k5KDWpTRm+TBPrhqDUU+A==
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def To(): yield from (
    φ(r'"[A-Z][a-z]{2} [A-Z][a-z]{11}" <[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}>')
     #2:"Lon Cherryholmes" <lcherryh@yahoo.com>
|   φ(r'<[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}>')
     #6:<lcherryh@yahoo.com>
     #5:<LCherryh@yahoo.com>
     #1:<LCherryh@Yahoo.com>
|   φ(r'"[A-Z][a-z]{2} [A-Z][a-z]{3}" <(?:(?:[A-Za-z0-9-]+\\.)+[A-Za-z]{2,}|localhost|(?:\d{1,3}\\.){3}\d{1,3})@(?:(?:[A-Za-z0-9-]+\\.)+[A-Za-z]{2,}|localhost|(?:\d{1,3}\\.){3}\d{1,3})>')
     #1:"Pat Luis" <pat.luis@quest.com>
|   φ(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}')
     #1:lcherryh@yahoo.com
     #2:LCherryh@Yahoo.com
|   φ(r'"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}" <[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}>')
     #5:"LCherryh@Yahoo.com" <LCherryh@Yahoo.com>
|   φ(r'"[A-Z]{2}:" <[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}>')
     #1:"RE:" <LCherryh@Yahoo.com>
|   φ(r'[A-Z][a-z]{2} [A-Z][a-z]{11} <(?:(?:[A-Za-z0-9-]+\\.)+[A-Za-z]{2,}|localhost|(?:\d{1,3}\\.){3}\d{1,3})@(?:(?:[A-Za-z0-9-]+\\.)+[A-Za-z]{2,}|localhost|(?:\d{1,3}\\.){3}\d{1,3})>, [A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}')
     #6:Lon Cherryholmes <lon.cherryholmes@quest.com>, lcherryh@yahoo.com
|   φ(r'[A-Z][a-z]{2} [A-Z][a-z]{11} <[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}>, [A-Z][a-z]{2} [A-Z][a-z]{11}')
     #2:Lon Cherryholmes <lcherryh@yahoo.com>, Lon Cherryholmes
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_Account_Key(): yield from (
    φ(r'[a-z]{7}[0-9]')
     #32:account1
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_ELNK_Trace(): yield from (
    φ(r'[A-Z][a-z]{7} [A-Z][a-z] [A-Z][a-z]{8} [A-Z][a-z]{3}[A-Z]{3} [A-Z][0-9]\.[0-9]{2}\.[0-9]{4}\.[0-9]{4}')
     #1:Produced By Microsoft MimeOLE V6.00.2900.3198
|   φ(r'\ a3d8c057f9c6b8f389e6754a908ffd6934c7e5330eb4d16d9aa54211302f97d780a966c17e7b0748350badd9bab72f9c350badd9bab72f9c350badd9bab72f9c')
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_MAIL_FROM(): yield from (
    φ(r'<(?:(?:[A-Za-z0-9-]+\\.)+[A-Za-z]{2,}|localhost|(?:\d{1,3}\\.){3}\d{1,3})@(?:(?:[A-Za-z0-9-]+\\.)+[A-Za-z]{2,}|localhost|(?:\d{1,3}\\.){3}\d{1,3})>')
     #1:<tony.delollis@ventisolutions.com>
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_MIMEOLE(): yield from (
    φ(r'[A-Z][a-z]{7} [A-Z][a-z] [A-Z][a-z]{8} [A-Z][a-z]{3}[A-Z]{3} [A-Z][0-9]\.[0-9]\.[0-9]{4}\.[0-9]{5}')
     #1:Produced By Microsoft MimeOLE V6.0.6000.16480
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_MS_Has_Attach(): yield from (
    φ(r'[a-z]{3}')
     #5:yes
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_MS_TNEF_Correlator(): yield from (
    φ(r' ')
     #7: 
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_MSMail_Priority(): yield from (
    φ(r'[A-Z][a-z]{5}')
     #5:Normal
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_Mailer(): yield from (
    φ(r'[A-Z][a-z]{8} [A-Z][a-z]{5} [A-Z][a-z]{6} [0-9]{2}')
     #2:Microsoft Office Outlook 11
|   φ(r'[A-Z][a-z]{8} [A-Z][a-z]{6} [A-Z][a-z]{3} [0-9]\.[0-9]\.[0-9]{4}\.[0-9]{5}')
     #1:Microsoft Windows Mail 6.0.6000.16480
|   φ(r'[A-Z][a-z]{8} [A-Z][a-z]{6} [A-Z][a-z]{6} [0-9]\.[0-9]{2}\.[0-9]{4}\.[0-9]{4}')
     #4:Microsoft Outlook Express 6.00.2900.3138
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_MimeOLE(): yield from (
    φ(r'[A-Z][a-z]{7} [A-Z][a-z] [A-Z][a-z]{8} [A-Z][a-z]{7} [A-Z][0-9]\.[0-9]')
     #6:Produced By Microsoft Exchange V6.5
|   φ(r'[A-Z][a-z]{7} [A-Z][a-z] [A-Z][a-z]{8} [A-Z][a-z]{3}[A-Z]{3} [A-Z][0-9]\.[0-9]{2}\.[0-9]{4}\.[0-9]{4}')
     #1:Produced By Microsoft MimeOLE V6.00.3790.2929
     #1:Produced By Microsoft MimeOLE V6.00.2900.3138
     #5:Produced By Microsoft MimeOLE V6.00.2900.3198
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_OriginalArrivalTime(): yield from (
    φ(r'[0-9]{2} (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{4} \([A-Z]{3}\) [A-Z]{8}=\[[0-9][A-Z][0-9][A-Z]{2}[0-9]{3}:[0-9]{2}[A-Z][0-9]{3}[A-Z]{2}\]')
     #1:04 Dec 2006 13:51:56.0083 (UTC) FILETIME=[5C6CD030:01C717AB]
|   φ(r'[0-9]{2} (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{4} \([A-Z]{3}\) [A-Z]{8}=\[[0-9]{5}[A-Z][0-9]{2}:[0-9]{2}[A-Z][0-9]{3}[A-Z][0-9]\]')
     #1:04 Dec 2006 18:46:00.0912 (UTC) FILETIME=[71900D00:01C717D4]
|   φ(r'[0-9]{2} (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{4} \([A-Z]{3}\) [A-Z]{8}=\[[0-9]{2}[A-Z]{2}[0-9]{2}[A-Z][0-9]:[0-9]{2}[A-Z][0-9]{3}[A-Z]{2}\]')
     #1:04 Dec 2006 19:27:36.0302 (UTC) FILETIME=[40EE58E0:01C717DA]
|   φ(r'[0-9]{2} (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{4} \([A-Z]{3}\) [A-Z]{8}=\[[0-9][A-Z]{2}[0-9]{2}[A-Z][0-9]{2}:[0-9]{2}[A-Z][0-9]{3}[A-Z]{2}\]')
     #1:04 Dec 2006 19:55:17.0081 (UTC) FILETIME=[1ED51C90:01C717DE]
|   φ(r'[0-9]{2} (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{4} \([A-Z]{3}\) [A-Z]{8}=\[[0-9]{4}[A-Z][0-9]{3}:[0-9]{2}[A-Z][0-9][A-Z][0-9][A-Z][0-9]\]')
     #1:27 Aug 2007 16:21:56.0899 (UTC) FILETIME=[6335D730:01C7E8C6]
|   φ(r'[0-9]{2} (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{4} \([A-Z]{3}\) [A-Z]{8}=\[[0-9]{3}[A-Z][0-9][A-Z][0-9]{2}:[0-9]{2}[A-Z][0-9]{2}[A-Z][0-9][A-Z]\]')
     #1:30 Dec 2007 23:56:16.0969 (UTC) FILETIME=[911D2B90:01C84B3F]
|   φ(r'[0-9]{2} (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{4} \([A-Z]{3}\) [A-Z]{8}=\[[A-Z]{4}[0-9][A-Z]{2}[0-9]:[0-9]{2}[A-Z][0-9]{2}[A-Z]{3}\]')
     #1:02 Jan 2008 01:00:50.0700 (UTC) FILETIME=[EADD1CC0:01C84CDA]
|   φ(r'[0-9]{2} (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{4} \([A-Z]{3}\) [A-Z]{8}=\[[A-Z][0-9]{4}[A-Z]{2}[0-9]:[0-9]{2}[A-Z][0-9]{2}[A-Z][0-9]{2}\]')
     #1:04 Jan 2008 01:25:28.0042 (UTC) FILETIME=[B0411CA0:01C84E70]
|   φ(r'[0-9]{2} (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{4} \([A-Z]{3}\) [A-Z]{8}=\[[A-Z][0-9]{7}:[0-9]{2}[A-Z][0-9]{5}\]')
     #1:13 Jan 2008 04:00:21.0559 (UTC) FILETIME=[D1570470:01C85598]
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_Originating_IP(): yield from (
    φ(r'[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}')
     #1:4.230.144.125
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_Priority(): yield from (
    φ(r'[0-9]')
     #5:3
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_SF_Loop(): yield from (
    φ(r'[0-9]')
     #1:1
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_SOURCE_IP(): yield from (
    φ(r'\[[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\]')
     #1:[199.239.254.40]
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_Spam(): yield from (
    φ(r'\[[A-Z]=[0-9]\.[0-9]{10}; [a-z]{4}=[0-9]\.[0-9]{3}\([0-9]{4}\); [a-z]{4}=[0-9]\.[0-9]{3}; [a-z]{8}\-[a-z]{4}=[0-9]\.[0-9]{3}\([0-9]{10}\)\]')
     #1:[F=0.0148648649; heur=0.500(1500); stat=0.010; spamtraq-heur=0.599(2007082706)]
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_Spam_Flag(): yield from (
    φ(r'\ NO')
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_Virus_Scanned(): yield from (
    φ(r'[A-Z][a-z]{7} [A-Z][a-z]{3}[A-Z][a-z]{4} [A-Z][a-z]{3} [A-Z][a-z]{5}')
     #1:Symantec AntiVirus Scan Engine
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_YMail_OSG(): yield from (
    φ(r'\ SBhbpigVM1mi6K6gSZFzUO5Px6dsZJjQ6ubRxZhrVEhyKzYh1T0V6QgLyBxIrn2_2IUB6i3OT_ELxSxJP6bX5aYroyJNiV_DZxnTQJtaNfv3GV7jekUoME3InUsu7aWrw\.U9ePJEpzfVM5SJp2nhNZYsAg\-\-')
|   φ(r'\ 8rMvSCAVM1n\.wUr0gCKzpRZqif4LaXD3H8hxoQDTaBxFKvM1ez2_1BYamTG8rhW\.TzzbvHOmYDf1YuxlM9CAa9fo2wW8Kqly15AjtTsurTMDztacrZijKgYJNaVOrO0oEW_cOlVsLUDtBPkzMHQCoRTU0Q\-\-')
|   φ(r'\ CCr43HYVM1lnU5nd7FBJo43LkCeLCmAeNlOe5in1cxGirMT4cbiP15BPyaohgk7ImrXmD12y6wC96UffV4z37uNfwqUHDUPsLLwQxPPdnSwZBj8\.VvReCkmPPqi_uA6GbyWOR5IvErOWMhQ\-')
|   φ(r'\ Cug3HEsVM1nt5TOlV2nMi86MuhLcBOHxwq\.3VlHr5XXyAfnV0Q2Svi9sF7SalPYNDoGsf3yrzNhPCIp8SBh9BxGqMYFrBbcL8HN5mg1aJwWFbLHLQlp4mwLeX5krDbOtEyIruzm6hQrOIzc\-')
|   φ(r'\ tglsUiwVM1nqRaLdY416S5\.tRuJv\.A9FwMYIVBI5TXOEN\.DsahHbpr6G3L77YtenDB0A\.1KkxfLFdEH08iDBRPGBxdxFBiNJcWRlBQGajmN38KuGaXKPvI4cf7jNZkVKHpDR2GjmtkB6Rws\-')
|   φ(r'\ GwU5ougVM1mT\.tfhvBjR0JeOccXuFW0jQ3x0L5167in1SDDgS33MtQ\.Og19gmnOOVJ_un66sMYN1geNZ9g8TWAj9Q8oKGwz8TIJ8Edqh458TktGJM5fA8ags2a_mI034LoLRuPTnDxL7sKtkClDLmlY_Xw\-\-')
|   φ(r'\ tDfT\.swVM1lwLUjwRWSXFLh1Aa6WZ0EvoUjCMRrrLPtn\.2q0bzpskmO\.798Lz0myVCg_G6fluF8ohlCUFfLR0aa5CKocbiP77DhvUN_dIdEihOAEIFAMNZt68IXVCxpptK328gQFCssjoqubux4G1\.XR')
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_Yahoo_Newman_Property(): yield from (
    φ(r'[a-z]{6}\-[a-z]{6}')
     #1:groups-bounce
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def acceptlanguage(): yield from (
    φ(r'\ en\-US')
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def thread_index(): yield from (
    φ(r'[A-Z][a-z]{5}\+[A-Z][a-z][0-9][A-Z]{3}[0-9][A-Z]{3}[a-z][A-Z][a-z][A-Z][0-9][A-Z][a-z]{3}[A-Z]{3}[a-z]==')
     #1:Acfoxj+Fy3ABX1UHRgSdI7CnwxKTKw==
|   φ(r'[A-Z][a-z]{2}[A-Z][0-9][a-z]{2}[A-Z]{2}[a-z][0-9]{2}[A-Z][0-9][a-z]{2}[A-Z]{2}[a-z][A-Z][a-z][A-Z][a-z][A-Z]{2}[a-z]{2}[A-Z]{3}==')
     #1:AchW8csYNr02G2rlRZiGjYiUAouHXA==
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def Inbox(): yield from (
    φ(rex_From) + η() + X_Account_Key() + η() + X_UIDL() + η() + X_Mozilla_Status() + η() + X_Mozilla_Status2() + η() + X_Mozilla_Keys() + η() + X_Apparently_To() + η() + X_Originating_IP() + η() + Return_Path() + η() + Authentication_Results() + η() + Received() + η() + Received() + η() + X_MimeOLE() + η() + Content_class() + η() + MIME_Version() + η() + Content_Type() + η() + Subject() + η() + Date() + η() + Message_ID() + η() + X_MS_Has_Attach() + η() + X_MS_TNEF_Correlator() + η() + Thread_Topic() + η() + Thread_Index() + η() + From() + η() + To() + η() + Return_Path() + η() + X_OriginalArrivalTime() + η() + Content_Length() + η()
|   φ(rex_From) + η() + X_Account_Key() + η() + X_UIDL() + η() + X_Mozilla_Status() + η() + X_Mozilla_Status2() + η() + X_Mozilla_Keys() + η() + X_Apparently_To() + η() + X_Originating_IP() + η() + Return_Path() + η() + Authentication_Results() + η() + Received() + η() + Received() + η() + X_MimeOLE() + η() + Content_class() + η() + MIME_Version() + η() + Content_Type() + η() + Subject() + η() + Date() + η() + Message_ID() + η() + X_MS_Has_Attach() + η() + X_MS_TNEF_Correlator() + η() + Thread_Topic() + η() + Thread_Index() + η() + From() + η() + To() + η() + Cc() + η() + Return_Path() + η() + X_OriginalArrivalTime() + η() + Content_Length() + η()
|   φ(rex_From) + η() + X_Account_Key() + η() + X_UIDL() + η() + X_Mozilla_Status() + η() + X_Mozilla_Status2() + η() + X_Mozilla_Keys() + η() + X_Apparently_To() + η() + X_Originating_IP() + η() + Return_Path() + η() + Authentication_Results() + η() + Received() + η() + Received() + η() + X_MimeOLE() + η() + Content_class() + η() + MIME_Version() + η() + Content_Type() + η() + Subject() + η() + Date() + η() + Message_ID() + η() + In_Reply_To() + η() + X_MS_Has_Attach() + η() + X_MS_TNEF_Correlator() + η() + Thread_Topic() + η() + Thread_Index() + η() + From() + η() + To() + η() + Cc() + η() + Return_Path() + η() + X_OriginalArrivalTime() + η() + Content_Length() + η()
|   φ(rex_From) + η() + X_Account_Key() + η() + X_UIDL() + η() + X_Mozilla_Status() + η() + X_Mozilla_Status2() + η() + X_Mozilla_Keys() + η() + X_Apparently_To() + η() + X_Originating_IP() + η() + Return_Path() + η() + Authentication_Results() + η() + Received() + η() + Received() + η() + Received() + η() + X_MimeOLE() + η() + Content_class() + η() + MIME_Version() + η() + Content_Type() + η() + Subject() + η() + Date() + η() + Message_ID() + η() + X_MS_Has_Attach() + η() + X_MS_TNEF_Correlator() + η() + Thread_Topic() + η() + Thread_Index() + η() + References() + η() + From() + η() + To() + η() + Cc() + η() + Return_Path() + η() + X_OriginalArrivalTime() + η() + Content_Length() + η()
|   φ(rex_From) + η() + X_Account_Key() + η() + X_UIDL() + η() + X_Mozilla_Status() + η() + X_Mozilla_Status2() + η() + X_Mozilla_Keys() + η() + X_Apparently_To() + η() + X_Originating_IP() + η() + Return_Path() + η() + Authentication_Results() + η() + Received() + η() + Comment() + η() + DomainKey_Signature() + η() + Received() + η() + Received() + η() + Received() + η() + Date() + η() + Message_ID() + η() + X_Yahoo_Newman_Property() + η() + MIME_Version() + η() + To() + η() + From() + η() + Subject() + η() + Content_Type() + η() + Content_Length() + η()
|   φ(rex_From) + η() + X_Account_Key() + η() + X_UIDL() + η() + X_Mozilla_Status() + η() + X_Mozilla_Status2() + η() + X_Mozilla_Keys() + η() + X_Apparently_To() + η() + X_Originating_IP() + η() + Return_Path() + η() + Authentication_Results() + η() + Received() + η() + Received() + η() + Received() + η() + X_MimeOLE() + η() + Content_class() + η() + MIME_Version() + η() + Content_Type() + η() + Content_Transfer_Encoding() + η() + Subject() + η() + Date() + η() + Message_ID() + η() + X_MS_Has_Attach() + η() + X_MS_TNEF_Correlator() + η() + Importance() + η() + Priority() + η() + Thread_Topic() + η() + Thread_Index() + η() + From() + η() + To() + η() + Return_Path() + η() + X_OriginalArrivalTime() + η() + Content_Length() + η()
|   φ(rex_From) + η() + X_Account_Key() + η() + X_UIDL() + η() + X_Mozilla_Status() + η() + X_Mozilla_Status2() + η() + X_Mozilla_Keys() + η() + X_Apparently_To() + η() + X_Originating_IP() + η() + Return_Path() + η() + Authentication_Results() + η() + Received() + η() + Received() + η() + Received() + η() + Received() + η() + Received() + η() + From() + η() + To() + η() + Subject() + η() + Date() + η() + Message_ID() + η() + MIME_Version() + η() + Content_Type() + η() + X_Mailer() + η() + X_MimeOLE() + η() + Thread_Index() + η() + X_Spam() + η() + X_MAIL_FROM() + η() + X_SOURCE_IP() + η() + X_SF_Loop() + η() + Content_Length() + η()
|   φ(rex_From) + η() + X_Account_Key() + η() + X_UIDL() + η() + X_Mozilla_Status() + η() + X_Mozilla_Status2() + η() + X_Mozilla_Keys() + η() + X_Apparently_To() + η() + X_Originating_IP() + η() + Return_Path() + η() + Authentication_Results() + η() + Received() + η() + Received() + η() + Message_ID() + η() + From() + η() + To() + η() + Subject() + η() + Date() + η() + MIME_Version() + η() + Content_Type() + η() + X_Priority() + η() + X_MSMail_Priority() + η() + X_Mailer() + η() + X_MimeOLE() + η() + X_Virus_Scanned() + η() + Content_Length() + η()
|   φ(rex_From) + η() + X_Account_Key() + η() + X_UIDL() + η() + X_Mozilla_Status() + η() + X_Mozilla_Status2() + η() + X_Mozilla_Keys() + η() + X_Apparently_To() + η() + X_Originating_IP() + η() + Return_Path() + η() + Authentication_Results() + η() + Received() + η() + Received() + η() + Received() + η() + From() + η() + To() + η() + Subject() + η() + Date() + η() + Message_ID() + η() + MIME_Version() + η() + Content_Type() + η() + X_Mailer() + η() + X_MimeOLE() + η() + Thread_Index() + η() + Content_Length() + η()
|   φ(rex_From) + η() + X_Account_Key() + η() + X_UIDL() + η() + X_Mozilla_Status() + η() + X_Mozilla_Status2() + η() + X_Mozilla_Keys() + η() + X_Apparently_To() + η() + X_Originating_IP() + η() + Return_Path() + η() + Authentication_Results() + η() + Received() + η() + Received() + η() + Received() + η() + From() + η() + To() + η() + Date() + η() + Subject() + η() + Thread_Topic() + η() + Thread_Index() + η() + Message_ID() + η() + σ('Accept-Language') + η() + σ('Content-Language') + η() + X_MS_Has_Attach() + η() + X_MS_TNEF_Correlator() + η() + σ('acceptlanguage') + η() + Content_Type() + η() + MIME_Version() + η() + Return_Path() + η() + Content_Length() + η()
|   φ(rex_From) + η() + X_Account_Key() + η() + X_UIDL() + η() + X_Mozilla_Status() + η() + X_Mozilla_Status2() + η() + X_Mozilla_Keys() + η() + X_Apparently_To() + η() + X_Originating_IP() + η() + Return_Path() + η() + Authentication_Results() + η() + Received() + η() + Received() + η() + Received() + η() + From() + η() + To() + η() + Date() + η() + Subject() + η() + Thread_Topic() + η() + Thread_Index() + φ(r'[A-Z]+') + φ(r'[a-z]+') + φ(r'[A-Z]+') + φ(r'[a-z]') + φ(r'[A-Z]') + φ(r'[0-9]') + φ(r'[A-Z]') + σ('=') + σ('=') + η() + Message_ID() + η() + σ('Accept-Language') + η() + σ('Content-Language') + η() + X_MS_Has_Attach() + η() + X_MS_TNEF_Correlator() + η() + σ('acceptlanguage') + η() + Content_Type() + η() + MIME_Version() + η() + Return_Path() + η() + Content_Length() + η()
|   φ(rex_From) + η() + X_Account_Key() + η() + X_UIDL() + η() + X_Mozilla_Status() + η() + X_Mozilla_Status2() + η() + X_Mozilla_Keys() + η() + X_Apparently_To() + η() + X_Originating_IP() + η() + Return_Path() + η() + Authentication_Results() + η() + Received() + η() + Received() + η() + Received() + η() + From() + η() + To() + η() + Date() + η() + Subject() + η() + Thread_Topic() + η() + Thread_Index() + φ(r'[A-Z]+') + σ('+') + φ(r'[A-Z]') + φ(r'[a-z]') + φ(r'[A-Z]+') + φ(r'[0-9]') + φ(r'[a-z]') + φ(r'[A-Z]') + φ(r'[a-z]') + φ(r'[A-Z]+') + φ(r'[0-9]') + φ(r'[A-Z]') + φ(r'[0-9]') + φ(r'[A-Z]') + η() + Message_ID() + η() + σ('Accept-Language') + η() + σ('Content-Language') + η() + X_MS_Has_Attach() + η() + X_MS_TNEF_Correlator() + η() + σ('acceptlanguage') + η() + Content_Type() + η() + MIME_Version() + η() + Return_Path() + η() + Content_Length() + η()
|   φ(rex_From) + η() + X_Account_Key() + η() + X_UIDL() + η() + X_Mozilla_Status() + η() + X_Mozilla_Status2() + η() + X_Mozilla_Keys() + η() + X_Apparently_To() + η() + X_Originating_IP() + η() + Return_Path() + η() + Authentication_Results() + η() + Received() + η() + Received() + η() + Message_ID() + η() + Return_Path() + η() + Content_Type() + η() + X_Originating_IP() + η() + From() + η() + To() + η() + Subject() + η() + Date() + η() + Importance() + η() + MIME_Version() + η() + X_OriginalArrivalTime() + η() + Content_Length() + η()
|   φ(rex_From) + η() + X_Account_Key() + η() + X_UIDL() + η() + X_Mozilla_Status() + η() + X_Mozilla_Status2() + η() + X_Mozilla_Keys() + η() + X_Apparently_To() + η() + X_Originating_IP() + η() + Return_Path() + η() + Authentication_Results() + η() + Received() + η() + Received() + η() + DomainKey_Signature() + η() + μ() + φ(r'[a-z]') + σ('=') + φ(r'[A-Z]') + σ('-') + φ(r'[A-Z]+') + φ(r'[a-z]+') + σ('-') + φ(r'[A-Z]+') + σ(':') + Received() + η() + σ('X-YMail-OSG') + η() + Received() + η() + Date() + η() + From() + η() + Subject() + η() + To() + η() + MIME_Version() + η() + Content_Type() + η() + Message_ID() + η() + Content_Length() + η()
|   φ(rex_From) + η() + X_Account_Key() + η() + X_UIDL() + η() + X_Mozilla_Status() + η() + X_Mozilla_Status2() + η() + X_Mozilla_Keys() + η() + X_Apparently_To() + η() + X_Originating_IP() + η() + Return_Path() + η() + Authentication_Results() + η() + Received() + η() + Received() + η() + Message_ID() + η() + Return_Path() + η() + Content_Type() + η() + X_Originating_IP() + η() + From() + η() + To() + η() + μ() + σ('<') + φ(r'[a-z]+') + σ('.') + φ(r'[a-z]+') + σ('@') + φ(r'[a-z]+') + σ('.') + φ(r'[a-z]+') + σ('>') + η() + Subject() + η() + Date() + η() + Importance() + η() + MIME_Version() + η() + X_OriginalArrivalTime() + η() + Content_Length() + η()
|   φ(rex_From) + η() + X_Account_Key() + η() + X_UIDL() + η() + X_Mozilla_Status() + η() + X_Mozilla_Status2() + η() + X_Mozilla_Keys() + η() + X_Apparently_To() + η() + X_Originating_IP() + η() + Return_Path() + η() + Authentication_Results() + η() + Received() + η() + Received() + η() + Received() + η() + X_MimeOLE() + η() + Content_class() + η() + MIME_Version() + η() + Content_Type() + η() + Subject() + η() + Date() + η() + Message_ID() + η() + X_MS_Has_Attach() + η() + X_MS_TNEF_Correlator() + η() + Thread_Topic() + η() + Thread_Index() + η() + From() + η() + To() + η() + Return_Path() + η() + X_OriginalArrivalTime() + η() + Content_Length() + η()
|   φ(rex_From) + η() + X_Account_Key() + η() + X_UIDL() + η() + X_Mozilla_Status() + η() + X_Mozilla_Status2() + η() + X_Mozilla_Keys() + η() + X_Apparently_To() + η() + X_Originating_IP() + η() + Return_Path() + η() + Authentication_Results() + η() + Received() + η() + Received() + η() + Message_ID() + η() + From() + η() + To() + η() + Subject() + η() + Date() + η() + MIME_Version() + η() + Content_Type() + η() + X_Priority() + η() + X_MSMail_Priority() + η() + X_Mailer() + η() + X_MimeOLE() + η() + Content_Length() + η()
|   φ(rex_From) + η() + X_Account_Key() + η() + X_UIDL() + η() + X_Mozilla_Status() + η() + X_Mozilla_Status2() + η() + X_Mozilla_Keys() + η() + X_Apparently_To() + η() + X_Originating_IP() + η() + Return_Path() + η() + Authentication_Results() + η() + Received() + η() + X_MimeOLE() + η() + Content_class() + η() + MIME_Version() + η() + Content_Type() + η() + Subject() + η() + Date() + η() + Message_ID() + η() + X_MS_Has_Attach() + η() + X_MS_TNEF_Correlator() + η() + Thread_Topic() + η() + Thread_Index() + η() + From() + η() + To() + η() + Cc() + η() + Content_Length() + η()
|   φ(rex_From) + η() + X_Account_Key() + η() + X_UIDL() + η() + X_Mozilla_Status() + η() + X_Mozilla_Status2() + η() + X_Mozilla_Keys() + η() + X_Apparently_To() + η() + X_Originating_IP() + η() + Return_Path() + η() + Authentication_Results() + η() + Received() + η() + Received() + η() + Message_ID() + η() + σ('Reply-To') + η() + From() + η() + To() + η() + Subject() + η() + Date() + η() + MIME_Version() + η() + Content_Type() + η() + X_Priority() + η() + X_MSMail_Priority() + η() + X_Mailer() + η() + X_MimeOLE() + η() + σ('X-ELNK-Trace') + η() + X_Originating_IP() + η() + Content_Length() + η()
|   φ(rex_From) + η() + X_Account_Key() + η() + X_UIDL() + η() + X_Mozilla_Status() + η() + X_Mozilla_Status2() + η() + X_Mozilla_Keys() + η() + X_Apparently_To() + η() + X_Originating_IP() + η() + Return_Path() + η() + Authentication_Results() + η() + Received() + η() + Received() + η() + Message_ID() + η() + σ('Reply-To') + η() + From() + η() + To() + η() + References() + η() + Subject() + η() + Date() + η() + MIME_Version() + η() + Content_Type() + η() + X_Priority() + η() + X_MSMail_Priority() + η() + X_Mailer() + η() + X_MimeOLE() + η() + Content_Length() + η()
|   φ(rex_From) + η() + X_Account_Key() + η() + X_UIDL() + η() + X_Mozilla_Status() + η() + X_Mozilla_Status2() + η() + X_Mozilla_Keys() + η() + X_Apparently_To() + η() + X_Originating_IP() + η() + Return_Path() + η() + Authentication_Results() + η() + Received() + η() + Received() + η() + From() + η() + Message_ID() + η() + Date() + η() + Subject() + η() + To() + η() + MIME_Version() + η() + Content_Type() + η() + σ('X-Spam-Flag') + η() + Content_Length() + η()
)
