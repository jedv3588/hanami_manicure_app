@echo off
echo Creating project structure...
mkdir manicurist_app
cd manicurist_app
mkdir invoice_template
echo. > main.py
echo. > database.py
echo. > models.py
echo. > services.py
echo. > gui.py
echo. > requirements.txt
cd invoice_template
echo. > template.html
cd ..
echo Project structure created successfully!
pause