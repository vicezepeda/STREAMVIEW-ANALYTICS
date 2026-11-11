"""Colores y contraste de los gráficos de la entrega EP5/EP6."""
PALETTE = {'Película':'#1F4E79','Serie':'#A34B00'}
TEXT = '#26384A'

def luminance(hex_color):
    channels=[int(hex_color.lstrip('#')[i:i+2],16)/255 for i in (0,2,4)]
    linear=[v/12.92 if v<=0.04045 else ((v+0.055)/1.055)**2.4 for v in channels]
    return sum(a*b for a,b in zip(linear,(0.2126,0.7152,0.0722)))

def contrast(foreground,background='#FFFFFF'):
    a,b=sorted([luminance(foreground),luminance(background)])
    return (b+0.05)/(a+0.05)
