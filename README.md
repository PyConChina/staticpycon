# staticpycon

PyCon China 2014 官网生成工具

## 使用

代码push到master后5分钟内会自动发布到[官网](http://cn.pycon.org).

---

## 翻译规则

翻译是对`src/data/`下的yaml文件进行处理;
对需要翻译的字段(如`name`),创建后缀`_en`的新字段(`name_en`),以译文作为字段的值. 举例(见`_proposals.yaml`):

```
-
  name: 李宽
  city_beijing: 1
  city: 北京
  city_en: Beijing
  avatar: http://pyconcn.qiniudn.com/zoomquiet/stuff14/id/li-kuan.png?imageView2/2/h/80
  intro: 中科院微生物所,生物信息工程师
  intro_en: Bioinformatics engineer, Institute of Microbiology, Chinese Academy of Sciences
```

`city_en`,`intro_en`是对`city`,`intro`的翻译,在英文版网页将显示它们的值(译文内容). 

注意:
 1. 所有翻译字段必须有对应的原字段,如`city_en`对应`city`,否则将不会产生效果
 2. 翻译字段在模板中是可以访问的,但请用原字段,数据加载中自动做了替换处理
 3. 非翻译字段**不能**以`_cn`或`_en`结尾

----

## Changelog

见[提交历史](https://gitcafe.com/PyConChina/staticpycon/commits/master). 
