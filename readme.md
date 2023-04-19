# E621对接qq机器人发送插件

**当前仅支持 onebot v11 适配器**

|参数名称|参数类型|解释|
|:--:|:--:|:--:|
|e621_account|str|e621登录用户名|
|e621_api_key|str|e621的api key|

## 使用说明

**命令**: e621/621/来点图

|参数|示例|说明|
|:--:|:--|--|
|-t|-t furry feral|==tags==|
|-o|-o new|==order== 拉取时的排序顺序，可选 new / score / random(**默认**)|
|-s|-s q|==safety== 内容敏感程度，[s]afe，[q]uestionable，[e]xplicit|
|-r|-r 50|==rating== 最低分数，最高为100，超过100会自动变成100|
|-n|-n 5|==number== 一次返回的图片数量，最大为5，超过5会变成5，防止信息发送超时，默认为1，看你的服务器带宽上传速率而定|

**示例**

```
/621 -t feral dragon monster_hunter -s q -r 50 -n 3
```