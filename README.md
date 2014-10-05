# staticpycon
静态化 PyCon 网站生成工具

## 背景
[PyConChina/MkDoc4PyCon - GitCafe](https://gitcafe.com/PyConChina/MkDoc4PyCon/blob/master/README.md)

为了更加快捷的发布 cn.pycon.org 我们进行了多方折腾

## 设想
处理pycon网站的过程中,我发现使用基于mkdocs的实现,存在以下问题:

- markdown的表现力有限,对样式的定制和修改非常不便;一种妥协的办法是在markdown中大量嵌入html,但代码会特别难看;
- 网站内容有很多重复的结构化数据,使用markdown处理它们也很难受;

## 实现
于是我用staticjinja重构了一下,主要思想是数据和表现分离,所有结构数据使用yaml文件保存,表现使用jinja2模板,多说无益,还是看代码吧

## 使用

    $ pip install staticjinja mkdocs
    $ git clone git@gitcafe.com:toddgao/staticpycon.git
    $ cd staticpycon
    $ python app.py

----

## 翻译规则

翻译是对`src/data/`下的yaml文件进行处理；
对需要翻译的字段（如`name`），创建后缀`_en`的新字段（`name_en`），以译文作为字段的值。举例（见`_proposals.yaml`）:

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

`city_en`、`intro_en`是对`city`、`intro`的翻译，在英文版网页将显示它们的值（译文内容）。

注意：
 1. 所有翻译字段必须有对应的原字段，如`city_en`对应`city`，否则将不会产生效果
 2. 翻译字段在模板中是可以访问的，但请用原字段，数据加载中自动做了替换处理
 3. 非翻译字段**不能**以`_cn`或`_en`结尾


## Changelog

- 141002 大妈尝试 替换 当前的 MkDocs/local -> 7niu 流程
- 140928 大妈整体复制为 https://gitcafe.com/PyConChina/staticpycon
- 140927 Todd Gao 发布
