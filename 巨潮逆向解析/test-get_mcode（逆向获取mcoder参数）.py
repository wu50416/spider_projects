import execjs
import js2py
'''
通过这个函数获取
var indexcode={
    getResCode:function(){
        var time=Math.floor(new Date().getTime()/1000);
        return window.JSonToCSV.missjson(""+time);
    }
}
'''
def get_mcode():
    with open('123.js','r',encoding='utf-8')as f:
        read_js=f.read()
    return_js=execjs.compile(read_js) #
    # 用来获取time参数
    time1 = js2py.eval_js('Math.floor(new Date().getTime()/1000)')
    mcode = return_js.call('missjson','{}'.format(time1))
    print(mcode)
if __name__ == '__main__':
    get_mcode()