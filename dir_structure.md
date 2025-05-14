SFS_InfoBot
C:.
|   # Git Contribution Statistics.md
|   README.md
|   
+---bot_data
|   +---Alumni_Achievements_Clubs
|   |       achievers.json
|   |       alumni_2020.json
|   |       marketing_club.json
|   |       ncc_orientation.json
|   |       
|   +---College_News_ Events
|   |       college_news.json
|   |       media_coverage.json
|   |       newsletter.json
|   |
|   +---contact
|   |       contact_info.json
|   |       feedback_form.json
|   |
|   +---courses
|   |   +---pg_courses
|   |   |       pg_courses_available.json
|   |   |       pg_fee_details.json
|   |   |       pg_syllabus.json
|   |   |
|   |   \---ug_courses
|   |           ug_courses_available.json
|   |           ug_faculties.json
|   |           ug_fee_details.json
|   |           ug_programs_details.json
|   |           ug_syllabus.json
|   |
|   +---events
|   |       college_events.json
|   |       festivals_special_days.json
|   |       upcoming_events.json
|   |
|   +---facilities
|   |       cultural_sports_facilities.json
|   |       facilities_at_sfs.json
|   |       ict_facilities.json
|   |       library_facilities.json
|   |       physical_facilities.json
|   |       welfare_facilities.json
|   |       wifi_facilities.json
|   |
|   +---institute_info
|   |   |   campus.json
|   |   |   college_timings.json
|   |   |   founder.json
|   |   |   history.json
|   |   |   logo_anthem.json
|   |   |   naac_data.json
|   |   |   patron.json
|   |   |   principal_message.json
|   |   |   social_media_and_brochure.json
|   |   |   values.json
|   |   |   vision.json
|   |   |
|   |   \---admissions
|   |           admission_details.json
|   |
|   +---Results_and_exam
|   |       exam_results.json
|   |       question_papers.json
|   |       result_certification.json
|   |
|   \---Skill_Development _Workshops
|           advanced_excel_workshop.json
|           personal_branding_workshop.json
|           python_programming_workshop.json
|
+---frontend
|   |   db_auth.py
|   |   index.html
|   |
|   +---assets
|   |   |   site
|   |   |
|   |   +---apps
|   |   |       icons8-facebook-logo-48.png
|   |   |       icons8-google-mail-48.png
|   |   |       icons8-google-maps-48.png
|   |   |       icons8-instagram-logo-48.png
|   |   |       icons8-linkedin-48.png
|   |   |       icons8-twitter.svg
|   |   |       icons8-whatsapp-48.png
|   |   |       icons8-youtube.svg
|   |   |
|   |   +---favicons
|   |   |       android-chrome-192x192.png
|   |   |       android-chrome-512x512.png
|   |   |       apple-touch-icon.png
|   |   |       favicon-16x16.png
|   |   |       favicon-32x32.png
|   |   |       favicon.ico
|   |   |
|   |   \---icons
|   |           icons8-chatbot-94.png
|   |           icons8-chatbot.gif
|   |           icons8-close-48.png
|   |           icons8-history-50.png
|   |           icons8-menu-vertical-48.png
|   |           icons8-mic-32.png
|   |           icons8-refresh-48.png
|   |           icons8-send-48.png
|   |           icons8-settings-94.png
|   |
|   +---css
|   |       login.css
|   |       styles.css
|   |
|   +---js
|   |       login.js
|   |       script.js
|   |
|   \---__pycache__
|           db_auth.cpython-39.pyc
|
+---logs
|   +---contributions
|   |       sambramam_contributions.csv
|   |       vnikitha_contributions.csv
|   |
|   \---docs
|           logs_readme.md
|
+---rasa
|   |   config.yml
|   |   credentials.yml
|   |   domain.yml
|   |   endpoints.yml
|   |   spell_checker_component.py
|   |
|   +---.rasa
|   |   \---cache
|   |       |   cache.db
|   |       |
|   |       +---tmp4jmq378b
|   |       |       patterns.json
|   |       |
|   |       +---tmpaik_7uvt
|   |       |       feature_to_idx_dict.json
|   |       |
|   |       +---tmpb4cqz_2i
|   |       |       oov_words.json
|   |       |       vocabularies.json
|   |       |
|   |       +---tmpd_ne0qib
|   |       |       featurizer.json
|   |       |       memorized_turns.json
|   |       |
|   |       +---tmpgn55fzqg
|   |       |       synonyms.json
|   |       |
|   |       +---tmpqww7v3ah
|   |       \---tmpu5f4xkg3
|   |               checkpoint
|   |               DIETClassifier.data_example.st
|   |               DIETClassifier.data_example_metadata.json   
|   |               DIETClassifier.entity_tag_specs.json        
|   |               DIETClassifier.index_label_id_mapping.json  
|   |               DIETClassifier.label_data.st
|   |               DIETClassifier.label_data_metadata.json     
|   |               DIETClassifier.sparse_feature_sizes.json    
|   |               DIETClassifier.tf_model.data-00000-of-00001 
|   |               DIETClassifier.tf_model.index
|   |
|   +---actions
|   |   |   action.py
|   |   |   events.py
|   |   |   facilities.py
|   |   |   pg_courses.py
|   |   |   ug_courses.py
|   |   |
|   |   \---__pycache__
|   |           action.cpython-39.pyc
|   |           events.cpython-39.pyc
|   |           facilities.cpython-39.pyc
|   |           pg_courses.cpython-39.pyc
|   |           ug_courses.cpython-39.pyc
|   |
|   +---data
|   |       Alumni_Achivements_Clubs_nlu.yml
|   |       Alumni_Achivements_Clubs_rules.yml
|   |       Alumni_Achivements_Clubs_stories.yml
|   |       basic_nlu.yml
|   |       basic_rules.yml
|   |       basic_stories.yml
|   |       College_News_ Events_nlu.yml
|   |       College_News_ Events_rules.yml
|   |       College_News_ Events_stories.yml
|   |       contact_nlu.yml
|   |       contact_rules.yml
|   |       contact_stories.yml
|   |       events_nlu.yml
|   |       events_rules.yml
|   |       events_stories.yml
|   |       facilities_nlu.yml
|   |       facilities_rules.yml
|   |       facilities_stories.yml
|   |       pg_courses_nlu.yml
|   |       pg_courses_rules.yml
|   |       pg_courses_stories.yml
|   |       Results_and_exam_nlu.yml
|   |       Results_and_exam_rules.yml
|   |       Result_and_exam_stories.yml
|   |       Skill_Development _Workshops_nlu.yml
|   |       Skill_Development _Workshops_rules.yml
|   |       Skill_Development _Workshops_stories.yml
|   |       ug_courses_nlu.yml
|   |       ug_courses_rules.yml
|   |       ug_courses_stories.yml
|   |
|   +---models
|   \---__pycache__
|           spell_checker_component.cpython-39.pyc
|
+---scripts
|   |   import_to_mongodb.py
|   |
|   \---__pycache__
|           import_to_mongodb.cpython-39.pyc
|
\---__pycache__
        spell_checker_component.cpython-39.pyc

