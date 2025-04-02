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
|   φ(rex_From) + η() + X_Account_Key() + η() + X_UIDL() + η() + X_Mozilla_Status() + η() + X_Mozilla_Status2() + η() + X_Mozilla_Keys() + η() + X_Apparently_To() + η() + X_Originating_IP() + η() + Return_Path() + η() + Authentication_Results() + η() + Received() + η() + Received() + η() + Received() + η() + From() + η() + To() + η() + Date() + η() + Subject() + η() + Thread_Topic() + η() + Thread_Index() + η() + Message_ID() + η() + σ('Accept-Language:') + μ() + φ(r"[a-z]+") + σ('-') + φ(r"[A-Z]+") + η() + σ('Content-Language:') + μ() + φ(r"[a-z]+") + σ('-') + φ(r"[A-Z]+") + η() + X_MS_Has_Attach() + η() + X_MS_TNEF_Correlator() + η() + σ('acceptlanguage:') + μ() + φ(r"[a-z]+") + σ('-') + φ(r"[A-Z]+") + η() + Content_Type() + η() + MIME_Version() + η() + Return_Path() + η() + Content_Length() + η()
|   φ(rex_From) + η() + X_Account_Key() + η() + X_UIDL() + η() + X_Mozilla_Status() + η() + X_Mozilla_Status2() + η() + X_Mozilla_Keys() + η() + X_Apparently_To() + η() + X_Originating_IP() + η() + Return_Path() + η() + Authentication_Results() + η() + Received() + η() + Received() + η() + Received() + η() + From() + η() + To() + η() + Date() + η() + Subject() + η() + Thread_Topic() + η() + Thread_Index() + φ(r"[A-Z]+") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[A-Z]") + σ('=') + σ('=') + η() + Message_ID() + η() + σ('Accept-Language:') + μ() + φ(r"[a-z]+") + σ('-') + φ(r"[A-Z]+") + η() + σ('Content-Language:') + μ() + φ(r"[a-z]+") + σ('-') + φ(r"[A-Z]+") + η() + X_MS_Has_Attach() + η() + X_MS_TNEF_Correlator() + η() + σ('acceptlanguage:') + μ() + φ(r"[a-z]+") + σ('-') + φ(r"[A-Z]+") + η() + Content_Type() + η() + MIME_Version() + η() + Return_Path() + η() + Content_Length() + η()
|   φ(rex_From) + η() + X_Account_Key() + η() + X_UIDL() + η() + X_Mozilla_Status() + η() + X_Mozilla_Status2() + η() + X_Mozilla_Keys() + η() + X_Apparently_To() + η() + X_Originating_IP() + η() + Return_Path() + η() + Authentication_Results() + η() + Received() + η() + Received() + η() + Received() + η() + From() + η() + To() + η() + Date() + η() + Subject() + η() + Thread_Topic() + η() + Thread_Index() + φ(r"[A-Z]+") + σ('+') + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[A-Z]") + η() + Message_ID() + η() + σ('Accept-Language:') + μ() + φ(r"[a-z]+") + σ('-') + φ(r"[A-Z]+") + η() + σ('Content-Language:') + μ() + φ(r"[a-z]+") + σ('-') + φ(r"[A-Z]+") + η() + X_MS_Has_Attach() + η() + X_MS_TNEF_Correlator() + η() + σ('acceptlanguage:') + μ() + φ(r"[a-z]+") + σ('-') + φ(r"[A-Z]+") + η() + Content_Type() + η() + MIME_Version() + η() + Return_Path() + η() + Content_Length() + η()
|   φ(rex_From) + η() + X_Account_Key() + η() + X_UIDL() + η() + X_Mozilla_Status() + η() + X_Mozilla_Status2() + η() + X_Mozilla_Keys() + η() + X_Apparently_To() + η() + X_Originating_IP() + η() + Return_Path() + η() + Authentication_Results() + η() + Received() + η() + Received() + η() + Message_ID() + η() + Return_Path() + η() + Content_Type() + η() + X_Originating_IP() + η() + From() + η() + To() + η() + Subject() + η() + Date() + η() + Importance() + η() + MIME_Version() + η() + X_OriginalArrivalTime() + η() + Content_Length() + η()
|   φ(rex_From) + η() + X_Account_Key() + η() + X_UIDL() + η() + X_Mozilla_Status() + η() + X_Mozilla_Status2() + η() + X_Mozilla_Keys() + η() + X_Apparently_To() + η() + X_Originating_IP() + η() + Return_Path() + η() + Authentication_Results() + η() + Received() + η() + Received() + η() + DomainKey_Signature() + η() + μ() + φ(r"[a-z]") + σ('=') + φ(r"[A-Z]") + σ('-') + φ(r"[A-Z]+") + φ(r"[a-z]+") + σ('-') + φ(r"[A-Z]+") + σ(':') + Received() + η() + σ('X-YMail-OSG:') + μ() + φ(r"[A-Z]+") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[0-9]") + σ('_') + φ(r"[0-9]") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[A-Z]+") + σ('_') + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]") + σ('_') + φ(r"[A-Z]+") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[0-9]") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]+") + σ('.') + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + σ('-') + σ('-') + η() + Received() + η() + Date() + η() + From() + η() + Subject() + η() + To() + η() + MIME_Version() + η() + Content_Type() + η() + Message_ID() + η() + Content_Length() + η()
|   φ(rex_From) + η() + X_Account_Key() + η() + X_UIDL() + η() + X_Mozilla_Status() + η() + X_Mozilla_Status2() + η() + X_Mozilla_Keys() + η() + X_Apparently_To() + η() + X_Originating_IP() + η() + Return_Path() + η() + Authentication_Results() + η() + Received() + η() + Received() + η() + Message_ID() + η() + Return_Path() + η() + Content_Type() + η() + X_Originating_IP() + η() + From() + η() + To() + η() + μ() + σ('<') + φ(r"[a-z]+") + σ('.') + φ(r"[a-z]+") + σ('@') + φ(r"[a-z]+") + σ('.') + φ(r"[a-z]+") + σ('>') + η() + Subject() + η() + Date() + η() + Importance() + η() + MIME_Version() + η() + X_OriginalArrivalTime() + η() + Content_Length() + η()
|   φ(rex_From) + η() + X_Account_Key() + η() + X_UIDL() + η() + X_Mozilla_Status() + η() + X_Mozilla_Status2() + η() + X_Mozilla_Keys() + η() + X_Apparently_To() + η() + X_Originating_IP() + η() + Return_Path() + η() + Authentication_Results() + η() + Received() + η() + Received() + η() + DomainKey_Signature() + η() + μ() + φ(r"[a-z]") + σ('=') + φ(r"[A-Z]") + σ('-') + φ(r"[A-Z]+") + φ(r"[a-z]+") + σ('-') + φ(r"[A-Z]+") + σ(':') + Received() + η() + σ('X-YMail-OSG:') + μ() + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[a-z]") + σ('.') + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[a-z]+") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[0-9]") + σ('_') + φ(r"[0-9]") + φ(r"[A-Z]+") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[A-Z]") + σ('.') + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[0-9]+") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[A-Z]+") + σ('_') + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[A-Z]") + σ('-') + σ('-') + η() + Received() + η() + Date() + η() + From() + η() + Subject() + η() + To() + η() + MIME_Version() + η() + Content_Type() + η() + Message_ID() + η() + Content_Length() + η()
|   φ(rex_From) + η() + X_Account_Key() + η() + X_UIDL() + η() + X_Mozilla_Status() + η() + X_Mozilla_Status2() + η() + X_Mozilla_Keys() + η() + X_Apparently_To() + η() + X_Originating_IP() + η() + Return_Path() + η() + Authentication_Results() + η() + Received() + η() + Received() + η() + DomainKey_Signature() + η() + μ() + φ(r"[a-z]") + σ('=') + φ(r"[A-Z]") + σ('-') + φ(r"[A-Z]+") + φ(r"[a-z]+") + σ('-') + φ(r"[A-Z]+") + σ(':') + Received() + η() + σ('X-YMail-OSG:') + μ() + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[0-9]+") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[0-9]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[0-9]+") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[0-9]+") + φ(r"[A-Z]+") + φ(r"[a-z]+") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[0-9]+") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[0-9]+") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[0-9]+") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[0-9]") + σ('.') + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[a-z]+") + σ('_') + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]") + σ('-') + η() + Received() + η() + Date() + η() + From() + η() + Subject() + η() + To() + η() + MIME_Version() + η() + Content_Type() + η() + Message_ID() + η() + Content_Length() + η()
|   φ(rex_From) + η() + X_Account_Key() + η() + X_UIDL() + η() + X_Mozilla_Status() + η() + X_Mozilla_Status2() + η() + X_Mozilla_Keys() + η() + X_Apparently_To() + η() + X_Originating_IP() + η() + Return_Path() + η() + Authentication_Results() + η() + Received() + η() + Received() + η() + DomainKey_Signature() + η() + μ() + φ(r"[a-z]") + σ('=') + φ(r"[A-Z]") + σ('-') + φ(r"[A-Z]+") + φ(r"[a-z]+") + σ('-') + φ(r"[A-Z]+") + σ(':') + Received() + η() + σ('X-YMail-OSG:') + μ() + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[0-9]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[0-9]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[0-9]+") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]+") + σ('.') + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]+") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]+") + σ('-') + η() + Received() + η() + Date() + η() + From() + η() + Subject() + η() + To() + η() + MIME_Version() + η() + Content_Type() + η() + Message_ID() + η() + Content_Length() + η()
|   φ(rex_From) + η() + X_Account_Key() + η() + X_UIDL() + η() + X_Mozilla_Status() + η() + X_Mozilla_Status2() + η() + X_Mozilla_Keys() + η() + X_Apparently_To() + η() + X_Originating_IP() + η() + Return_Path() + η() + Authentication_Results() + η() + Received() + η() + Received() + η() + DomainKey_Signature() + η() + μ() + φ(r"[a-z]") + σ('=') + φ(r"[A-Z]") + σ('-') + φ(r"[A-Z]+") + φ(r"[a-z]+") + σ('-') + φ(r"[A-Z]+") + σ(':') + Received() + η() + σ('X-YMail-OSG:') + μ() + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[0-9]+") + φ(r"[A-Z]") + φ(r"[0-9]") + σ('.') + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + σ('.') + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[A-Z]+") + σ('.') + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[0-9]+") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[A-Z]") + σ('.') + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[0-9]+") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[0-9]+") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[a-z]+") + σ('-') + η() + Received() + η() + Date() + η() + From() + η() + Subject() + η() + To() + η() + MIME_Version() + η() + Content_Type() + η() + Message_ID() + η() + Content_Length() + η()
|   φ(rex_From) + η() + X_Account_Key() + η() + X_UIDL() + η() + X_Mozilla_Status() + η() + X_Mozilla_Status2() + η() + X_Mozilla_Keys() + η() + X_Apparently_To() + η() + X_Originating_IP() + η() + Return_Path() + η() + Authentication_Results() + η() + Received() + η() + Received() + η() + DomainKey_Signature() + η() + μ() + φ(r"[a-z]") + σ('=') + φ(r"[A-Z]") + σ('-') + φ(r"[A-Z]+") + φ(r"[a-z]+") + σ('-') + φ(r"[A-Z]+") + σ(':') + Received() + η() + σ('X-YMail-OSG:') + μ() + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[A-Z]") + σ('.') + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[0-9]+") + φ(r"[a-z]+") + φ(r"[0-9]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[0-9]+") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + σ('.') + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[0-9]+") + φ(r"[a-z]+") + φ(r"[A-Z]+") + σ('_') + φ(r"[a-z]+") + φ(r"[0-9]+") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]+") + φ(r"[0-9]") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[0-9]+") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[0-9]") + φ(r"[a-z]") + σ('_') + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[0-9]+") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]+") + φ(r"[A-Z]") + σ('_') + φ(r"[A-Z]") + φ(r"[a-z]") + σ('-') + σ('-') + η() + Received() + η() + Date() + η() + From() + η() + Subject() + η() + To() + η() + MIME_Version() + η() + Content_Type() + η() + Message_ID() + η() + Content_Length() + η()
|   φ(rex_From) + η() + X_Account_Key() + η() + X_UIDL() + η() + X_Mozilla_Status() + η() + X_Mozilla_Status2() + η() + X_Mozilla_Keys() + η() + X_Apparently_To() + η() + X_Originating_IP() + η() + Return_Path() + η() + Authentication_Results() + η() + Received() + η() + Received() + η() + Received() + η() + X_MimeOLE() + η() + Content_class() + η() + MIME_Version() + η() + Content_Type() + η() + Subject() + η() + Date() + η() + Message_ID() + η() + X_MS_Has_Attach() + η() + X_MS_TNEF_Correlator() + η() + Thread_Topic() + η() + Thread_Index() + η() + From() + η() + To() + η() + Return_Path() + η() + X_OriginalArrivalTime() + η() + Content_Length() + η()
|   φ(rex_From) + η() + X_Account_Key() + η() + X_UIDL() + η() + X_Mozilla_Status() + η() + X_Mozilla_Status2() + η() + X_Mozilla_Keys() + η() + X_Apparently_To() + η() + X_Originating_IP() + η() + Return_Path() + η() + Authentication_Results() + η() + Received() + η() + Received() + η() + Message_ID() + η() + From() + η() + To() + η() + Subject() + η() + Date() + η() + MIME_Version() + η() + Content_Type() + η() + X_Priority() + η() + X_MSMail_Priority() + η() + X_Mailer() + η() + X_MimeOLE() + η() + Content_Length() + η()
|   φ(rex_From) + η() + X_Account_Key() + η() + X_UIDL() + η() + X_Mozilla_Status() + η() + X_Mozilla_Status2() + η() + X_Mozilla_Keys() + η() + X_Apparently_To() + η() + X_Originating_IP() + η() + Return_Path() + η() + Authentication_Results() + η() + Received() + η() + Received() + η() + DomainKey_Signature() + η() + μ() + φ(r"[a-z]") + σ('=') + φ(r"[A-Z]") + σ('-') + φ(r"[A-Z]+") + φ(r"[a-z]+") + σ('-') + φ(r"[A-Z]+") + σ(':') + Received() + η() + σ('X-YMail-OSG:') + μ() + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + σ('.') + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[a-z]+") + σ('.') + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[A-Z]") + σ('.') + φ(r"[0-9]+") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[a-z]") + σ('_') + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[0-9]") + φ(r"[A-Z]+") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[0-9]+") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[A-Z]+") + σ('_') + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]") + φ(r"[A-Z]") + φ(r"[a-z]+") + φ(r"[A-Z]+") + φ(r"[a-z]") + φ(r"[0-9]+") + φ(r"[A-Z]+") + φ(r"[a-z]+") + φ(r"[A-Z]") + φ(r"[0-9]+") + φ(r"[a-z]") + φ(r"[A-Z]+") + φ(r"[a-z]+") + φ(r"[0-9]") + φ(r"[A-Z]") + φ(r"[0-9]") + σ('.') + φ(r"[A-Z]+") + η() + Received() + η() + Date() + η() + From() + η() + Subject() + η() + To() + η() + MIME_Version() + η() + Content_Type() + η() + Message_ID() + η() + Content_Length() + η()
|   φ(rex_From) + η() + X_Account_Key() + η() + X_UIDL() + η() + X_Mozilla_Status() + η() + X_Mozilla_Status2() + η() + X_Mozilla_Keys() + η() + X_Apparently_To() + η() + X_Originating_IP() + η() + Return_Path() + η() + Authentication_Results() + η() + Received() + η() + X_MimeOLE() + η() + Content_class() + η() + MIME_Version() + η() + Content_Type() + η() + Subject() + η() + Date() + η() + Message_ID() + η() + X_MS_Has_Attach() + η() + X_MS_TNEF_Correlator() + η() + Thread_Topic() + η() + Thread_Index() + η() + From() + η() + To() + η() + Cc() + η() + Content_Length() + η()
|   φ(rex_From) + η() + X_Account_Key() + η() + X_UIDL() + η() + X_Mozilla_Status() + η() + X_Mozilla_Status2() + η() + X_Mozilla_Keys() + η() + X_Apparently_To() + η() + X_Originating_IP() + η() + Return_Path() + η() + Authentication_Results() + η() + Received() + η() + Received() + η() + Message_ID() + η() + σ('Reply-To:') + μ() + σ('"') + φ(r"[A-Z]") + φ(r"[a-z]+") + μ() + φ(r"[A-Z]") + φ(r"[a-z]+") + σ('"') + μ() + σ('<') + φ(r"[a-z]+") + σ('@') + φ(r"[a-z]+") + σ('.') + φ(r"[a-z]+") + σ('>') + η() + From() + η() + To() + η() + Subject() + η() + Date() + η() + MIME_Version() + η() + Content_Type() + η() + X_Priority() + η() + X_MSMail_Priority() + η() + X_Mailer() + η() + X_MimeOLE() + η() + σ('X-ELNK-Trace:') + μ() + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[0-9]+") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[0-9]+") + φ(r"[a-z]") + φ(r"[0-9]+") + φ(r"[a-z]") + φ(r"[0-9]+") + φ(r"[a-z]+") + φ(r"[0-9]+") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[0-9]+") + φ(r"[a-z]+") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[0-9]+") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[0-9]+") + φ(r"[a-z]") + φ(r"[0-9]+") + φ(r"[a-z]") + φ(r"[0-9]+") + φ(r"[a-z]") + φ(r"[0-9]+") + φ(r"[a-z]") + φ(r"[0-9]+") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[0-9]+") + φ(r"[a-z]+") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[0-9]+") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[0-9]+") + φ(r"[a-z]+") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[0-9]+") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[a-z]") + φ(r"[0-9]+") + φ(r"[a-z]+") + φ(r"[0-9]") + φ(r"[a-z]+") + φ(r"[0-9]+") + φ(r"[a-z]") + φ(r"[0-9]") + φ(r"[a-z]") + η() + X_Originating_IP() + η() + Content_Length() + η()
|   φ(rex_From) + η() + X_Account_Key() + η() + X_UIDL() + η() + X_Mozilla_Status() + η() + X_Mozilla_Status2() + η() + X_Mozilla_Keys() + η() + X_Apparently_To() + η() + X_Originating_IP() + η() + Return_Path() + η() + Authentication_Results() + η() + Received() + η() + Received() + η() + Message_ID() + η() + σ('Reply-To:') + μ() + σ('"') + φ(r"[a-z]+") + μ() + φ(r"[a-z]+") + μ() + φ(r"[a-z]+") + σ('"') + μ() + σ('<') + φ(r"[a-z]+") + σ('@') + φ(r"[a-z]+") + σ('-') + φ(r"[a-z]+") + σ('.') + φ(r"[a-z]+") + σ('>') + η() + From() + η() + To() + η() + References() + η() + Subject() + η() + Date() + η() + MIME_Version() + η() + Content_Type() + η() + X_Priority() + η() + X_MSMail_Priority() + η() + X_Mailer() + η() + X_MimeOLE() + η() + Content_Length() + η()
|   φ(rex_From) + η() + X_Account_Key() + η() + X_UIDL() + η() + X_Mozilla_Status() + η() + X_Mozilla_Status2() + η() + X_Mozilla_Keys() + η() + X_Apparently_To() + η() + X_Originating_IP() + η() + Return_Path() + η() + Authentication_Results() + η() + Received() + η() + Received() + η() + From() + η() + Message_ID() + η() + Date() + η() + Subject() + η() + To() + η() + MIME_Version() + η() + Content_Type() + η() + σ('X-Spam-Flag:') + μ() + φ(r"[A-Z]+") + η() + Content_Length() + η()
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_Account_Key(): yield from (
    r'account1'
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_UIDL(): yield from (
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_Mozilla_Status(): yield from (
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_Mozilla_Status2(): yield from (
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_Mozilla_Keys(): yield from (
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_Apparently_To(): yield from (
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_Originating_IP(): yield from (
    r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'
   #1:4.230.144.125
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def Return_Path(): yield from (
    r'<[a-z]{3}\.[a-z]{5}@[a-z]{5}\.[a-z]{3}>'
   #1:<ken.moses@quest.com>
   #2:<adi.izhar@quest.com>
|   r'[A-Z][a-z]{2}\.[A-Z][a-z]{4}@[a-z]{5}\.[a-z]{3}'
   #1:Ken.Moses@quest.com
|   r'<[a-z]{3}\.[a-z]{4}@[a-z]{5}\.[a-z]{3}>'
   #1:<pat.luis@quest.com>
|   r'[a-z]{3}\.[a-z]{4}@[a-z]{5}\.[a-z]{3}'
   #1:pat.luis@quest.com
|   r'<[a-z]{4}\.[a-z]{7}@[a-z]{5}\.[a-z]{3}>'
   #1:<lisa.radford@quest.com>
|   r'[A-Z][a-z]{3}\.[A-Z][a-z]{6}@[a-z]{5}\.[a-z]{3}'
   #1:Lisa.Radford@quest.com
|   r'<[a-z]{5}\.[a-z]{8}@[a-z]{5}\.[a-z]{3}>'
   #1:<keren.kamilian@quest.com>
|   r'[A-Z][a-z]{4}\.[A-Z][a-z]{7}@[a-z]{5}\.[a-z]{3}'
   #1:Keren.Kamilian@quest.com
|   r'<>'
   #1:<>
|   r'<[a-z]{3}\.[a-z]{12}@[a-z]{5}\.[a-z]{3}>'
   #5:<lon.cherryholmes@quest.com>
|   r'<[A-Z][a-z]{2}\.[A-Z][a-z]{11}@[a-z]{5}\.[a-z]{3}>'
   #1:<Lon.Cherryholmes@quest.com>
|   r'<[a-z]{4}\.[a-z]{8}@[a-z]{14}\.[a-z]{3}>'
   #1:<tony.delollis@ventisolutions.com>
|   r'<[a-z]{10}@[a-z]{6}\.[a-z]{2}\.[a-z]{3}>'
   #1:<rbullerman@austin.rr.com>
|   r'<[a-z]{4}\.[a-z]{3}@[a-z]{8}\-[a-z]{8}\.[a-z]{3}>'
   #1:<jeff.omo@database-brothers.com>
|   r'[A-Z][a-z]{2}\.[A-Z][a-z]{11}@[a-z]{5}\.[a-z]{3}'
   #4:Lon.Cherryholmes@quest.com
|   r'[a-z]{3}\.[a-z]{5}@[a-z]{5}\.[a-z]{3}'
   #2:adi.izhar@quest.com
|   r'<[a-z]{18}@[a-z]{7}\.[a-z]{3}>'
   #3:<lesliecherryholmes@hotmail.com>
|   r'[a-z]{18}@[a-z]{7}\.[a-z]{3}'
   #3:lesliecherryholmes@hotmail.com
|   r'<[a-z]{4}_[0-9]{5}@[a-z]{5}\.[a-z]{3}>'
   #6:<ness_78759@yahoo.com>
|   r'<[a-z]{8}@[a-z]{5}\.[a-z]{3}>'
   #1:<lcherryh@yahoo.com>
|   r'<[a-z]{5}\.[a-z]{6}@[a-z]{5}\.[a-z]{3}>'
   #1:<chris.sheets@alcoa.com>
|   r'[A-Z][a-z]{4}\.[A-Z][a-z]{5}@[a-z]{5}\.[a-z]{3}'
   #1:Chris.Sheets@alcoa.com
|   r'<[a-z]{8}@[a-z]{6}\.[a-z]{2}\.[a-z]{3}>'
   #2:<tdeatley@austin.rr.com>
|   r'<[a-z]{9}@[a-z]{19}\.[a-z]{3}>'
   #1:<bthompson@riverranchradiology.com>
|   r'<[a-z]{11}@[a-z]{8}\.[a-z]{3}>'
   #1:<shalomyaall@peoplepc.com>
|   r'<[a-z]{5}@[a-z]{2}\-[a-z]{2}\.[a-z]{3}>'
   #1:<parts@mw-ar.com>
|   r'<[a-z]{11}[0-9]{2}@[a-z]{3}\.[a-z]{3}>'
   #1:<cmoneymaker72@aol.com>
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def Authentication_Results(): yield from (
    r'mta526\.mail\.mud\.yahoo\.com\ \ from=quest\.com;\ domainkeys=neutral\ \(no\ sig\)'
|   r'mta188\.mail\.re3\.yahoo\.com\ \ from=quest\.com;\ domainkeys=neutral\ \(no\ sig\)'
|   r'mta224\.mail\.re4\.yahoo\.com\ \ from=quest\.com;\ domainkeys=neutral\ \(no\ sig\)'
|   r'mta368\.mail\.re4\.yahoo\.com\ \ from=quest\.com;\ domainkeys=neutral\ \(no\ sig\)'
|   r'mta243\.mail\.re4\.yahoo\.com\ \ from=yahoogroups\.com;\ domainkeys=pass\ \(ok\)'
|   r'mta305\.mail\.re4\.yahoo\.com\ \ from=quest\.com;\ domainkeys=neutral\ \(no\ sig\)'
|   r'mta179\.mail\.re4\.yahoo\.com\ \ from=VentiSolutions\.com;\ domainkeys=neutral\ \(no\ sig\)'
|   r'mta416\.mail\.mud\.yahoo\.com\ \ from=austin\.rr\.com;\ domainkeys=neutral\ \(no\ sig\)'
|   r'mta191\.mail\.re3\.yahoo\.com\ \ from=database\-brothers\.com;\ domainkeys=neutral\ \(no\ sig\)'
|   r'mta199\.mail\.re4\.yahoo\.com\ \ from=quest\.com;\ domainkeys=neutral\ \(no\ sig\)'
|   r'mta312\.mail\.mud\.yahoo\.com\ \ from=quest\.com;\ domainkeys=neutral\ \(no\ sig\)'
|   r'mta303\.mail\.mud\.yahoo\.com\ \ from=quest\.com;\ domainkeys=neutral\ \(no\ sig\)'
|   r'mta219\.mail\.mud\.yahoo\.com\ \ from=quest\.com;\ domainkeys=neutral\ \(no\ sig\)'
|   r'mta233\.mail\.re4\.yahoo\.com\ \ from=hotmail\.com;\ domainkeys=neutral\ \(no\ sig\)'
|   r'mta234\.mail\.re3\.yahoo\.com\ \ from=yahoo\.com;\ domainkeys=pass\ \(ok\)'
|   r'mta253\.mail\.mud\.yahoo\.com\ \ from=hotmail\.com;\ domainkeys=neutral\ \(no\ sig\)'
|   r'mta233\.mail\.mud\.yahoo\.com\ \ from=yahoo\.com;\ domainkeys=pass\ \(ok\)'
|   r'mta499\.mail\.mud\.yahoo\.com\ \ from=yahoo\.com;\ domainkeys=pass\ \(ok\)'
|   r'mta203\.mail\.mud\.yahoo\.com\ \ from=hotmail\.com;\ domainkeys=neutral\ \(no\ sig\)'
|   r'mta352\.mail\.mud\.yahoo\.com\ \ from=yahoo\.com;\ domainkeys=pass\ \(ok\)'
|   r'mta186\.mail\.re4\.yahoo\.com\ \ from=quest\.com;\ domainkeys=neutral\ \(no\ sig\)'
|   r'mta159\.mail\.re4\.yahoo\.com\ \ from=yahoo\.com;\ domainkeys=pass\ \(ok\)'
|   r'mta230\.mail\.re4\.yahoo\.com\ \ from=yahoo\.com;\ domainkeys=pass\ \(ok\)'
|   r'mta188\.mail\.mud\.yahoo\.com\ \ from=alcoa\.com;\ domainkeys=neutral\ \(no\ sig\)'
|   r'mta268\.mail\.re4\.yahoo\.com\ \ from=austin\.rr\.com;\ domainkeys=neutral\ \(no\ sig\)'
|   r'mta500\.mail\.mud\.yahoo\.com\ \ from=yahoo\.com;\ domainkeys=pass\ \(ok\)'
|   r'mta243\.mail\.re4\.yahoo\.com\ \ from=riverranchradiology\.com;\ domainkeys=neutral\ \(no\ sig\)'
|   r'mta544\.mail\.mud\.yahoo\.com\ \ from=peoplepc\.com;\ domainkeys=neutral\ \(no\ sig\)'
|   r'mta173\.mail\.re2\.yahoo\.com\ \ from=austin\.rr\.com;\ domainkeys=neutral\ \(no\ sig\)'
|   r'mta294\.mail\.re4\.yahoo\.com\ \ from=mw\-ar\.com;\ domainkeys=neutral\ \(no\ sig\)'
|   r'mta215\.mail\.mud\.yahoo\.com\ \ from=aol\.com;\ domainkeys=neutral\ \(no\ sig\)'
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def Received(): yield from (
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_MimeOLE(): yield from (
    r'[A-Z][a-z]{7} [A-Z][a-z] [A-Z][a-z]{8} [A-Z][a-z]{7} [A-Z][0-9]\.[0-9]'
   #6:Produced By Microsoft Exchange V6.5
|   r'[A-Z][a-z]{7} [A-Z][a-z] [A-Z][a-z]{8} [A-Z][a-z]{3}[A-Z]{3} [A-Z][0-9]\.[0-9]{2}\.[0-9]{4}\.[0-9]{4}'
   #1:Produced By Microsoft MimeOLE V6.00.3790.2929
   #1:Produced By Microsoft MimeOLE V6.00.2900.3138
   #5:Produced By Microsoft MimeOLE V6.00.2900.3198
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def Content_class(): yield from (
    r'urn:content\-classes:message'
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def MIME_Version(): yield from (
    r'1\.0'
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def Content_Type(): yield from (
    r'multipart/mixed;\n\ \ boundary="PytmzYxs55LzQoiEiE\-9nUgfn6JY6oCyUsXFY9Y"'
|   r'multipart/mixed;\n\tboundary="\-\-\-\-_=_NextPart_001_01C7E8C6\.62989397"'
|   r'multipart/alternative;\n\tboundary="\-\-\-\-=_NextPart_000_007D_01C7EF12\.9C5AE1C0"'
|   r'multipart/alternative;\n\tboundary="\-\-\-\-=_NextPart_000_02C9_01C7F830\.FDE88060"'
|   r'multipart/related;\n\tboundary="\-\-\-\-=_NextPart_000_0055_01C81248\.792D0D00"'
|   r'multipart/mixed;\n\tboundary="_004_E52BA26B1940E24FAF1E0BD9F876E23847F2D468UKBXMBW01prodqu_"'
|   r'multipart/alternative;\n\tboundary="_000_E52BA26B1940E24FAF1E0BD9F876E23847F2D4BEUKBXMBW01prodqu_"'
|   r'multipart/alternative;\n\tboundary="_000_E52BA26B1940E24FAF1E0BD9F876E23847F2D4BFUKBXMBW01prodqu_"'
|   r'multipart/alternative;\n\tboundary="_000_E52BA26B1940E24FAF1E0BD9F876E23847F2D4C1UKBXMBW01prodqu_"'
|   r'multipart/alternative;\n\tboundary="_000_65BB6DF6A76DAF4984F1B08936F2FC34A68B2119UKBXMBW01prodqu_"'
|   r'multipart/alternative;\n\tboundary="_064391a5\-c6c4\-496d\-b5d3\-d646e45f8071_"'
|   r'multipart/mixed;\ boundary="0\-169234684\-1199209661=:95298"\nContent\-Transfer\-Encoding:\ 8bit'
|   r'multipart/alternative;\n\tboundary="_e71c60b7\-934e\-495d\-8ca5\-68d022d0756b_"'
|   r'multipart/alternative;\ boundary="0\-1690936920\-1199262114=:23902"\nContent\-Transfer\-Encoding:\ 8bit'
|   r'multipart/mixed;\ boundary="0\-1242512665\-1199285010=:51156"\nContent\-Transfer\-Encoding:\ 8bit'
|   r'multipart/alternative;\n\tboundary="_05c4e171\-16e4\-433e\-b2a4\-4f1cce49c8a5_"'
|   r'multipart/mixed;\ boundary="0\-1957197243\-1199790550=:98701"\nContent\-Transfer\-Encoding:\ 8bit'
|   r'multipart/mixed;\n\tboundary="_005_65BB6DF6A76DAF4984F1B08936F2FC34A6B4B6D5UKBXMBW01prodqu_"'
|   r'multipart/alternative;\ boundary="0\-1728457870\-1199890176=:36147"\nContent\-Transfer\-Encoding:\ 8bit'
|   r'multipart/mixed;\ boundary="0\-237260743\-1199989036=:89358"\nContent\-Transfer\-Encoding:\ 8bit'
|   r'multipart/mixed;\n\tboundary="\-\-\-\-_=_NextPart_001_01C85598\.D0B82877"'
|   r'multipart/alternative;\n\tboundary="\-\-\-\-=_NextPart_000_003F_01C8568B\.A7A9DFF0"'
|   r'multipart/mixed;\ boundary="0\-282327629\-1200330844=:6022"\nContent\-Transfer\-Encoding:\ 8bit'
|   r'multipart/mixed;\n\tboundary="\-\-\-\-_=_NextPart_001_01C856F1\.CAFCB0E2"'
|   r'multipart/alternative;\n\tboundary="\-\-\-\-=_NextPart_000_0024_01C8574E\.8A6FD6B0"'
|   r'multipart/alternative;\n\tboundary="\-\-\-\-=_NextPart_000_00BC_01C8577E\.C8509840"'
|   r'multipart/alternative;\n\tboundary="\-\-\-\-=_NextPart_000_015F_01C857CE\.43B00DF0"'
|   r'multipart/alternative;\ boundary="\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-1200488544"\nX\-Mailer:\ 9\.0\ SE\ for\ Windows\ sub\ 5004'
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def Subject(): yield from (
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def Date(): yield from (
    r'(Sun|Mon|Tue|Wed|Thu|Fri|Sat), [0-9] (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2} \+[0-9]{4}'
   #1:Mon, 4 Dec 2006 21:51:55 +0800
   #1:Wed, 9 Jan 2008 11:30:43 +0000
|   r'(Sun|Mon|Tue|Wed|Thu|Fri|Sat), [0-9] (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2} \-[0-9]{4}'
   #1:Mon, 4 Dec 2006 10:46:00 -0800
   #1:Mon, 4 Dec 2006 11:27:33 -0800
   #1:Mon, 4 Dec 2006 19:55:13 -0000
   #1:Tue, 4 Sep 2007 16:42:31 -0600
   #1:Tue, 1 Jan 2008 19:00:50 -0600
   #1:Thu, 3 Jan 2008 19:25:27 -0600
|   r'[0-9] (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2} \-[0-9]{4}'
   #1:6 May 2007 13:14:56 -0000
|   r'(Sun|Mon|Tue|Wed|Thu|Fri|Sat), [0-9]{2} (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2} \-[0-9]{4}'
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
|   r'(Sun|Mon|Tue|Wed|Thu|Fri|Sat), [0-9]{2} (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2} \+[0-9]{4}'
   #1:Thu, 27 Dec 2007 13:48:30 +0000
   #1:Thu, 27 Dec 2007 14:09:12 +0000
   #1:Thu, 27 Dec 2007 14:09:22 +0000
   #1:Thu, 27 Dec 2007 14:09:46 +0000
   #1:Thu, 27 Dec 2007 16:35:15 +0000
|   r'(Sun|Mon|Tue|Wed|Thu|Fri|Sat), [0-9] (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2} -[0-9]{4} \([A-Z]{3}\)'
   #1:Tue, 1 Jan 2008 09:47:41 -0800 (PST)
   #1:Wed, 2 Jan 2008 00:21:54 -0800 (PST)
   #1:Wed, 2 Jan 2008 06:43:30 -0800 (PST)
   #1:Tue, 8 Jan 2008 03:09:10 -0800 (PST)
   #1:Wed, 9 Jan 2008 06:49:36 -0800 (PST)
|   r'(Sun|Mon|Tue|Wed|Thu|Fri|Sat), [0-9]{2} (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2} -[0-9]{4} \([A-Z]{3}\)'
   #1:Thu, 10 Jan 2008 10:17:16 -0800 (PST)
   #1:Mon, 14 Jan 2008 09:14:04 -0800 (PST)
|   r'(Sun|Mon|Tue|Wed|Thu|Fri|Sat), [0-9]{2} (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2} [A-Z]{3}'
   #1:Wed, 16 Jan 2008 08:02:24 EST
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def Message_ID(): yield from (
    r'<78CD474EB76D9C4C9E8F03720184A36B0B5BCBF2@ALVMBXW02\.prod\.quest\.corp>'
|   r'<FA13712B13469646A618BC95F7E1BA8F01ABD6E9@alvmbxw01\.prod\.quest\.corp>'
|   r'<81B3912B246E23449049CFA9C12D04F6036620A7@alvmbxw01\.prod\.quest\.corp>'
|   r'<E61E658006418E47861A484DE76F4FC507310D8B@ukbmbxw01\.prod\.quest\.corp>'
|   r'<1178457296\.118\.80517\.m48@yahoogroups\.com>'
|   r'<23D8DB429EF0494783E86044C51F865903DB9CEB@ALVMBXW02\.prod\.quest\.corp>'
|   r'<007c01c7ef44\$e6f551c0\$6501a8c0@VentiRD>'
|   r'<07E41628A4DA494AAA597D2D0C85A834@ownerPC>'
|   r'<005401c81272\$62031500\$ea0a14ac@jomolaptop>'
|   r'<E52BA26B1940E24FAF1E0BD9F876E23847F2D468@UKBXMBW01\.prod\.quest\.corp>'
|   r'<E52BA26B1940E24FAF1E0BD9F876E23847F2D4BE@UKBXMBW01\.prod\.quest\.corp>'
|   r'<E52BA26B1940E24FAF1E0BD9F876E23847F2D4BF@UKBXMBW01\.prod\.quest\.corp>'
|   r'<E52BA26B1940E24FAF1E0BD9F876E23847F2D4C1@UKBXMBW01\.prod\.quest\.corp>'
|   r'<65BB6DF6A76DAF4984F1B08936F2FC34A68B2119@UKBXMBW01\.prod\.quest\.corp>'
|   r'<BAY124\-W3489E28ECAB87E6AF5089AD2570@phx\.gbl>'
|   r'<851320\.95298\.qm@web52611\.mail\.re2\.yahoo\.com>'
|   r'<BAY124\-W459446EDB4502DFA58F5CD2520@phx\.gbl>'
|   r'<600240\.23902\.qm@web52601\.mail\.re2\.yahoo\.com>'
|   r'<364748\.51156\.qm@web52604\.mail\.re2\.yahoo\.com>'
|   r'<BAY124\-W746E761573BD76BDEF3EED24C0@phx\.gbl>'
|   r'<482054\.98701\.qm@web52605\.mail\.re2\.yahoo\.com>'
|   r'<65BB6DF6A76DAF4984F1B08936F2FC34A6B4B6D5@UKBXMBW01\.prod\.quest\.corp>'
|   r'<659587\.36147\.qm@web52610\.mail\.re2\.yahoo\.com>'
|   r'<454556\.89358\.qm@web59107\.mail\.re1\.yahoo\.com>'
|   r'<9BDA6601615804418B799762F41EA1D7021D166D@NOANDC\-MXU24\.NOA\.Alcoa\.com>'
|   r'<004201c856bd\$f2aad9f0\$a9557046@DeAtleyFloor>'
|   r'<467603\.6022\.qm@web52605\.mail\.re2\.yahoo\.com>'
|   r'<B9307879C62717418BD7CB1FF0E256730315BB29@server\.RiverRanchRadiology\.local>'
|   r'<002701c85780\$d64510a0\$7d90e604@your27e1513d96>'
|   r'<00bf01c857b1\$13458450\$a9557046@DeAtleyFloor>'
|   r'<016401c85800\$8e8ae250\$6701a8c0@VALUED2D4C2DDC>'
|   r'<bcd\.1d0cad8e\.34bf5a60@aol\.com>'
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_MS_Has_Attach(): yield from (
    r'[a-z]{3}'
   #5:yes
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_MS_TNEF_Correlator(): yield from (
    r' '
   #7: 
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def Thread_Topic(): yield from (
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def Thread_Index(): yield from (
    r'[A-Z][a-z]{2}[A-Z][0-9][A-Z]{3}[0-9][a-z][A-Z][a-z][A-Z]{3}[a-z][A-Z][0-9][A-Z][a-z][A-Z][a-z][0-9][A-Z]{4}[0-9][a-z]{2}=='
   #1:AccX1HFT7mXxXKMqQ4WfYy2XVAP9zw==
|   r'[A-Z][a-z]{3}[A-Z]{3}[a-z]{3}[A-Z][a-z]{4}[A-Z]{2}[a-z][0-9][a-z]{2}[A-Z]{6}[a-z]{3}=='
   #1:AcfvRODlxbBswqcURw6mlUYZAKBweg==
|   r'[A-Z][a-z]{2}[A-Z][a-z]{2}[A-Z][0-9][A-Z]{3}[a-z][A-Z][a-z][0-9][a-z][A-Z]{2}[a-z]{2}[0-9]{2}[A-Z]/[A-Z][a-z][A-Z][a-z][A-Z][a-z]=='
   #1:AcgScmE6LBBfMi0bTIap03W/RkVbJg==
|   r'[A-Z][a-z]{2}[A-Z][a-z]{5}[A-Z]{3}[a-z][A-Z]{2}[0-9][A-Z][a-z][A-Z][a-z][A-Z][a-z][A-Z]{3}[0-9][a-z][A-Z]{3}=='
   #1:AchIjypdoDOCeFK0ReOoChMXS6xNCQ==
|   r'[A-Z][a-z]{2}[A-Z][a-z]{2}[A-Z]{2}[0-9][A-Z][a-z][0-9][a-z][A-Z]{2}[a-z][A-Z]{2}[0-9][A-Z][a-z]{3}[0-9][a-z]{2}[A-Z]/[A-Z]{2}=='
   #1:AchIpnXL8Ol6iCZlSV2Acxm1jfU/DA==
|   r'[A-Z][a-z]{2}[A-Z][a-z]{2}[A-Z]{2}[a-z]{2}[A-Z][a-z][0-9][a-z][A-Z][a-z][A-Z][a-z]{4}\+[a-z]{7}[A-Z]=='
   #1:AchSsxJDtbUm7pYaTdyke+uzwwtfkQ==
|   r'[A-Z][a-z]{2}[A-Z][a-z][A-Z]{3}[0-9][a-z][0-9][A-Z]{3}[a-z][A-Z]{2}[a-z]\+[A-Z]{3}[a-z]{3}[A-Z]{3}\+[A-Z]=='
   #1:AchVmNAQ2k5KDWpTRm+TBPrhqDUU+A==
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def From(): yield from (
    r'"[A-Z][a-z]{2} [A-Z][a-z]{4}" <[A-Z][a-z]{2}\.[A-Z][a-z]{4}@[a-z]{5}\.[a-z]{3}>'
   #1:"Ken Moses" <Ken.Moses@quest.com>
|   r'"[A-Z][a-z]{2} [A-Z][a-z]{3}" <[a-z]{3}\.[a-z]{4}@[a-z]{5}\.[a-z]{3}>'
   #1:"Pat Luis" <pat.luis@quest.com>
|   r'"[A-Z][a-z]{3} [A-Z][a-z]{6}" <[A-Z][a-z]{3}\.[A-Z][a-z]{6}@[a-z]{5}\.[a-z]{3}>'
   #1:"Lisa Radford" <Lisa.Radford@quest.com>
|   r'"[A-Z][a-z]{4} [A-Z][a-z]{7}" <[A-Z][a-z]{4}\.[A-Z][a-z]{7}@[a-z]{5}\.[a-z]{3}>'
   #1:"Keren Kamilian" <Keren.Kamilian@quest.com>
|   r'[A-Z][a-z]{4}! [A-Z][a-z]{5} <[a-z]{6}@[a-z]{11}\.[a-z]{3}>'
   #1:Yahoo! Groups <notify@yahoogroups.com>
|   r'"[A-Z][a-z]{2} [A-Z][a-z]{11}" <[A-Z][a-z]{2}\.[A-Z][a-z]{11}@[a-z]{5}\.[a-z]{3}>'
   #1:"Lon Cherryholmes" <Lon.Cherryholmes@quest.com>
|   r'"[A-Z][a-z]{3} [A-Z][a-z][A-Z][a-z]{5}" <[A-Z][a-z]{3}\.[A-Z][a-z][A-Z][a-z]{5}@[A-Z][a-z]{4}[A-Z][a-z]{8}\.[a-z]{3}>'
   #1:"Tony DeLollis" <Tony.DeLollis@VentiSolutions.com>
|   r'"[A-Z][a-z]{4} [A-Z][a-z]{8}" <[a-z]{10}@[a-z]{6}\.[a-z]{2}\.[a-z]{3}>'
   #1:"Rusty Bullerman" <rbullerman@austin.rr.com>
|   r'"[A-Z][a-z]{3} [A-Z][a-z]{2}" <[a-z]{4}\.[a-z]{3}@[a-z]{8}\-[a-z]{8}\.[a-z]{3}>'
   #1:"Jeff Omo" <jeff.omo@database-brothers.com>
|   r'[A-Z][a-z]{2} [A-Z][a-z]{11} <[A-Z][a-z]{2}\.[A-Z][a-z]{11}@[a-z]{5}\.[a-z]{3}>'
   #4:Lon Cherryholmes <Lon.Cherryholmes@quest.com>
|   r'[A-Z][a-z]{2} [A-Z][a-z]{4} <[a-z]{3}\.[a-z]{5}@[a-z]{5}\.[a-z]{3}>'
   #2:Adi Izhar <adi.izhar@quest.com>
|   r'[A-Z][a-z]{5} [A-Z][a-z]{11} <[a-z]{18}@[a-z]{7}\.[a-z]{3}>'
   #3:Leslie Cherryholmes <lesliecherryholmes@hotmail.com>
|   r'"[A-Z][a-z]{2} [A-Z]\. [A-Z][a-z]{11}" <[a-z]{4}_[0-9]{5}@[a-z]{5}\.[a-z]{3}>'
   #6:"Lon T. Cherryholmes" <ness_78759@yahoo.com>
|   r'[A-Z][a-z]{2} [A-Z][a-z]{11} <[a-z]{8}@[a-z]{5}\.[a-z]{3}>'
   #1:Lon Cherryholmes <lcherryh@yahoo.com>
|   r'"[A-Z][a-z]{5}, [A-Z][a-z]{4} [A-Z] \\\([A-Z]\&[A-Z]\\\)" <[A-Z][a-z]{4}\.[A-Z][a-z]{5}@[a-z]{5}\.[a-z]{3}>'
   #1:"Sheets, Chris A \(T&K\)" <Chris.Sheets@alcoa.com>
|   r'"[A-Z][a-z][A-Z][a-z]{4} [A-Z][a-z]{3} \& [A-Z][a-z]{4}" <[a-z]{8}@[a-z]{6}\.[a-z]{2}\.[a-z]{3}>'
   #2:"DeAtley Tile & Stone" <tdeatley@austin.rr.com>
|   r'"[A-Z][a-z]{4} [A-Z][a-z]{7}[ ]{2}\- [A-Z][a-z]{4} [A-Z][a-z]{4} [A-Z][a-z]{8}" <[a-z]{9}@[a-z]{19}\.[a-z]{3}>'
   #1:"Becky Thompson  - River Ranch Radiology" <bthompson@riverranchradiology.com>
|   r'"[A-Z][a-z]{8} [A-Z][a-z]{6}" <[a-z]{11}@[a-z]{8}\.[a-z]{3}>'
   #1:"Elizabeth Flowers" <shalomyaall@peoplepc.com>
|   r'"[a-z]{7} [a-z]{4} [a-z]{9}" <[a-z]{5}@[a-z]{2}\-[a-z]{2}\.[a-z]{3}>'
   #1:"midwest auto recycling" <parts@mw-ar.com>
|   r'[A-Z]{11}[0-9]{2}@[a-z]{3}\.[a-z]{3}'
   #1:CMONEYMAKER72@aol.com
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def To(): yield from (
    r'"[A-Z][a-z]{2} [A-Z][a-z]{11}" <[a-z]{8}@[a-z]{5}\.[a-z]{3}>'
   #2:"Lon Cherryholmes" <lcherryh@yahoo.com>
|   r'<[a-z]{8}@[a-z]{5}\.[a-z]{3}>'
   #6:<lcherryh@yahoo.com>
|   r'"[A-Z][a-z]{2} [A-Z][a-z]{3}" <[a-z]{3}\.[a-z]{4}@[a-z]{5}\.[a-z]{3}>'
   #1:"Pat Luis" <pat.luis@quest.com>
|   r'[a-z]{8}@[a-z]{5}\.[a-z]{3}'
   #1:lcherryh@yahoo.com
|   r'<[A-Z]{2}[a-z]{6}@[a-z]{5}\.[a-z]{3}>'
   #5:<LCherryh@yahoo.com>
|   r'"[A-Z]{2}[a-z]{6}@[A-Z][a-z]{4}\.[a-z]{3}" <[A-Z]{2}[a-z]{6}@[A-Z][a-z]{4}\.[a-z]{3}>'
   #5:"LCherryh@Yahoo.com" <LCherryh@Yahoo.com>
|   r'"[A-Z]{2}:" <[A-Z]{2}[a-z]{6}@[A-Z][a-z]{4}\.[a-z]{3}>'
   #1:"RE:" <LCherryh@Yahoo.com>
|   r'[A-Z][a-z]{2} [A-Z][a-z]{11} <[a-z]{3}\.[a-z]{12}@[a-z]{5}\.[a-z]{3}>, [a-z]{8}@[a-z]{5}\.[a-z]{3}'
   #6:Lon Cherryholmes <lon.cherryholmes@quest.com>, lcherryh@yahoo.com
|   r'[A-Z][a-z]{2} [A-Z][a-z]{11} <[a-z]{8}@[a-z]{5}\.[a-z]{3}>, [A-Z][a-z]{2} [A-Z][a-z]{11}'
   #2:Lon Cherryholmes <lcherryh@yahoo.com>, Lon Cherryholmes
|   r'[A-Z]{2}[a-z]{6}@[A-Z][a-z]{4}\.[a-z]{3}'
   #2:LCherryh@Yahoo.com
|   r'<[A-Z]{2}[a-z]{6}@[A-Z][a-z]{4}\.[a-z]{3}>'
   #1:<LCherryh@Yahoo.com>
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_OriginalArrivalTime(): yield from (
    r'[0-9]{2} (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{4} \([A-Z]{3}\) [A-Z]{8}=\[[0-9][A-Z][0-9][A-Z]{2}[0-9]{3}:[0-9]{2}[A-Z][0-9]{3}[A-Z]{2}\]'
   #1:04 Dec 2006 13:51:56.0083 (UTC) FILETIME=[5C6CD030:01C717AB]
|   r'[0-9]{2} (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{4} \([A-Z]{3}\) [A-Z]{8}=\[[0-9]{5}[A-Z][0-9]{2}:[0-9]{2}[A-Z][0-9]{3}[A-Z][0-9]\]'
   #1:04 Dec 2006 18:46:00.0912 (UTC) FILETIME=[71900D00:01C717D4]
|   r'[0-9]{2} (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{4} \([A-Z]{3}\) [A-Z]{8}=\[[0-9]{2}[A-Z]{2}[0-9]{2}[A-Z][0-9]:[0-9]{2}[A-Z][0-9]{3}[A-Z]{2}\]'
   #1:04 Dec 2006 19:27:36.0302 (UTC) FILETIME=[40EE58E0:01C717DA]
|   r'[0-9]{2} (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{4} \([A-Z]{3}\) [A-Z]{8}=\[[0-9][A-Z]{2}[0-9]{2}[A-Z][0-9]{2}:[0-9]{2}[A-Z][0-9]{3}[A-Z]{2}\]'
   #1:04 Dec 2006 19:55:17.0081 (UTC) FILETIME=[1ED51C90:01C717DE]
|   r'[0-9]{2} (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{4} \([A-Z]{3}\) [A-Z]{8}=\[[0-9]{4}[A-Z][0-9]{3}:[0-9]{2}[A-Z][0-9][A-Z][0-9][A-Z][0-9]\]'
   #1:27 Aug 2007 16:21:56.0899 (UTC) FILETIME=[6335D730:01C7E8C6]
|   r'[0-9]{2} (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{4} \([A-Z]{3}\) [A-Z]{8}=\[[0-9]{3}[A-Z][0-9][A-Z][0-9]{2}:[0-9]{2}[A-Z][0-9]{2}[A-Z][0-9][A-Z]\]'
   #1:30 Dec 2007 23:56:16.0969 (UTC) FILETIME=[911D2B90:01C84B3F]
|   r'[0-9]{2} (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{4} \([A-Z]{3}\) [A-Z]{8}=\[[A-Z]{4}[0-9][A-Z]{2}[0-9]:[0-9]{2}[A-Z][0-9]{2}[A-Z]{3}\]'
   #1:02 Jan 2008 01:00:50.0700 (UTC) FILETIME=[EADD1CC0:01C84CDA]
|   r'[0-9]{2} (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{4} \([A-Z]{3}\) [A-Z]{8}=\[[A-Z][0-9]{4}[A-Z]{2}[0-9]:[0-9]{2}[A-Z][0-9]{2}[A-Z][0-9]{2}\]'
   #1:04 Jan 2008 01:25:28.0042 (UTC) FILETIME=[B0411CA0:01C84E70]
|   r'[0-9]{2} (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{4} \([A-Z]{3}\) [A-Z]{8}=\[[A-Z][0-9]{7}:[0-9]{2}[A-Z][0-9]{5}\]'
   #1:13 Jan 2008 04:00:21.0559 (UTC) FILETIME=[D1570470:01C85598]
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def Content_Length(): yield from (
    r'1150'
|   r'7937'
|   r'6054'
|   r'8406'
|   r'5286'
|   r'286450'
|   r'7732'
|   r'1216'
|   r'18240'
|   r'3275573'
|   r'16011'
|   r'10432'
|   r'19338'
|   r'6492'
|   r'1672'
|   r'2749'
|   r'2285'
|   r'2308'
|   r'3094'
|   r'1256'
|   r'5341'
|   r'5368575'
|   r'1562'
|   r'130401'
|   r'193837'
|   r'2595'
|   r'3889'
|   r'602608'
|   r'1971'
|   r'1858'
|   r'5492'
|   r'9145'
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def Cc(): yield from (
    r'"[A-Z][a-z]{2} [A-Z][a-z]{4}" <[A-Z][a-z]{2}\.[A-Z][a-z]{4}@[a-z]{5}\.[a-z]{3}>,\\n\\t"[A-Z][a-z]{4} [A-Z][a-z]{7}" <[A-Z][a-z]{4}\.[A-Z][a-z]{7}@[a-z]{5}\.[a-z]{3}>'
   #1:"Ken Moses" <Ken.Moses@quest.com>,\n	"Keren Kamilian" <Keren.Kamilian@quest.com>
|   r'"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z] [A-Z][a-z]{5}" <(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]\.[A-Z][a-z]{5}@[a-z]{5}\.[a-z]{3}>'
   #1:"Mark Wright" <Mark.Wright@quest.com>
|   r'"[A-Z][a-z]{2} [A-Z][a-z]{4}" <[A-Z][a-z]{2}\.[A-Z][a-z]{4}@[a-z]{5}\.[a-z]{3}>,\\n\\t"[a-z]{8}@[a-z]{5}\.[a-z]{3}" <'[a-z]{8}@[a-z]{5}\.[a-z]{3}'>'
   #1:"Ken Moses" <Ken.Moses@quest.com>,\n	"lcherryh@yahoo.com" <'lcherryh@yahoo.com'>
|   r'"[A-Z][a-z]{4} [A-Z][a-z]{5} \- [A-Z][a-z]{4} [A-Z][a-z]{4} [A-Z][a-z]{8}" <[a-z]{7}@[a-z]{19}\.[a-z]{3}>'
   #1:"Angie Garcia - River Ranch Radiology" <agarcia@riverranchradiology.com>
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def In_Reply_To(): yield from (
    r'<[0-9]{6}\.[0-9]{5}\.[a-z]{2}@[a-z]{3}[0-9]{5}\.[a-z]{4}\.[a-z]{2}[0-9]\.[a-z]{5}\.[a-z]{3}>'
   #1:<721514.94331.qm@web59106.mail.re1.yahoo.com>
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def References(): yield from (
    r'<[A-Z]{2}[0-9]{5}[A-Z][0-9]{8}[A-Z][0-9]{3}[A-Z]{2}[0-9]{2}[A-Z][0-9][A-Z][0-9][A-Z]{2}[0-9][A-Z][0-9]{2}[A-Z]{3}[0-9][A-Z][0-9]@[a-z]{7}[0-9]{2}\.[a-z]{4}\.[a-z]{5}\.[a-z]{4}>'
   #1:<FA13712B13469646A618BC95F7E1BA8F01ABD6E9@alvmbxw01.prod.quest.corp>
|   r'<[0-9]{14}\.[0-9]{4}\.[a-z]{5}@[a-z]{8}\.[a-z]{16}\.[a-z]{3}>'
   #1:<20080116033202.6569.qmail@outbound.qualityautoparts.com>
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def Comment(): yield from (
    r'[A-Z][a-z]{5}[A-Z][a-z]{3}\? [A-Z][a-z]{2} [a-z]{4}://[a-z]{8}\.[a-z]{5}\.[a-z]{3}/[a-z]{10}'
   #1:DomainKeys? See http://antispam.yahoo.com/domainkeys
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def DomainKey_Signature(): yield from (
    r'[a-z]=[a-z]{3}\-[a-z]{3}[0-9]; [a-z]=[a-z]{3}; [a-z]=[a-z]{5}; [a-z]=[a-z]{4}; [a-z]=[a-z]{11}\.[a-z]{3};\\n\\t[a-z]=[a-z]{3}[0-9][a-z][A-Z][a-z]{2}[A-Z]{2}[a-z]{2}[0-9][a-z][0-9]\+[A-Z]{5}[a-z]{4}[A-Z][a-z][A-Z][0-9][A-Z]{2}[a-z][A-Z]{2}[0-9][A-Z][a-z]/[A-Z]{4}[a-z]{3}[A-Z]{2}[0-9][a-z][0-9][a-z][A-Z][0-9][A-Z]{2}[a-z][A-Z][a-z][A-Z]{6}[a-z]{3}[A-Z]{2}/[A-Z]{2}[a-z]{6}[A-Z]/[a-z][0-9]{2}[a-z][A-Z][a-z][A-Z][a-z][A-Z][a-z][A-Z]{3}[a-z]{2}/[A-Z]{2}[a-z][A-Z][a-z]{2}[A-Z][0-9][A-Z][a-z][A-Z][a-z]\+[A-Z]{2}[0-9][A-Z][a-z][A-Z]{2}\+[a-z]{3}[0-9]{3}[A-Z][a-z][0-9][a-z][A-Z];'
   #1:a=rsa-sha1; q=dns; c=nofws; s=lima; d=yahoogroups.com;\n	b=nce6rTvfJLmw6r7+SDFNRbllvIiA8ZMhRY0Hj/XSTWwxkPG1z0lS3OHfTlVSRJLKtxwEE/HLdaoimnN/d19uSvWuKmSZLwt/JTfWwoO8SgSw+RD6HaXY+wkf196Vz2dP;
|   r'[a-z]=[a-z]{3}\-[a-z]{3}[0-9]; [a-z]=[a-z]{3}; [a-z]=[a-z]{5};\\n[ ]{2}[a-z]=[a-z][0-9]{4}; [a-z]=[a-z]{5}\.[a-z]{3};'
   #7:a=rsa-sha1; q=dns; c=nofws;\n  s=s1024; d=yahoo.com;
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_Yahoo_Newman_Property(): yield from (
    r'[a-z]{6}\-[a-z]{6}'
   #1:groups-bounce
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def Content_Class(): yield from (
    r'urn:content\-classes:message'
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def Content_Transfer_Encoding(): yield from (
    r'[0-9][a-z]{3}'
   #1:7bit
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def Importance(): yield from (
    r'[a-z]{6}'
   #1:normal
|   r'[A-Z][a-z]{5}'
   #3:Normal
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def Priority(): yield from (
    r'[a-z]{6}'
   #1:normal
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def thread_index(): yield from (
    r'[A-Z][a-z]{5}\+[A-Z][a-z][0-9][A-Z]{3}[0-9][A-Z]{3}[a-z][A-Z][a-z][A-Z][0-9][A-Z][a-z]{3}[A-Z]{3}[a-z]=='
   #1:Acfoxj+Fy3ABX1UHRgSdI7CnwxKTKw==
|   r'[A-Z][a-z]{2}[A-Z][0-9][a-z]{2}[A-Z]{2}[a-z][0-9]{2}[A-Z][0-9][a-z]{2}[A-Z]{2}[a-z][A-Z][a-z][A-Z][a-z][A-Z]{2}[a-z]{2}[A-Z]{3}=='
   #1:AchW8csYNr02G2rlRZiGjYiUAouHXA==
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_Mailer(): yield from (
    r'[A-Z][a-z]{8} [A-Z][a-z]{5} [A-Z][a-z]{6} [0-9]{2}'
   #2:Microsoft Office Outlook 11
|   r'[A-Z][a-z]{8} [A-Z][a-z]{6} [A-Z][a-z]{3} [0-9]\.[0-9]\.[0-9]{4}\.[0-9]{5}'
   #1:Microsoft Windows Mail 6.0.6000.16480
|   r'[A-Z][a-z]{8} [A-Z][a-z]{6} [A-Z][a-z]{6} [0-9]\.[0-9]{2}\.[0-9]{4}\.[0-9]{4}'
   #4:Microsoft Outlook Express 6.00.2900.3138
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_Spam(): yield from (
    r'\[[A-Z]=[0-9]\.[0-9]{10}; [a-z]{4}=[0-9]\.[0-9]{3}\([0-9]{4}\); [a-z]{4}=[0-9]\.[0-9]{3}; [a-z]{8}\-[a-z]{4}=[0-9]\.[0-9]{3}\([0-9]{10}\)\]'
   #1:[F=0.0148648649; heur=0.500(1500); stat=0.010; spamtraq-heur=0.599(2007082706)]
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_MAIL_FROM(): yield from (
    r'<[a-z]{4}\.[a-z]{8}@[a-z]{14}\.[a-z]{3}>'
   #1:<tony.delollis@ventisolutions.com>
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_SOURCE_IP(): yield from (
    r'\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\]'
   #1:[199.239.254.40]
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_SF_Loop(): yield from (
    r'[0-9]'
   #1:1
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_Priority(): yield from (
    r'[0-9]'
   #5:3
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_MSMail_Priority(): yield from (
    r'[A-Z][a-z]{5}'
   #5:Normal
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_MIMEOLE(): yield from (
    r'[A-Z][a-z]{7} [A-Z][a-z] [A-Z][a-z]{8} [A-Z][a-z]{3}[A-Z]{3} [A-Z][0-9]\.[0-9]\.[0-9]{4}\.[0-9]{5}'
   #1:Produced By Microsoft MimeOLE V6.0.6000.16480
)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def X_Virus_Scanned(): yield from (
    r'[A-Z][a-z]{7} [A-Z][a-z]{3}[A-Z][a-z]{4} [A-Z][a-z]{3} [A-Z][a-z]{5}'
   #1:Symantec AntiVirus Scan Engine
)
