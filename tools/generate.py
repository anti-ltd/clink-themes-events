#!/usr/bin/env python3
"""Generate the Events collection from editable, paired art-direction palettes."""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def rgba(value: str, alpha: float = 1) -> dict:
    if not re.fullmatch(r'#[0-9A-Fa-f]{6}', value):
        raise ValueError('Use a six-digit hex colour: ' + value)
    return {**{c: round(int(value[i:i+2], 16) / 255, 8) for c, i in zip('rgb', (1, 3, 5))}, 'a': alpha}


def cap(fill, text, radius):
    return dict(fill=fill, text=text, activeFill=fill, activeText=text, pressed=fill, cornerRadius=radius)


def appearance(record, dark):
    p = {k: rgba(v) for k, v in record['dark' if dark else 'light'].items()}
    style = record['style']; radius = style['cornerRadius']
    theme = dict(id=record['id'], name=record['name'], source='eventsRepository', isDark=dark,
        **{k:p[k] for k in ['background','keyFill','keyText','specialKeyFill','specialKeyText']},
        suggestionText=p['keyText'], accent=p['returnFill'],
        material=style['material'], threeDVariant=style['threeDVariant'],
        keySurfaceMaterial=style['keySurfaceMaterial'], liquidGlass=False,
        keyFontDesign='rounded' if style['material']=='bubble' else 'default', keyFontWeight='medium',
        keyCapShape='rect', grainDensity=0.65, grainSize=0.5, grainStrength=0.035,
        glossStrength=0.55, glossSpread=0.32, mechanicalFaceInset=2.4,
        mechanicalInnerRadius=radius-2, mechanicalRaised=True, mechanicalShowEdges=True,
        bevelDepth=2.2, bevelLightAngle=315, neumorphicDepth=2, neumorphicSoftness=4,
        neumorphicStrength=0.55, neowriterRimWidth=1.2, neowriterRingWidth=0.6,
        neowriterRingInset=1.2, neowriterDepth=2, neowriterSoftness=1.5,
        neowriterRimColor=p['secondaryFill'], neowriterRingColor=p['returnFill'],
        backgroundGradient=dict(type='linear',rotation=135,stops=[
            dict(position=0,color=p['background']),dict(position=1,color=p['backgroundEnd'])]),
        groupPaint={
            'letters':dict(cornerRadius=radius), 'numbers':dict(cornerRadius=radius),
            'punctuation':dict(cornerRadius=radius),
            'modifiers':{**cap(p['specialKeyFill'],p['specialKeyText'],radius),
                         'activeFill':p['returnFill'],'activeText':p['returnText']},
            'return':cap(p['returnFill'],p['returnText'],radius),
            'space':cap(p['secondaryFill'],p['secondaryText'],radius),
            'backspace':{**cap(p['specialKeyFill'],p['specialKeyText'],radius),'pressed':p['returnFill']},
        },
        backgroundEffect=dict(style=style['effect'],speed=0.35,intensity=0.26 if dark else 0.12,
            density=0.22,scale=0.7,reactive=True,reactionStrength=0.35,blend='glow',
            colorMode='custom',customColor=p['returnFill'],secondaryColorMode='custom',customColor2=p['secondaryFill']))
    return theme


def documents():
    records=json.loads((ROOT/'palettes.json').read_text())['themes']
    ids=[r['id'] for r in records]
    if not ids or len(set(ids))!=len(ids) or any(not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',i) for i in ids):
        raise ValueError('Theme IDs must be unique, permanent lowercase slugs')
    result={}
    for r in records:
        light,dark=appearance(r,False),appearance(r,True)
        result[ROOT/'Themes'/f'{r["id"]}.clinktheme']=json.dumps({**light,'pairedVariants':[light,dark]},ensure_ascii=False,indent=2)+'\n'
    result[ROOT/'catalog.json']=json.dumps(dict(version=1,name='Events',themes=[f'Themes/{i}.clinktheme' for i in ids]),indent=2)+'\n'
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--check',action='store_true'); args=parser.parse_args()
    for path,text in documents().items():
        if args.check:
            if not path.exists() or path.read_text()!=text: raise SystemExit('Regenerate '+str(path.relative_to(ROOT)))
        else:
            path.parent.mkdir(parents=True,exist_ok=True); path.write_text(text)
    print('Events paired collection '+('verified' if args.check else 'generated'))

if __name__=='__main__': main()
