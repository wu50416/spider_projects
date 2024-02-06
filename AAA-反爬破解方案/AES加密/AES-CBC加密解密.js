let CryptoJS = require('crypto-js');		// 调用crypto-js 模块

// ## AES-CBC模式加密
let key = CryptoJS.enc.Utf8.parse('0CoJUm6Qyw8W8jud'),  //密钥必须是16位，utf8编码方式
	iv = CryptoJS.enc.Utf8.parse("0102030405060708");   //iv也是16位哦, utf8编码方式

function jiami(text){
	let srcs = CryptoJS.enc.Utf8.parse(text);
	let encryptedData  = CryptoJS.AES.encrypt(srcs, key, {
		iv: iv,
	    mode: CryptoJS.mode.CBC,
	    padding: CryptoJS.pad.Pkcs7
	});
	let hexData = encryptedData.ciphertext.toString();
	return hexData;
}

// hexData = 5d405dde1859ed49e8eaed988b82c8bf

// ## AES-CBC模式解密
function jiemi(hexData){
    let encryptedHexStr  = CryptoJS.enc.Hex.parse(hexData), //把加密数据以Hex编码方式转成数组
    	encryptedBase64Str  = CryptoJS.enc.Base64.stringify(encryptedHexStr), //把上一步的数组以Baes64编码方式转成字符串 
    	decryptedData  = CryptoJS.AES.decrypt(encryptedBase64Str, key, {
        iv: iv,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7
});  
    let text = decryptedData.toString(CryptoJS.enc.Utf8);  
    return text;  // 得到解密结果
}

console.log('加密后：',jiami('123456'));
console.log('加密前：',jiemi('3ea397412b78f3a1974640e6b3294c98'))
