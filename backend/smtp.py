import smtplib
from email.message import EmailMessage
from email.utils import make_msgid
import os
import requests

def send_password_reset_email(Nom_, email, reset_link):
    msg = EmailMessage()

    # Générer un identifiant unique pour l'email
    email_cid = make_msgid()

    # Contenu de l'email (HTML)
    msg.set_content("Ceci est un e-mail de récupération de mot de passe.")

    msg.add_alternative(f"""
        <h3>🔒 Réinitialisation de votre mot de passe</h3>
        <p>Bonjour {Nom_},</p>

        <p>Nous avons reçu une demande de réinitialisation de votre mot de passe.</p>
        <p>Si vous êtes à l'origine de cette demande, veuillez cliquer sur le bouton ci-dessous :</p>

        <p style="text-align: center;">
            <a href="{reset_link}" 
                style="background-color: #007bff; color: #ffffff; padding: 10px 20px; 
                text-decoration: none; border-radius: 5px; display: inline-block;">
                🔑 Réinitialiser mon mot de passe
            </a>
        </p>

        <p>Ce lien est valable pendant <strong>30 minutes</strong>. Passé ce délai, vous devrez faire une nouvelle demande.</p>

        <p>Si vous n'êtes pas à l'origine de cette demande, vous pouvez ignorer cet e-mail.</p>

        <p>Cordialement,<br>
        <strong>L'équipe de support</strong></p>
    """, subtype='html')

    # Paramètres d'envoi
    fromEmail = 'haitham.abdedaim@gmail.com'
    email_password = "shlggkijfpkftsef"  # 🔒 Utiliser une variable d'environnement pour plus de sécurité
    
    # Configuration des en-têtes de l'email
    msg['Subject'] = '🔑 Réinitialisation de votre mot de passe'
    msg['From'] = fromEmail
    msg['To'] = email

    try:
        # Connexion au serveur SMTP
        with smtplib.SMTP('smtp.gmail.com', 587) as s:
            s.starttls()
            s.login(fromEmail, email_password)  # 🔒 Connexion sécurisée
            s.send_message(msg)

        print(f"✅ Email de réinitialisation envoyé à {email}")

    except Exception as e:
        print(f"❌ Échec de l'envoi de l'email : {e}")



    
    
        
    






