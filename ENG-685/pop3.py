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
def X_Account_Key:: yield from (
    r' [a-z]+[0-9]'
   #32: account1
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
|   r' [A-Z]+[0-9][a-z]+[A-Z]+[a-z][A-Z][a-z][0-9][A-Z]+[0-9]+[a-z]+[A-Z]+'
   #1: AA1lxEIAAYZdRj3WIQ33ixfqhTU
|   r' [A-Z]+[a-z]+[A-Z]+[a-z][A-Z][a-z][A-Z][0-9][A-Z][a-z][0-9][a-z][0-9][A-Z][a-z]+[A-Z]+'
   #1: ABJlxEIAATKjRtL6Jw0h4WnzwOU
|   r' [A-Z]+[a-z]+[A-Z]+[0-9][A-Z]+[a-z][0-9][a-z][A-Z]+[a-z][A-Z][a-z][A-Z]+'
   #1: AAxlxEIAAE6TRt3fZQnYbWOJNXI
|   r' [A-Z]+[a-z]+[A-Z]+[a-z][0-9][A-Z][a-z][0-9][a-z][A-Z]+[a-z]+[A-Z][a-z]+[0-9][A-Z]'
   #1: ABBlxEIAAKj6Ru0fRQIHplHll4M
|   r' [A-Z]+[a-z]+[A-Z]+[a-z]+[A-Z][a-z][0-9][A-Z][a-z][0-9][a-z][A-Z][a-z][A-Z]+'
   #1: ABBlxEIAALLIRxjkWw7Rr3oAeBI
|   r' [A-Z]+[a-z]+[A-Z]+[0-9]+[A-Z][0-9][A-Z][a-z]+[A-Z]+[a-z]+[A-Z][a-z]+[A-Z]'
   #1: ABBlxEIAAL16R3OtrARolBlwdbY
|   r' [A-Z]+[a-z]+[A-Z]+[0-9][A-Z]+[0-9][A-Z][a-z][A-Z]+[0-9][a-z][A-Z][0-9]'
   #1: ABplxEIAAN1OR3OyDQGOXDR2fM0
|   r' [A-Z]+[a-z]+[A-Z]+[a-z]+[A-Z][0-9][A-Z][0-9][a-z]+[A-Z][0-9][A-Z]+[0-9]+[A-Z]+'
   #1: ABJlxEIAABgzR3O0bwM1OC78ZGA
|   r' [A-Z]+[a-z]+[A-Z]+[a-z][A-Z]+[0-9][A-Z][0-9][a-z][A-Z]+[a-z]+[0-9][A-Z]+[a-z]'
   #1: ABBlxEIAAOhBR3O0cAGupwp5ITo
|   r' [A-Z]+[a-z]+[A-Z]+[0-9][a-z][A-Z][0-9][A-Z]+[a-z][A-Z][a-z][A-Z]+[a-z]+'
   #1: ABBlxEIAAC5iR3PUhQtOZCefofc
|   r' [A-Z]+[a-z]+[A-Z]+\+[A-Z]+[0-9][a-z]+[A-Z]+[a-z]+[A-Z]/[0-9][A-Z][0-9][A-Z]'
   #1: ABllxEIAAG+CR3gxMQLiyS/3Y2U
|   r' [A-Z]+[a-z]+[A-Z]+[a-z][A-Z][0-9][a-z][0-9][a-z][A-Z]+[a-z][0-9][A-Z][a-z][A-Z][a-z][0-9][A-Z]'
   #1: ABZlxEIAAYMxR3p8wANp8CsZh3U
|   r' [A-Z]+[0-9][a-z]+[A-Z]+[0-9][A-Z][0-9][a-z]+[A-Z][0-9][A-Z][a-z][A-Z]+[a-z]+[A-Z]'
   #1: AA5lxEIAAUD6R3riyA2MxBLWhmI
|   r' [A-Z]+[a-z]+[A-Z]+[a-z]+[A-Z][0-9][a-z][A-Z][a-z]+[A-Z]+[0-9][a-z][A-Z][a-z]'
   #1: AAxlxEIAAAnrR3tJowTNTGB5eGs
|   r' [A-Z]+[0-9][a-z]+[A-Z]+[a-z][A-Z]+[0-9][a-z]+[A-Z][a-z][A-Z]+[a-z][A-Z]+[a-z][0-9]+'
   #1: AA9lxEIAAWbVR3ujEwLNtFPk664
|   r' [A-Z]+[a-z]+[A-Z]+[0-9][A-Z][0-9]+[A-Z]+[a-z][A-Z][a-z][A-Z]+[0-9][a-z]'
   #1: ABVlxEIAAFI9R32MBwKzOTMWW8k
|   r' [A-Z]+[a-z]+[A-Z]+[a-z][A-Z][0-9][A-Z]+[0-9][a-z][A-Z]+[a-z]+[A-Z][a-z][A-Z]+[0-9]'
   #1: AAxlxEIAACRvR4NZ1wRZnzNbED8
|   r' [A-Z]+[a-z]+[A-Z]+[a-z][0-9][A-Z][0-9][A-Z][a-z]+[A-Z]+[0-9][a-z][0-9][a-z][A-Z]+'
   #1: ABplxEIAAWc7R4SxqgjOV2d3rDM
|   r' [A-Z]+[a-z]+[A-Z]+[0-9][A-Z][a-z][A-Z]+[a-z][A-Z]+[a-z]+[A-Z][a-z]'
   #1: AAxlxEIAAWMIR4TfAQmOEkunjTc
|   r' [A-Z]+[a-z]+[A-Z]+[0-9][A-Z][a-z][A-Z]+[a-z][A-Z]+[a-z]+[0-9][a-z]+'
   #1: ABFlxEIAAPFRR4ZhLAuZYUhw5ok
|   r' [A-Z]+[a-z]+[A-Z]+[a-z][A-Z]+[0-9][a-z][A-Z][0-9][A-Z][a-z][A-Z][a-z]+[0-9][A-Z]+[a-z]+'
   #1: ABZlxEIAAMeIR4mM2AaCyj5GExg
|   r' [A-Z]+[a-z]+[A-Z]+[a-z][0-9][A-Z][0-9][a-z][0-9][a-z]+[A-Z][a-z][A-Z][a-z]+[A-Z][a-z]'
   #1: ABhlxEIAABy7R4t4tgcXpAbafKo
|   r' [A-Z]+[a-z]+[A-Z]+[a-z][0-9][A-Z][0-9][a-z][A-Z]+[a-z][A-Z]+'
   #1: ABFlxEIAADc6R4uYXQVWYBgAZEM
|   r' [A-Z]+[a-z]+[A-Z]+[a-z][A-Z][0-9][a-z][A-Z][a-z][A-Z][a-z]+[A-Z]+/[a-z][A-Z][a-z]+'
   #1: ABNlxEIAASNvR4vPpAevBR/yXso
|   r' [A-Z]+[a-z]+[A-Z]+[a-z]+[A-Z][0-9][a-z]/[a-z]+\+[a-z]+[A-Z][0-9]+'
   #1: ABplxEIAAPssR4y/cwkq+lvtM48
|   r' [A-Z]+[a-z]+[A-Z]+[a-z][A-Z]+[0-9]+[A-Z][a-z]+[0-9]+[a-z][A-Z]+'
   #1: ABFlxEIAAJbHR40Qjwvts31wWYA
|   r' [A-Z]+[a-z]+[A-Z]+[0-9][a-z][A-Z][0-9]+[A-Z][0-9][A-Z][a-z][A-Z][a-z][0-9][A-Z][a-z]+[0-9][A-Z]'
   #1: ABFlxEIAAJ8bR42V4QsHm0Ydt3U
|   r' [A-Z]+[0-9][a-z]+[A-Z]+\+[A-Z]+[0-9]+[A-Z]+[a-z]+[A-Z]+[0-9][a-z]+'
   #1: AA1lxEIAAA+SR44AYweZLVYR0wc
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_Mozilla_Status:: yield from (
    r' [0-9]+'
   #25: 0000
   #1: 0011
   #6: 0001
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_Mozilla_Status2:: yield from (
    r' [0-9]+'
   #31: 00000000
   #1: 10000000
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_Mozilla_Keys:: yield from (
    r'[ ]+'
   #32:                                                                                 
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_Apparently_To:: yield from (
    r' [a-z]+@[a-z]+\.[a-z]+ [a-z]+ [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+; [A-Z][a-z]+, [0-9]+ [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ -[0-9]+'
   #1: lcherryh@yahoo.com via 66.196.101.21; Mon, 04 Dec 2006 05:51:56 -0800
   #1: lcherryh@yahoo.com via 66.196.101.16; Mon, 04 Dec 2006 10:46:01 -0800
   #1: lcherryh@yahoo.com via 66.196.101.12; Mon, 04 Dec 2006 11:27:37 -0800
   #1: lcherryh@yahoo.com via 66.196.101.24; Mon, 04 Dec 2006 11:55:19 -0800
   #1: lcherryh@yahoo.com via 66.196.101.13; Sun, 06 May 2007 06:20:33 -0700
   #1: lcherryh@yahoo.com via 66.196.101.18; Mon, 27 Aug 2007 09:21:59 -0700
   #1: lcherryh@yahoo.com via 66.196.101.12; Tue, 04 Sep 2007 15:42:45 -0700
   #1: lcherryh@yahoo.com via 66.196.101.16; Sun, 16 Sep 2007 05:19:17 -0700
   #1: lcherryh@yahoo.com via 66.196.101.16; Fri, 19 Oct 2007 10:07:39 -0700
   #1: lcherryh@yahoo.com via 66.196.101.16; Thu, 27 Dec 2007 05:50:35 -0800
   #1: lcherryh@yahoo.com via 66.196.101.26; Thu, 27 Dec 2007 06:09:16 -0800
   #1: lcherryh@yahoo.com via 66.196.101.18; Thu, 27 Dec 2007 06:19:27 -0800
   #1: lcherryh@yahoo.com via 66.196.101.16; Thu, 27 Dec 2007 06:19:27 -0800
   #1: lcherryh@yahoo.com via 66.196.101.16; Thu, 27 Dec 2007 08:36:21 -0800
   #1: lcherryh@yahoo.com via 66.196.101.25; Sun, 30 Dec 2007 16:00:49 -0800
   #1: lcherryh@yahoo.com via 66.196.101.22; Tue, 01 Jan 2008 09:47:44 -0800
   #1: lcherryh@yahoo.com via 66.196.101.14; Tue, 01 Jan 2008 17:03:04 -0800
   #1: lcherryh@yahoo.com via 66.196.101.12; Wed, 02 Jan 2008 00:21:55 -0800
   #1: lcherryh@yahoo.com via 66.196.101.15; Wed, 02 Jan 2008 06:43:30 -0800
   #1: lcherryh@yahoo.com via 66.196.101.21; Thu, 03 Jan 2008 17:29:43 -0800
   #1: lcherryh@yahoo.com via 66.196.101.12; Tue, 08 Jan 2008 03:09:11 -0800
   #1: lcherryh@yahoo.com via 66.196.101.26; Wed, 09 Jan 2008 03:36:10 -0800
   #1: lcherryh@yahoo.com via 66.196.101.12; Wed, 09 Jan 2008 06:49:37 -0800
   #1: lcherryh@yahoo.com via 66.196.101.17; Thu, 10 Jan 2008 10:17:16 -0800
   #1: lcherryh@yahoo.com via 66.196.101.22; Sat, 12 Jan 2008 20:00:24 -0800
   #1: lcherryh@yahoo.com via 66.196.101.24; Mon, 14 Jan 2008 06:59:02 -0800
   #1: lcherryh@yahoo.com via 66.196.101.17; Mon, 14 Jan 2008 09:14:05 -0800
   #1: lcherryh@yahoo.com via 66.196.101.19; Mon, 14 Jan 2008 13:09:56 -0800
   #1: lcherryh@yahoo.com via 66.196.101.26; Tue, 15 Jan 2008 06:13:07 -0800
   #1: lcherryh@yahoo.com via 66.196.101.17; Tue, 15 Jan 2008 11:59:11 -0800
   #1: lcherryh@yahoo.com via 66.196.101.17; Tue, 15 Jan 2008 21:28:01 -0800
   #1: lcherryh@yahoo.com via 66.196.101.13; Wed, 16 Jan 2008 05:02:27 -0800
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_Originating_IP:: yield from (
    r' \[[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\]'
   #1: [12.106.87.68]
   #3: [12.106.87.70]
   #1: [66.94.237.55]
   #1: [12.106.87.69]
   #1: [204.202.242.120]
   #1: [24.93.47.43]
   #1: [64.202.165.99]
   #1: [65.54.246.77]
   #2: [76.183.90.53]
   #1: [206.190.48.214]
   #1: [65.54.246.83]
   #1: [206.190.48.204]
   #1: [206.190.48.207]
   #1: [65.54.246.86]
   #1: [170.252.248.206]
   #2: [206.190.48.208]
   #1: [206.190.48.213]
   #1: [66.196.101.18]
   #3: [71.74.56.123]
   #1: [71.41.16.226]
   #1: [209.86.89.73]
|   r' \[[0-9]+\.[0-9]\.[0-9]+\.[0-9]+\]'
   #6: [213.1.252.135]
|   r' \[[0-9]+\.[0-9]+\.[0-9]\.[0-9]+\]'
   #1: [147.154.9.220]
|   r' [0-9]\.[0-9]+\.[0-9]+\.[0-9]+'
   #1: 4.230.144.125
|   r' \[[0-9]+\.[0-9]+\.[0-9]+\.[0-9]\]'
   #1: [64.12.137.7]
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def Return_Path:: yield from (
    r' <[a-z]+\.[a-z]+@[a-z]+\.[a-z]+>'
   #1: <ken.moses@quest.com>
   #1: <pat.luis@quest.com>
   #1: <lisa.radford@quest.com>
   #1: <keren.kamilian@quest.com>
   #5: <lon.cherryholmes@quest.com>
   #1: <tony.delollis@ventisolutions.com>
   #2: <adi.izhar@quest.com>
   #1: <chris.sheets@alcoa.com>
|   r' [A-Z][a-z]+\.[A-Z][a-z]+@[a-z]+\.[a-z]+'
   #1: Ken.Moses@quest.com
   #1: Lisa.Radford@quest.com
   #1: Keren.Kamilian@quest.com
   #4: Lon.Cherryholmes@quest.com
   #1: Chris.Sheets@alcoa.com
|   r' [a-z]+\.[a-z]+@[a-z]+\.[a-z]+'
   #1: pat.luis@quest.com
   #2: adi.izhar@quest.com
|   r' <>'
   #1: <>
|   r' <[A-Z][a-z]+\.[A-Z][a-z]+@[a-z]+\.[a-z]+>'
   #1: <Lon.Cherryholmes@quest.com>
|   r' <[a-z]+@[a-z]+\.[a-z]+\.[a-z]+>'
   #1: <rbullerman@austin.rr.com>
   #2: <tdeatley@austin.rr.com>
|   r' <[a-z]+\.[a-z]+@[a-z]+-[a-z]+\.[a-z]+>'
   #1: <jeff.omo@database-brothers.com>
|   r' <[a-z]+@[a-z]+\.[a-z]+>'
   #3: <lesliecherryholmes@hotmail.com>
   #1: <lcherryh@yahoo.com>
   #1: <bthompson@riverranchradiology.com>
   #1: <shalomyaall@peoplepc.com>
|   r' [a-z]+@[a-z]+\.[a-z]+'
   #3: lesliecherryholmes@hotmail.com
|   r' <[a-z]+_[0-9]+@[a-z]+\.[a-z]+>'
   #6: <ness_78759@yahoo.com>
|   r' <[a-z]+@[a-z]+-[a-z]+\.[a-z]+>'
   #1: <parts@mw-ar.com>
|   r' <[a-z]+[0-9]+@[a-z]+\.[a-z]+>'
   #1: <cmoneymaker72@aol.com>
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def Authentication_Results:: yield from (
    r' [a-z]+[0-9]+\.[a-z]+\.[a-z]+\.[a-z]+\.[a-z]+[ ]+[a-z]+=[a-z]+\.[a-z]+; [a-z]+=[a-z]+ \([a-z]+ [a-z]+\)'
   #1: mta526.mail.mud.yahoo.com  from=quest.com; domainkeys=neutral (no sig)
   #1: mta312.mail.mud.yahoo.com  from=quest.com; domainkeys=neutral (no sig)
   #2: mta303.mail.mud.yahoo.com  from=quest.com; domainkeys=neutral (no sig)
   #1: mta219.mail.mud.yahoo.com  from=quest.com; domainkeys=neutral (no sig)
   #1: mta253.mail.mud.yahoo.com  from=hotmail.com; domainkeys=neutral (no sig)
   #1: mta203.mail.mud.yahoo.com  from=hotmail.com; domainkeys=neutral (no sig)
   #1: mta188.mail.mud.yahoo.com  from=alcoa.com; domainkeys=neutral (no sig)
   #1: mta544.mail.mud.yahoo.com  from=peoplepc.com; domainkeys=neutral (no sig)
   #1: mta215.mail.mud.yahoo.com  from=aol.com; domainkeys=neutral (no sig)
|   r' [a-z]+[0-9]+\.[a-z]+\.[a-z]+[0-9]\.[a-z]+\.[a-z]+[ ]+[a-z]+=[a-z]+\.[a-z]+; [a-z]+=[a-z]+ \([a-z]+ [a-z]+\)'
   #1: mta188.mail.re3.yahoo.com  from=quest.com; domainkeys=neutral (no sig)
   #1: mta224.mail.re4.yahoo.com  from=quest.com; domainkeys=neutral (no sig)
   #1: mta368.mail.re4.yahoo.com  from=quest.com; domainkeys=neutral (no sig)
   #1: mta305.mail.re4.yahoo.com  from=quest.com; domainkeys=neutral (no sig)
   #1: mta199.mail.re4.yahoo.com  from=quest.com; domainkeys=neutral (no sig)
   #1: mta233.mail.re4.yahoo.com  from=hotmail.com; domainkeys=neutral (no sig)
   #1: mta186.mail.re4.yahoo.com  from=quest.com; domainkeys=neutral (no sig)
   #1: mta243.mail.re4.yahoo.com  from=riverranchradiology.com; domainkeys=neutral (no sig)
|   r' [a-z]+[0-9]+\.[a-z]+\.[a-z]+[0-9]\.[a-z]+\.[a-z]+[ ]+[a-z]+=[a-z]+\.[a-z]+; [a-z]+=[a-z]+ \([a-z]+\)'
   #1: mta243.mail.re4.yahoo.com  from=yahoogroups.com; domainkeys=pass (ok)
   #1: mta234.mail.re3.yahoo.com  from=yahoo.com; domainkeys=pass (ok)
   #1: mta159.mail.re4.yahoo.com  from=yahoo.com; domainkeys=pass (ok)
   #1: mta230.mail.re4.yahoo.com  from=yahoo.com; domainkeys=pass (ok)
|   r' [a-z]+[0-9]+\.[a-z]+\.[a-z]+[0-9]\.[a-z]+\.[a-z]+[ ]+[a-z]+=[A-Z][a-z]+[A-Z][a-z]+\.[a-z]+; [a-z]+=[a-z]+ \([a-z]+ [a-z]+\)'
   #1: mta179.mail.re4.yahoo.com  from=VentiSolutions.com; domainkeys=neutral (no sig)
|   r' [a-z]+[0-9]+\.[a-z]+\.[a-z]+\.[a-z]+\.[a-z]+[ ]+[a-z]+=[a-z]+\.[a-z]+\.[a-z]+; [a-z]+=[a-z]+ \([a-z]+ [a-z]+\)'
   #1: mta416.mail.mud.yahoo.com  from=austin.rr.com; domainkeys=neutral (no sig)
|   r' [a-z]+[0-9]+\.[a-z]+\.[a-z]+[0-9]\.[a-z]+\.[a-z]+[ ]+[a-z]+=[a-z]+-[a-z]+\.[a-z]+; [a-z]+=[a-z]+ \([a-z]+ [a-z]+\)'
   #1: mta191.mail.re3.yahoo.com  from=database-brothers.com; domainkeys=neutral (no sig)
   #1: mta294.mail.re4.yahoo.com  from=mw-ar.com; domainkeys=neutral (no sig)
|   r' [a-z]+[0-9]+\.[a-z]+\.[a-z]+\.[a-z]+\.[a-z]+[ ]+[a-z]+=[a-z]+\.[a-z]+; [a-z]+=[a-z]+ \([a-z]+\)'
   #1: mta233.mail.mud.yahoo.com  from=yahoo.com; domainkeys=pass (ok)
   #1: mta499.mail.mud.yahoo.com  from=yahoo.com; domainkeys=pass (ok)
   #1: mta352.mail.mud.yahoo.com  from=yahoo.com; domainkeys=pass (ok)
   #1: mta500.mail.mud.yahoo.com  from=yahoo.com; domainkeys=pass (ok)
|   r' [a-z]+[0-9]+\.[a-z]+\.[a-z]+[0-9]\.[a-z]+\.[a-z]+[ ]+[a-z]+=[a-z]+\.[a-z]+\.[a-z]+; [a-z]+=[a-z]+ \([a-z]+ [a-z]+\)'
   #1: mta268.mail.re4.yahoo.com  from=austin.rr.com; domainkeys=neutral (no sig)
   #1: mta173.mail.re2.yahoo.com  from=austin.rr.com; domainkeys=neutral (no sig)
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
   #1: from 12.106.87.69  (EHLO alvbhxw01.quest.com) (12.106.87.69){bslash}n  by mta305.mail.re4.yahoo.com with SMTP; Mon, 27 Aug 2007 09:21:59 -0700
|   r' [a-z]+ [a-z]+[0-9]+\.[a-z]+\.[a-z]+\.[a-z]+ \(\[[0-9]+\.[0-9]\.[0-9]+\.[0-9]+\]\) [a-z]+ [a-z]+[0-9]+\.[a-z]+\.[a-z]+ [a-z]+ [A-Z][a-z]+ [A-Z]+\([0-9]\.[0-9]\.[0-9]+\.[0-9]+\);\n\t [A-Z][a-z]+, [0-9] [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ -[0-9]+'
   #1: from alvmbxw01.prod.quest.corp ([10.1.50.13]) by irvbhxw03.quest.com with Microsoft SMTPSVC(6.0.3790.1830);{bslash}n	 Mon, 4 Dec 2006 10:46:00 -0800
   #1: from alvmbxw01.prod.quest.corp ([10.1.50.13]) by irvbhxw03.quest.com with Microsoft SMTPSVC(6.0.3790.1830);{bslash}n	 Mon, 4 Dec 2006 11:27:36 -0800
   #1: from alvmbxw01.prod.quest.corp ([10.1.50.13]) by irvbhxw03.quest.com with Microsoft SMTPSVC(6.0.3790.1830);{bslash}n	 Mon, 4 Dec 2006 11:55:17 -0800
|   r' [a-z]+ [a-z]+[0-9]+\.[a-z]+\.[a-z]+\.[a-z]+ \(\[[0-9]+\.[0-9]+\.[0-9]\.[0-9]+\]\) [a-z]+ [a-z]+[0-9]+\.[a-z]+\.[a-z]+\.[a-z]+ [a-z]+ [A-Z][a-z]+ [A-Z]+\([0-9]\.[0-9]\.[0-9]+\.[0-9]+\);\n\t [A-Z][a-z]+, [0-9] [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ -[0-9]+'
   #1: from ukbmbxw01.prod.quest.corp ([10.10.1.34]) by alvmbxw01.prod.quest.corp with Microsoft SMTPSVC(6.0.3790.1830);{bslash}n	 Mon, 4 Dec 2006 11:55:17 -0800
|   r' [a-z]+ [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+[ ]+\([A-Z]+ [a-z][0-9]+\.[a-z]+\.[a-z]+\.[a-z]+\.[a-z]+\) \([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\)\n[ ]+[a-z]+ [a-z]+[0-9]+\.[a-z]+\.[a-z]+[0-9]\.[a-z]+\.[a-z]+ [a-z]+ [A-Z]+; [A-Z][a-z]+, [0-9]+ [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ -[0-9]+'
   #1: from 66.94.237.55  (HELO n26.bullet.scd.yahoo.com) (66.94.237.55){bslash}n  by mta243.mail.re4.yahoo.com with SMTP; Sun, 06 May 2007 06:20:33 -0700
|   r' [a-z]+ \[[0-9]+\.[0-9]+\.[0-9]+\.[0-9]\] [a-z]+ [a-z][0-9]+\.[a-z]+\.[a-z]+\.[a-z]+\.[a-z]+ [a-z]+ [A-Z]+; [0-9]+ [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ -[0-9]+'
   #1: from [66.218.69.6] by n26.bullet.scd.yahoo.com with NNFMP; 06 May 2007 13:14:58 -0000
|   r' [a-z]+ \[[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\] [a-z]+ [a-z][0-9]\.[a-z]+\.[a-z]+\.[a-z]+\.[a-z]+ [a-z]+ [A-Z]+; [0-9]+ [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ -[0-9]+'
   #1: from [66.218.67.84] by t6.bullet.scd.yahoo.com with NNFMP; 06 May 2007 13:14:56 -0000
|   r' \([a-z]+ [0-9]+ [a-z]+ [a-z]+ [a-z]+ [0-9]+\); [0-9] [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ -[0-9]+'
   #1: (qmail 80547 invoked by uid 7800); 6 May 2007 13:14:56 -0000
   #1: (qmail 3343 invoked by uid 60001); 1 Jan 2008 17:47:41 -0000
   #1: (qmail 24956 invoked by uid 60001); 2 Jan 2008 08:21:54 -0000
   #1: (qmail 51172 invoked by uid 60001); 2 Jan 2008 14:43:30 -0000
   #1: (qmail 99197 invoked by uid 60001); 8 Jan 2008 11:09:10 -0000
   #1: (qmail 37753 invoked by uid 60001); 9 Jan 2008 14:49:36 -0000
|   r' [a-z]+ [a-z]+[0-9]+\.[a-z]+\.[a-z]+ \(\[[0-9]+\.[0-9]\.[0-9]+\.[0-9]+\]\) [a-z]+ [a-z]+[0-9]+\.[a-z]+\.[a-z]+ [a-z]+ [A-Z][a-z]+ [A-Z]+\([0-9]\.[0-9]\.[0-9]+\.[0-9]+\); [A-Z][a-z]+, [0-9]+ [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ -[0-9]+'
   #1: from irvbhxw02.quest.com ([10.1.120.32]) by alvbhxw01.quest.com with Microsoft SMTPSVC(6.0.3790.1830); Mon, 27 Aug 2007 09:21:56 -0700
|   r' [a-z]+ [a-z]+[0-9]+\.[a-z]+\.[a-z]+\.[a-z]+ \(\[[0-9]+\.[0-9]\.[0-9]\.[0-9]+\]\) [a-z]+ [a-z]+[0-9]+\.[a-z]+\.[a-z]+ [a-z]+ [A-Z][a-z]+ [A-Z]+\([0-9]\.[0-9]\.[0-9]+\.[0-9]+\); [A-Z][a-z]+, [0-9]+ [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ -[0-9]+'
   #1: from alvmbxw02.prod.quest.corp ([10.1.0.209]) by irvbhxw02.quest.com with Microsoft SMTPSVC(6.0.3790.1830); Mon, 27 Aug 2007 09:21:56 -0700
|   r' [a-z]+ [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+[ ]+\([A-Z]+ [a-z]+[0-9]+[a-z]\.[a-z][0-9]+\.[a-z]+\.[a-z]+\) \([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\)\n[ ]+[a-z]+ [a-z]+[0-9]+\.[a-z]+\.[a-z]+[0-9]\.[a-z]+\.[a-z]+ [a-z]+ [A-Z]+; [A-Z][a-z]+, [0-9]+ [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ -[0-9]+'
   #1: from 204.202.242.120  (HELO mail19d.g19.rapidsite.net) (204.202.242.120){bslash}n  by mta179.mail.re4.yahoo.com with SMTP; Tue, 04 Sep 2007 15:42:45 -0700
|   r' [a-z]+ [a-z]+[0-9]+\.[a-z]+[0-9]+\.[a-z]+\.[a-z]+\.[a-z]+ \([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\)\n\t[a-z]+ [a-z]+[0-9]+[a-z]\.[a-z][0-9]+\.[a-z]+\.[a-z]+ \([A-Z]+ [a-z]+ [0-9]\.[0-9]\.[0-9]+[a-z]+\) [a-z]+ [A-Z]+ [a-z]+ [0-9]-[0-9]+\n\t[a-z]+ <[a-z]+@[a-z]+\.[a-z]+>; [A-Z][a-z]+,[ ]+[0-9] [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ -[0-9]+ \([A-Z]+\)'
   #1: from mx19.stngva01.us.mxservers.net (204.202.242.102){bslash}n	by mail19d.g19.rapidsite.net (RS ver 1.0.95vs) with SMTP id 3-0134695763{bslash}n	for <lcherryh@yahoo.com>; Tue,  4 Sep 2007 18:42:44 -0400 (EDT)
|   r' [a-z]+ [a-z]+[0-9]+\.[a-z]+[0-9]+-[a-z]+\.[a-z]+ \[[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\] \([A-Z]+ [a-z]+[0-9]+\.[a-z]+[0-9]+-[a-z]+\.[a-z]+\)\n\t[a-z]+ [a-z]+[0-9]+\.[a-z]+[0-9]+\.[a-z]+\.[a-z]+\.[a-z]+ \([a-z]+_[a-z]+-[0-9]\.[0-9]\.[0-9]-[0-9]+[a-z][0-9]\) [a-z]+ [A-Z]+ [a-z]+ [0-9]+[a-z]+[0-9]+\.[0-9]+\.[0-9]+\.[a-z]+[0-9]+\.[a-z]+[0-9]+\.[a-z]+\.[a-z]+\.[a-z]+;\n\t[A-Z][a-z]+, [0-9]+ [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ -[0-9]+ \([A-Z]+\)'
   #1: from mxw1901.dulles19-verio.com [199.239.254.40] (EHLO mxw1901.dulles19-verio.com){bslash}n	by mx19.stngva01.us.mxservers.net (mxl_mta-1.3.8-10p4) with ESMTP id 36fddd64.4801.219.mx19.stngva01.us.mxservers.net;{bslash}n	Tue, 04 Sep 2007 18:42:43 -0400 (EDT)
|   r' \([a-z]+ [0-9]+ [a-z]+ [a-z]+ [a-z]+\); [0-9] [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ -[0-9]+'
   #1: (qmail 4324 invoked from network); 4 Sep 2007 22:42:43 -0000
|   r' [a-z]+ [a-z]+ \([A-Z]+ [A-Z][a-z]+[A-Z]+\) \([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\)\n[ ]+[a-z]+[ ]+[a-z]+ [A-Z]+; [0-9] [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ -[0-9]+'
   #1: from unknown (HELO VentiRD) (206.53.19.108){bslash}n  by  with SMTP; 4 Sep 2007 22:42:43 -0000
|   r' [a-z]+ [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+[ ]+\([A-Z]+ [a-z]+-[a-z]+-[0-9]+\.[a-z]+\.[a-z]+\.[a-z]+\) \([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\)\n[ ]+[a-z]+ [a-z]+[0-9]+\.[a-z]+\.[a-z]+\.[a-z]+\.[a-z]+ [a-z]+ [A-Z]+; [A-Z][a-z]+, [0-9]+ [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ -[0-9]+'
   #1: from 24.93.47.43  (EHLO ms-smtp-04.texas.rr.com) (24.93.47.43){bslash}n  by mta416.mail.mud.yahoo.com with SMTP; Sun, 16 Sep 2007 05:19:16 -0700
|   r' [a-z]+ [a-z]+[A-Z]+ \([a-z]+-[0-9]+-[0-9]+-[0-9]+-[0-9]+\.[a-z]+\.[a-z]+\.[a-z]+\.[a-z]+ \[[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\] \([a-z]+ [a-z]+ [a-z]+\)\)\n\t[a-z]+ [a-z]+-[a-z]+-[0-9]+\.[a-z]+\.[a-z]+\.[a-z]+ \([0-9]\.[0-9]+\.[0-9]/[0-9]\.[0-9]+\.[0-9]\) [a-z]+ [A-Z]+ [a-z]+ [a-z][0-9][A-Z]+[0-9][A-Z]+[0-9]+\n\t[a-z]+ <[A-Z]+[a-z]+@[a-z]+\.[a-z]+>; [A-Z][a-z]+, [0-9]+ [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ -[0-9]+ \([A-Z]+\)'
   #1: from ownerPC (cpe-72-183-113-90.austin.res.rr.com [72.183.113.90] (may be forged)){bslash}n	by ms-smtp-04.texas.rr.com (8.13.6/8.13.6) with SMTP id l8GCJ0SN027272{bslash}n	for <LCherryh@yahoo.com>; Sun, 16 Sep 2007 07:19:00 -0500 (CDT)
|   r' [a-z]+ [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+[ ]+\([A-Z]+ [a-z]+[0-9]+\.[a-z]+\.[a-z]+[0-9]\.[a-z]+\.[a-z]+\) \([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\)\n[ ]+[a-z]+ [a-z]+[0-9]+\.[a-z]+\.[a-z]+[0-9]\.[a-z]+\.[a-z]+ [a-z]+ [A-Z]+; [A-Z][a-z]+, [0-9]+ [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ -[0-9]+'
   #1: from 64.202.165.99  (HELO smtpauth05.prod.mesa1.secureserver.net) (64.202.165.99){bslash}n  by mta191.mail.re3.yahoo.com with SMTP; Fri, 19 Oct 2007 10:07:39 -0700
   #1: from 206.190.48.214  (HELO web52611.mail.re2.yahoo.com) (206.190.48.214){bslash}n  by mta234.mail.re3.yahoo.com with SMTP; Tue, 01 Jan 2008 09:47:41 -0800
   #1: from 206.190.48.213  (HELO web52610.mail.re2.yahoo.com) (206.190.48.213){bslash}n  by mta159.mail.re4.yahoo.com with SMTP; Wed, 09 Jan 2008 06:49:36 -0800
   #1: from 66.196.101.18  (HELO web59107.mail.re1.yahoo.com) (66.196.101.18){bslash}n  by mta230.mail.re4.yahoo.com with SMTP; Thu, 10 Jan 2008 10:17:16 -0800
|   r' \([a-z]+ [0-9]+ [a-z]+ [a-z]+ [a-z]+\); [0-9]+ [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ -[0-9]+'
   #1: (qmail 11404 invoked from network); 19 Oct 2007 17:07:38 -0000
|   r' [a-z]+ [a-z]+ \([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\)\n[ ]+[a-z]+ [a-z]+[0-9]+\.[a-z]+\.[a-z]+[0-9]\.[a-z]+\.[a-z]+ \([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\) [a-z]+ [A-Z]+; [0-9]+ [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ -[0-9]+'
   #1: from unknown (67.79.204.98){bslash}n  by smtpauth05.prod.mesa1.secureserver.net (64.202.165.99) with ESMTP; 19 Oct 2007 17:07:38 -0000
|   r' [a-z]+ [0-9]+\.[0-9]\.[0-9]+\.[0-9]+[ ]+\([A-Z]+ [A-Z]+[0-9]+\.[a-z]+\.[a-z]+\.[a-z]+\) \([0-9]+\.[0-9]\.[0-9]+\.[0-9]+\)\n[ ]+[a-z]+ [a-z]+[0-9]+\.[a-z]+\.[a-z]+[0-9]\.[a-z]+\.[a-z]+ [a-z]+ [A-Z]+; [A-Z][a-z]+, [0-9]+ [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ -[0-9]+'
   #1: from 213.1.252.135  (EHLO UKBXETW01.prod.quest.corp) (213.1.252.135){bslash}n  by mta199.mail.re4.yahoo.com with SMTP; Thu, 27 Dec 2007 05:49:46 -0800
   #1: from 213.1.252.135  (EHLO UKBXETW01.prod.quest.corp) (213.1.252.135){bslash}n  by mta186.mail.re4.yahoo.com with SMTP; Wed, 09 Jan 2008 03:36:08 -0800
|   r' [a-z]+ [A-Z]+[0-9]+\.[a-z]+\.[a-z]+\.[a-z]+ \([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\) [a-z]+\n [A-Z]+[0-9]+\.[a-z]+\.[a-z]+\.[a-z]+ \([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\) [a-z]+ [A-Z][a-z]+ [A-Z]+ [A-Z][a-z]+ \([A-Z]+\) [a-z]+\n [0-9]\.[0-9]\.[0-9]+\.[0-9]; [A-Z][a-z]+, [0-9]+ [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ \+[0-9]+'
   #1: from UKBXHTW02.prod.quest.corp (10.10.100.104) by{bslash}n UKBXETW01.prod.quest.corp (10.10.113.21) with Microsoft SMTP Server (TLS) id{bslash}n 8.1.240.5; Thu, 27 Dec 2007 13:46:44 +0000
   #1: from UKBXHTW02.prod.quest.corp (10.10.100.104) by{bslash}n UKBXETW01.prod.quest.corp (10.10.113.21) with Microsoft SMTP Server (TLS) id{bslash}n 8.1.240.5; Thu, 27 Dec 2007 14:06:33 +0000
   #1: from UKBXHTW02.prod.quest.corp (10.10.100.104) by{bslash}n UKBXETW01.prod.quest.corp (10.10.113.21) with Microsoft SMTP Server (TLS) id{bslash}n 8.1.240.5; Thu, 27 Dec 2007 14:06:43 +0000
   #1: from UKBXHTW02.prod.quest.corp (10.10.100.104) by{bslash}n UKBXETW01.prod.quest.corp (10.10.113.21) with Microsoft SMTP Server (TLS) id{bslash}n 8.1.240.5; Thu, 27 Dec 2007 14:07:06 +0000
   #1: from UKBXHTW02.prod.quest.corp (10.10.100.104) by{bslash}n UKBXETW01.prod.quest.corp (10.10.113.21) with Microsoft SMTP Server (TLS) id{bslash}n 8.1.240.5; Thu, 27 Dec 2007 16:32:35 +0000
|   r' [a-z]+ [A-Z]+[0-9]+\.[a-z]+\.[a-z]+\.[a-z]+ \(\[[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\]\) [a-z]+\n [A-Z]+[0-9]+\.[a-z]+\.[a-z]+\.[a-z]+ \(\[[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\]\) [a-z]+ [a-z]+; [A-Z][a-z]+, [0-9]+ [A-Z][a-z]+ [0-9]+\n [0-9]+:[0-9]+:[0-9]+ \+[0-9]+'
   #1: from UKBXMBW01.prod.quest.corp ([10.10.100.101]) by{bslash}n UKBXHTW02.prod.quest.corp ([10.10.100.104]) with mapi; Thu, 27 Dec 2007{bslash}n 13:49:24 +0000
   #1: from UKBXMBW01.prod.quest.corp ([10.10.100.101]) by{bslash}n UKBXHTW02.prod.quest.corp ([10.10.100.104]) with mapi; Thu, 27 Dec 2007{bslash}n 14:09:14 +0000
   #1: from UKBXMBW01.prod.quest.corp ([10.10.100.101]) by{bslash}n UKBXHTW02.prod.quest.corp ([10.10.100.104]) with mapi; Thu, 27 Dec 2007{bslash}n 14:09:24 +0000
   #1: from UKBXMBW01.prod.quest.corp ([10.10.100.101]) by{bslash}n UKBXHTW02.prod.quest.corp ([10.10.100.104]) with mapi; Thu, 27 Dec 2007{bslash}n 14:09:47 +0000
   #1: from UKBXMBW01.prod.quest.corp ([10.10.100.101]) by{bslash}n UKBXHTW02.prod.quest.corp ([10.10.100.104]) with mapi; Thu, 27 Dec 2007{bslash}n 16:35:17 +0000
|   r' [a-z]+ [0-9]+\.[0-9]\.[0-9]+\.[0-9]+[ ]+\([A-Z]+ [A-Z]+[0-9]+\.[a-z]+\.[a-z]+\.[a-z]+\) \([0-9]+\.[0-9]\.[0-9]+\.[0-9]+\)\n[ ]+[a-z]+ [a-z]+[0-9]+\.[a-z]+\.[a-z]+\.[a-z]+\.[a-z]+ [a-z]+ [A-Z]+; [A-Z][a-z]+, [0-9]+ [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ -[0-9]+'
   #1: from 213.1.252.135  (EHLO UKBXETW01.prod.quest.corp) (213.1.252.135){bslash}n  by mta312.mail.mud.yahoo.com with SMTP; Thu, 27 Dec 2007 06:09:16 -0800
   #1: from 213.1.252.135  (EHLO UKBXETW01.prod.quest.corp) (213.1.252.135){bslash}n  by mta303.mail.mud.yahoo.com with SMTP; Thu, 27 Dec 2007 06:19:26 -0800
   #1: from 213.1.252.135  (EHLO UKBXETW01.prod.quest.corp) (213.1.252.135){bslash}n  by mta303.mail.mud.yahoo.com with SMTP; Thu, 27 Dec 2007 06:19:27 -0800
   #1: from 213.1.252.135  (EHLO UKBXETW01.prod.quest.corp) (213.1.252.135){bslash}n  by mta219.mail.mud.yahoo.com with SMTP; Thu, 27 Dec 2007 08:36:21 -0800
|   r' [a-z]+ [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+[ ]+\([A-Z]+ [a-z]+[0-9]-[a-z]+[0-9]-[a-z][0-9]\.[a-z]+[0-9]\.[a-z]+\.[a-z]+\) \([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\)\n[ ]+[a-z]+ [a-z]+[0-9]+\.[a-z]+\.[a-z]+[0-9]\.[a-z]+\.[a-z]+ [a-z]+ [A-Z]+; [A-Z][a-z]+, [0-9]+ [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ -[0-9]+'
   #1: from 65.54.246.77  (EHLO bay0-omc1-s5.bay0.hotmail.com) (65.54.246.77){bslash}n  by mta233.mail.re4.yahoo.com with SMTP; Sun, 30 Dec 2007 16:00:48 -0800
|   r' [a-z]+ [A-Z]+[0-9]+-[A-Z][0-9]+ \(\[[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\]\) [a-z]+ [a-z]+[0-9]-[a-z]+[0-9]-[a-z][0-9]\.[a-z]+[0-9]\.[a-z]+\.[a-z]+ [a-z]+ [A-Z][a-z]+ [A-Z]+\([0-9]\.[0-9]\.[0-9]+\.[0-9]+\);\n\t [A-Z][a-z]+, [0-9]+ [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ -[0-9]+'
   #1: from BAY124-W34 ([207.46.11.197]) by bay0-omc1-s5.bay0.hotmail.com with Microsoft SMTPSVC(6.0.3790.3959);{bslash}n	 Sun, 30 Dec 2007 15:56:16 -0800
|   r'Date:[A-Z][a-z]+:[A-Z][a-z]+:[A-Z][a-z]:[A-Z]+-[A-Z][a-z]+:[A-Z][a-z]+-[A-Z][a-z]+:[A-Z][a-z]+-[A-Z][a-z]+-[A-Z][a-z]+:[A-Z][a-z]+-[A-Z]+;\n[ ]+[a-z]=[A-Z][a-z][0-9][A-Z][a-z]+[A-Z]+[a-z][A-Z]+[a-z][A-Z][0-9][A-Z][a-z]+[A-Z][0-9][a-z][A-Z][a-z][A-Z]+[a-z][A-Z]+[a-z]/[A-Z][a-z]+[A-Z][a-z]+[A-Z][a-z]+[A-Z]+[a-z][A-Z]+[a-z][A-Z]+[a-z][A-Z][a-z]+[A-Z]+[a-z][A-Z][0-9][A-Z]+[a-z]+[A-Z][a-z][A-Z]+[a-z][A-Z]+[a-z][A-Z][a-z][0-9][a-z][A-Z][a-z]+\+[a-z][A-Z][a-z]+[0-9][a-z][A-Z][a-z][A-Z][a-z]/[a-z]+[A-Z][a-z][A-Z][a-z][0-9][a-z][A-Z]+[0-9][A-Z][0-9][A-Z][a-z]+[A-Z][0-9]+[A-Z]+[a-z][A-Z][a-z]+[A-Z][a-z]+[0-9][a-z][A-Z][a-z]+[A-Z][0-9][a-z][A-Z]+[a-z][A-Z][a-z]+[A-Z]+[a-z]+[0-9][a-z][0-9][A-Z]+/[a-z][0-9][a-z][0-9][a-z][A-Z][a-z]+[A-Z][a-z]+[A-Z][0-9]+[A-Z]+=;'
   #1:Date:From:Subject:To:MIME-Version:Content-Type:Content-Transfer-Encoding:Message-ID;{bslash}n  b=Yt8DawZHkEGOXhZ7TwxR6bOdFRqLTGKx/AlbFflKjipuREsYIRfADRYnIosHEYXTgP4KOupOaTEGUyKPxSm6sYlb+wIae6kNqUq/yrSuKo0eGF3W4GtfO016EUOnFbsAce6qRfaA3rHFaTtvOFPnj3c1MT/d3k5xWrlYtpT17OE=;
|   r' [a-z]+ \[[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\] [a-z]+ [a-z]+[0-9]+\.[a-z]+\.[a-z]+[0-9]\.[a-z]+\.[a-z]+ [a-z]+ [A-Z]+; [A-Z][a-z]+, [0-9]+ [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ [A-Z]+'
   #1: from [132.66.201.218] by web52611.mail.re2.yahoo.com via HTTP; Tue, 01 Jan 2008 09:47:41 PST
   #1: from [132.66.201.109] by web52601.mail.re2.yahoo.com via HTTP; Wed, 02 Jan 2008 00:21:54 PST
   #1: from [132.66.201.218] by web52604.mail.re2.yahoo.com via HTTP; Wed, 02 Jan 2008 06:43:30 PST
   #1: from [132.66.201.158] by web52605.mail.re2.yahoo.com via HTTP; Tue, 08 Jan 2008 03:09:10 PST
   #1: from [132.66.201.189] by web52610.mail.re2.yahoo.com via HTTP; Wed, 09 Jan 2008 06:49:36 PST
   #1: from [12.173.168.199] by web59107.mail.re1.yahoo.com via HTTP; Thu, 10 Jan 2008 10:17:16 PST
   #1: from [132.66.201.206] by web52605.mail.re2.yahoo.com via HTTP; Mon, 14 Jan 2008 09:14:04 PST
|   r' [a-z]+ [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+[ ]+\([A-Z]+ [a-z]+[0-9]-[a-z]+[0-9]-[a-z][0-9]+\.[a-z]+[0-9]\.[a-z]+\.[a-z]+\) \([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\)\n[ ]+[a-z]+ [a-z]+[0-9]+\.[a-z]+\.[a-z]+\.[a-z]+\.[a-z]+ [a-z]+ [A-Z]+; [A-Z][a-z]+, [0-9]+ [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ -[0-9]+'
   #1: from 65.54.246.83  (EHLO bay0-omc1-s11.bay0.hotmail.com) (65.54.246.83){bslash}n  by mta253.mail.mud.yahoo.com with SMTP; Tue, 01 Jan 2008 17:03:04 -0800
   #1: from 65.54.246.86  (EHLO bay0-omc1-s14.bay0.hotmail.com) (65.54.246.86){bslash}n  by mta203.mail.mud.yahoo.com with SMTP; Thu, 03 Jan 2008 17:29:42 -0800
|   r' [a-z]+ [A-Z]+[0-9]+-[A-Z][0-9] \(\[[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\]\) [a-z]+ [a-z]+[0-9]-[a-z]+[0-9]-[a-z][0-9]+\.[a-z]+[0-9]\.[a-z]+\.[a-z]+ [a-z]+ [A-Z][a-z]+ [A-Z]+\([0-9]\.[0-9]\.[0-9]+\.[0-9]+\);\n\t [A-Z][a-z]+, [0-9] [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ -[0-9]+'
   #1: from BAY124-W4 ([207.46.11.167]) by bay0-omc1-s11.bay0.hotmail.com with Microsoft SMTPSVC(6.0.3790.3959);{bslash}n	 Tue, 1 Jan 2008 17:00:50 -0800
   #1: from BAY124-W7 ([207.46.11.170]) by bay0-omc1-s14.bay0.hotmail.com with Microsoft SMTPSVC(6.0.3790.3959);{bslash}n	 Thu, 3 Jan 2008 17:25:28 -0800
|   r' [a-z]+ [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+[ ]+\([A-Z]+ [a-z]+[0-9]+\.[a-z]+\.[a-z]+[0-9]\.[a-z]+\.[a-z]+\) \([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\)\n[ ]+[a-z]+ [a-z]+[0-9]+\.[a-z]+\.[a-z]+\.[a-z]+\.[a-z]+ [a-z]+ [A-Z]+; [A-Z][a-z]+, [0-9]+ [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ -[0-9]+'
   #1: from 206.190.48.204  (HELO web52601.mail.re2.yahoo.com) (206.190.48.204){bslash}n  by mta233.mail.mud.yahoo.com with SMTP; Wed, 02 Jan 2008 00:21:55 -0800
   #1: from 206.190.48.207  (HELO web52604.mail.re2.yahoo.com) (206.190.48.207){bslash}n  by mta499.mail.mud.yahoo.com with SMTP; Wed, 02 Jan 2008 06:43:30 -0800
   #1: from 206.190.48.208  (HELO web52605.mail.re2.yahoo.com) (206.190.48.208){bslash}n  by mta352.mail.mud.yahoo.com with SMTP; Tue, 08 Jan 2008 03:09:10 -0800
   #1: from 206.190.48.208  (HELO web52605.mail.re2.yahoo.com) (206.190.48.208){bslash}n  by mta500.mail.mud.yahoo.com with SMTP; Mon, 14 Jan 2008 09:14:04 -0800
|   r'Date:[A-Z][a-z]+:[A-Z][a-z]+:[A-Z][a-z]:[A-Z]+-[A-Z][a-z]+:[A-Z][a-z]+-[A-Z][a-z]+:[A-Z][a-z]+-[A-Z][a-z]+-[A-Z][a-z]+:[A-Z][a-z]+-[A-Z]+;\n[ ]+[a-z]=[A-Z]+[a-z][0-9][a-z][A-Z]+[a-z][A-Z]+[a-z]/[A-Z]+[a-z]+[A-Z][a-z][0-9][a-z][A-Z]+[a-z][0-9][A-Z][a-z]+[A-Z][0-9][A-Z][0-9]+[A-Z][a-z]+[0-9][a-z][A-Z][a-z]+[0-9][A-Z]+[a-z][A-Z]+[a-z]+[0-9][a-z][A-Z]+[a-z][0-9]+[a-z]+[A-Z]+[0-9][A-Z]+[0-9][a-z]+[A-Z][a-z][A-Z][a-z][A-Z]+[a-z]+[0-9][a-z][0-9][A-Z][a-z]+[A-Z][a-z][A-Z][0-9][A-Z]+[a-z]\+[A-Z][a-z]+[A-Z]+[a-z]+[0-9][a-z][0-9][A-Z]+[a-z]+[A-Z][a-z][A-Z]+[a-z]+[0-9][a-z][0-9][a-z][A-Z][a-z][A-Z][a-z]+[A-Z][0-9]+[A-Z]+[0-9][A-Z][a-z]+[A-Z]+[a-z][A-Z]+[a-z][A-Z]+[0-9][a-z]+[A-Z][a-z]+[A-Z][a-z]+[A-Z][a-z]+[A-Z]+=;'
   #1:Date:From:Subject:To:MIME-Version:Content-Type:Content-Transfer-Encoding:Message-ID;{bslash}n  b=OLOb9kDTZbLRy/EPgjeZx4hHMYu0NhhQ7Y38Idcy4yQix4JJlHYqszp0hSHk05zxiVRU4HZ3swacvnDjSnHTdc9d0JztcUnQ9LHQr+GgcGKon9s1ZPpnaNcBQJxncbex3m1gDoZsqY95NF1PoyrYPwKNrJK8krEnbEybFcjgcNQ=;
|   r'Date:[A-Z][a-z]+:[A-Z][a-z]+:[A-Z][a-z]:[A-Z]+-[A-Z][a-z]+:[A-Z][a-z]+-[A-Z][a-z]+:[A-Z][a-z]+-[A-Z][a-z]+-[A-Z][a-z]+:[A-Z][a-z]+-[A-Z]+;\n[ ]+[a-z]=[a-z]+[A-Z]+[0-9][a-z][A-Z][a-z]+[A-Z]+[a-z][A-Z][0-9][A-Z]\+[0-9][A-Z][0-9][a-z]+[A-Z][a-z][0-9][a-z]+[0-9][a-z][A-Z]/[a-z][A-Z]+[0-9][A-Z]+[0-9][a-z][A-Z][a-z][A-Z]/[A-Z][a-z]+[A-Z][a-z][A-Z][a-z][A-Z][a-z][A-Z]+[0-9][A-Z][0-9][a-z][0-9][A-Z]/[0-9][A-Z]+[a-z]+[A-Z]+[a-z][0-9][A-Z]+[a-z]/[A-Z]+[a-z]+[A-Z]+[a-z][0-9][a-z][A-Z][0-9][a-z]+[0-9][a-z][A-Z]/[A-Z][a-z]+[A-Z]+[a-z][A-Z]+[a-z]+[A-Z][a-z]+[A-Z]+[a-z][A-Z][0-9][a-z][A-Z]+[a-z][0-9][a-z]+[A-Z][0-9][A-Z][a-z][A-Z]+[0-9]/[A-Z]+\+[0-9][A-Z][a-z]/[a-z][A-Z]+[a-z]+[A-Z][a-z][A-Z]+[a-z]+[A-Z][0-9][a-z]+/[a-z][A-Z][0-9][a-z][A-Z][a-z][A-Z][a-z]=;'
   #1:Date:From:Subject:To:MIME-Version:Content-Type:Content-Transfer-Encoding:Message-ID;{bslash}n  b=vjYO9jMudpcsEIkF1M+3M7qyJk8zid0xE/eGJXH8EX4gYzB/IqcJsKcDuSX5K0m7X/6WHQUvqOVp6SCe/KUkebGWp9jT1erevz3vA/DmiMOAQfBWKpvCeweIPzA6zKGq5fyN6OyTH0/ZT+2At/vIVggjRnBLajW0pe/dJ8bLqNo=;
|   r'Date:[A-Z][a-z]+:[A-Z][a-z]+:[A-Z][a-z]:[A-Z]+-[A-Z][a-z]+:[A-Z][a-z]+-[A-Z][a-z]+:[A-Z][a-z]+-[A-Z][a-z]+-[A-Z][a-z]+:[A-Z][a-z]+-[A-Z]+;\n[ ]+[a-z]=[a-z]+[A-Z]\+[a-z]+[0-9]+[a-z][A-Z]+[a-z][A-Z]+[a-z]+[A-Z][a-z]+[A-Z][a-z][A-Z]+[0-9][A-Z][a-z]\+[A-Z]+[a-z][A-Z]+[0-9][a-z][A-Z][a-z][A-Z]+[a-z][A-Z]+[0-9][a-z]+[A-Z]+[a-z][0-9]+[A-Z][a-z]+[0-9][a-z]+[0-9][A-Z][0-9]/[A-Z][a-z][A-Z][a-z]+[A-Z]+[a-z]+[0-9][A-Z]+[a-z]+[0-9][A-Z]+[a-z]+[A-Z]+[0-9][a-z][A-Z]+[a-z]+[0-9][a-z]+\+[a-z][A-Z][0-9]+[A-Z]+[a-z]+[0-9]+[a-z][A-Z][0-9][a-z][A-Z][a-z]+[A-Z][0-9]+[a-z][A-Z][a-z][0-9][A-Z][0-9][A-Z][0-9][A-Z][a-z][0-9][A-Z][a-z]+[0-9][A-Z][a-z][0-9][A-Z][a-z]+[A-Z][a-z][A-Z][a-z][A-Z]+[a-z]+[A-Z]+=;'
   #1:Date:From:Subject:To:MIME-Version:Content-Type:Content-Transfer-Encoding:Message-ID;{bslash}n  b=goM+os272cDHNKVoWEccwBtsoNiOYN7Yp+LSpPY0lKrSBXhJLDE6csqiwLWz91Ura8hmayioa7O8/ToYjeYPkw0LKcr7VJDCJFOheHPL7zCSkg8zd+aD194BQRjt82bP6oDqeE44rMk8W7N1Im0Umr2Sf5GceRvJfIAokUXUWAY=;
|   r' [a-z]+ [A-Z]+[0-9]+\.[a-z]+\.[a-z]+\.[a-z]+ \([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\) [a-z]+\n [A-Z]+[0-9]+\.[a-z]+\.[a-z]+\.[a-z]+ \([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\) [a-z]+ [A-Z][a-z]+ [A-Z]+ [A-Z][a-z]+ \([A-Z]+\) [a-z]+\n [0-9]\.[0-9]\.[0-9]+\.[0-9]; [A-Z][a-z]+, [0-9] [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ \+[0-9]+'
   #1: from UKBXHTW01.prod.quest.corp (10.10.100.103) by{bslash}n UKBXETW01.prod.quest.corp (10.10.113.21) with Microsoft SMTP Server (TLS) id{bslash}n 8.1.240.5; Wed, 9 Jan 2008 11:32:48 +0000
|   r' [a-z]+ [A-Z]+[0-9]+\.[a-z]+\.[a-z]+\.[a-z]+ \(\[[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\]\) [a-z]+\n [A-Z]+[0-9]+\.[a-z]+\.[a-z]+\.[a-z]+ \(\[[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\]\) [a-z]+ [a-z]+; [A-Z][a-z]+, [0-9] [A-Z][a-z]+ [0-9]+\n [0-9]+:[0-9]+:[0-9]+ \+[0-9]+'
   #1: from UKBXMBW01.prod.quest.corp ([10.10.100.101]) by{bslash}n UKBXHTW01.prod.quest.corp ([10.10.100.103]) with mapi; Wed, 9 Jan 2008{bslash}n 11:35:41 +0000
|   r'Date:[A-Z][a-z]+:[A-Z][a-z]+:[A-Z][a-z]:[A-Z]+-[A-Z][a-z]+:[A-Z][a-z]+-[A-Z][a-z]+:[A-Z][a-z]+-[A-Z][a-z]+-[A-Z][a-z]+:[A-Z][a-z]+-[A-Z]+;\n[ ]+[a-z]=[0-9][a-z]+[A-Z]+[0-9]+[A-Z]+[a-z][A-Z][a-z][A-Z]+[a-z][A-Z][0-9][a-z][A-Z]+[a-z]+[A-Z][0-9][a-z][0-9][A-Z]+[a-z][A-Z][0-9][a-z][A-Z]+[a-z]+/[a-z]+[A-Z]+[a-z]+[0-9][A-Z]+[a-z][0-9][a-z][A-Z][a-z]+[0-9][a-z][0-9][a-z]+[A-Z]+[a-z][0-9][a-z][A-Z][0-9][A-Z][a-z][A-Z][a-z][0-9][A-Z][0-9][a-z]+/[a-z]+[A-Z][0-9][A-Z][a-z][A-Z][a-z]+[0-9][a-z]+[A-Z]+/[0-9][a-z]+[A-Z][a-z][0-9][A-Z]+[0-9][a-z]+[A-Z][a-z]+[0-9][A-Z]+[a-z][A-Z][a-z][A-Z]/[A-Z]+[0-9]+[A-Z][a-z][0-9][A-Z]+[0-9]+[a-z][A-Z][a-z][A-Z][a-z][0-9][A-Z][a-z][A-Z]+[a-z][A-Z]+[a-z][A-Z][a-z][0-9][A-Z][0-9][a-z][0-9][A-Z][a-z][A-Z][0-9][A-Z]+=;'
   #1:Date:From:Subject:To:MIME-Version:Content-Type:Content-Transfer-Encoding:Message-ID;{bslash}n  b=6bnLOAZ101ZJgEoPCkD5sMTWAsaY0b7IXAoH4tELhq/qzCUhc6ZVUTq2mTfp5c1rxLTk7jN1OaBp3Z4vh/jtgzT1CwSyod3annDBKY/7nwqUs1WKUA9xfbrPkg9SSUxOmK/SQU23Xr5MY74oBdMa8ZjEVaZRrNv7N9z6FfN3ZKE=;
|   r' \([a-z]+ [0-9]+ [a-z]+ [a-z]+ [a-z]+ [0-9]+\); [0-9]+ [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ -[0-9]+'
   #1: (qmail 90080 invoked by uid 60001); 10 Jan 2008 18:17:16 -0000
   #1: (qmail 6927 invoked by uid 60001); 14 Jan 2008 17:14:04 -0000
|   r'Date:[A-Z][a-z]+:[A-Z][a-z]+:[A-Z][a-z]:[A-Z]+-[A-Z][a-z]+:[A-Z][a-z]+-[A-Z][a-z]+:[A-Z][a-z]+-[A-Z][a-z]+-[A-Z][a-z]+:[A-Z][a-z]+-[A-Z]+;\n[ ]+[a-z]=[A-Z]+[a-z]+[A-Z]+[a-z][A-Z]+[0-9]+[a-z][0-9]+[A-Z][0-9][a-z][0-9][A-Z]+[a-z]+[0-9][a-z][A-Z]+[a-z][0-9]+[a-z][A-Z][a-z][A-Z][a-z][A-Z]+[a-z][0-9]+[A-Z]+[a-z][A-Z][a-z][A-Z]+[0-9][a-z]+[A-Z]+[a-z]+\+[0-9][A-Z][a-z][A-Z][a-z]+[0-9][a-z][A-Z][0-9]+[A-Z]+[a-z][0-9][A-Z]+[0-9][A-Z][a-z][A-Z][a-z]/[a-z]+[0-9][a-z][A-Z][a-z]+[0-9][a-z]+[A-Z]+[a-z][A-Z]+[a-z]+[A-Z]+[a-z][0-9][a-z]+[A-Z]+[a-z][A-Z]+[0-9][A-Z][a-z]+[A-Z]+[a-z][A-Z]+[a-z][A-Z]+[a-z][A-Z][0-9][a-z]+[A-Z]+[0-9]+[A-Z]+[a-z]+[A-Z]+[a-z][0-9][a-z]+[A-Z][a-z][A-Z]+=;'
   #1:Date:From:Subject:To:MIME-Version:Content-Type:Content-Transfer-Encoding:Message-ID;{bslash}n  b=UIuxEGGEuSKMY06t95Z6i7EVSMQiohe4gITUNGk70aEhWoDPj65GARkHrYNF2xsFGSci+3EgIvto9sS56VCPRg3KA7UaXn/aoch4sNqc8snqYVUsGPURJgpXGXp7mpvUCyGK8MbrODnBMvEErX7nleRL171JOMddDBv6wqbGqWE=;
|   r' [a-z]+ [0-9]+\.[0-9]+\.[0-9]\.[0-9]+[ ]+\([A-Z]+ [A-Z]+-[A-Z]+[0-9]+\.[A-Z]+\.[A-Z][a-z]+\.[a-z]+\) \([0-9]+\.[0-9]+\.[0-9]\.[0-9]+\)\n[ ]+[a-z]+ [a-z]+[0-9]+\.[a-z]+\.[a-z]+\.[a-z]+\.[a-z]+ [a-z]+ [A-Z]+; [A-Z][a-z]+, [0-9]+ [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ -[0-9]+'
   #1: from 147.154.9.220  (EHLO NOAADC-MSW03.NOA.Alcoa.com) (147.154.9.220){bslash}n  by mta188.mail.mud.yahoo.com with SMTP; Sat, 12 Jan 2008 20:00:24 -0800
|   r' [a-z]+ [A-Z]+-[A-Z]+[0-9]+\.[A-Z]+\.[A-Z][a-z]+\.[a-z]+ \([a-z]+ \[[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\]\) [a-z]+ [A-Z]+-[A-Z]+[0-9]+\.[A-Z]+\.[A-Z][a-z]+\.[a-z]+\n \([A-Z][a-z]+ [A-Z][a-z]+ [A-Z]+ [0-9]\.[0-9]\.[0-9]+\) [a-z]+ [A-Z]+ [a-z]+ <[A-Z][0-9]+[a-z]+[0-9]+[a-z][0-9]+[a-z]+[0-9]+@[A-Z]+-[A-Z]+[0-9]+\.[A-Z]+\.[A-Z][a-z]+\.[a-z]+> [a-z]+ <[A-Z]+[a-z]+@[a-z]+\.[a-z]+>;\n [A-Z][a-z]+, [0-9]+ [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ -[0-9]+'
   #1: from NOANDC-MXI03.NOA.Alcoa.com (unverified [132.226.228.13]) by NOAADC-MSW03.NOA.Alcoa.com{bslash}n (Content Technologies SMTPRS 4.3.20) with ESMTP id <T847ca44009939a09dc504@NOAADC-MSW03.NOA.Alcoa.com> for <LCherryh@yahoo.com>;{bslash}n Sat, 12 Jan 2008 23:00:22 -0500
|   r' [a-z]+ [A-Z]+-[A-Z]+[0-9]+\.[A-Z]+\.[A-Z][a-z]+\.[a-z]+ \(\[[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\]\) [a-z]+ [A-Z]+-[A-Z]+[0-9]+\.[A-Z]+\.[A-Z][a-z]+\.[a-z]+ [a-z]+ [A-Z][a-z]+ [A-Z]+\([0-9]\.[0-9]\.[0-9]+\.[0-9]+\);\n\t [A-Z][a-z]+, [0-9]+ [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ -[0-9]+'
   #1: from NOANDC-MXU24.NOA.Alcoa.com ([132.226.228.204]) by NOANDC-MXI03.NOA.Alcoa.com with Microsoft SMTPSVC(6.0.3790.3959);{bslash}n	 Sat, 12 Jan 2008 23:00:21 -0500
|   r' [a-z]+ [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+[ ]+\([A-Z]+ [a-z]+-[a-z]+\.[a-z]+\.[a-z]+\.[a-z]+\) \([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\)\n[ ]+[a-z]+ [a-z]+[0-9]+\.[a-z]+\.[a-z]+[0-9]\.[a-z]+\.[a-z]+ [a-z]+ [A-Z]+; [A-Z][a-z]+, [0-9]+ [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ -[0-9]+'
   #1: from 71.74.56.123  (EHLO hrndva-omtalb.mail.rr.com) (71.74.56.123){bslash}n  by mta268.mail.re4.yahoo.com with SMTP; Mon, 14 Jan 2008 06:59:02 -0800
   #1: from 71.74.56.123  (EHLO hrndva-omtalb.mail.rr.com) (71.74.56.123){bslash}n  by mta173.mail.re2.yahoo.com with SMTP; Tue, 15 Jan 2008 11:59:11 -0800
   #1: from 71.74.56.123  (EHLO hrndva-omtalb.mail.rr.com) (71.74.56.123){bslash}n  by mta294.mail.re4.yahoo.com with SMTP; Tue, 15 Jan 2008 21:27:59 -0800
|   r' [a-z]+ [A-Z][a-z][A-Z][a-z]+[A-Z][a-z]+ \(\[[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\]\) [a-z]+ [a-z]+-[a-z]+[0-9]+\.[a-z]+\.[a-z]+\.[a-z]+\n[ ]+[a-z]+ [A-Z]+\n[ ]+[a-z]+ <[0-9]+\.[A-Z]+[0-9]+\.[a-z]+-[a-z]+[0-9]+\.[a-z]+\.[a-z]+\.[a-z]+@[A-Z][a-z][A-Z][a-z]+[A-Z][a-z]+>\n[ ]+[a-z]+ <[a-z]+@[a-z]+\.[a-z]+>; [A-Z][a-z]+, [0-9]+ [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ \+[0-9]+'
   #1: from DeAtleyFloor ([70.112.85.169]) by hrndva-omta02.mail.rr.com{bslash}n          with SMTP{bslash}n          id <20080114145902.SLKA7595.hrndva-omta02.mail.rr.com@DeAtleyFloor>{bslash}n          for <lcherryh@yahoo.com>; Mon, 14 Jan 2008 14:59:02 +0000
   #1: from DeAtleyFloor ([70.112.85.169]) by hrndva-omta03.mail.rr.com{bslash}n          with SMTP{bslash}n          id <20080115195911.ZCKR16504.hrndva-omta03.mail.rr.com@DeAtleyFloor>{bslash}n          for <lcherryh@yahoo.com>; Tue, 15 Jan 2008 19:59:11 +0000
|   r'Date:[A-Z][a-z]+:[A-Z][a-z]+:[A-Z][a-z]:[A-Z]+-[A-Z][a-z]+:[A-Z][a-z]+-[A-Z][a-z]+:[A-Z][a-z]+-[A-Z][a-z]+-[A-Z][a-z]+:[A-Z][a-z]+-[A-Z]+;\n[ ]+[a-z]=[a-z][0-9][a-z][0-9][a-z][A-Z][0-9][a-z][A-Z]+[a-z]+[A-Z]+[a-z][0-9][A-Z][a-z][A-Z][a-z][A-Z][a-z][A-Z]+[a-z][A-Z][a-z][A-Z]+[0-9][a-z][A-Z][a-z][0-9][a-z][A-Z][a-z][A-Z][a-z][A-Z][a-z]\+[a-z][A-Z]+[a-z]+[0-9][A-Z][a-z][A-Z]+[a-z][0-9]/[a-z][0-9][a-z][A-Z][a-z]+[A-Z]+[0-9]/[a-z][A-Z]+[0-9][a-z][A-Z]+[a-z]+[A-Z]+[a-z][0-9]+[a-z][A-Z]+[0-9][a-z]+[A-Z][0-9]/[0-9][A-Z]+[0-9][a-z]+[A-Z][0-9][a-z][A-Z][a-z]+[0-9][A-Z][0-9][a-z][A-Z][0-9][a-z][A-Z][a-z]+[A-Z]+[0-9]+[A-Z][0-9][a-z]/[0-9][a-z]+[A-Z]+[a-z][A-Z]+[0-9][A-Z][a-z]+[A-Z][a-z][A-Z]+[0-9]+[A-Z]+[0-9][A-Z][0-9][A-Z][a-z]+[0-9][A-Z]+[a-z]+=;'
   #1:Date:From:Subject:To:MIME-Version:Content-Type:Content-Transfer-Encoding:Message-ID;{bslash}n  b=z8g4hF0iQONDWDroooZNs4IqVlPzVMvUtJRD2dYv6kHgFcLr+oLMys8EyJNo4/z9bVlysIP8/mYK2vNGXpqiPYu25uHA1jwS6/9XED0mzR5iXnq2B1tZ4nPjsLTEP63V7w/8wiBOTyCM5SaizZyXLAW24UXHN5W7Hpsr7PLUMiw=;
|   r' [a-z]+ [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+[ ]+\([A-Z]+ [a-z]+\.[A-Z][a-z]+[A-Z][a-z]+[A-Z][a-z]+\.[a-z]+\) \([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\)\n[ ]+[a-z]+ [a-z]+[0-9]+\.[a-z]+\.[a-z]+[0-9]\.[a-z]+\.[a-z]+ [a-z]+ [A-Z]+; [A-Z][a-z]+, [0-9]+ [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ -[0-9]+'
   #1: from 71.41.16.226  (EHLO server.RiverRanchRadiology.local) (71.41.16.226){bslash}n  by mta243.mail.re4.yahoo.com with SMTP; Mon, 14 Jan 2008 13:09:54 -0800
|   r' [a-z]+ [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+[ ]+\([A-Z]+ [a-z]+[0-9]+\.[a-z]+\.[a-z]+\.[a-z]+\.[a-z]+\) \([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\)\n[ ]+[a-z]+ [a-z]+[0-9]+\.[a-z]+\.[a-z]+\.[a-z]+\.[a-z]+ [a-z]+ [A-Z]+; [A-Z][a-z]+, [0-9]+ [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ -[0-9]+'
   #1: from 209.86.89.73  (EHLO smtpauth13.mail.atl.earthlink.net) (209.86.89.73){bslash}n  by mta544.mail.mud.yahoo.com with SMTP; Tue, 15 Jan 2008 06:13:07 -0800
|   r' [a-z]+ \[[0-9]\.[0-9]+\.[0-9]+\.[0-9]+\] \([a-z]+=[a-z]+[0-9]+[a-z][0-9]+[a-z][0-9]+\)\n\t[a-z]+ [a-z]+[0-9]+\.[a-z]+\.[a-z]+\.[a-z]+\.[a-z]+ [a-z]+ [a-z]+ \([A-Z][a-z]+ [0-9]\.[0-9]+\)\n\t[a-z]+ [0-9][A-Z]+[a-z][A-Z]+-[0-9]+[a-z][0-9]-[A-Z]+\n\t[a-z]+ [A-Z]+[a-z]+@[a-z]+\.[a-z]+; [A-Z][a-z]+, [0-9]+ [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ -[0-9]+'
   #1: from [4.230.144.125] (helo=your27e1513d96){bslash}n	by smtpauth13.mail.atl.earthlink.net with asmtp (Exim 4.34){bslash}n	id 1JEmXH-0004r3-MM{bslash}n	for LCherryh@yahoo.com; Tue, 15 Jan 2008 09:13:04 -0500
|   r' [a-z]+ [A-Z]+[0-9][A-Z][0-9][A-Z][0-9][A-Z]+ \(\[[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\]\)\n[ ]+[a-z]+ [a-z]+-[a-z]+[0-9]+\.[a-z]+\.[a-z]+\.[a-z]+ [a-z]+ [A-Z]+\n[ ]+[a-z]+ <[0-9]+\.[A-Z]+[0-9]+\.[a-z]+-[a-z]+[0-9]+\.[a-z]+\.[a-z]+\.[a-z]+@[A-Z]+[0-9][A-Z][0-9][A-Z][0-9][A-Z]+>\n[ ]+[a-z]+ <[A-Z]+[a-z]+@[A-Z][a-z]+\.[a-z]+>; [A-Z][a-z]+, [0-9]+ [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ \+[0-9]+'
   #1: from VALUED2D4C2DDC ([67.53.228.116]){bslash}n          by hrndva-omta06.mail.rr.com with ESMTP{bslash}n          id <20080116052759.OUZU11360.hrndva-omta06.mail.rr.com@VALUED2D4C2DDC>{bslash}n          for <LCherryh@Yahoo.com>; Wed, 16 Jan 2008 05:27:59 +0000
|   r' [a-z]+ [0-9]+\.[0-9]+\.[0-9]+\.[0-9][ ]+\([A-Z]+ [a-z]+-[a-z][0-9]+\.[a-z]+\.[a-z]+\.[a-z]+\) \([0-9]+\.[0-9]+\.[0-9]+\.[0-9]\)\n[ ]+[a-z]+ [a-z]+[0-9]+\.[a-z]+\.[a-z]+\.[a-z]+\.[a-z]+ [a-z]+ [A-Z]+; [A-Z][a-z]+, [0-9]+ [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ -[0-9]+'
   #1: from 64.12.137.7  (EHLO imo-m26.mx.aol.com) (64.12.137.7){bslash}n  by mta215.mail.mud.yahoo.com with SMTP; Wed, 16 Jan 2008 05:02:27 -0800
|   r' [a-z]+ [A-Z]+[0-9]+@[a-z]+\.[a-z]+\n\t[a-z]+ [a-z]+-[a-z][0-9]+\.[a-z]+\.[a-z]+\.[a-z]+ \([a-z]+_[a-z]+_[a-z][0-9]+_[a-z][0-9]\.[0-9]\.\) [a-z]+ [a-z]\.[a-z]+\.[0-9][a-z][0-9][a-z]+[0-9][a-z] \([0-9]+\)\n\t [a-z]+ <[A-Z]+[a-z]+@[a-z]+\.[a-z]+>; [A-Z][a-z]+, [0-9]+ [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ -[0-9]+ \([A-Z]+\)'
   #1: from CMONEYMAKER72@aol.com{bslash}n	by imo-m26.mx.aol.com (mail_out_v38_r9.3.) id r.bcd.1d0cad8e (14502){bslash}n	 for <LCherryh@yahoo.com>; Wed, 16 Jan 2008 08:02:24 -0500 (EST)
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_MimeOLE:: yield from (
    r' [A-Z][a-z]+ [A-Z][a-z] [A-Z][a-z]+ [A-Z][a-z]+ [A-Z][0-9]\.[0-9]'
   #6: Produced By Microsoft Exchange V6.5
|   r' [A-Z][a-z]+ [A-Z][a-z] [A-Z][a-z]+ [A-Z][a-z]+[A-Z]+ [A-Z][0-9]\.[0-9]+\.[0-9]+\.[0-9]+'
   #1: Produced By Microsoft MimeOLE V6.00.3790.2929
   #1: Produced By Microsoft MimeOLE V6.00.2900.3138
   #5: Produced By Microsoft MimeOLE V6.00.2900.3198
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def Content_class:: yield from (
    r' [a-z]+:[a-z]+-[a-z]+:[a-z]+'
   #6: urn:content-classes:message
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def MIME_Version:: yield from (
    r' [0-9]\.[0-9]'
   #32: 1.0
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
|   r' [a-z]+/[a-z]+;\n[ ]+[a-z]+="[A-Z][a-z]+[A-Z][a-z]+[0-9]+[A-Z][a-z][A-Z][a-z]+[A-Z][a-z][A-Z]-[0-9][a-z][A-Z][a-z]+[0-9][A-Z]+[0-9][a-z][A-Z][a-z][A-Z][a-z][A-Z]+[0-9][A-Z]"'
   #1: multipart/mixed;{bslash}n  boundary="PytmzYxs55LzQoiEiE-9nUgfn6JY6oCyUsXFY9Y"
|   r' [a-z]+/[a-z]+;\n\t[a-z]+="----_=_[A-Z][a-z]+[A-Z][a-z]+_[0-9]+_[0-9]+[A-Z][0-9][A-Z][0-9][A-Z][0-9]\.[0-9]+"'
   #1: multipart/mixed;{bslash}n	boundary="----_=_NextPart_001_01C7E8C6.62989397"
|   r' [a-z]+/[a-z]+;\n\t[a-z]+="----=_[A-Z][a-z]+[A-Z][a-z]+_[0-9]+_[0-9]+[A-Z]_[0-9]+[A-Z][0-9][A-Z]+[0-9]+\.[0-9][A-Z][0-9][A-Z]+[0-9][A-Z][0-9]"'
   #1: multipart/alternative;{bslash}n	boundary="----=_NextPart_000_007D_01C7EF12.9C5AE1C0"
|   r' [a-z]+/[a-z]+;\n\t[a-z]+="----=_[A-Z][a-z]+[A-Z][a-z]+_[0-9]+_[0-9]+[A-Z][0-9]_[0-9]+[A-Z][0-9][A-Z][0-9]+\.[A-Z]+[0-9]+"'
   #1: multipart/alternative;{bslash}n	boundary="----=_NextPart_000_02C9_01C7F830.FDE88060"
|   r' [a-z]+/[a-z]+;\n\t[a-z]+="----=_[A-Z][a-z]+[A-Z][a-z]+_[0-9]+_[0-9]+_[0-9]+[A-Z][0-9]+\.[0-9]+[A-Z][0-9][A-Z][0-9]+"'
   #1: multipart/related;{bslash}n	boundary="----=_NextPart_000_0055_01C81248.792D0D00"
|   r' [a-z]+/[a-z]+;\n\t[a-z]+="_[0-9]+_[A-Z][0-9]+[A-Z]+[0-9]+[A-Z][0-9]+[A-Z][0-9]+[A-Z]+[0-9][A-Z][0-9][A-Z]+[0-9][A-Z][0-9]+[A-Z][0-9]+[A-Z][0-9][A-Z][0-9]+[A-Z]+[0-9]+[a-z]+_"'
   #1: multipart/mixed;{bslash}n	boundary="_004_E52BA26B1940E24FAF1E0BD9F876E23847F2D468UKBXMBW01prodqu_"
|   r' [a-z]+/[a-z]+;\n\t[a-z]+="_[0-9]+_[A-Z][0-9]+[A-Z]+[0-9]+[A-Z][0-9]+[A-Z][0-9]+[A-Z]+[0-9][A-Z][0-9][A-Z]+[0-9][A-Z][0-9]+[A-Z][0-9]+[A-Z][0-9][A-Z][0-9][A-Z]+[0-9]+[a-z]+_"'
   #1: multipart/alternative;{bslash}n	boundary="_000_E52BA26B1940E24FAF1E0BD9F876E23847F2D4BEUKBXMBW01prodqu_"
   #1: multipart/alternative;{bslash}n	boundary="_000_E52BA26B1940E24FAF1E0BD9F876E23847F2D4BFUKBXMBW01prodqu_"
|   r' [a-z]+/[a-z]+;\n\t[a-z]+="_[0-9]+_[A-Z][0-9]+[A-Z]+[0-9]+[A-Z][0-9]+[A-Z][0-9]+[A-Z]+[0-9][A-Z][0-9][A-Z]+[0-9][A-Z][0-9]+[A-Z][0-9]+[A-Z][0-9][A-Z][0-9][A-Z][0-9][A-Z]+[0-9]+[a-z]+_"'
   #1: multipart/alternative;{bslash}n	boundary="_000_E52BA26B1940E24FAF1E0BD9F876E23847F2D4C1UKBXMBW01prodqu_"
|   r' [a-z]+/[a-z]+;\n\t[a-z]+="_[0-9]+_[0-9]+[A-Z]+[0-9][A-Z]+[0-9][A-Z][0-9]+[A-Z]+[0-9]+[A-Z][0-9][A-Z][0-9]+[A-Z][0-9][A-Z]+[0-9]+[A-Z][0-9]+[A-Z][0-9]+[A-Z]+[0-9]+[a-z]+_"'
   #1: multipart/alternative;{bslash}n	boundary="_000_65BB6DF6A76DAF4984F1B08936F2FC34A68B2119UKBXMBW01prodqu_"
|   r' [a-z]+/[a-z]+;\n\t[a-z]+="_[0-9]+[a-z][0-9]-[a-z][0-9][a-z][0-9]-[0-9]+[a-z]-[a-z][0-9][a-z][0-9]-[a-z][0-9]+[a-z][0-9]+[a-z][0-9]+_"'
   #1: multipart/alternative;{bslash}n	boundary="_064391a5-c6c4-496d-b5d3-d646e45f8071_"
|   r' [a-z]+/[a-z]+; [a-z]+="[0-9]-[0-9]+-[0-9]+=:[0-9]+"\n[A-Z][a-z]+-[A-Z][a-z]+-[A-Z][a-z]+: [0-9][a-z]+'
   #1: multipart/mixed; boundary="0-169234684-1199209661=:95298"{bslash}nContent-Transfer-Encoding: 8bit
   #1: multipart/alternative; boundary="0-1690936920-1199262114=:23902"{bslash}nContent-Transfer-Encoding: 8bit
   #1: multipart/mixed; boundary="0-1242512665-1199285010=:51156"{bslash}nContent-Transfer-Encoding: 8bit
   #1: multipart/mixed; boundary="0-1957197243-1199790550=:98701"{bslash}nContent-Transfer-Encoding: 8bit
   #1: multipart/alternative; boundary="0-1728457870-1199890176=:36147"{bslash}nContent-Transfer-Encoding: 8bit
   #1: multipart/mixed; boundary="0-237260743-1199989036=:89358"{bslash}nContent-Transfer-Encoding: 8bit
   #1: multipart/mixed; boundary="0-282327629-1200330844=:6022"{bslash}nContent-Transfer-Encoding: 8bit
|   r' [a-z]+/[a-z]+;\n\t[a-z]+="_[a-z][0-9]+[a-z][0-9]+[a-z][0-9]-[0-9]+[a-z]-[0-9]+[a-z]-[0-9][a-z]+[0-9]-[0-9]+[a-z][0-9]+[a-z][0-9]+[a-z]_"'
   #1: multipart/alternative;{bslash}n	boundary="_e71c60b7-934e-495d-8ca5-68d022d0756b_"
|   r' [a-z]+/[a-z]+;\n\t[a-z]+="_[0-9]+[a-z][0-9][a-z][0-9]+-[0-9]+[a-z][0-9]-[0-9]+[a-z]-[a-z][0-9][a-z][0-9]-[0-9][a-z][0-9][a-z]+[0-9]+[a-z][0-9][a-z][0-9]_"'
   #1: multipart/alternative;{bslash}n	boundary="_05c4e171-16e4-433e-b2a4-4f1cce49c8a5_"
|   r' [a-z]+/[a-z]+;\n\t[a-z]+="_[0-9]+_[0-9]+[A-Z]+[0-9][A-Z]+[0-9][A-Z][0-9]+[A-Z]+[0-9]+[A-Z][0-9][A-Z][0-9]+[A-Z][0-9][A-Z]+[0-9]+[A-Z][0-9][A-Z][0-9][A-Z][0-9][A-Z][0-9][A-Z]+[0-9]+[a-z]+_"'
   #1: multipart/mixed;{bslash}n	boundary="_005_65BB6DF6A76DAF4984F1B08936F2FC34A6B4B6D5UKBXMBW01prodqu_"
|   r' [a-z]+/[a-z]+;\n\t[a-z]+="----_=_[A-Z][a-z]+[A-Z][a-z]+_[0-9]+_[0-9]+[A-Z][0-9]+\.[A-Z][0-9][A-Z][0-9]+"'
   #1: multipart/mixed;{bslash}n	boundary="----_=_NextPart_001_01C85598.D0B82877"
|   r' [a-z]+/[a-z]+;\n\t[a-z]+="----=_[A-Z][a-z]+[A-Z][a-z]+_[0-9]+_[0-9]+[A-Z]_[0-9]+[A-Z][0-9]+[A-Z]\.[A-Z][0-9][A-Z][0-9][A-Z]+[0-9]"'
   #1: multipart/alternative;{bslash}n	boundary="----=_NextPart_000_003F_01C8568B.A7A9DFF0"
|   r' [a-z]+/[a-z]+;\n\t[a-z]+="----_=_[A-Z][a-z]+[A-Z][a-z]+_[0-9]+_[0-9]+[A-Z][0-9]+[A-Z][0-9]\.[A-Z]+[0-9][A-Z][0-9]"'
   #1: multipart/mixed;{bslash}n	boundary="----_=_NextPart_001_01C856F1.CAFCB0E2"
|   r' [a-z]+/[a-z]+;\n\t[a-z]+="----=_[A-Z][a-z]+[A-Z][a-z]+_[0-9]+_[0-9]+_[0-9]+[A-Z][0-9]+[A-Z]\.[0-9][A-Z][0-9][A-Z]+[0-9][A-Z][0-9]"'
   #1: multipart/alternative;{bslash}n	boundary="----=_NextPart_000_0024_01C8574E.8A6FD6B0"
|   r' [a-z]+/[a-z]+;\n\t[a-z]+="----=_[A-Z][a-z]+[A-Z][a-z]+_[0-9]+_[0-9]+[A-Z]+_[0-9]+[A-Z][0-9]+[A-Z]\.[A-Z][0-9]+"'
   #1: multipart/alternative;{bslash}n	boundary="----=_NextPart_000_00BC_01C8577E.C8509840"
|   r' [a-z]+/[a-z]+;\n\t[a-z]+="----=_[A-Z][a-z]+[A-Z][a-z]+_[0-9]+_[0-9]+[A-Z]_[0-9]+[A-Z][0-9]+[A-Z]+\.[0-9]+[A-Z][0-9]+[A-Z]+[0-9]"'
   #1: multipart/alternative;{bslash}n	boundary="----=_NextPart_000_015F_01C857CE.43B00DF0"
|   r' [a-z]+/[a-z]+; [a-z]+="-----------------------------[0-9]+"\n[A-Z]-[A-Z][a-z]+: [0-9]\.[0-9] [A-Z]+ [a-z]+ [A-Z][a-z]+ [a-z]+ [0-9]+'
   #1: multipart/alternative; boundary="-----------------------------1200488544"{bslash}nX-Mailer: 9.0 SE for Windows sub 5004
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
|   r' [A-Z][a-z]+ [a-z]+ [a-z]+ [a-z]+ [a-z]+'
   #1: Unable to deliver your message
   #1: Great to hear from you
|   r' [A-Z][a-z]+'
   #1: Xarchive
   #1: Hey
   #1: Thailand
   #1: Van
|   r' [A-Z]+ [a-z]+'
   #1: HSDC assistance
|   r' [A-Z][a-z]+!!!'
   #1: Transport!!!
   #1: Resume!!!
|   r' [A-Z]+: [0-9]+ [A-Z][a-z]+ [a-z]+ [A-Z][a-z]+'
   #1: FW: 2835 Minutes of Lon
|   r' [A-Z]+: [A-Z]+ [A-Z][a-z]+'
   #1: FW: SQL Stuff
|   r' [A-Z]+: [A-Z][a-z]+ [a-z]+ [A-Z][a-z]+!'
   #1: FW: Coming to America!
|   r' [a-z]+ [a-z]+'
   #2: your visit
|   r' [A-Z][a-z]+ \([A-Z][a-z]+ [0-9]+\)'
   #1: Programs (Assignment 10)
|   r' [A-Z]+: [a-z]+ [a-z]+'
   #1: FW: your visit
|   r' [A-Z][a-z]+ [A-Z][a-z]+ "[A-Z][a-z]+"'
   #1: Happy New "Year"
|   r' [A-Z][a-z] [A-Z][a-z]+ \([A-Z][a-z]+\)'
   #1: My Programs (Tochniotai)
|   r' [A-Z][a-z] [A-Z][a-z]+!'
   #1: My Programs!
|   r' [A-Z][a-z]+ [A-Z][a-z]+'[a-z] [a-z]+'
   #1: From Ariel's wedding
|   r' [A-Z][a-z]+ [A-Z][a-z]+ [A-Z][a-z]+'
   #1: Combining Two Arrays
|   r' [A-Z][a-z]+ [a-z]+ [a-z]+'
   #1: Mortgage extra payments
|   r' [A-Z][a-z]+ \([A-Z][a-z] [A-Z][a-z]+\) [A-Z][a-z]+ [0-9]+[a-z], [0-9]+[a-z]'
   #1: Tochniotai (My Programs) Assignment 12a, 12b
|   r' [A-Z][a-z]+ [A-Z][a-z]+ [A-Z][a-z]+ [a-z]+ [A-Z][a-z]+ [A-Z][a-z]+ [A-Z][a-z]+'
   #1: Your Upcoming Appointment with River Ranch Radiology
|   r' [A-Z][a-z]+![ ]+[A-Z][a-z]+ '
   #1: Shalom!  Lon 
|   r' [a-z]+ [a-z]+\.\.\.\.'
   #1: van veredict....
|   r' [A-Z][a-z]: [0-9]+-[A-Z]+-[0-9]+-[A-Z][a-z]+-[A-Z]+'
   #1: Re: 1999-GMC-1500-Engine-TX
|   r' [A-Z][a-z]: [A-Z]+: [0-9]+-[A-Z]+-[0-9]+-[A-Z][a-z]+-[A-Z]+'
   #1: Re: APLS: 1999-GMC-1500-Engine-TX
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def Date:: yield from (
    r' [A-Z][a-z]+, [0-9] [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ \+[0-9]+'
   #1: Mon, 4 Dec 2006 21:51:55 +0800
   #1: Wed, 9 Jan 2008 11:30:43 +0000
|   r' [A-Z][a-z]+, [0-9] [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ -[0-9]+'
   #1: Mon, 4 Dec 2006 10:46:00 -0800
   #1: Mon, 4 Dec 2006 11:27:33 -0800
   #1: Mon, 4 Dec 2006 19:55:13 -0000
   #1: Tue, 4 Sep 2007 16:42:31 -0600
   #1: Tue, 1 Jan 2008 19:00:50 -0600
   #1: Thu, 3 Jan 2008 19:25:27 -0600
|   r' [0-9] [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ -[0-9]+'
   #1: 6 May 2007 13:14:56 -0000
|   r' [A-Z][a-z]+, [0-9]+ [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ -[0-9]+'
   #1: Mon, 27 Aug 2007 09:20:57 -0700
   #1: Sun, 16 Sep 2007 07:12:50 -0500
   #1: Fri, 19 Oct 2007 12:06:25 -0500
   #1: Sun, 30 Dec 2007 17:56:16 -0600
   #1: Sat, 12 Jan 2008 23:00:19 -0500
   #1: Mon, 14 Jan 2008 08:58:39 -0600
   #1: Mon, 14 Jan 2008 15:09:47 -0600
   #1: Tue, 15 Jan 2008 08:13:42 -0600
   #1: Tue, 15 Jan 2008 13:59:01 -0600
   #1: Tue, 15 Jan 2008 23:27:59 -0600
|   r' [A-Z][a-z]+, [0-9]+ [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ \+[0-9]+'
   #1: Thu, 27 Dec 2007 13:48:30 +0000
   #1: Thu, 27 Dec 2007 14:09:12 +0000
   #1: Thu, 27 Dec 2007 14:09:22 +0000
   #1: Thu, 27 Dec 2007 14:09:46 +0000
   #1: Thu, 27 Dec 2007 16:35:15 +0000
|   r' [A-Z][a-z]+, [0-9] [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ -[0-9]+ \([A-Z]+\)'
   #1: Tue, 1 Jan 2008 09:47:41 -0800 (PST)
   #1: Wed, 2 Jan 2008 00:21:54 -0800 (PST)
   #1: Wed, 2 Jan 2008 06:43:30 -0800 (PST)
   #1: Tue, 8 Jan 2008 03:09:10 -0800 (PST)
   #1: Wed, 9 Jan 2008 06:49:36 -0800 (PST)
|   r' [A-Z][a-z]+, [0-9]+ [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ -[0-9]+ \([A-Z]+\)'
   #1: Thu, 10 Jan 2008 10:17:16 -0800 (PST)
   #1: Mon, 14 Jan 2008 09:14:04 -0800 (PST)
|   r' [A-Z][a-z]+, [0-9]+ [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ [A-Z]+'
   #1: Wed, 16 Jan 2008 08:02:24 EST
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
|   r' <[0-9]+\.[0-9]+\.[0-9]+\.[a-z][0-9]+@[a-z]+\.[a-z]+>'
   #1: <1178457296.118.80517.m48@yahoogroups.com>
|   r' <[0-9]+[A-Z][0-9][A-Z]+[0-9]+[A-Z]+[0-9]+[A-Z][0-9]+[A-Z][0-9]+[A-Z][0-9]+[A-Z]+[0-9][A-Z]+@[A-Z]+[0-9]+\.[a-z]+\.[a-z]+\.[a-z]+>'
   #1: <23D8DB429EF0494783E86044C51F865903DB9CEB@ALVMBXW02.prod.quest.corp>
|   r' <[0-9]+[a-z][0-9]+[a-z][0-9][a-z]+[0-9]+\$[a-z][0-9][a-z][0-9]+[a-z][0-9]\$[0-9]+[a-z][0-9][a-z][0-9]@[A-Z][a-z]+[A-Z]+>'
   #1: <007c01c7ef44$e6f551c0$6501a8c0@VentiRD>
|   r' <[0-9]+[A-Z][0-9]+[A-Z][0-9][A-Z]+[0-9]+[A-Z]+[0-9]+[A-Z][0-9][A-Z][0-9][A-Z][0-9]+[A-Z][0-9]+@[a-z]+[A-Z]+>'
   #1: <07E41628A4DA494AAA597D2D0C85A834@ownerPC>
|   r' <[0-9]+[a-z][0-9]+\$[0-9]+\$[a-z]+[0-9][a-z][0-9]+[a-z]+@[a-z]+>'
   #1: <005401c81272$62031500$ea0a14ac@jomolaptop>
|   r' <[A-Z][0-9]+[A-Z]+[0-9]+[A-Z][0-9]+[A-Z][0-9]+[A-Z]+[0-9][A-Z][0-9][A-Z]+[0-9][A-Z][0-9]+[A-Z][0-9]+[A-Z][0-9][A-Z][0-9]+@[A-Z]+[0-9]+\.[a-z]+\.[a-z]+\.[a-z]+>'
   #1: <E52BA26B1940E24FAF1E0BD9F876E23847F2D468@UKBXMBW01.prod.quest.corp>
|   r' <[A-Z][0-9]+[A-Z]+[0-9]+[A-Z][0-9]+[A-Z][0-9]+[A-Z]+[0-9][A-Z][0-9][A-Z]+[0-9][A-Z][0-9]+[A-Z][0-9]+[A-Z][0-9][A-Z][0-9][A-Z]+@[A-Z]+[0-9]+\.[a-z]+\.[a-z]+\.[a-z]+>'
   #1: <E52BA26B1940E24FAF1E0BD9F876E23847F2D4BE@UKBXMBW01.prod.quest.corp>
   #1: <E52BA26B1940E24FAF1E0BD9F876E23847F2D4BF@UKBXMBW01.prod.quest.corp>
|   r' <[A-Z][0-9]+[A-Z]+[0-9]+[A-Z][0-9]+[A-Z][0-9]+[A-Z]+[0-9][A-Z][0-9][A-Z]+[0-9][A-Z][0-9]+[A-Z][0-9]+[A-Z][0-9][A-Z][0-9][A-Z][0-9]@[A-Z]+[0-9]+\.[a-z]+\.[a-z]+\.[a-z]+>'
   #1: <E52BA26B1940E24FAF1E0BD9F876E23847F2D4C1@UKBXMBW01.prod.quest.corp>
|   r' <[0-9]+[A-Z]+[0-9][A-Z]+[0-9][A-Z][0-9]+[A-Z]+[0-9]+[A-Z][0-9][A-Z][0-9]+[A-Z][0-9][A-Z]+[0-9]+[A-Z][0-9]+[A-Z][0-9]+@[A-Z]+[0-9]+\.[a-z]+\.[a-z]+\.[a-z]+>'
   #1: <65BB6DF6A76DAF4984F1B08936F2FC34A68B2119@UKBXMBW01.prod.quest.corp>
|   r' <[A-Z]+[0-9]+-[A-Z][0-9]+[A-Z][0-9]+[A-Z]+[0-9]+[A-Z][0-9][A-Z]+[0-9]+[A-Z]+[0-9]+@[a-z]+\.[a-z]+>'
   #1: <BAY124-W3489E28ECAB87E6AF5089AD2570@phx.gbl>
|   r' <[0-9]+\.[0-9]+\.[a-z]+@[a-z]+[0-9]+\.[a-z]+\.[a-z]+[0-9]\.[a-z]+\.[a-z]+>'
   #1: <851320.95298.qm@web52611.mail.re2.yahoo.com>
   #1: <600240.23902.qm@web52601.mail.re2.yahoo.com>
   #1: <364748.51156.qm@web52604.mail.re2.yahoo.com>
   #1: <482054.98701.qm@web52605.mail.re2.yahoo.com>
   #1: <659587.36147.qm@web52610.mail.re2.yahoo.com>
   #1: <454556.89358.qm@web59107.mail.re1.yahoo.com>
   #1: <467603.6022.qm@web52605.mail.re2.yahoo.com>
|   r' <[A-Z]+[0-9]+-[A-Z][0-9]+[A-Z]+[0-9]+[A-Z]+[0-9]+[A-Z][0-9][A-Z]+[0-9]+@[a-z]+\.[a-z]+>'
   #1: <BAY124-W459446EDB4502DFA58F5CD2520@phx.gbl>
|   r' <[A-Z]+[0-9]+-[A-Z][0-9]+[A-Z][0-9]+[A-Z]+[0-9]+[A-Z]+[0-9][A-Z]+[0-9]+[A-Z][0-9]@[a-z]+\.[a-z]+>'
   #1: <BAY124-W746E761573BD76BDEF3EED24C0@phx.gbl>
|   r' <[0-9]+[A-Z]+[0-9][A-Z]+[0-9][A-Z][0-9]+[A-Z]+[0-9]+[A-Z][0-9][A-Z][0-9]+[A-Z][0-9][A-Z]+[0-9]+[A-Z][0-9][A-Z][0-9][A-Z][0-9][A-Z][0-9]@[A-Z]+[0-9]+\.[a-z]+\.[a-z]+\.[a-z]+>'
   #1: <65BB6DF6A76DAF4984F1B08936F2FC34A6B4B6D5@UKBXMBW01.prod.quest.corp>
|   r' <[0-9][A-Z]+[0-9]+[A-Z][0-9]+[A-Z][0-9]+[A-Z]+[0-9][A-Z][0-9]+[A-Z][0-9]+[A-Z]@[A-Z]+-[A-Z]+[0-9]+\.[A-Z]+\.[A-Z][a-z]+\.[a-z]+>'
   #1: <9BDA6601615804418B799762F41EA1D7021D166D@NOANDC-MXU24.NOA.Alcoa.com>
|   r' <[0-9]+[a-z][0-9]+[a-z]+\$[a-z][0-9][a-z]+[0-9][a-z][0-9]\$[a-z][0-9]+@[A-Z][a-z][A-Z][a-z]+[A-Z][a-z]+>'
   #1: <004201c856bd$f2aad9f0$a9557046@DeAtleyFloor>
|   r' <[A-Z][0-9]+[A-Z][0-9]+[A-Z]+[0-9][A-Z]+[0-9][A-Z]+[0-9][A-Z][0-9]+[A-Z]+[0-9]+@[a-z]+\.[A-Z][a-z]+[A-Z][a-z]+[A-Z][a-z]+\.[a-z]+>'
   #1: <B9307879C62717418BD7CB1FF0E256730315BB29@server.RiverRanchRadiology.local>
|   r' <[0-9]+[a-z][0-9]+\$[a-z][0-9]+[a-z][0-9]\$[0-9][a-z][0-9]+[a-z][0-9]+@[a-z]+[0-9]+[a-z][0-9]+[a-z][0-9]+>'
   #1: <002701c85780$d64510a0$7d90e604@your27e1513d96>
|   r' <[0-9]+[a-z]+[0-9]+[a-z][0-9]+[a-z][0-9]\$[0-9]+\$[a-z][0-9]+@[A-Z][a-z][A-Z][a-z]+[A-Z][a-z]+>'
   #1: <00bf01c857b1$13458450$a9557046@DeAtleyFloor>
|   r' <[0-9]+[a-z][0-9]+\$[0-9][a-z][0-9][a-z]+[0-9]+\$[0-9]+[a-z][0-9][a-z][0-9]@[A-Z]+[0-9][A-Z][0-9][A-Z][0-9][A-Z]+>'
   #1: <016401c85800$8e8ae250$6701a8c0@VALUED2D4C2DDC>
|   r' <[a-z]+\.[0-9][a-z][0-9][a-z]+[0-9][a-z]\.[0-9]+[a-z]+[0-9][a-z][0-9]+@[a-z]+\.[a-z]+>'
   #1: <bcd.1d0cad8e.34bf5a60@aol.com>
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_MS_Has_Attach:: yield from (
    r' '
   #4: 
|   r' [a-z]+'
   #5: yes
|   r''
   #4:
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_MS_TNEF_Correlator:: yield from (
    r' '
   #7: 
|   r''
   #6:
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
|   r' [A-Z][a-z]+'
   #1: Xarchive
   #1: Thailand
|   r' [A-Z][a-z]+!!!'
   #1: Transport!!!
|   r' [0-9]+ [A-Z][a-z]+ [a-z]+ [A-Z][a-z]+'
   #1: 2835 Minutes of Lon
|   r' [A-Z]+ [A-Z][a-z]+'
   #1: SQL Stuff
|   r' [A-Z][a-z]+ [a-z]+ [A-Z][a-z]+!'
   #1: Coming to America!
|   r' [A-Z][a-z]+ [A-Z][a-z]+'[a-z] [a-z]+'
   #1: From Ariel's wedding
|   r' [A-Z][a-z]+ [a-z]+ [a-z]+'
   #1: Mortgage extra payments
|   r' [A-Z][a-z]+ [A-Z][a-z]+ [A-Z][a-z]+ [a-z]+ [A-Z][a-z]+ [A-Z][a-z]+ [A-Z][a-z]+'
   #1: Your Upcoming Appointment with River Ranch Radiology
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
|   r' [A-Z][a-z]+[A-Z]+[a-z]+[A-Z][a-z]+[A-Z]+[a-z][0-9][a-z]+[A-Z]+[a-z]+=='
   #1: AcfvRODlxbBswqcURw6mlUYZAKBweg==
|   r' [A-Z][a-z]+[A-Z][a-z]+[A-Z][0-9][A-Z]+[a-z][A-Z][a-z][0-9][a-z][A-Z]+[a-z]+[0-9]+[A-Z]/[A-Z][a-z][A-Z][a-z][A-Z][a-z]=='
   #1: AcgScmE6LBBfMi0bTIap03W/RkVbJg==
|   r' [A-Z][a-z]+[A-Z][a-z]+[A-Z]+[a-z][A-Z]+[0-9][A-Z][a-z][A-Z][a-z][A-Z][a-z][A-Z]+[0-9][a-z][A-Z]+=='
   #1: AchIjypdoDOCeFK0ReOoChMXS6xNCQ==
|   r' [A-Z][a-z]+[A-Z][0-9][A-Z][a-z][A-Z][a-z]+[A-Z][a-z]+[0-9][A-Z][a-z][A-Z]+[a-z]+[A-Z]+[a-z][A-Z]+[0-9]+[a-z][A-Z]+[a-z]+[A-Z]+[a-z][A-Z][0-9][A-Z]=='
   #1: AchH6VeJttshQpw2TjWNpbBBGeUJBAACO28wACLXmiAABRgL4A==
|   r' [A-Z][a-z]+[A-Z][a-z][A-Z][a-z][0-9]+[A-Z]+[a-z]+[A-Z]+[0-9][A-Z]+[0-9][a-z][0-9][a-z][0-9][A-Z][0-9][a-z][A-Z]+[a-z]+'
   #1: AchIhUb16EPFUViiSZK5VH4v4x5N2wADMtpg
|   r' [A-Z][a-z]+[A-Z]+[0-9][A-Z]\+[A-Z]+[0-9][A-Z]+[a-z]+[A-Z]+[a-z][0-9][a-z]+[A-Z]+[a-z][A-Z]+[a-z][0-9][A-Z][a-z][A-Z]+\+[A-Z][a-z][A-Z]+[0-9][a-z][A-Z][a-z][A-Z]+[0-9][A-Z][0-9][A-Z]'
   #1: AchGWTPP7D+ADM6UTbazMAp0qfWOwQASh4PgAA+AzCAAU1zGkAAY1X7Q
|   r' [A-Z][a-z]+[A-Z][a-z]+[A-Z]+[0-9][A-Z][a-z][0-9][a-z][A-Z]+[a-z][A-Z]+[0-9][A-Z][a-z]+[0-9][a-z]+[A-Z]/[A-Z]+=='
   #1: AchIpnXL8Ol6iCZlSV2Acxm1jfU/DA==
|   r' [A-Z][a-z]+[A-Z][a-z]+[A-Z]+[a-z]+[A-Z][a-z][0-9][a-z][A-Z][a-z][A-Z][a-z]+\+[a-z]+[A-Z]=='
   #1: AchSsxJDtbUm7pYaTdyke+uzwwtfkQ==
|   r' [A-Z][a-z]+[A-Z][a-z][A-Z]+[0-9][a-z][0-9][A-Z]+[a-z][A-Z]+[a-z]\+[A-Z]+[a-z]+[A-Z]+\+[A-Z]=='
   #1: AchVmNAQ2k5KDWpTRm+TBPrhqDUU+A==
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def From:: yield from (
    r' "[A-Z][a-z]+ [A-Z][a-z]+" <[A-Z][a-z]+\.[A-Z][a-z]+@[a-z]+\.[a-z]+>'
   #1: "Ken Moses" <Ken.Moses@quest.com>
   #1: "Lisa Radford" <Lisa.Radford@quest.com>
   #1: "Keren Kamilian" <Keren.Kamilian@quest.com>
   #1: "Lon Cherryholmes" <Lon.Cherryholmes@quest.com>
|   r' "[A-Z][a-z]+ [A-Z][a-z]+" <[a-z]+\.[a-z]+@[a-z]+\.[a-z]+>'
   #1: "Pat Luis" <pat.luis@quest.com>
|   r' [A-Z][a-z]+! [A-Z][a-z]+ <[a-z]+@[a-z]+\.[a-z]+>'
   #1: Yahoo! Groups <notify@yahoogroups.com>
|   r' "[A-Z][a-z]+ [A-Z][a-z][A-Z][a-z]+" <[A-Z][a-z]+\.[A-Z][a-z][A-Z][a-z]+@[A-Z][a-z]+[A-Z][a-z]+\.[a-z]+>'
   #1: "Tony DeLollis" <Tony.DeLollis@VentiSolutions.com>
|   r' "[A-Z][a-z]+ [A-Z][a-z]+" <[a-z]+@[a-z]+\.[a-z]+\.[a-z]+>'
   #1: "Rusty Bullerman" <rbullerman@austin.rr.com>
|   r' "[A-Z][a-z]+ [A-Z][a-z]+" <[a-z]+\.[a-z]+@[a-z]+-[a-z]+\.[a-z]+>'
   #1: "Jeff Omo" <jeff.omo@database-brothers.com>
|   r' [A-Z][a-z]+ [A-Z][a-z]+ <[A-Z][a-z]+\.[A-Z][a-z]+@[a-z]+\.[a-z]+>'
   #4: Lon Cherryholmes <Lon.Cherryholmes@quest.com>
|   r' [A-Z][a-z]+ [A-Z][a-z]+ <[a-z]+\.[a-z]+@[a-z]+\.[a-z]+>'
   #2: Adi Izhar <adi.izhar@quest.com>
|   r' [A-Z][a-z]+ [A-Z][a-z]+ <[a-z]+@[a-z]+\.[a-z]+>'
   #3: Leslie Cherryholmes <lesliecherryholmes@hotmail.com>
   #1: Lon Cherryholmes <lcherryh@yahoo.com>
|   r' "[A-Z][a-z]+ [A-Z]\. [A-Z][a-z]+" <[a-z]+_[0-9]+@[a-z]+\.[a-z]+>'
   #6: "Lon T. Cherryholmes" <ness_78759@yahoo.com>
|   r' "[A-Z][a-z]+, [A-Z][a-z]+ [A-Z] \\([A-Z]&[A-Z]\\)" <[A-Z][a-z]+\.[A-Z][a-z]+@[a-z]+\.[a-z]+>'
   #1: "Sheets, Chris A \(T&K\)" <Chris.Sheets@alcoa.com>
|   r' "[A-Z][a-z][A-Z][a-z]+ [A-Z][a-z]+ & [A-Z][a-z]+" <[a-z]+@[a-z]+\.[a-z]+\.[a-z]+>'
   #2: "DeAtley Tile & Stone" <tdeatley@austin.rr.com>
|   r' "[A-Z][a-z]+ [A-Z][a-z]+[ ]+- [A-Z][a-z]+ [A-Z][a-z]+ [A-Z][a-z]+" <[a-z]+@[a-z]+\.[a-z]+>'
   #1: "Becky Thompson  - River Ranch Radiology" <bthompson@riverranchradiology.com>
|   r' "[A-Z][a-z]+ [A-Z][a-z]+" <[a-z]+@[a-z]+\.[a-z]+>'
   #1: "Elizabeth Flowers" <shalomyaall@peoplepc.com>
|   r' "[a-z]+ [a-z]+ [a-z]+" <[a-z]+@[a-z]+-[a-z]+\.[a-z]+>'
   #1: "midwest auto recycling" <parts@mw-ar.com>
|   r' [A-Z]+[0-9]+@[a-z]+\.[a-z]+'
   #1: CMONEYMAKER72@aol.com
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def To:: yield from (
    r' "[A-Z][a-z]+ [A-Z][a-z]+" <[a-z]+@[a-z]+\.[a-z]+>'
   #2: "Lon Cherryholmes" <lcherryh@yahoo.com>
|   r' <[a-z]+@[a-z]+\.[a-z]+>'
   #6: <lcherryh@yahoo.com>
|   r' "[A-Z][a-z]+ [A-Z][a-z]+" <[a-z]+\.[a-z]+@[a-z]+\.[a-z]+>'
   #1: "Pat Luis" <pat.luis@quest.com>
|   r' [a-z]+@[a-z]+\.[a-z]+'
   #1: lcherryh@yahoo.com
|   r' <[A-Z]+[a-z]+@[a-z]+\.[a-z]+>'
   #5: <LCherryh@yahoo.com>
|   r' "[A-Z]+[a-z]+@[A-Z][a-z]+\.[a-z]+" <[A-Z]+[a-z]+@[A-Z][a-z]+\.[a-z]+>'
   #5: "LCherryh@Yahoo.com" <LCherryh@Yahoo.com>
|   r' "[A-Z]+:" <[A-Z]+[a-z]+@[A-Z][a-z]+\.[a-z]+>'
   #1: "RE:" <LCherryh@Yahoo.com>
|   r' [A-Z][a-z]+ [A-Z][a-z]+ <[a-z]+\.[a-z]+@[a-z]+\.[a-z]+>, [a-z]+@[a-z]+\.[a-z]+'
   #6: Lon Cherryholmes <lon.cherryholmes@quest.com>, lcherryh@yahoo.com
|   r' [A-Z][a-z]+ [A-Z][a-z]+ <[a-z]+@[a-z]+\.[a-z]+>, [A-Z][a-z]+ [A-Z][a-z]+'
   #2: Lon Cherryholmes <lcherryh@yahoo.com>, Lon Cherryholmes
|   r' [A-Z]+[a-z]+@[A-Z][a-z]+\.[a-z]+'
   #2: LCherryh@Yahoo.com
|   r' <[A-Z]+[a-z]+@[A-Z][a-z]+\.[a-z]+>'
   #1: <LCherryh@Yahoo.com>
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
|   r' [0-9]+ [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+\.[0-9]+ \([A-Z]+\) [A-Z]+=\[[0-9]+[A-Z][0-9]+:[0-9]+[A-Z][0-9][A-Z][0-9][A-Z][0-9]\]'
   #1: 27 Aug 2007 16:21:56.0899 (UTC) FILETIME=[6335D730:01C7E8C6]
|   r' [0-9]+ [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+\.[0-9]+ \([A-Z]+\) [A-Z]+=\[[0-9]+[A-Z][0-9][A-Z][0-9]+:[0-9]+[A-Z][0-9]+[A-Z][0-9][A-Z]\]'
   #1: 30 Dec 2007 23:56:16.0969 (UTC) FILETIME=[911D2B90:01C84B3F]
|   r' [0-9]+ [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+\.[0-9]+ \([A-Z]+\) [A-Z]+=\[[A-Z]+[0-9][A-Z]+[0-9]:[0-9]+[A-Z][0-9]+[A-Z]+\]'
   #1: 02 Jan 2008 01:00:50.0700 (UTC) FILETIME=[EADD1CC0:01C84CDA]
|   r' [0-9]+ [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+\.[0-9]+ \([A-Z]+\) [A-Z]+=\[[A-Z][0-9]+[A-Z]+[0-9]:[0-9]+[A-Z][0-9]+[A-Z][0-9]+\]'
   #1: 04 Jan 2008 01:25:28.0042 (UTC) FILETIME=[B0411CA0:01C84E70]
|   r' [0-9]+ [A-Z][a-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+\.[0-9]+ \([A-Z]+\) [A-Z]+=\[[A-Z][0-9]+:[0-9]+[A-Z][0-9]+\]'
   #1: 13 Jan 2008 04:00:21.0559 (UTC) FILETIME=[D1570470:01C85598]
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def Content_Length:: yield from (
    r' [0-9]+'
   #1: 1150
   #1: 7937
   #1: 6054
   #1: 8406
   #1: 5286
   #1: 286450
   #1: 7732
   #1: 1216
   #1: 18240
   #1: 3275573
   #1: 16011
   #1: 10432
   #1: 19338
   #1: 6492
   #1: 1672
   #1: 2749
   #1: 2285
   #1: 2308
   #1: 3094
   #1: 1256
   #1: 5341
   #1: 5368575
   #1: 1562
   #1: 130401
   #1: 193837
   #1: 2595
   #1: 3889
   #1: 602608
   #1: 1971
   #1: 1858
   #1: 5492
   #1: 9145
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
|   r' "[A-Z][a-z]+ [A-Z][a-z]+ - [A-Z][a-z]+ [A-Z][a-z]+ [A-Z][a-z]+" <[a-z]+@[a-z]+\.[a-z]+>'
   #1: "Angie Garcia - River Ranch Radiology" <agarcia@riverranchradiology.com>
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
|   r' <[0-9]+\.[0-9]+\.[a-z]+@[a-z]+\.[a-z]+\.[a-z]+>'
   #1: <20080116033202.6569.qmail@outbound.qualityautoparts.com>
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def Comment:: yield from (
    r' [A-Z][a-z]+[A-Z][a-z]+\? [A-Z][a-z]+ [a-z]+://[a-z]+\.[a-z]+\.[a-z]+/[a-z]+'
   #1: DomainKeys? See http://antispam.yahoo.com/domainkeys
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def DomainKey_Signature:: yield from (
    r' [a-z]=[a-z]+-[a-z]+[0-9]; [a-z]=[a-z]+; [a-z]=[a-z]+; [a-z]=[a-z]+; [a-z]=[a-z]+\.[a-z]+;\n\t[a-z]=[a-z]+[0-9][a-z][A-Z][a-z]+[A-Z]+[a-z]+[0-9][a-z][0-9]\+[A-Z]+[a-z]+[A-Z][a-z][A-Z][0-9][A-Z]+[a-z][A-Z]+[0-9][A-Z][a-z]/[A-Z]+[a-z]+[A-Z]+[0-9][a-z][0-9][a-z][A-Z][0-9][A-Z]+[a-z][A-Z][a-z][A-Z]+[a-z]+[A-Z]+/[A-Z]+[a-z]+[A-Z]/[a-z][0-9]+[a-z][A-Z][a-z][A-Z][a-z][A-Z][a-z][A-Z]+[a-z]+/[A-Z]+[a-z][A-Z][a-z]+[A-Z][0-9][A-Z][a-z][A-Z][a-z]\+[A-Z]+[0-9][A-Z][a-z][A-Z]+\+[a-z]+[0-9]+[A-Z][a-z][0-9][a-z][A-Z];'
   #1: a=rsa-sha1; q=dns; c=nofws; s=lima; d=yahoogroups.com;{bslash}n	b=nce6rTvfJLmw6r7+SDFNRbllvIiA8ZMhRY0Hj/XSTWwxkPG1z0lS3OHfTlVSRJLKtxwEE/HLdaoimnN/d19uSvWuKmSZLwt/JTfWwoO8SgSw+RD6HaXY+wkf196Vz2dP;
|   r' [a-z]=[a-z]+-[a-z]+[0-9]; [a-z]=[a-z]+; [a-z]=[a-z]+;\n[ ]+[a-z]=[a-z][0-9]+; [a-z]=[a-z]+\.[a-z]+;'
   #7: a=rsa-sha1; q=dns; c=nofws;{bslash}n  s=s1024; d=yahoo.com;
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_Yahoo_Newman_Property:: yield from (
    r' [a-z]+-[a-z]+'
   #1: groups-bounce
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def Content_Class:: yield from (
    r' [a-z]+:[a-z]+-[a-z]+:[a-z]+'
   #1: urn:content-classes:message
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def Content_Transfer_Encoding:: yield from (
    r' [0-9][a-z]+'
   #1: 7bit
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def Importance:: yield from (
    r' [a-z]+'
   #1: normal
|   r' [A-Z][a-z]+'
   #3: Normal
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def Priority:: yield from (
    r' [a-z]+'
   #1: normal
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def thread_index:: yield from (
    r' [A-Z][a-z]+\+[A-Z][a-z][0-9][A-Z]+[0-9][A-Z]+[a-z][A-Z][a-z][A-Z][0-9][A-Z][a-z]+[A-Z]+[a-z]=='
   #1: Acfoxj+Fy3ABX1UHRgSdI7CnwxKTKw==
|   r' [A-Z][a-z]+[A-Z][0-9][a-z]+[A-Z]+[a-z][0-9]+[A-Z][0-9][a-z]+[A-Z]+[a-z][A-Z][a-z][A-Z][a-z][A-Z]+[a-z]+[A-Z]+=='
   #1: AchW8csYNr02G2rlRZiGjYiUAouHXA==
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_Mailer:: yield from (
    r' [A-Z][a-z]+ [A-Z][a-z]+ [A-Z][a-z]+ [0-9]+'
   #2: Microsoft Office Outlook 11
|   r' [A-Z][a-z]+ [A-Z][a-z]+ [A-Z][a-z]+ [0-9]\.[0-9]\.[0-9]+\.[0-9]+'
   #1: Microsoft Windows Mail 6.0.6000.16480
|   r' [A-Z][a-z]+ [A-Z][a-z]+ [A-Z][a-z]+ [0-9]\.[0-9]+\.[0-9]+\.[0-9]+'
   #4: Microsoft Outlook Express 6.00.2900.3138
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_Spam:: yield from (
    r' \[[A-Z]=[0-9]\.[0-9]+; [a-z]+=[0-9]\.[0-9]+\([0-9]+\); [a-z]+=[0-9]\.[0-9]+; [a-z]+-[a-z]+=[0-9]\.[0-9]+\([0-9]+\)\]'
   #1: [F=0.0148648649; heur=0.500(1500); stat=0.010; spamtraq-heur=0.599(2007082706)]
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_MAIL_FROM:: yield from (
    r' <[a-z]+\.[a-z]+@[a-z]+\.[a-z]+>'
   #1: <tony.delollis@ventisolutions.com>
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_SOURCE_IP:: yield from (
    r' \[[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\]'
   #1: [199.239.254.40]
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_SF_Loop:: yield from (
    r' [0-9]'
   #1: 1
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_Priority:: yield from (
    r' [0-9]'
   #5: 3
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_MSMail_Priority:: yield from (
    r' [A-Z][a-z]+'
   #5: Normal
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_MIMEOLE:: yield from (
    r' [A-Z][a-z]+ [A-Z][a-z] [A-Z][a-z]+ [A-Z][a-z]+[A-Z]+ [A-Z][0-9]\.[0-9]\.[0-9]+\.[0-9]+'
   #1: Produced By Microsoft MimeOLE V6.0.6000.16480
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_Virus_Scanned:: yield from (
    r' [A-Z][a-z]+ [A-Z][a-z]+[A-Z][a-z]+ [A-Z][a-z]+ [A-Z][a-z]+'
   #1: Symantec AntiVirus Scan Engine
)
{'φ(From_rex) + η()\n + X_Account_Key() + η()\n + X_UIDL() + η()\n + X_Mozilla_Status() + η()\n + X_Mozilla_Status2() + η()\n + X_Mozilla_Keys() + η()\n + X_Apparently_To() + η()\n + X_Originating_IP() + η()\n + Return_Path() + η()\n + Authentication_Results() + η()\n + Received() + η()\n + Comment() + η()\n + DomainKey_Signature() + η()\n + Received() + η()\n + Received() + η()\n + Received() + η()\n + Date() + η()\n + Message_ID() + η()\n + X_Yahoo_Newman_Property() + η()\n + MIME_Version() + η()\n + To() + η()\n + From() + η()\n + Subject() + η()\n + Content_Type() + η()\n + Content_Length() + η()\n': 1,
 'φ(From_rex) + η()\n + X_Account_Key() + η()\n + X_UIDL() + η()\n + X_Mozilla_Status() + η()\n + X_Mozilla_Status2() + η()\n + X_Mozilla_Keys() + η()\n + X_Apparently_To() + η()\n + X_Originating_IP() + η()\n + Return_Path() + η()\n + Authentication_Results() + η()\n + Received() + η()\n + Received() + η()\n + DomainKey_Signature() + η()\n + μ() + φ(r"[a-z]") + σ(\'=\') + φ(r"[A-Z]") + σ(\'-\') + φ(r"[A-Z]+") + φ(r"[a-z]+") + σ(\'-\') + φ(r"[A-Z]+") + σ(\':\') + Received() + η()\n + σ(\'X-YMail-OSG:\') + μ() + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[a-z]") + σ(\'.\') + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[a-z]+") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[0-9]") + σ(\'_\') + φ(r"[0-9]") + φ(r"[A-Z]+") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[A-Z]") + σ(\'.\') + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[0-9]+") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[A-Z]+") + σ(\'_\') + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[A-Z]") + σ(\'-\') + σ(\'-\') + η()\n + Received() + η()\n + Date() + η()\n + From() + η()\n + Subject() + η()\n + To() + η()\n + MIME_Version() + η()\n + Content_Type() + η()\n + Message_ID() + η()\n + Content_Length() + η()\n': 1,
 'φ(From_rex) + η()\n + X_Account_Key() + η()\n + X_UIDL() + η()\n + X_Mozilla_Status() + η()\n + X_Mozilla_Status2() + η()\n + X_Mozilla_Keys() + η()\n + X_Apparently_To() + η()\n + X_Originating_IP() + η()\n + Return_Path() + η()\n + Authentication_Results() + η()\n + Received() + η()\n + Received() + η()\n + DomainKey_Signature() + η()\n + μ() + φ(r"[a-z]") + σ(\'=\') + φ(r"[A-Z]") + σ(\'-\') + φ(r"[A-Z]+") + φ(r"[a-z]+") + σ(\'-\') + φ(r"[A-Z]+") + σ(\':\') + Received() + η()\n + σ(\'X-YMail-OSG:\') + μ() + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[A-Z]") + σ(\'.\') + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[0-9]+") + φ(r"[a-z]+") + φ(r"[0-9]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[0-9]+") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + σ(\'.\') + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[0-9]+") + φ(r"[a-z]+") + φ(r"[A-Z]+") + σ(\'_\') + φ(r"[a-z]+") + φ(r"[0-9]+") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]+") + φ(r"[0-9]") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[0-9]+") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[0-9]") + φ(r"[a-z]") + σ(\'_\') + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[0-9]+") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]+") + φ(r"[A-Z]") + σ(\'_\') + φ(r"[A-Z]") + φ(r"[a-z]") + σ(\'-\') + σ(\'-\') + η()\n + Received() + η()\n + Date() + η()\n + From() + η()\n + Subject() + η()\n + To() + η()\n + MIME_Version() + η()\n + Content_Type() + η()\n + Message_ID() + η()\n + Content_Length() + η()\n': 1,
 'φ(From_rex) + η()\n + X_Account_Key() + η()\n + X_UIDL() + η()\n + X_Mozilla_Status() + η()\n + X_Mozilla_Status2() + η()\n + X_Mozilla_Keys() + η()\n + X_Apparently_To() + η()\n + X_Originating_IP() + η()\n + Return_Path() + η()\n + Authentication_Results() + η()\n + Received() + η()\n + Received() + η()\n + DomainKey_Signature() + η()\n + μ() + φ(r"[a-z]") + σ(\'=\') + φ(r"[A-Z]") + σ(\'-\') + φ(r"[A-Z]+") + φ(r"[a-z]+") + σ(\'-\') + φ(r"[A-Z]+") + σ(\':\') + Received() + η()\n + σ(\'X-YMail-OSG:\') + μ() + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[0-9]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[0-9]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[0-9]+") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]+") + σ(\'.\') + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]+") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]+") + σ(\'-\') + η()\n + Received() + η()\n + Date() + η()\n + From() + η()\n + Subject() + η()\n + To() + η()\n + MIME_Version() + η()\n + Content_Type() + η()\n + Message_ID() + η()\n + Content_Length() + η()\n': 1,
 'φ(From_rex) + η()\n + X_Account_Key() + η()\n + X_UIDL() + η()\n + X_Mozilla_Status() + η()\n + X_Mozilla_Status2() + η()\n + X_Mozilla_Keys() + η()\n + X_Apparently_To() + η()\n + X_Originating_IP() + η()\n + Return_Path() + η()\n + Authentication_Results() + η()\n + Received() + η()\n + Received() + η()\n + DomainKey_Signature() + η()\n + μ() + φ(r"[a-z]") + σ(\'=\') + φ(r"[A-Z]") + σ(\'-\') + φ(r"[A-Z]+") + φ(r"[a-z]+") + σ(\'-\') + φ(r"[A-Z]+") + σ(\':\') + Received() + η()\n + σ(\'X-YMail-OSG:\') + μ() + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[0-9]+") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[0-9]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[0-9]+") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[0-9]+") + φ(r"[A-Z]+") + φ(r"[a-z]+") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[0-9]+") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[0-9]+") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[0-9]+") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[0-9]") + σ(\'.\') + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[a-z]+") + σ(\'_\') + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]") + σ(\'-\') + η()\n + Received() + η()\n + Date() + η()\n + From() + η()\n + Subject() + η()\n + To() + η()\n + MIME_Version() + η()\n + Content_Type() + η()\n + Message_ID() + η()\n + Content_Length() + η()\n': 1,
 'φ(From_rex) + η()\n + X_Account_Key() + η()\n + X_UIDL() + η()\n + X_Mozilla_Status() + η()\n + X_Mozilla_Status2() + η()\n + X_Mozilla_Keys() + η()\n + X_Apparently_To() + η()\n + X_Originating_IP() + η()\n + Return_Path() + η()\n + Authentication_Results() + η()\n + Received() + η()\n + Received() + η()\n + DomainKey_Signature() + η()\n + μ() + φ(r"[a-z]") + σ(\'=\') + φ(r"[A-Z]") + σ(\'-\') + φ(r"[A-Z]+") + φ(r"[a-z]+") + σ(\'-\') + φ(r"[A-Z]+") + σ(\':\') + Received() + η()\n + σ(\'X-YMail-OSG:\') + μ() + φ(r"[A-Z]+") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[0-9]") + σ(\'_\') + φ(r"[0-9]") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[A-Z]+") + σ(\'_\') + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]") + σ(\'_\') + φ(r"[A-Z]+") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[0-9]") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]+") + σ(\'.\') + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + σ(\'-\') + σ(\'-\') + η()\n + Received() + η()\n + Date() + η()\n + From() + η()\n + Subject() + η()\n + To() + η()\n + MIME_Version() + η()\n + Content_Type() + η()\n + Message_ID() + η()\n + Content_Length() + η()\n': 1,
 'φ(From_rex) + η()\n + X_Account_Key() + η()\n + X_UIDL() + η()\n + X_Mozilla_Status() + η()\n + X_Mozilla_Status2() + η()\n + X_Mozilla_Keys() + η()\n + X_Apparently_To() + η()\n + X_Originating_IP() + η()\n + Return_Path() + η()\n + Authentication_Results() + η()\n + Received() + η()\n + Received() + η()\n + DomainKey_Signature() + η()\n + μ() + φ(r"[a-z]") + σ(\'=\') + φ(r"[A-Z]") + σ(\'-\') + φ(r"[A-Z]+") + φ(r"[a-z]+") + σ(\'-\') + φ(r"[A-Z]+") + σ(\':\') + Received() + η()\n + σ(\'X-YMail-OSG:\') + μ() + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + σ(\'.\') + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[a-z]+") + σ(\'.\') + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[A-Z]") + σ(\'.\') + φ(r"[0-9]+") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[a-z]") + σ(\'_\') + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[0-9]") + φ(r"[A-Z]+") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[0-9]+") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[A-Z]+") + σ(\'_\') + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[0-9]+") + φ(r"[A-Z]+") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[0-9]+") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]+") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[0-9]") + σ(\'.\') + φ(r"[A-Z]+") + η()\n + Received() + η()\n + Date() + η()\n + From() + η()\n + Subject() + η()\n + To() + η()\n + MIME_Version() + η()\n + Content_Type() + η()\n + Message_ID() + η()\n + Content_Length() + η()\n': 1,
 'φ(From_rex) + η()\n + X_Account_Key() + η()\n + X_UIDL() + η()\n + X_Mozilla_Status() + η()\n + X_Mozilla_Status2() + η()\n + X_Mozilla_Keys() + η()\n + X_Apparently_To() + η()\n + X_Originating_IP() + η()\n + Return_Path() + η()\n + Authentication_Results() + η()\n + Received() + η()\n + Received() + η()\n + DomainKey_Signature() + η()\n + μ() + φ(r"[a-z]") + σ(\'=\') + φ(r"[A-Z]") + σ(\'-\') + φ(r"[A-Z]+") + φ(r"[a-z]+") + σ(\'-\') + φ(r"[A-Z]+") + σ(\':\') + Received() + η()\n + σ(\'X-YMail-OSG:\') + μ() + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[0-9]+") + φ(r"[A-Z]") + φ(r"[0-9]") + σ(\'.\') + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + σ(\'.\') + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[A-Z]+") + σ(\'.\') + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[0-9]+") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[A-Z]") + σ(\'.\') + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[0-9]+") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[0-9]+") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[a-z]+") + σ(\'-\') + η()\n + Received() + η()\n + Date() + η()\n + From() + η()\n + Subject() + η()\n + To() + η()\n + MIME_Version() + η()\n + Content_Type() + η()\n + Message_ID() + η()\n + Content_Length() + η()\n': 1,
 'φ(From_rex) + η()\n + X_Account_Key() + η()\n + X_UIDL() + η()\n + X_Mozilla_Status() + η()\n + X_Mozilla_Status2() + η()\n + X_Mozilla_Keys() + η()\n + X_Apparently_To() + η()\n + X_Originating_IP() + η()\n + Return_Path() + η()\n + Authentication_Results() + η()\n + Received() + η()\n + Received() + η()\n + From() + η()\n + Message_ID() + η()\n + Date() + η()\n + Subject() + η()\n + To() + η()\n + MIME_Version() + η()\n + Content_Type() + η()\n + σ(\'X-Spam-Flag:\') + μ() + φ(r"[A-Z]+") + η()\n + Content_Length() + η()\n': 1,
 'φ(From_rex) + η()\n + X_Account_Key() + η()\n + X_UIDL() + η()\n + X_Mozilla_Status() + η()\n + X_Mozilla_Status2() + η()\n + X_Mozilla_Keys() + η()\n + X_Apparently_To() + η()\n + X_Originating_IP() + η()\n + Return_Path() + η()\n + Authentication_Results() + η()\n + Received() + η()\n + Received() + η()\n + Message_ID() + η()\n + From() + η()\n + To() + η()\n + Subject() + η()\n + Date() + η()\n + MIME_Version() + η()\n + Content_Type() + η()\n + X_Priority() + η()\n + X_MSMail_Priority() + η()\n + X_Mailer() + η()\n + X_MimeOLE() + η()\n + Content_Length() + η()\n': 2,
 'φ(From_rex) + η()\n + X_Account_Key() + η()\n + X_UIDL() + η()\n + X_Mozilla_Status() + η()\n + X_Mozilla_Status2() + η()\n + X_Mozilla_Keys() + η()\n + X_Apparently_To() + η()\n + X_Originating_IP() + η()\n + Return_Path() + η()\n + Authentication_Results() + η()\n + Received() + η()\n + Received() + η()\n + Message_ID() + η()\n + From() + η()\n + To() + η()\n + Subject() + η()\n + Date() + η()\n + MIME_Version() + η()\n + Content_Type() + η()\n + X_Priority() + η()\n + X_MSMail_Priority() + η()\n + X_Mailer() + η()\n + X_MimeOLE() + η()\n + X_Virus_Scanned() + η()\n + Content_Length() + η()\n': 1,
 'φ(From_rex) + η()\n + X_Account_Key() + η()\n + X_UIDL() + η()\n + X_Mozilla_Status() + η()\n + X_Mozilla_Status2() + η()\n + X_Mozilla_Keys() + η()\n + X_Apparently_To() + η()\n + X_Originating_IP() + η()\n + Return_Path() + η()\n + Authentication_Results() + η()\n + Received() + η()\n + Received() + η()\n + Message_ID() + η()\n + Return_Path() + η()\n + Content_Type() + η()\n + X_Originating_IP() + η()\n + From() + η()\n + To() + η()\n + Subject() + η()\n + Date() + η()\n + Importance() + η()\n + MIME_Version() + η()\n + X_OriginalArrivalTime() + η()\n + Content_Length() + η()\n': 1,
 'φ(From_rex) + η()\n + X_Account_Key() + η()\n + X_UIDL() + η()\n + X_Mozilla_Status() + η()\n + X_Mozilla_Status2() + η()\n + X_Mozilla_Keys() + η()\n + X_Apparently_To() + η()\n + X_Originating_IP() + η()\n + Return_Path() + η()\n + Authentication_Results() + η()\n + Received() + η()\n + Received() + η()\n + Message_ID() + η()\n + Return_Path() + η()\n + Content_Type() + η()\n + X_Originating_IP() + η()\n + From() + η()\n + To() + η()\n + μ() + σ(\'<\') + φ(r"[a-z]+") + σ(\'.\') + φ(r"[a-z]+") + σ(\'@\') + φ(r"[a-z]+") + σ(\'.\') + φ(r"[a-z]+") + σ(\'>\') + η()\n + Subject() + η()\n + Date() + η()\n + Importance() + η()\n + MIME_Version() + η()\n + X_OriginalArrivalTime() + η()\n + Content_Length() + η()\n': 2,
 'φ(From_rex) + η()\n + X_Account_Key() + η()\n + X_UIDL() + η()\n + X_Mozilla_Status() + η()\n + X_Mozilla_Status2() + η()\n + X_Mozilla_Keys() + η()\n + X_Apparently_To() + η()\n + X_Originating_IP() + η()\n + Return_Path() + η()\n + Authentication_Results() + η()\n + Received() + η()\n + Received() + η()\n + Message_ID() + η()\n + σ(\'Reply-To:\') + μ() + σ(\'"\') + φ(r"[A-Z]") + φ(r"[a-z]+") + μ() + φ(r"[A-Z]") + φ(r"[a-z]+") + σ(\'"\') + μ() + σ(\'<\') + φ(r"[a-z]+") + σ(\'@\') + φ(r"[a-z]+") + σ(\'.\') + φ(r"[a-z]+") + σ(\'>\') + η()\n + From() + η()\n + To() + η()\n + Subject() + η()\n + Date() + η()\n + MIME_Version() + η()\n + Content_Type() + η()\n + X_Priority() + η()\n + X_MSMail_Priority() + η()\n + X_Mailer() + η()\n + X_MimeOLE() + η()\n + σ(\'X-ELNK-Trace:\') + μ() + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[0-9]+") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[0-9]+") + φ(r"[a-z]") + φ(r"[0-9]+") + φ(r"[a-z]") + φ(r"[0-9]+") + φ(r"[a-z]+") + φ(r"[0-9]+") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[0-9]+") + φ(r"[a-z]+") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[0-9]+") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[0-9]+") + φ(r"[a-z]") + φ(r"[0-9]+") + φ(r"[a-z]") + φ(r"[0-9]+") + φ(r"[a-z]") + φ(r"[0-9]+") + φ(r"[a-z]") + φ(r"[0-9]+") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[0-9]+") + φ(r"[a-z]+") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[0-9]+") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[0-9]+") + φ(r"[a-z]+") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[0-9]+") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[0-9]+") + φ(r"[a-z]+") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[0-9]+") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[a-z]") + η()\n + X_Originating_IP() + η()\n + Content_Length() + η()\n': 1,
 'φ(From_rex) + η()\n + X_Account_Key() + η()\n + X_UIDL() + η()\n + X_Mozilla_Status() + η()\n + X_Mozilla_Status2() + η()\n + X_Mozilla_Keys() + η()\n + X_Apparently_To() + η()\n + X_Originating_IP() + η()\n + Return_Path() + η()\n + Authentication_Results() + η()\n + Received() + η()\n + Received() + η()\n + Message_ID() + η()\n + σ(\'Reply-To:\') + μ() + σ(\'"\') + φ(r"[a-z]+") + μ() + φ(r"[a-z]+") + μ() + φ(r"[a-z]+") + σ(\'"\') + μ() + σ(\'<\') + φ(r"[a-z]+") + σ(\'@\') + φ(r"[a-z]+") + σ(\'-\') + φ(r"[a-z]+") + σ(\'.\') + φ(r"[a-z]+") + σ(\'>\') + η()\n + From() + η()\n + To() + η()\n + References() + η()\n + Subject() + η()\n + Date() + η()\n + MIME_Version() + η()\n + Content_Type() + η()\n + X_Priority() + η()\n + X_MSMail_Priority() + η()\n + X_Mailer() + η()\n + X_MimeOLE() + η()\n + Content_Length() + η()\n': 1,
 'φ(From_rex) + η()\n + X_Account_Key() + η()\n + X_UIDL() + η()\n + X_Mozilla_Status() + η()\n + X_Mozilla_Status2() + η()\n + X_Mozilla_Keys() + η()\n + X_Apparently_To() + η()\n + X_Originating_IP() + η()\n + Return_Path() + η()\n + Authentication_Results() + η()\n + Received() + η()\n + Received() + η()\n + Received() + η()\n + From() + η()\n + To() + η()\n + Date() + η()\n + Subject() + η()\n + Thread_Topic() + η()\n + Thread_Index() + η()\n + Message_ID() + η()\n + σ(\'Accept-Language:\') + μ() + φ(r"[a-z]+") + σ(\'-\') + φ(r"[A-Z]+") + η()\n + σ(\'Content-Language:\') + μ() + φ(r"[a-z]+") + σ(\'-\') + φ(r"[A-Z]+") + η()\n + X_MS_Has_Attach() + η()\n + X_MS_TNEF_Correlator() + η()\n + σ(\'acceptlanguage:\') + μ() + φ(r"[a-z]+") + σ(\'-\') + φ(r"[A-Z]+") + η()\n + Content_Type() + η()\n + MIME_Version() + η()\n + Return_Path() + η()\n + Content_Length() + η()\n': 6,
 'φ(From_rex) + η()\n + X_Account_Key() + η()\n + X_UIDL() + η()\n + X_Mozilla_Status() + η()\n + X_Mozilla_Status2() + η()\n + X_Mozilla_Keys() + η()\n + X_Apparently_To() + η()\n + X_Originating_IP() + η()\n + Return_Path() + η()\n + Authentication_Results() + η()\n + Received() + η()\n + Received() + η()\n + Received() + η()\n + From() + η()\n + To() + η()\n + Subject() + η()\n + Date() + η()\n + Message_ID() + η()\n + MIME_Version() + η()\n + Content_Type() + η()\n + X_Mailer() + η()\n + X_MimeOLE() + η()\n + Thread_Index() + η()\n + Content_Length() + η()\n': 1,
 'φ(From_rex) + η()\n + X_Account_Key() + η()\n + X_UIDL() + η()\n + X_Mozilla_Status() + η()\n + X_Mozilla_Status2() + η()\n + X_Mozilla_Keys() + η()\n + X_Apparently_To() + η()\n + X_Originating_IP() + η()\n + Return_Path() + η()\n + Authentication_Results() + η()\n + Received() + η()\n + Received() + η()\n + Received() + η()\n + Received() + η()\n + Received() + η()\n + From() + η()\n + To() + η()\n + Subject() + η()\n + Date() + η()\n + Message_ID() + η()\n + MIME_Version() + η()\n + Content_Type() + η()\n + X_Mailer() + η()\n + X_MimeOLE() + η()\n + Thread_Index() + η()\n + X_Spam() + η()\n + X_MAIL_FROM() + η()\n + X_SOURCE_IP() + η()\n + X_SF_Loop() + η()\n + Content_Length() + η()\n': 1,
 'φ(From_rex) + η()\n + X_Account_Key() + η()\n + X_UIDL() + η()\n + X_Mozilla_Status() + η()\n + X_Mozilla_Status2() + η()\n + X_Mozilla_Keys() + η()\n + X_Apparently_To() + η()\n + X_Originating_IP() + η()\n + Return_Path() + η()\n + Authentication_Results() + η()\n + Received() + η()\n + Received() + η()\n + Received() + η()\n + X_MimeOLE() + η()\n + Content_class() + η()\n + MIME_Version() + η()\n + Content_Type() + η()\n + Content_Transfer_Encoding() + η()\n + Subject() + η()\n + Date() + η()\n + Message_ID() + η()\n + X_MS_Has_Attach() + η()\n + X_MS_TNEF_Correlator() + η()\n + Importance() + η()\n + Priority() + η()\n + Thread_Topic() + η()\n + Thread_Index() + η()\n + From() + η()\n + To() + η()\n + Return_Path() + η()\n + X_OriginalArrivalTime() + η()\n + Content_Length() + η()\n': 1,
 'φ(From_rex) + η()\n + X_Account_Key() + η()\n + X_UIDL() + η()\n + X_Mozilla_Status() + η()\n + X_Mozilla_Status2() + η()\n + X_Mozilla_Keys() + η()\n + X_Apparently_To() + η()\n + X_Originating_IP() + η()\n + Return_Path() + η()\n + Authentication_Results() + η()\n + Received() + η()\n + Received() + η()\n + Received() + η()\n + X_MimeOLE() + η()\n + Content_class() + η()\n + MIME_Version() + η()\n + Content_Type() + η()\n + Subject() + η()\n + Date() + η()\n + Message_ID() + η()\n + X_MS_Has_Attach() + η()\n + X_MS_TNEF_Correlator() + η()\n + Thread_Topic() + η()\n + Thread_Index() + η()\n + From() + η()\n + To() + η()\n + Return_Path() + η()\n + X_OriginalArrivalTime() + η()\n + Content_Length() + η()\n': 1,
 'φ(From_rex) + η()\n + X_Account_Key() + η()\n + X_UIDL() + η()\n + X_Mozilla_Status() + η()\n + X_Mozilla_Status2() + η()\n + X_Mozilla_Keys() + η()\n + X_Apparently_To() + η()\n + X_Originating_IP() + η()\n + Return_Path() + η()\n + Authentication_Results() + η()\n + Received() + η()\n + Received() + η()\n + Received() + η()\n + X_MimeOLE() + η()\n + Content_class() + η()\n + MIME_Version() + η()\n + Content_Type() + η()\n + Subject() + η()\n + Date() + η()\n + Message_ID() + η()\n + X_MS_Has_Attach() + η()\n + X_MS_TNEF_Correlator() + η()\n + Thread_Topic() + η()\n + Thread_Index() + η()\n + References() + η()\n + From() + η()\n + To() + η()\n + Cc() + η()\n + Return_Path() + η()\n + X_OriginalArrivalTime() + η()\n + Content_Length() + η()\n': 1,
 'φ(From_rex) + η()\n + X_Account_Key() + η()\n + X_UIDL() + η()\n + X_Mozilla_Status() + η()\n + X_Mozilla_Status2() + η()\n + X_Mozilla_Keys() + η()\n + X_Apparently_To() + η()\n + X_Originating_IP() + η()\n + Return_Path() + η()\n + Authentication_Results() + η()\n + Received() + η()\n + Received() + η()\n + X_MimeOLE() + η()\n + Content_class() + η()\n + MIME_Version() + η()\n + Content_Type() + η()\n + Subject() + η()\n + Date() + η()\n + Message_ID() + η()\n + In_Reply_To() + η()\n + X_MS_Has_Attach() + η()\n + X_MS_TNEF_Correlator() + η()\n + Thread_Topic() + η()\n + Thread_Index() + η()\n + From() + η()\n + To() + η()\n + Cc() + η()\n + Return_Path() + η()\n + X_OriginalArrivalTime() + η()\n + Content_Length() + η()\n': 1,
 'φ(From_rex) + η()\n + X_Account_Key() + η()\n + X_UIDL() + η()\n + X_Mozilla_Status() + η()\n + X_Mozilla_Status2() + η()\n + X_Mozilla_Keys() + η()\n + X_Apparently_To() + η()\n + X_Originating_IP() + η()\n + Return_Path() + η()\n + Authentication_Results() + η()\n + Received() + η()\n + Received() + η()\n + X_MimeOLE() + η()\n + Content_class() + η()\n + MIME_Version() + η()\n + Content_Type() + η()\n + Subject() + η()\n + Date() + η()\n + Message_ID() + η()\n + X_MS_Has_Attach() + η()\n + X_MS_TNEF_Correlator() + η()\n + Thread_Topic() + η()\n + Thread_Index() + η()\n + From() + η()\n + To() + η()\n + Cc() + η()\n + Return_Path() + η()\n + X_OriginalArrivalTime() + η()\n + Content_Length() + η()\n': 1,
 'φ(From_rex) + η()\n + X_Account_Key() + η()\n + X_UIDL() + η()\n + X_Mozilla_Status() + η()\n + X_Mozilla_Status2() + η()\n + X_Mozilla_Keys() + η()\n + X_Apparently_To() + η()\n + X_Originating_IP() + η()\n + Return_Path() + η()\n + Authentication_Results() + η()\n + Received() + η()\n + Received() + η()\n + X_MimeOLE() + η()\n + Content_class() + η()\n + MIME_Version() + η()\n + Content_Type() + η()\n + Subject() + η()\n + Date() + η()\n + Message_ID() + η()\n + X_MS_Has_Attach() + η()\n + X_MS_TNEF_Correlator() + η()\n + Thread_Topic() + η()\n + Thread_Index() + η()\n + From() + η()\n + To() + η()\n + Return_Path() + η()\n + X_OriginalArrivalTime() + η()\n + Content_Length() + η()\n': 1,
 'φ(From_rex) + η()\n + X_Account_Key() + η()\n + X_UIDL() + η()\n + X_Mozilla_Status() + η()\n + X_Mozilla_Status2() + η()\n + X_Mozilla_Keys() + η()\n + X_Apparently_To() + η()\n + X_Originating_IP() + η()\n + Return_Path() + η()\n + Authentication_Results() + η()\n + Received() + η()\n + X_MimeOLE() + η()\n + Content_class() + η()\n + MIME_Version() + η()\n + Content_Type() + η()\n + Subject() + η()\n + Date() + η()\n + Message_ID() + η()\n + X_MS_Has_Attach() + η()\n + X_MS_TNEF_Correlator() + η()\n + Thread_Topic() + η()\n + Thread_Index() + η()\n + From() + η()\n + To() + η()\n + Cc() + η()\n + Content_Length() + η()\n': 1}
