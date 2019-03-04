:loop

"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"^
 --disable-smart-shrinking --javascript-delay 3000 -T 0 -B 0 -L 0 -R 0^
 test.html^
 test.pdf

goto loop
