
function string10to64(a) {
    var b = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-~'['split']('')
      , c = b['length']
      , d = +a
      , e = [];
    do {
        mod = d % c;
        d = (d - mod) / c;
        e['unshift'](b[mod]);
    } while (d);
    return e['join']('');
}

function prefixInteger(a, b) {
    return (Array(b)['join'](0x0) + a)['slice'](-b);
}

function pretreatment(a, b, c) {
    var d = this;
    var e = string10to64(Math['abs'](a));
    var f = '';
    if (!c) {
        f += a > 0x0 ? '1' : '0';
    }
    f += prefixInteger(e, b);
    return f;
}

function getCoordinate (a) {
        var b = this;
        var c = new Array();
        for (var d = 0x0; d < a['length']; d++) {
            if (d == 0x0) {
                c['push'](pretreatment(a[d][0x0] < 0x3ffff ? a[d][0x0] : 0x3ffff, 0x3, !![]));
                c['push'](pretreatment(a[d][0x1] < 0xffffff ? a[d][0x1] : 0xffffff, 0x4, !![]));
                c['push'](pretreatment(a[d][0x2] < 0x3ffffffffff ? a[d][0x2] : 0x3ffffffffff, 0x7, !![]));
            } else {
                var e = a[d][0x0] - a[d - 0x1][0x0];
                var f = a[d][0x1] - a[d - 0x1][0x1];
                var g = a[d][0x2] - a[d - 0x1][0x2];
                c['push'](pretreatment(e < 0xfff ? e : 0xfff, 0x2, ![]));
                c['push'](pretreatment(f < 0xfff ? f : 0xfff, 0x2, ![]));
                c['push'](pretreatment(g < 0xffffff ? g : 0xffffff, 0x4, !![]));
            }
        }
        return c['join']('');
    }

//     console.log(getCoordinate([
//     [
//         "1177",
//         "339",
//         1697443399055
//     ],
//     [
//         "1211",
//         "369",
//         1697443399055
//     ],
//     [
//         "1211",
//         "369",
//         1697443399058
//     ],
//     [
//         "1212",
//         "369",
//         1697443399067
//     ],
//     [
//         "1212",
//         "369",
//         1697443399075
//     ],
//     [
//         "1213",
//         "369",
//         1697443399099
//     ],
//     [
//         "1214",
//         "369",
//         1697443399114
//     ],
//     [
//         "1216",
//         "369",
//         1697443399122
//     ],
//     [
//         "1218",
//         "369",
//         1697443399138
//     ],
//     [
//         "1219",
//         "369",
//         1697443399146
//     ],
//     [
//         "1221",
//         "369",
//         1697443399154
//     ],
//     [
//         "1222",
//         "369",
//         1697443399162
//     ],
//     [
//         "1224",
//         "369",
//         1697443399170
//     ],
//     [
//         "1225",
//         "369",
//         1697443399178
//     ],
//     [
//         "1227",
//         "369",
//         1697443399194
//     ],
//     [
//         "1228",
//         "369",
//         1697443399210
//     ],
//     [
//         "1230",
//         "369",
//         1697443399271
//     ],
//     [
//         "1231",
//         "369",
//         1697443399354
//     ],
//     [
//         "1232",
//         "369",
//         1697443399378
//     ],
//     [
//         "1234",
//         "369",
//         1697443399394
//     ],
//     [
//         "1235",
//         "369",
//         1697443399402
//     ],
//     [
//         "1236",
//         "369",
//         1697443399410
//     ],
//     [
//         "1237",
//         "369",
//         1697443399419
//     ],
//     [
//         "1238",
//         "369",
//         1697443399426
//     ],
//     [
//         "1239",
//         "369",
//         1697443399442
//     ],
//     [
//         "1241",
//         "369",
//         1697443399514
//     ],
//     [
//         "1241",
//         "369",
//         1697443399530
//     ]
// ]))


//0ip005joITwImf10y10u0000000000000310100000090000000008101000000o101000000f1020000008102000000g10100000081020000008101000000810200000081010000008102000000g101000000g102000000Z101000001j101000000o102000000g1010000008101000000810100000091010000007101000000g1020000018000000000g
//0ip005joITwImf10y10u0000000000000310100000090000000008101000000o101000000f1020000008102000000g10100000081020000008101000000810200000081010000008102000000g101000000g102000000Z101000001j101000000o102000000g1010000008101000000810100000091010000007101000000g1020000018000000000g


