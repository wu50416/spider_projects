window = global

var ot = function() {
    return false || "number" !== typeof window.D ? +String(Date.now()).substr(0, 10) : +String(Date.now()).substr(0, 10) + window.D
}

let CryptoJS = require('crypto-js');		// 调用crypto-js 模块
let D = {
        ne: function(e, t) {
        return CryptoJS.AES.encrypt(CryptoJS.enc.Utf8.parse(e), CryptoJS.enc.Utf8.parse(t.substr(0, 32)), {
            iv: CryptoJS.enc.Utf8.parse(t.substr(-16)),
            mode: CryptoJS.mode.CBC,
            padding: CryptoJS.pad.Pkcs7
        }).ciphertext.toString().toUpperCase()
    }
}

let r_obj = {
    utf8: {
        stringToBytes: function(e) {
            return r_obj.bin.stringToBytes(unescape(encodeURIComponent(e)))
        },
        bytesToString: function(e) {
            return decodeURIComponent(escape(r_obj.bin.bytesToString(e)))
        }
    },
    bin: {
        stringToBytes: function(e) {
            for (var t = [], n = 0; n < e.length; n++)
                t.push(255 & e.charCodeAt(n));
            return t
        },
        bytesToString: function(e) {
            for (var t = [], n = 0; n < e.length; n++)
                t.push(String.fromCharCode(e[n]));
            return t.join("")
        }
    }
}

i = function(e, n) {
    var r = r_obj.utf8
                e.constructor == String ? e = n && "binary" === n.encoding ? a.stringToBytes(e) : r.stringToBytes(e) : o(e) ? e = Array.prototype.slice.call(e, 0) : Array.isArray(e) || e.constructor === Uint8Array || (e = e.toString());
                for (var c = t.bytesToWords(e), u = 8 * e.length, l = 1732584193, s = -271733879, f = -1732584194, d = 271733878, p = 0; p < c.length; p++)
                    c[p] = 16711935 & (c[p] << 8 | c[p] >>> 24) | 4278255360 & (c[p] << 24 | c[p] >>> 8);
                c[u >>> 5] |= 128 << u % 32,
                c[14 + (u + 64 >>> 9 << 4)] = u;

                i._ff = function(e, t, n, r, o, a, i) {
                    var c = e + (t & n | ~t & r) + (o >>> 0) + i;
                    return (c << a | c >>> 32 - a) + t
                }
                ,
                i._gg = function(e, t, n, r, o, a, i) {
                    var c = e + (t & r | n & ~r) + (o >>> 0) + i;
                    return (c << a | c >>> 32 - a) + t
                }
                ,
                i._hh = function(e, t, n, r, o, a, i) {
                    var c = e + (t ^ n ^ r) + (o >>> 0) + i;
                    return (c << a | c >>> 32 - a) + t
                }
                ,
                i._ii = function(e, t, n, r, o, a, i) {
                    var c = e + (n ^ (t | ~r)) + (o >>> 0) + i;
                    return (c << a | c >>> 32 - a) + t
                }
                var v = i._ff
                  , m = i._gg
                  , h = i._hh
                  , y = i._ii;



                for (p = 0; p < c.length; p += 16) {
                    var g = l
                      , b = s
                      , x = f
                      , w = d;
                    l = v(l, s, f, d, c[p + 0], 7, -680876936),
                    d = v(d, l, s, f, c[p + 1], 12, -389564586),
                    f = v(f, d, l, s, c[p + 2], 17, 606105819),
                    s = v(s, f, d, l, c[p + 3], 22, -1044525330),
                    l = v(l, s, f, d, c[p + 4], 7, -176418897),
                    d = v(d, l, s, f, c[p + 5], 12, 1200080426),
                    f = v(f, d, l, s, c[p + 6], 17, -1473231341),
                    s = v(s, f, d, l, c[p + 7], 22, -45705983),
                    l = v(l, s, f, d, c[p + 8], 7, 1770035416),
                    d = v(d, l, s, f, c[p + 9], 12, -1958414417),
                    f = v(f, d, l, s, c[p + 10], 17, -42063),
                    s = v(s, f, d, l, c[p + 11], 22, -1990404162),
                    l = v(l, s, f, d, c[p + 12], 7, 1804603682),
                    d = v(d, l, s, f, c[p + 13], 12, -40341101),
                    f = v(f, d, l, s, c[p + 14], 17, -1502002290),
                    l = m(l, s = v(s, f, d, l, c[p + 15], 22, 1236535329), f, d, c[p + 1], 5, -165796510),
                    d = m(d, l, s, f, c[p + 6], 9, -1069501632),
                    f = m(f, d, l, s, c[p + 11], 14, 643717713),
                    s = m(s, f, d, l, c[p + 0], 20, -373897302),
                    l = m(l, s, f, d, c[p + 5], 5, -701558691),
                    d = m(d, l, s, f, c[p + 10], 9, 38016083),
                    f = m(f, d, l, s, c[p + 15], 14, -660478335),
                    s = m(s, f, d, l, c[p + 4], 20, -405537848),
                    l = m(l, s, f, d, c[p + 9], 5, 568446438),
                    d = m(d, l, s, f, c[p + 14], 9, -1019803690),
                    f = m(f, d, l, s, c[p + 3], 14, -187363961),
                    s = m(s, f, d, l, c[p + 8], 20, 1163531501),
                    l = m(l, s, f, d, c[p + 13], 5, -1444681467),
                    d = m(d, l, s, f, c[p + 2], 9, -51403784),
                    f = m(f, d, l, s, c[p + 7], 14, 1735328473),
                    l = h(l, s = m(s, f, d, l, c[p + 12], 20, -1926607734), f, d, c[p + 5], 4, -378558),
                    d = h(d, l, s, f, c[p + 8], 11, -2022574463),
                    f = h(f, d, l, s, c[p + 11], 16, 1839030562),
                    s = h(s, f, d, l, c[p + 14], 23, -35309556),
                    l = h(l, s, f, d, c[p + 1], 4, -1530992060),
                    d = h(d, l, s, f, c[p + 4], 11, 1272893353),
                    f = h(f, d, l, s, c[p + 7], 16, -155497632),
                    s = h(s, f, d, l, c[p + 10], 23, -1094730640),
                    l = h(l, s, f, d, c[p + 13], 4, 681279174),
                    d = h(d, l, s, f, c[p + 0], 11, -358537222),
                    f = h(f, d, l, s, c[p + 3], 16, -722521979),
                    s = h(s, f, d, l, c[p + 6], 23, 76029189),
                    l = h(l, s, f, d, c[p + 9], 4, -640364487),
                    d = h(d, l, s, f, c[p + 12], 11, -421815835),
                    f = h(f, d, l, s, c[p + 15], 16, 530742520),
                    l = y(l, s = h(s, f, d, l, c[p + 2], 23, -995338651), f, d, c[p + 0], 6, -198630844),
                    d = y(d, l, s, f, c[p + 7], 10, 1126891415),
                    f = y(f, d, l, s, c[p + 14], 15, -1416354905),
                    s = y(s, f, d, l, c[p + 5], 21, -57434055),
                    l = y(l, s, f, d, c[p + 12], 6, 1700485571),
                    d = y(d, l, s, f, c[p + 3], 10, -1894986606),
                    f = y(f, d, l, s, c[p + 10], 15, -1051523),
                    s = y(s, f, d, l, c[p + 1], 21, -2054922799),
                    l = y(l, s, f, d, c[p + 8], 6, 1873313359),
                    d = y(d, l, s, f, c[p + 15], 10, -30611744),
                    f = y(f, d, l, s, c[p + 6], 15, -1560198380),
                    s = y(s, f, d, l, c[p + 13], 21, 1309151649),
                    l = y(l, s, f, d, c[p + 4], 6, -145523070),
                    d = y(d, l, s, f, c[p + 11], 10, -1120210379),
                    f = y(f, d, l, s, c[p + 2], 15, 718787259),
                    s = y(s, f, d, l, c[p + 9], 21, -343485551),
                    l = l + g >>> 0,
                    s = s + b >>> 0,
                    f = f + x >>> 0,
                    d = d + w >>> 0
                }
                return t.endian([l, s, f, d])
            }

