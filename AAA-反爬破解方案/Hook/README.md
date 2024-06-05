### Hook案例说明

#### 原理
Hook最主要的作用是将某个函数捕获到后，针对某一个函数进行重写，实现自定义的改写里面的代码


#### 本次暂时只处理如何突破 无线debugger 的情况
##### 无线debugger原理
1. debugger关键词
2. eval('debugger') 原理跟1类似，只不过是在虚拟机里面执行debugger的方法
3. Function('debugger')() 及其变种 原理跟2类似，只不过是在虚拟机里面执行匿名函数，匿名函数里有debugger的方法

##### 突破无线debugger
    了解了原理之后就可以知道，通过 Function('debugger')() 的部分，学习过JS的原型链后就知道他最终一定会经过Function
    因此我们直接改写Function
    代码：
    _Function = Function
    Function.prototype.constructor = function(){
        if (arguments[0].indexOf('debugger') != -1){
                arguments[0] = arguments[0].replaceAll('debugger','')
            }
        return _Function.apply(this,arguments )
    }
    当然eval也是相同原理，去重写eval即可

##### 使用油猴执行
虽然可以直接在浏览器控制台直接执行Hook，但每次都会被刷新掉太麻烦，因此我们借助油猴来帮助我们执行

![image](https://github.com/wu50416/spider_projects/assets/103317042/0dd83eb8-775f-474c-9d14-52917d9d4ccc)


