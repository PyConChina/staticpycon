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
    $ git@gitcafe.com:toddgao/staticpycon.git
    $ cd staticpycon
    $ python app.py



## Changelog

- 141002 大妈尝试 替换 当前的 MkDocs/local -> 7niu 流程
- 140928 大妈整体复制为 https://gitcafe.com/PyConChina/staticpycon
- 140927 Todd Gao 发布