t = {
    wordsToBytes: function(e) {
        for (var t = [], n = 0; n < 32 * e.length; n += 8)
            t.push(e[n >>> 5] >>> 24 - n % 32 & 255);
        return t
    },
    bytesToWords: function(e) {
        for (var t = [], n = 0, r = 0; n < e.length; n++,
        r += 8)
            t[r >>> 5] |= e[n] << 24 - r % 32;
        return t
    },
    bytesToHex: function(e) {
        for (var t = [], n = 0; n < e.length; n++)
            t.push((e[n] >>> 4).toString(16)),
            t.push((15 & e[n]).toString(16));
        return t.join("")
    },
    rotl: function(e, t) {
        return e << t | e >>> 32 - t
    },
    rotr: function(e, t) {
        return e << 32 - t | e >>> t
    },

    endian: function(e) {
        if (e.constructor == Number)
            return 16711935 & t.rotl(e, 8) | 4278255360 & t.rotl(e, 24);
        for (var x = 0; x < e.length; x++)
            e[x] = t.endian(e[x]);
        return e
    }
}

aaa = function (e,n){
    // if (void 0 === e || null === e)
    //     throw new Error("Illegal argument " + e);
    var r = t.wordsToBytes(i(e, n));
    return n && n.asBytes ? r : n && n.asString ? a.bytesToString(r) : t.bytesToHex(r)
}

var get_pas_word = function(e,a){
    var o = e.password
      , s = e.mobile
      // , a = ot()
    var l = D.ne("".concat(a).concat(o), aaa(("".concat(s.slice(3)).concat(a))));
    return l
}
var e_dic = {
    "mobile": "17836797789",
    "password": "123wu123123"
}
a = 1686207919
console.log(get_pas_word(e_dic,a))
