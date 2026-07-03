import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto.settings')
django.setup()

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from aplicacion.views_reportes import dibujar_encabezado

doc = SimpleDocTemplate("test_reporte.pdf", pagesize=letter, topMargin=95)
styles = getSampleStyleSheet()
elements = []
elements.append(Paragraph("TEST", styles['Heading1']))

doc.build(elements, onFirstPage=dibujar_encabezado, onLaterPages=dibujar_encabezado)
print("PDF generated successfully.")
