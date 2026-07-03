import sys
try:
    from reportlab.pdfgen.canvas import Canvas
    # pyrefly: ignore [missing-import]
    from reportlab.lib.extgstate import ExtGraphicState
    print("ExtGraphicState is available.")
except ImportError as e:
    print("Error:", e)

c = Canvas("test.pdf")
print("Methods on Canvas:")
print(dir(c))
