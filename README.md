# staticpycon

PyCon China 2014 官网生成工具

## 2015 官网发布

- 分支: https://gitcafe.com/PyConChina/staticpycon/tree/2015
- 发布: http://pyconcn.qiniudn.com/2015/
- 代理: http://cn.pycon.org/



## 构建环境配置

```sh
virtualenv venv-foo  # 预先 .gitignore 了 venv-* 和 test 所以不用担心
. ./venv-foo/bin/activate
pip install -r requirements.txt
```

## 本地构建方法

```sh
# 会执行构建, 并在本地 8080 端口启动测试服务器
# 请访问 http://127.0.0.1:8080 观看效果
./bin/app.py
```

## 代码部署

```sh
# 下载源码
git clone git@github.com:PyConChina/staticpycon.git
# 或者通过 HTTPS 下载:
git clone https://github.com/PyConChina/staticpycon.git

cd staticpycon
# 然后按照上边的方法安装依赖关系

# 构建:
#
# 首次构建会自动创建 out/ 目录
# 编辑 src/ 目录下的文件
# 会在 out/ 下生成网页
python bin/app.py -g
# 只编译 Sass:
python bin/app.py --sass
# 也可以开启自动生成服务, 监听到文件修改即时生成新的文件, 在本地进行调试
python bin/app.py
```

代码push到master后5分钟内会自动发布到[官网](http://cn.pycon.org).

---

## 翻译规则

翻译是对`src/data/`下的yaml文件进行处理;
对需要翻译的字段(如`name`),创建后缀`_en`的新字段(`name_en`),以译文作为字段的值. 举例(见`_speakers.yaml`):

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

见[提交历史](https://github.com/PyConChina/staticpycon/commits/master).

# 整个儿的故事:

其实,一个技术大会官网的折腾历史本身也是非常有趣的呢,
基本上,体现了一个技术社区的活跃度 ;-)

## 2014 以前

2011 发起 PyConChina 年度大会以来,一直坚持以社区核心成员为主力的思路来折腾,

所以:

- 赞助从核心成员所在东家为起点
- 组委都是核心成员,老的,,,
- 官网自然而然的也锁定在 Limodou 的原创框架 UliWeb 上

然后:

- 运营的各种折腾哪,,,


## 2014 以来

大妈,以往基于 Jekyll/Pelican 等等静态网站引擎发布了很多社区网站,
又算 42% 位运维工程师, 所以,从运维角度多考虑了点什么...

- 就无法忍受动态的 UliWeb 框架了
- 因为,大会已经举办了三年, 依然是一个全部是静态信息发布网站
- 那些,应该是 UliWeb 大显身手的功能:
    + 注册
    + 购票
    + 在线讨论
    + 抽奖
    + 提醒
    + ...etc.
- 都没有开发, 目测也用不上...
- 现在第三方服务越来越多的通过 JS 嵌入到静态页面中就好,根本不用自个儿支撑所有动态功能了

于是决定加以改变

### UliWeb 静态输出

首先,当然是想在 UliWeb 上追加静态输出的功能就好

但是:

- 原先为了对静态信息的多种形式发布, Limodou 折腾出了各种形式的数据集:
    + json
    + py
    + html 片段
    + ...etc.
- 而且都不是 UliWeb 擅长的,纯粹都在特制化了模板而来
- 进一步的还完成了部分 i18N 功能
- 这导致静态输出没有那么简单
- 折腾了两周,给出一个原型功能分支后, limodou 表示可以了... 

然后,没有了然后...

### MkDocs 原型
时间不等人, 大妈 于是独自用 MkDocs 快速完成一个静态原型刚刚,配合完整的协同工作流,
抛了出来:

- [PyConChina/MkDoc4PyCon](https://gitcafe.com/PyConChina/MkDoc4PyCon)
- 通过本地 `fabric` 脚本,完成编译,以及推送到 7niu CDN
- 绑定了 `cn.pycon.org` 域名的服务端嘦处理好 UlkiWeb 历史系统和反代 CDN 目录到正确 URI 就好

一切看起来可行,但是:

- MkDocs 毕竟是文档网站工具,对一个大会官网需要的多种表现形式无法通过 md 自身实现
- 要不都手工用 html 完成, 这就没有了工具的意义


怎么办?

### staticPyCon 工具
大家都说要有新的静态化工具, 然后就有了: [PyConChina/staticpycon](https://github.com/PyConChina/staticpycon)

- [Todd Gao](https://github.com/7c00) 用了一夜完成的工具
- 复用了 MkDocs 的样式,基于 `staticjinja` 完成编译工具, 统一使用 `ymal` 为数据格式

一切看起来可行,但是:

- 高速修订起来才发现 7niu CDN 好象无法实时完成全网同步
- 无论我们怎么折腾 nginx 的反代配置,都无法在完成了内容发布后,从官网看到
- 目测原因是:
    + cn.pycon.org 没有备案
    + 所以,在国外 VPS 中
    + 7niu 的国外节点少,所以,同步不及时
    + 现象就是发布新内容后, 官网只能用 `?v=233` 形式来强行读取到, 而通过 7niu 默认 bucket URI 就可以看到最新内容!

肿么办?

### 持续折腾 staticPyCon

首先,整体规划:

- [工单 #1: 为长期运维进行 URI 重构 · PyConChina/PyConChina - GitCafe](https://gitcafe.com/PyConChina/PyConChina/tickets/1)

然后分步迁移:

- 部署外网多主机空间的自动化同步/编译脚本
- 在测试 端口上配置新策略 官网
- 验证通过后, 快速切换

于是就变成了:

```
[[DigitalOcean hosts]]
  ^ |     | | |           (git pull & re-gen.)
  | |     +-+-+-------+
  | |                 |
  | |[[Linode host]]  |
  | | |(cron task) >>>| 
  | | |               +- (git pull & re-gen.)
  | V V                  ^    
  |((Nginx))             |            
  |                      |
  +------ [[gitcafe repo.]]
            |^
            V|
<<local editor>>
```