mongo db collections
use sfs_infobot_db
switched to db sfs_infobot_db
show collections
Alumni_Achievements_Clubs_achievers
Alumni_Achievements_Clubs_alumni_2020
Alumni_Achievements_Clubs_marketing_club
Alumni_Achievements_Clubs_ncc_orientation
College_News_ Events_college_news
College_News_ Events_media_coverage
College_News_ Events_newsletter
contact_contact_info
contact_feedback_form
courses_pg_courses_pg_courses_available
courses_pg_courses_pg_fee_details
courses_pg_courses_pg_syllabus
courses_ug_courses_ug_courses_available
courses_ug_courses_ug_faculties
courses_ug_courses_ug_fee_details
courses_ug_courses_ug_programs_details
courses_ug_courses_ug_syllabus
events_college_events
events_festivals_special_days
events_upcoming_events
facilities_cultural_sports_facilities
facilities_facilities_at_sfs
facilities_ict_facilities
facilities_library_facilities
facilities_physical_facilities
facilities_welfare_facilities
facilities_wifi_facilities
institute_info_admissions_admission_details
institute_info_campus
institute_info_college_timings
institute_info_founder
institute_info_history
institute_info_logo_anthem
institute_info_naac_data
institute_info_patron
institute_info_principal_message
institute_info_social_media_and_brochure
institute_info_values
institute_info_vision
Results_and_exam_exam_results
Results_and_exam_question_papers
Results_and_exam_result_certification
Skill_Development _Workshops_advanced_excel_workshop
Skill_Development _Workshops_personal_branding_workshop
Skill_Development _Workshops_python_programming_workshop
users


