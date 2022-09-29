function jsvm_this_initialization(E) {
    for (var e = 5; void 0 !== e; )
        switch (e % 10) {
        case 0:
            !function(s, n) {
                switch (e / 10 | 0) {
                case 0:
                    return void (e = c < 64 ? 70 : 3);
                case 1:
                    return void (e = c < t ? 6 : 90);
                case 2:
                    return void (e = c < i ? 31 : 2);
                case 3:
                    return b = -b,
                    void (e = 51);
                case 4:
                    return c += 4,
                    void (e = 60);
                case 5:
                    return o += E.charCodeAt(c),
                    void (e = 1);
                case 6:
                    return void (e = c < a.length ? 9 : 12);
                case 7:
                    return p[r.charAt(c)] = c,
                    void (e = 91);
                case 8:
                    return void (e = 0 == b ? 41 : 51);
                case 9:
                    c = 0,
                    e = 60
                }
            }();
            break;
        case 1:
            !function(E, s) {
                switch (e / 10 | 0) {
                case 0:
                    return c++,
                    void (e = 11);
                case 1:
                    return void (e = c < i ? 50 : 7);
                case 2:
                    return c++,
                    void (e = 20);
                case 3:
                    return b = 31 * b + ~c >>> 0,
                    u[c] = b % i,
                    void (e = 21);
                case 4:
                    return b = 13,
                    void (e = 51);
                case 5:
                    return c = 0,
                    void (e = 20);
                case 6:
                    return c += 4,
                    void (e = 10);
                case 7:
                    return c++,
                    void (e = 81);
                case 8:
                    return void (e = c < i ? 8 : 4);
                case 9:
                    c++,
                    e = 0
                }
            }();
            break;
        case 2:
            !function(E, s) {
                switch (e / 10 | 0) {
                case 0:
                    return c = 0,
                    void (e = 81);
                case 1:
                    jsvm_this_sdata = n.join("|"),
                    e = void 0
                }
            }();
            break;
        case 3:
            var s = n.pop();
            t = s.length,
            jsvm_this_insns = [],
            c = 0,
            e = 10;
            break;
        case 4:
            E = n.join("");
            var a = (n = E.split("|")).pop()
              , r = n.pop()
              , p = {};
            c = 0,
            e = 0;
            break;
        case 5:
            var c, t, n = E.split(""), i = n.length, u = [], o = 0;
            c = 0,
            e = 11;
            break;
        case 6:
            var h = p[s.charAt(c + 0)] << 18 | p[s.charAt(c + 1)] << 12 | p[s.charAt(c + 2)] << 6 | p[s.charAt(c + 3)];
            jsvm_this_insns.push(h),
            e = 61;
            break;
        case 7:
            var b = ~(o * i);
            e = b < 0 ? 30 : 80;
            break;
        case 8:
            var v = u[c]
              , k = n[v];
            n[v] = n[0],
            n[0] = k,
            e = 71;
            break;
        case 9:
            h = p[a.charAt(c + 0)] << 18 | p[a.charAt(c + 1)] << 12 | p[a.charAt(c + 2)] << 6 | p[a.charAt(c + 3)];
            jsvm_this_entrances.push(h),
            e = 40
        }
}
function jsvm_this_run(E, e) {
    function s(E) {
        return p[E]
    }
    function a(E, e) {
        p[E] = e
    }
    for (var r = 3; void 0 !== r; )
        switch (r % 7) {
        case 0:
            !function(E, s) {
                switch (r / 7 | 0) {
                case 0:
                    return void (r = 35);
                case 1:
                    return k = !1,
                    void (r = v > jsvm_this_insns.length ? 2 : 6);
                case 2:
                    return v += U + 1,
                    void (r = 28);
                case 3:
                    return void (r = void 0 === v ? 1 : 15);
                case 4:
                    return void (r = 7);
                case 5:
                    r = void 0;
                    break;
                case 6:
                    c = jsvm_this_entrances[e],
                    t = [],
                    n = [void 0],
                    i = [],
                    r = 8
                }
            }();
            break;
        case 1:
            !function(E, e) {
                switch (r / 7 | 0) {
                case 0:
                    return void (r = 35);
                case 1:
                    return void (r = 5);
                case 2:
                    return void (r = !1 === k ? 14 : 28);
                case 3:
                    return p = jsvm_this_sdata.split("\t"),
                    u = 0,
                    void (r = 29);
                case 4:
                    return void (r = u < p.length ? 4 : 42);
                case 5:
                    u++,
                    r = 29
                }
            }();
            break;
        case 2:
            return;
        case 3:
            var p, c, t, n, i, u, o, h, b;
            r = 22;
            break;
        case 4:
            try {
                p[u] = E(p[u])
            } catch (E) {
                p[u] = void 0
            }
            r = 36;
            break;
        case 5:
            var v, k, _, H, l = 0, d = 0, V = [], m = !0;
            H = [void 0],
            v = c - 1,
            _ = 0,
            r = 7;
            break;
        case 6:
            var f, j, g, D, w, M, G, y, A, U = 0;
            switch (127 & (f = jsvm_this_insns[v])) {
            case 26:
                U = 1,
                D = f >> 12 & 4095,
                w = (j = jsvm_this_insns[v + 1]) >> 0 & 31,
                t[g = f >> 7 & 31][D] = t[w];
                break;
            case 21:
                D = f >> 12 & 31,
                w = f >> 17 & 31,
                t[g = f >> 7 & 31] = t[D] === t[w];
                break;
            case 64:
                D = f >> 12 & 31,
                w = f >> 17 & 31,
                t[g = f >> 7 & 31] = s(t[D] + t[w]);
                break;
            case 96:
                U = 1,
                D = f >> 12 & 31,
                w = f >> 17 & 127,
                w |= ((j = jsvm_this_insns[v + 1]) >> 0 & 511) << 7,
                t[g = f >> 7 & 31] = s(t[D] + w);
                break;
            case 16:
                D = f >> 12 & 255,
                t[g = f >> 7 & 31] = 2 == D ? +t[g] : 0 == D ? {} : 1 == D ? [] : void 0;
                break;
            case 32:
                U = 1,
                D = f >> 12 & 4095,
                D |= ((j = jsvm_this_insns[v + 1]) >> 0 & 15) << 12,
                t[g = f >> 7 & 31] = D;
                break;
            case 48:
                U = 1,
                D = f >> 12 & 4095,
                D = (D |= ((j = jsvm_this_insns[v + 1]) >> 0 & 15) << 12) << 16 >> 16,
                t[g = f >> 7 & 31] = D;
                break;
            case 80:
                U = 1,
                D = f >> 23 & 1,
                a((g = f >> 7 & 65535) + (w = (j = jsvm_this_insns[v + 1]) >> 4 & 65535), t[D |= (j >> 0 & 15) << 1]);
                break;
            case 8:
                U = 1,
                g = f >> 7 & 31,
                D = f >> 12 & 31,
                w = f >> 17 & 31,
                M = f >> 22 & 3,
                M |= ((j = jsvm_this_insns[v + 1]) >> 0 & 7) << 2,
                G = j >> 3 & 31;
                try {
                    t[g] = 31 === D ? t[w](t[M], t[G]) : t[D][t[w]](t[M], t[G])
                } catch (E) {
                    if (k = !0,
                    null == (v = H.pop()))
                        break;
                    -1 === v && (v = H.pop()),
                    2 === l && (l = H.pop(),
                    -1 === (v = H.pop()) && (n.pop(),
                    v = H.pop())),
                    d = 3 + l,
                    l = (l + 1) % 3,
                    t[0] = E
                }
                break;
            case 112:
                U = 1,
                D = f >> 12 & 4095,
                D |= ((j = jsvm_this_insns[v + 1]) >> 0 & 15) << 12,
                w = j >> 4 & 31,
                t[g = f >> 7 & 31] = s(D + t[w]);
                break;
            case 72:
                U = 1,
                g = f >> 7 & 31,
                D = f >> 12 & 31,
                w = f >> 17 & 31,
                M = f >> 22 & 3,
                M |= ((j = jsvm_this_insns[v + 1]) >> 0 & 7) << 2;
                try {
                    t[g] = 31 === D ? t[w](t[M]) : t[D][t[w]](t[M])
                } catch (E) {
                    if (k = !0,
                    null == (v = H.pop()))
                        break;
                    -1 === v && (v = H.pop()),
                    2 === l && (l = H.pop(),
                    -1 === (v = H.pop()) && (n.pop(),
                    v = H.pop())),
                    d = 3 + l,
                    l = (l + 1) % 3,
                    t[0] = E
                }
                break;
            case 104:
                U = 1,
                g = f >> 7 & 31,
                D = f >> 12 & 31,
                w = f >> 17 & 31,
                M = f >> 22 & 3,
                M |= ((j = jsvm_this_insns[v + 1]) >> 0 & 7) << 2,
                G = j >> 3 & 31,
                y = j >> 8 & 31,
                A = j >> 13 & 31;
                try {
                    if (0 === _)
                        t[g] = 31 === D ? t[w](t[M], t[G], t[y], t[A]) : t[D][t[w]](t[M], t[G], t[y], t[A]);
                    else {
                        for (o = [],
                        h = 31 == D ? void 0 : t[D],
                        o.push(t[M]),
                        o.push(t[G]),
                        o.push(t[y]),
                        o.push(t[A]),
                        b = [],
                        u = 0; u < _; u++)
                            b.push(n.pop());
                        for (u = 0; u < _; u++)
                            o.push(b.pop());
                        t[g] = 31 == D ? t[w].apply(h, o) : h[t[w]].apply(h, o),
                        _ = 0
                    }
                } catch (E) {
                    if (k = !0,
                    null == (v = H.pop()))
                        break;
                    -1 === v && (v = H.pop()),
                    2 === l && (l = H.pop(),
                    -1 === (v = H.pop()) && (n.pop(),
                    v = H.pop())),
                    d = 3 + l,
                    l = (l + 1) % 3,
                    t[0] = E
                }
                break;
            case 24:
                g = f >> 7 & 31,
                D = f >> 12 & 31,
                w = f >> 17 & 31;
                try {
                    t[g] = 31 === D ? t[w]() : t[D][t[w]]()
                } catch (E) {
                    if (k = !0,
                    null == (v = H.pop()))
                        break;
                    -1 === v && (v = H.pop()),
                    2 === l && (l = H.pop(),
                    -1 === (v = H.pop()) && (n.pop(),
                    v = H.pop())),
                    d = 3 + l,
                    l = (l + 1) % 3,
                    t[0] = E
                }
                break;
            case 88:
                D = f >> 12 & 31,
                w = f >> 17 & 31,
                a(t[g = f >> 7 & 31] + t[w], t[D]);
                break;
            case 40:
                U = 1,
                g = f >> 7 & 31,
                D = f >> 12 & 31,
                w = f >> 17 & 31,
                M = f >> 22 & 3,
                M |= ((j = jsvm_this_insns[v + 1]) >> 0 & 7) << 2,
                G = j >> 3 & 31,
                y = j >> 8 & 31;
                try {
                    t[g] = 31 === D ? t[w](t[M], t[G], t[y]) : t[D][t[w]](t[M], t[G], t[y])
                } catch (E) {
                    if (k = !0,
                    null == (v = H.pop()))
                        break;
                    -1 === v && (v = H.pop()),
                    2 === l && (l = H.pop(),
                    -1 === (v = H.pop()) && (n.pop(),
                    v = H.pop())),
                    d = 3 + l,
                    l = (l + 1) % 3,
                    t[0] = E
                }
                break;
            case 120:
                D = f >> 12 & 31,
                t[g = f >> 7 & 31] = E(t[D]);
                break;
            case 4:
                g = f >> 7 & 31,
                D = f >> 12 & 31,
                w = f >> 17 & 31,
                _ += 3,
                n.push(t[g]),
                n.push(t[D]),
                n.push(t[w]);
                break;
            case 68:
                U = 1,
                D = f >> 12 & 31,
                w = f >> 17 & 127,
                w |= ((j = jsvm_this_insns[v + 1]) >> 0 & 511) << 7,
                a(t[g = f >> 7 & 31] + w, t[D]);
                break;
            case 36:
                g = f >> 7 & 31,
                _ += 1,
                n.push(t[g]);
                break;
            case 56:
                U = 1,
                g = f >> 7 & 31,
                D = f >> 12 & 31,
                w = f >> 17 & 31,
                M = f >> 22 & 3,
                M |= ((j = jsvm_this_insns[v + 1]) >> 0 & 7) << 2,
                _ += 4,
                n.push(t[g]),
                n.push(t[D]),
                n.push(t[w]),
                n.push(t[M]);
                break;
            case 100:
                g = f >> 7 & 31,
                D = f >> 12 & 31,
                _ += 2,
                n.push(t[g]),
                n.push(t[D]);
                break;
            case 20:
                U = 1,
                D = f >> 23 & 1,
                D |= ((j = jsvm_this_insns[v + 1]) >> 0 & 15) << 1,
                a((g = f >> 7 & 65535) + t[w = j >> 4 & 31], t[D]);
                break;
            case 84:
            case 52:
                g = (g = f >> 7 & 65535) << 16 >> 16,
                H.push(v + g);
                break;
            case 116:
                g = (g = f >> 7 & 65535) << 16 >> 16,
                H.push(l),
                d = 0,
                l = 0,
                H.push(v + g);
                break;
            case 12:
                g = f >> 7 & 31,
                t[0] = t[g],
                d = 3 + l;
                break;
            case 76:
                k = !0,
                v = H.pop(),
                l = H.pop(),
                d > 3 && -1 === (v = H.pop()) && (n.pop(),
                v = H.pop()),
                d = 0;
                break;
            case 44:
                k = !0,
                v = H.pop(),
                l++,
                0 === d && (v = H.pop(),
                l++);
                break;
            case 108:
                k = !0,
                v = H.pop(),
                l++;
                break;
            case 92:
                k = !0,
                v = (g = f >> 7 & 65535) - 1;
                break;
            case 60:
                U = 1,
                D = f >> 12 & 4095,
                D |= ((j = jsvm_this_insns[v + 1]) >> 0 & 15) << 12,
                t[g = f >> 7 & 31] = D;
                break;
            case 124:
                k = !0,
                v = t[g = f >> 7 & 31] - 1;
                break;
            case 28:
                g = f >> 7 & 31,
                k = !0,
                m = !1,
                n.push(v + 1 + U),
                v = t[g] - 1,
                H.push(-1),
                l = 0,
                d = 0;
                break;
            case 66:
                g = f >> 7 & 31,
                jsvm_this_tmpValue = t[D = f >> 12 & 31],
                E(t[g] + " = jsvm_this_tmpValue;");
                break;
            case 2:
                t[g = f >> 7 & 31] = {};
                break;
            case 98:
                D = f >> 12 & 31,
                w = f >> 17 & 31,
                t[g = f >> 7 & 31] = t[D] | t[w];
                break;
            case 34:
                D = f >> 12 & 31,
                w = f >> 17 & 31,
                t[g = f >> 7 & 31] = t[D] ^ t[w];
                break;
            case 82:
                D = f >> 12 & 31,
                w = f >> 17 & 31,
                t[g = f >> 7 & 31] = t[D] % t[w];
                break;
            case 18:
                D = f >> 12 & 31,
                w = f >> 17 & 31,
                t[g = f >> 7 & 31] = t[D] / t[w];
                break;
            case 114:
                D = f >> 12 & 31,
                w = f >> 17 & 31,
                t[g = f >> 7 & 31] = t[D] & t[w];
                break;
            case 50:
                D = f >> 12 & 31,
                t[g = f >> 7 & 31] = ~t[D];
                break;
            case 74:
                D = f >> 12 & 31,
                w = f >> 17 & 31,
                t[g = f >> 7 & 31] = t[D] * t[w];
                break;
            case 10:
                D = f >> 12 & 31,
                w = f >> 17 & 31,
                t[g = f >> 7 & 31] = t[D] - t[w];
                break;
            case 42:
                D = f >> 12 & 31,
                w = f >> 17 & 31,
                t[g = f >> 7 & 31] = t[D] + t[w];
                break;
            case 106:
                D = f >> 12 & 31,
                w = f >> 17 & 31,
                t[g = f >> 7 & 31] = t[D] >>> t[w];
                break;
            case 0:
                U = 1,
                D = f >> 12 & 4095,
                D |= ((j = jsvm_this_insns[v + 1]) >> 0 & 15) << 12,
                w = j >> 4 & 65535,
                t[g = f >> 7 & 31] = s(D + w);
                break;
            case 58:
                D = f >> 12 & 31,
                w = f >> 17 & 31,
                t[g = f >> 7 & 31] = t[D] << t[w];
                break;
            case 90:
                U = 1,
                D = f >> 12 & 31,
                w = f >> 17 & 127,
                w |= ((j = jsvm_this_insns[v + 1]) >> 0 & 31) << 7,
                t[g = f >> 7 & 31] = t[D][w];
                break;
            case 6:
                U = 1,
                D = f >> 12 & 4095,
                D |= ((j = jsvm_this_insns[v + 1]) >> 0 & 15) << 12,
                t[g = f >> 7 & 31] && (k = !0,
                v = D - 1);
                break;
            case 70:
                k = !0,
                H.pop(),
                void 0 === (v = n.pop()) && (v = -1);
                break;
            case 122:
                D = f >> 12 & 31,
                t[g = f >> 7 & 31] = E("" + t[D]);
                break;
            case 38:
                if (U = 1,
                g = (g = f >> 7 & 65535) << 16 >> 16,
                D = f >> 23 & 1,
                D |= ((j = jsvm_this_insns[v + 1]) >> 0 & 15) << 1,
                n.length <= g)
                    break;
                n[n.length - 1 - g] = t[D];
                break;
            case 22:
                if (g = f >> 7 & 31,
                D = f >> 12 & 31,
                n.length <= t[D])
                    break;
                t[g] = n[n.length - 1 - t[D]];
                break;
            case 86:
                if (g = f >> 7 & 31,
                D = f >> 12 & 31,
                n.length <= t[g])
                    break;
                n[n.length - 1 - t[g]] = t[D];
                break;
            case 54:
                if (D = f >> 12 & 31,
                w = f >> 17 & 31,
                void 0 === t[g = f >> 7 & 31])
                    jsvm_this_tmpValue = t[w],
                    E(t[D] + " = jsvm_this_tmpValue;");
                else
                    try {
                        t[g][t[D]] = t[w]
                    } catch (E) {
                        if (k = !0,
                        null == (v = H.pop()))
                            break;
                        -1 === v && (v = H.pop()),
                        2 === l && (l = H.pop(),
                        -1 === (v = H.pop()) && (n.pop(),
                        v = H.pop())),
                        d = 3 + l,
                        l = (l + 1) % 3,
                        t[0] = E
                    }
                break;
            case 102:
                D = f >> 12 & 31,
                t[g = f >> 7 & 31] && (k = !0,
                v = t[D] - 1);
                break;
            case 118:
                g = f >> 7 & 31,
                D = f >> 12 & 31,
                w = f >> 17 & 31;
                try {
                    t[g] = t[D][t[w]]
                } catch (E) {
                    if (k = !0,
                    null == (v = H.pop()))
                        break;
                    -1 === v && (v = H.pop()),
                    2 === l && (l = H.pop(),
                    -1 === (v = H.pop()) && (n.pop(),
                    v = H.pop())),
                    d = 3 + l,
                    l = (l + 1) % 3,
                    t[0] = E
                }
                break;
            case 14:
                U = 1,
                g = f >> 7 & 31,
                D = f >> 12 & 31,
                w = f >> 17 & 31,
                M = f >> 22 & 3,
                M |= ((j = jsvm_this_insns[v + 1]) >> 0 & 7) << 2,
                n.push(t[g]),
                n.push(t[D]),
                n.push(t[w]),
                n.push(t[M]);
                break;
            case 46:
                D = f >> 12 & 31,
                w = f >> 17 & 31,
                t[g = f >> 7 & 31] = n.pop(),
                i.push(t[g]),
                t[D] = n.pop(),
                i.push(t[D]),
                t[w] = n.pop(),
                i.push(t[w]);
                break;
            case 78:
                t[g = f >> 7 & 31] = n.pop(),
                i.push(t[g]);
                break;
            case 30:
                D = f >> 12 & 31,
                t[g = f >> 7 & 31] && n.push(t[D]);
                break;
            case 94:
                g = f >> 7 & 31,
                D = f >> 12 & 31,
                w = f >> 17 & 31,
                n.push(t[g]),
                n.push(t[D]),
                n.push(t[w]);
                break;
            case 62:
                D = f >> 12 & 31,
                t[g = f >> 7 & 31] = t[D];
                break;
            case 126:
                g = f >> 7 & 31,
                n.push(t[g]);
                break;
            case 110:
                D = f >> 12 & 31,
                t[g = f >> 7 & 31] = n.pop(),
                i.push(t[g]),
                t[D] = n.pop(),
                i.push(t[D]);
                break;
            case 65:
                D = f >> 12 & 31,
                w = f >> 17 & 31,
                t[g = f >> 7 & 31] = t[D] >= t[w];
                break;
            case 1:
                D = f >> 12 & 31,
                w = f >> 17 & 31,
                t[g = f >> 7 & 31] = t[D] <= t[w];
                break;
            case 33:
                D = f >> 12 & 31,
                w = f >> 17 & 31,
                t[g = f >> 7 & 31] = t[D] < t[w];
                break;
            case 97:
                D = f >> 12 & 31,
                w = f >> 17 & 31,
                t[g = f >> 7 & 31] = t[D] > t[w];
                break;
            case 17:
                D = f >> 12 & 31,
                w = f >> 17 & 31,
                t[g = f >> 7 & 31] = t[D] && t[w];
                break;
            case 81:
                D = f >> 12 & 31,
                w = f >> 17 & 31,
                t[g = f >> 7 & 31] = t[D] || t[w];
                break;
            case 113:
                D = f >> 12 & 31,
                t[g = f >> 7 & 31] = !t[D];
                break;
            case 9:
                D = f >> 12 & 31,
                w = f >> 17 & 31,
                t[g = f >> 7 & 31] = t[D] !== t[w];
                break;
            case 49:
                D = f >> 12 & 31,
                w = f >> 17 & 31,
                t[g = f >> 7 & 31] = t[D] >> t[w];
                break;
            case 41:
                D = f >> 12 & 31,
                w = f >> 17 & 31,
                t[g = f >> 7 & 31] = t[D] != t[w];
                break;
            case 73:
                if (U = 1,
                g = f >> 7 & 31,
                D = f >> 12 & 4095,
                D = (D |= ((j = jsvm_this_insns[v + 1]) >> 0 & 15) << 12) << 16 >> 16,
                n.length <= D)
                    break;
                t[g] = n[n.length - 1 - D];
                break;
            case 105:
                U = 1,
                D = f >> 12 & 31,
                w = f >> 17 & 31,
                M = f >> 22 & 3,
                M |= ((j = jsvm_this_insns[v + 1]) >> 0 & 7) << 2,
                t[g = f >> 7 & 31] = n.pop(),
                i.push(t[g]),
                t[D] = n.pop(),
                i.push(t[D]),
                t[w] = n.pop(),
                i.push(t[w]),
                t[M] = n.pop(),
                i.push(t[M]);
                break;
            case 89:
                D = f >> 12 & 31,
                w = f >> 17 & 31,
                t[g = f >> 7 & 31] = t[D]in t[w];
                break;
            case 57:
                t[g = f >> 7 & 31] = {};
                break;
            case 121:
                if (U = 1,
                D = f >> 12 & 4095,
                D |= ((j = jsvm_this_insns[v + 1]) >> 0 & 15) << 12,
                w = j >> 4 & 255,
                "number" == typeof t[g = f >> 7 & 31].jsvmfunc) {
                    for (u = 1; u <= w; u++)
                        V.push(s(D + u));
                    m = !0,
                    n.push(s(D)),
                    k = !0,
                    n.push(v + 1 + U),
                    v = t[g].jsvmfunc - 1,
                    H.push(-1),
                    l = 0,
                    d = 0
                } else {
                    for (o = [],
                    h = s(D),
                    u = 0; u < w; u++)
                        o.push(s(D + w - u));
                    "function" == typeof t[g] && n.push(t[g].apply(h, o))
                }
                break;
            case 25:
                t[g = f >> 7 & 31] = [];
                break;
            case 69:
                if (g = f >> 7 & 255,
                m)
                    for (u = 0; u < g; u++)
                        n.push(V.pop());
                V = [],
                m = !1;
                break;
            case 37:
                for (U = 1,
                g = f >> 7 & 65535,
                D = f >> 23 & 1,
                D |= ((j = jsvm_this_insns[v + 1]) >> 0 & 32767) << 1,
                u = 1; u <= D; u++)
                    a(g + D - u, n.pop());
                break;
            case 101:
                D = f >> 12 & 31,
                w = f >> 17 & 31,
                t[g = f >> 7 & 31] = t[D] == t[w];
                break;
            case 5:
                for (U = 1,
                g = f >> 7 & 65535,
                D = f >> 23 & 1,
                D |= ((j = jsvm_this_insns[v + 1]) >> 0 & 32767) << 1,
                u = 0; u < D; u++)
                    n.push(s(g + u));
                break;
            default:
                for (g = f >> 7 & 255,
                u = 0; u < g; u++)
                    n.push(i.pop())
            }
            r = -1 === v ? 0 : 21
        }
}
var jsvm_this_tmpValue, jsvm_this_insns = [], jsvm_this_sdata = [], jsvm_this_entrances = [], jsvm_this_privs = [];
jsvm_this_initialization("HeE\tGVE\tEHw''H'z'i'MEEE\t'1sEmEbspinVVetVbEHrEEaE'EDdcjie\tEjsEEEEEE'HcNdtpiMgdvcndEE4nEd\tuErewenEd'BneEEaEr\taEnEeE8aud\tinEuEEEEnl4fEE/dEErEEtvuE''H7EEVirEd\tHgElEtrEepeHEEetcvEc 'e\ttEiseG/cHEEHEeEEuHEnnmbuauAEr0wcMg ElUEdenE2E2\tEerVEE\t'sHlEt'aVEhaDC9deEEHE'leEgthE\tuEd'fWqe'|EuElEEEepVEEEVE''EEEnEVHpEayEEEjE/ElEEEcEH\tEDDEpuH'eEEEgEEHEhuVEEEEpEEED\tEpEEUuEEEEpEa'cpu'EVEaEE\tEEDEEEEHucEinDHEEHpnEEEEE0EnEcEEEEnVElMEEEeEGLoEuEyjGplEEaE4cEEnuEC1rEpEVHEEEEopHEEH4p+EVE'EEEgEErmEDVcElEEEEHEEHlEHE'EEEGED1EEErEEm8cErE2EEUEEElpEaEEEplEHEaHEEE7EEV'EELEEEEH'pVHEEEHEeEHEruEE7EHElEeglgHgErDEEEEaV42EEVDEKe2EEsV1EuEcEEupEwel4EEEEu_EEEEEEVEEVueEMEcHagEtEweHpE\tpeEE'EEEE'EEcEHDEEEEEt1E'1EEEbEbEEVE\trEHwlEtEEEEGEcdUcEhED1EEErEeEVeElE\tEEDEEHEEEEV'EEMDEEuE'EEHEEEecEuEEn1GE9EEEEVbHIEcpEiagEEgEnuEEeEceEsdEE1EEEEMpE4EEEEVDuuwEHEeupacE11EuEEwE/acuEwEEElDHEgdE7GEEEEEEDEDEE14EEEEEEEeeEEaE\thcHM'HElEHoulwElEEpEEEEp7aEDEc\tEaHEEuHEEVpBMl\tlEEuEegccEEEcE4aEEucpEEcEEEEVEugEEEeEElDEHEMEEEuEEEMDLDEVEEuEwEt1ugcHgrHVEEEEErEEEpEiEEEEHEEEEEeEEEEEElcEEEVEu\teEEExoHEEEEudEEDEVEv8EcEE6\tMaEEaUEE8HMlDH'EEHEEEaEEEDiEmHEEEciVEeEEEHEEacEEgHEEgEcEwiEEEiEuGEEOUEElpHEEd7Eu'EvEgfpeGEEHgwE'weEaenEeGEHEcEEEEeoEEeHEtEEhEVDeufElEu\tEYVKBEEEE'EEEEEpEneEEEV1tEEEEEaEEEDEEaHnuEcEEEE'j'HEEEEEEEHEDEjiEv8eGEEEEu6VDEeEEaHHlERwe1EEEVeEHEDEaEEEaeREEEE 7rEEEafEbpEEEVaEu'cEHrEEfEeEaV4EEEHh\tEHEGEEfEVHEEVppEa\tiEEEE7EEEEVulFEaEEutEEEcEEDrEwEjsP1UEcEHclDdEEeEVfVplsEuHEuEEEHnEE1iluGErEEEEEEHCcGEE8aeEEVH\tctEEQD2EEwEEVEMpeEEcEE8EEEbEEEEEEdrEBVEEEEuccEHpEwE\tEE4'ugcpEEeeEED'EaHE\t\t8lEEEEEupEEVEHEDHuEVVcXn2EcaHEEVcEElEEEcuEglLmEaHEnViEEEHpgEpE\ta3ELExE7rEEEHSsgEEEEleEVe8DEvDDclpE7MwaEpEEEEDE7rEfEgMuVV2E7reEEE2EaMer1VH3uMDEHEEEEudEEnEMEcrEuHeEE'H\tEV7EEEpEEVcwEE_'Euu4Egru1UHMfEsEEEEEEEEEVGeeElEUlaH\tVHCaEEMEEu8E1aEEEeHeEEr|DVDEEaE2KdEaEgtEHx4nA5DGJcE7yTEoEEjc'EEEfPEE8fcEnZUEk6EEsB28ESEq|EEEuErEA")
function token(n, t, r) {
    var e, o, s, u, i;
    n = n || "",
    t = t || 2;
    var jsvmportal_0_1 = function() {
        var inout = arguments, retval;
        return jsvm_this_run(function() {
            return eval(arguments[0])
        }, 0),
        retval
    };
    return jsvm_this_run(function() {
        return eval(arguments[0])
    }, 1),
    "" + e(u) + e(i)
}

function get_token(timestamp){
// var timestamp = 1638845202777;
var seedToken = '';
var pin = '';
var f = token(seedToken, pin, timestamp);
return f
}

function get_dynamicToken(seedToken, pin, timestamp){
    // var timestamp = 1638845202777;
    // var seedToken = '';
    // var pin = '';
    var f = token(seedToken, pin, timestamp);
    return f
    }
// console.log(get_dynamicToken('','',1638845202777))
