import numpy as np, sys
from PIL import Image
from scipy import ndimage as nd
D = sys.argv[1]
for n, ext in [('fenix','png'),('miracle_silver','jpg'),('miracle_blue','jpg'),('miracle_black','jpg'),('miracle_rain','jpg'),('extreme','jpg')]:
    a = np.asarray(Image.open(f'{D}/{n}.{ext}').convert('RGBA')).astype(float)
    A0 = a[...,3:]/255; rgb = a[...,:3]*A0 + 255*(1-A0)
    mn = rgb.min(-1); mx = rgb.max(-1); sat = mx - mn
    silver = 'silver' in n
    H, W = mn.shape
    # light, low-saturation pixels = background / shadow candidates
    cand = (mn >= (248 if silver else 222)) & (sat < 18)
    lab, k = nd.label(cand); sz = nd.sum(cand, lab, range(1, k+1))
    keep = np.zeros(k+1, bool); keep[1:] = sz > 300
    if silver:
        edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]])))
        keep[1:] &= np.array([i in edge for i in range(1, k+1)])
    bg = keep[lab]
    if n.startswith('miracle'):
        bg[int(H*0.62):, int(W*(0.86 if n=='miracle_rain' else 0.72)):] = True
    else:
        bg[int(H*0.81):, int(W*0.64):] = True          # QR / TIS logos
    fg = ~bg
    if n in ('fenix','extreme','miracle_black'):
        fg = ((mn < 175) | (sat > 35)) & ~bg
        fg = nd.binary_closing(fg, iterations=4)
        holes = nd.binary_fill_holes(fg) & ~fg
        hl, hk = nd.label(holes); hs = nd.sum(holes, hl, range(1, hk+1))
        small = np.zeros(hk+1, bool); small[1:] = hs < 600; fg |= small[hl]
        fc = nd.binary_closing(fg, iterations=10) & (mn < 252) & ~nd.binary_dilation(cand & (mn>=252), iterations=0) if False else nd.binary_closing(fg, iterations=10) & (mn < 252); fc[:int(H*0.6)] = False; fg |= fc
    if n=='fenix':
        r=np.zeros_like(fg); r[880:960,400:600]=True; fg |= r & (mn < 236) & nd.binary_dilation(fg, iterations=5)
    if n=='extreme':
        red = (rgb[...,0]>150)&(rgb[...,1]<120)&(rgb[...,2]<120); red[:800]=False
        fg &= ~nd.binary_dilation(red, iterations=25)
    if n in ('miracle_silver','miracle_blue'):
        z=np.zeros_like(fg); z[int(H*0.80):]=True
        fg &= ~(z & (mn >= 205) & (sat < 20))
    # drop small islands (logos, specks)
    lab2, k2 = nd.label(fg); sz2 = nd.sum(fg, lab2, range(1, k2+1))
    big = np.zeros(k2+1, bool); big[1:] = sz2 >= 0.01*sz2.max(); fg = big[lab2]
    fg = nd.binary_fill_holes(fg) if silver else fg
    # shrink 1px to kill the light fringe, then soften edge
    fg = nd.binary_erosion(fg, iterations=1)
    alpha = nd.gaussian_filter(fg.astype(float), 0.7)
    alpha = np.clip((alpha - 0.15) / 0.7, 0, 1)
    # colour decontamination: edge pixels take the colour of nearest solid interior pixel
    solid = nd.binary_erosion(fg, iterations=2)
    idx = nd.distance_transform_edt(~solid, return_distances=False, return_indices=True)
    col = rgb.copy(); edge = alpha < 0.999
    col[edge] = rgb[idx[0][edge], idx[1][edge]]
    out = np.dstack([col, alpha*255]).clip(0, 255).astype(np.uint8)
    img = Image.fromarray(out, 'RGBA'); img = img.crop(img.getbbox())
    img.save(f'{D}/{n}_cut.png'); print(n, img.size)
