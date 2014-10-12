# staticpycon

PyCon China 2014 官网生成工具

## 使用

 - 首次使用
 - (PUB_ACCESS_KEY 和 PUB_ACCESS_SECRET 请向大妈<zoomquiet+dama@gmail.com>索取)
 - 前提,成为志愿者(在官网提交过审请,并通过,且加入对应的工作列表)

        # 基本安装
        pip install staticjinja qiniu
        git clone git@gitcafe.com:PyConChina/staticpycon.git
        cd staticpycon
        # 发布相关
        cp bin/pubconf.py.example bin/pubconf.py
        vi bin/pubconf.py # 补充 PUB_ACCESS_KEY 和 PUB_ACCESS_SECRET

 - 开始编辑;开启自动生成服务器
        
        python ./bin/app.py        
        
 - 发布网站
 
        python ./bin/pub.py

`是也乎:`

- 发布网站,本质上就是将编译出来的静态页面,发布到合适的空间
- 这类空间包含:
  + github/gitcafe 等等 pages 空间
  + 7niu 类似CDN 空间
  + 自有主机空间
  + ... etc.
- 所以,这一仓库中包含了至少三种发布方式:
  + `bin/pub.py` 使用 7niu 接口SDK 包,自动完成上传
  + `fab put7niu` 使用 fabric 调用本地 7niu 同步工具完成上传
  + 完成自动渲染后,用命令行,自行同步


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
