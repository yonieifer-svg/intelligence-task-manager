An intelligence unit called ShadowNet needs a system to manage agents and tasks. The system is built on a FastAPI server and manages a
database for the ongoing management of agents and missions

========================================================================================================================================

- Folder structure -

intelligence-task-manager/
├── main.py
├── database/
│   ├── db_connection.py
│   ├── agent_db.py
│   └── mission_db.py
├── routes/
│ ├── agent_routes.py
│ ├── mission_routes.py
│ └── report_routes.py
├── logs/
│ └── app.log
├── README.md
├── requirements.txt
└── .gitignore

========================================================================================================================================

- agents table -

id
name
specialty
is_active
completed_missions
failed_missions
agent_rank


- missions table -

id
title
description
location
difficulty
importance
status
risk_level
assigned_agent_id

========================================================================================================================================

--- classes ---

- DB_connection -
מנהלת את החיבור לדאטה בייס כולל יצירתו ויצירת הטבלאות

get_connection() - מחזירה חיבור פעיל 
create_database() יוצרת את הדאטה בייס אם לא קיים
create_tables() - יוצרת את הטבלאות אם לא קיימות


- AgentDB -
מנהלת את הפעולות על טבלת הסוכנים בדאטה בייס

create_agent(data) - יוצרת סוכן חדש ומחזירה את המילון שלו
get_all_agents() - מחזירה רשימת כל הסוכנים
get_agent_by_id(id) - מחזירה סוכן אחד לפי ID, או None
update_agent(id, data) - מעדכנת נתונים לסוכן
deactivate_agent(id) - מגדירה מצב סוכן ללא פעיל
increment_completed(id) - מעדכן את כמות המשימות שהושלמו 
increment_failed(id) - מעדכן את כמות המשימות שנכשלו
get_agent_performance(id) - מחזירה מילון עם המפתחות האלו completed, failed, total, success_rate
count_active_agents() - מחזירה את מספר הסוכנים הפעילים 


- MissionDB -
מנהלת את הפעולות על טבלת המשימות בדאטה בייס

create_mission(data) - יצירת משימה חדשה ומחזירה את כל האובייקט
get_all_missions() - מחזירה את כל המשימות
get_mission_by_id(id) - מחזירה משימה אחת לפי ID, או None
assign_mission(m_id, a_id) - משייכת משימה לסוכן
update_mission_status(id, status) - משמשת לכל שינוי סטטוס
get_open_missions_by_agent(id) - מחזירה משימות ASSIGNED/IN_PROGRESS של סוכן
count_all_missions() - סה"כ משימות
count_by_status(status) - סופרת לפי סטטוס מסוים
count_open_missions() - סופרת משימות פתוחות
count_critical_missions() - סופרת משימות CRITICAL
get_top_agent() - הסוכן עם completed_missions הגבוה ביותר

========================================================================================================================================

- Rules -

1
rank חייב להיות Junior / Senior / Commander — כל ערך אחר זורק שגיאה.
2
difficulty ו-importance חייבים להיות בין 1 ל-10 — אחרת שגיאה.
3
risk_level מחושב אוטומטית בעת יצירת משימה — המשתמש לא שולח אותו.
4
סוכן עם is_active=False לא יכול לקבל משימות.
5
סוכן לא יכול להחזיק יותר מ-3 משימות פתוחות (ASSIGNED / IN_PROGRESS) במקביל.
6
אם risk_level=CRITICAL — רק סוכן בדרגת Commander יכול לקבל את המשימה.
7
ניתן לשייך רק משימה בסטטוס NEW. לאחר שיוך: status=ASSIGNED.
8
ניתן להתחיל רק משימה בסטטוס ASSIGNED. לאחר: status=IN_PROGRESS.
9
ניתן לסיים רק משימה. IN_PROGRESS  ולשנות לסטטוס failed or completed
10
ניתן לבטל רק משימה בסטטוס NEW או ASSIGNED — אחרת שגיאה.

========================================================================================================================================
Agents: 

[POST] /agents - יצירת סוכן חדש 
[GET] /agents - כל הסוכנים 
[GET] /agents/{id} ID לפי סוכן
[PUT] /agents/{id} סוכן עדכון
[PUT] /agents/{id}/deactivate סוכן השבתת
[GET] /agents/{id}/performance סוכן ביצועי



Missions: 

[POST] /missions - יצירת משימה
[GET] /missions - כל המשימות 
[GET] /missions/{id} ID לפי משימה
[PUT] /missions/{id}/assign/{agent_id} - שיוך לסוכן
[PUT] /missions/{id}/start - התחלת משימה
[PUT] /missions/{id}/complete - סיום בהצלחה
[PUT] /missions/{id}/fail - סיום בכישלון
[PUT] /missions/{id}/cancel - ביטול משימה



Reports: 

[GET] /reports/summary - דוח כללי של המערכת 
[GET] /reports/missions-by-status - סטטוס לפי משימות
[GET] /reports/top-agent - הסוכן המצטיין




========================================================================================================================================

- Running instructions -

$ docker run -d --name intelligence-mysql -e MYSQL_ROOT_PASSWORD=root \
  -e MYSQL_DATABASE=Intelligence_db -p 3306:3306 mysql:8.0

uvicorn main:app --reload