def d_file(url): 
    #url = "https://energyconsulting.monday.com/protected_static/8998901/resources/603744328/Rapport%20dAudit%20Humbert%20.pdf"
    
    payload={}
    headers = {
      'authority': 'energyconsulting.monday.com',
      'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
      'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7,ar;q=0.6',
      'cookie': 'bb_visitor_id=e27237f; xi_loc=33.5883%2C-7.6114; xi_ip=196.117.124.57; xi_time_diff=0; xi_region=Casablanca-Settat; xi_org=undefined; xi_country=MA; xi_city=Casablanca; xi_postal=undefined; m_referrer=https://www.google.com/; m_landing_page=https://monday.com/lang/fr/; cookiehub=eyJhbnN3ZXJlZCI6dHJ1ZSwicHJlY29uc2VudCI6ZmFsc2UsInJldmlzaW9uIjoxLCJkbnQiOmZhbHNlLCJjb29raWVMYXdzIjpmYWxzZSwidG9rZW4iOiJGTXFkTVFDWUJYTXRsbUF1N3NQRERaaXJpNHFiNFFMT1BkdmxxWHNBZ3NYajRyeUpKc2hwU0d4b2JYbk5MbXJ3IiwiY2F0ZWdvcmllcyI6W3siY2lkIjoxLCJpZCI6Im5lY2Vzc2FyeSIsInZhbHVlIjp0cnVlLCJwcmVjb25zZW50IjpmYWxzZSwiZmlyZWQiOmZhbHNlfSx7ImNpZCI6MiwiaWQiOiJwcmVmZXJlbmNlcyIsInZhbHVlIjp0cnVlLCJwcmVjb25zZW50Ijp0cnVlLCJmaXJlZCI6ZmFsc2V9LHsiY2lkIjozLCJpZCI6ImFuYWx5dGljcyIsInZhbHVlIjp0cnVlLCJwcmVjb25zZW50Ijp0cnVlLCJmaXJlZCI6ZmFsc2V9LHsiY2lkIjo0LCJpZCI6Im1hcmtldGluZyIsInZhbHVlIjp0cnVlLCJwcmVjb25zZW50IjpmYWxzZSwiZmlyZWQiOmZhbHNlfV19; hubspotutk=e5c0e312cb4428bbe64a26ffbf7ef797; hubspot_id_sent=true; bb_visitor_aliased=true; monday_pricing_version=9; monday_has_student_plan=false; monday_has_free_tier=true; monday_free_tier_account_creation_item_resource_credit=200; use_old_storage_settings=true; platform_hide_basic=false; bb_visitor_aliased_count=2; _hjSessionUser_1566695=eyJpZCI6IjM2N2YzZDFkLThlYmEtNTE4Zi1iNDhkLWM0OGYxM2RjMGQ2MyIsImNyZWF0ZWQiOjE2NDkzODI2ODkwMTYsImV4aXN0aW5nIjp0cnVlfQ==; _hjSessionUser_2272600=eyJpZCI6ImFiNWE3Y2FlLWE5NTMtNWEyMy1hOWFiLTM4Mjk2MmZiOGY5MSIsImNyZWF0ZWQiOjE2NDk2MTcyMzE0NDcsImV4aXN0aW5nIjp0cnVlfQ==; __hssrc=1; platform_free_tier_name_free=false; m_campaign=guests; force_fs=true; _hjSessionUser_2847380=eyJpZCI6IjBhNjE2ODk5LTZiMWEtNTE3YS05N2U1LWJhODE1ZjEyODUzMyIsImNyZWF0ZWQiOjE2NDk2MTYxMTYwMTgsImV4aXN0aW5nIjp0cnVlfQ==; mutiny.user.token=0a0637e4-26d3-4e1c-af18-740d98891d53; jwt_session_token=eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjE2MDcyMTI2OSwidWlkIjoyNTUxMzMxMywiaWFkIjoiMjAyMi0wNS0xNlQxNDowNDozMy41ODdaIiwicGVyIjoibWU6c2Vzc2lvbiIsImFjdGlkIjo4OTk4OTAxLCJyZ24iOiJ1c2UxIn0.RbFIc1WwK5acj_aKb-ziU890W0VRdjRZpYyyl2mxINU; platform_free_tier_version=version(){return%222021%22}; utm_campaign=broadcast; utm_source=virality; _cc_id=7216c4ce04d7a1d480ccefa96e7154a5; m_source=adwordsbrand; monday_active_account_slugs=%5B%22haitham-abdu%22%2C%22wikiassagmailcom%22%2C%22energyconsulting%22%2C%22wikiassa-hai%22%5D; dapulseAccountSlugs=%5B%22energyconsulting%22%2C%22haitham-abdu%22%2C%22wikiassagmailcom%22%2C%22wikiassa-hai%22%5D; dapulseLastLoginAccount=energyconsulting; dapulseUserId=25513313; should_see_purchase_now=false; platform_account_cluster=other; platform_account_sub_cluster=team_tasks_and_projects; platform_account_id=8998901; platform_user_id=25513313; platform_show_solutions_pricing=false; viewer_uid=bWFQZDVXQ1lsMUxUN1ZHRjR2OUpTMSt4MldoWG9LbDd5Y3lmWEJsL01yMD0tLXBlZ0kwSDZUTTBCZEQyT2pjSVF2Vmc9PQ%3D%3D--f11164fe03c89ae8e3ecf2be296eb487da87512d; amplitude_id_710046ca554fe7c78d358b8c5e09a168monday.com=eyJkZXZpY2VJZCI6IjBlMmRjNzdkLTk1YzctNDZlNC1hYTUyLWIyZDUyNDUxZmUyM1IiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTY1NTg5MTAwNjU5MCwibGFzdEV2ZW50VGltZSI6MTY1NTg5MTAyNjQ5OCwiZXZlbnRJZCI6MiwiaWRlbnRpZnlJZCI6MCwic2VxdWVuY2VOdW1iZXIiOjJ9; force_currency_homepage=usd; homepage_account_creation_item_resource_credit=200; utm_cluster_id=other; utm_sub_cluster_id=team_tasks_and_projects; experiment_visitor_id=1659956503495; new_ab_test_marketing_product_full_high_intent_ab_test=new_product_full_flow; new_ab_test_new_header_layout_test=new_header_layout; new_ab_test_work_management_in_mobile_menu_test=new_with_work_management; new_ab_test_welcome_back_account_homepage_test=old_redirect; new_ab_test_get_signup_prefetched_assets_test=new_with_prefetched_assets; _gcl_au=1.1.97429088.1659956511; _fbp=fb.1.1660675528494.968293914; fb_id_sent=true; region=use1; new_ab_test_header_new_layout_without_projects_test=new_header_layout_without_projects; new_ab_test_new_signup_with_product_page_without_product_recommendation_test=new_signup_with_product_page; new_ab_test_purchase_now_ab_test=old_without_purchase_now; cloudfront_viewer_country=MA; fs_uid=#WSWD#5536711580835840:4844734851485696:::#cd95a838#/1681616875; new_ab_test_header_new_layout_without_projects_v4_test=old_header; new_ab_test_FR_NoWorkOS_HP=old__lang_fr_; users_option=20; utm_locale_id=fr; _gid=GA1.2.2033938214.1664790414; panoramaId_expiry=1665395218297; panoramaId=c3cf67f08ca7dcf825c72ee3897a16d53938ba83c7a9e5123cd817f5b59ccd34; origin=https%3A%2F%2Fenergyconsulting.monday.com%2Fboards%2F2193360754; monday_slug_details=%5B%7B%22user_name%22%3A%22haitham+abdedaim%22%2C%22user_email%22%3A%22haitham.abdedaim%40gmail.com%22%2C%22user_image%22%3A%22https%3A%2F%2Fcdn1.monday.com%2Fdapulse_default_photo.png%22%2C%22account_name%22%3A%22haitham+abdu%22%2C%22slug%22%3A%22haitham-abdu%22%7D%2C%7B%22user_name%22%3A%22Haitham+Abdedaim%22%2C%22user_email%22%3A%22haitham.abdedaim%40gmail.com%22%2C%22user_image%22%3A%22https%3A%2F%2Fcdn1.monday.com%2Fdapulse_default_photo.png%22%2C%22account_name%22%3A%22wikiassa+hai%22%2C%22slug%22%3A%22wikiassa-hai%22%7D%2C%7B%22un%22%3A%22HA.service+technique%22%2C%22ue%22%3A%22haitham.energyconsulting%40gmail.com%22%2C%22ui%22%3A25513313%2C%22us%22%3A121%2C%22an%22%3A%22Service+technique%22%2C%22ac%22%3A%222021-05-17T15%3A03%3A32Z%22%2C%22ai%22%3A8998901%2C%22sl%22%3A%22energyconsulting%22%2C%22lu%22%3A%222022-10-03T15%3A54%3A30%2B00%3A00%22%7D%5D; _hjSession_2272600=eyJpZCI6IjMwOTJjZTQ4LTA5NjQtNDRlMS1iZjM0LTRkZTQ1MGE4MGQ5MiIsImNyZWF0ZWQiOjE2NjQ4MTMxOTc2MzEsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; _ga_500WE4S491=GS1.1.1664816530.15.1.1664816548.0.0.0; __zlcmid=1A0kvggO0lNjs9k; _ga=GA1.2.634187850.1649382693; _uetsid=51358ca0430011ed800855517dfcf9b2; _uetvid=6af66310b6de11eca95dbb7d9f66e326; __hstc=267501905.e5c0e312cb4428bbe64a26ffbf7ef797.1649382697879.1664811691691.1664818487267.50; __hssc=267501905.1.1664818487267; __cf_bm=I3Rz1CBw3bF1rObSrcAVNmB8m3VoihcN._HJXXbzwVw-1664818726-0-AYS6eFIxqxgy3MAy+WCSFA54P3avoQ/mIjpjReKPCBnfuwjS8jHjelfN3OaRqxgUnE6nMVV5SWDtTLokgy59CdLred1b4jKEE2668cZVMPE4; encUserId=eyJhbGciOiJIUzI1NiJ9.eyJleHAiOjMzOTI3OTc0MjUsImRhdCI6MjU1MTMzMTN9.3AlhJIMYCr349Pu1_1x81w3kcisC_AMn50aivdMH0vw; dapulse_session=bk16K2xHTm1wS3FWN25DRHJQOE5ocGdEeHh1aFVGZGVPM0hDcnFEcW1sdVQ4bURuMGFLcEVETEtDVEJLZHNCc0JzN0tOd0hlcmpJVzZ3Q2dGSklURTdaZzB6bFNWZUlsYUVVT0pHYUVIZ1lCU00xcXZpK2RxME5NVHAxMGNvZHZKdzhjazR3Z0V1cjE0Vm1NMkRzYWRvQ1pycWRwdmk0YmtXREQ5SHpwbGpkR2JrZVpsTHZkU3MwbVBuc0xCSXdZck40enBsSS9ETktMbk02VkhDZnFEUT09LS1Ob25DUlhHZkxnTU0ra0pYK0dnblB3PT0%3D--c76af694663f9f5c8c6888aefc150669a684b580; dapulseLastLoginAccount=energyconsulting; dapulseUserId=25513313; encUserId=eyJhbGciOiJIUzI1NiJ9.eyJleHAiOjMzOTI3OTc1MTksImRhdCI6MjU1MTMzMTN9.hRbv0qg97n27n5VQD9m67fLDCiGuct9Z2DvIgHrbWCc; dapulse_session=MmQ4UERDc1V5ZWN2dUxoY25LZzkzUXNia1B0Y0hFbXpubjZZOVU1T0NLVW8zSDg1WGxKV1NDMXQrRlVwWXFUYmV3WHc5bm1lOXczaDhZUm9LQm5qY0lLQkZTbHdGS2NJeGhaVzZrNG5lcm1td0lsemJNSUZOZUZKVGZhdVNPSU4rbFppYzhxbFZnNnlmYm9ENE4zZ0F2YjVRYW83S0JSeDFzb3g0QlZWR3o4N0hXMTNuMk12b2VsdVFzZDZDZEJCdzI0VWJ2NGhOUkpkeEhaNzJwQWpLQT09LS1qbTZhYWhxTDBQdEw1eDUvM0hwNm53PT0%3D--7de8d9039fd00e7a60aba273d98e6e54b933c94a',
      'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'document',
      'sec-fetch-mode': 'navigate',
      'sec-fetch-site': 'none',
      'sec-fetch-user': '?1',
      'upgrade-insecure-requests': '1',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
    }
    
    response = requests.request("GET", url, headers=headers, data=payload)

    return (response.content)


def send_msg_contact(Nom_,email,subject,message) :
    msg = EmailMessage()
    

    asparagus_cid = make_msgid()
    msg.set_content('This is a text message')
    msg.add_alternative(""" email : """ + email+"""  sujet : """+subject+"""  message   """ + message +"""

    
    """.format(asparagus_cid=asparagus_cid[1:-1]), subtype='html')
    
    
    #msg.get_payload()[1].add_related(d_file("https://energyconsulting.monday.com/protected_static/8998901/resources/652303919/Devis%20test.pdf","name_"), 'pdf', 'pdf', cid=asparagus_cid)
        
    
    
    ctype = 'application/octet-stream'
    maintype, subtype = ctype.split('/', 1)
    
    
    fromEmail = 'contact@enrcalc.fr'
    toEmail = "h.abdedaim@energy-consulting.fr"
    
    msg['Subject'] = subject + " - ENRCALC"
    msg['From'] = fromEmail
    msg['To'] = toEmail
    
    s = smtplib.SMTP('smtp.gmail.com', 587)
    
    s.starttls()
    
    s.login(fromEmail, 'kgjucpjyhksztdst')
            
    s.send_message(msg)
    s.quit()
