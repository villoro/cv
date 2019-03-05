cd src

:loop

"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"^
 --disable-smart-shrinking^
 --javascript-delay 5000^
 --print-media-type --dpi 300^
 -T 0 -B 0 -L 0 -R 0^
 localhost:5000^
 output/sample.pdf

goto loop
