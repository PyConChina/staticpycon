# 携带二次修改的第三方库

## 说明

* 仿照 [pip 的解决方案][pip-vendor]设置
* PyPI 的版本能正常工作的库不要放进来
* 一旦有正常版本进入 PyPI, 最好把这里的库去掉, track upstream 是美德



## 当前内容

* [pyScss][vendored-scss]: 上游版本功能不全, 且有不兼容行为.


[pip-vendor]: https://github.com/pypa/pip/tree/develop/pip/_vendor
[scss]: https://github.com/xen0n/pyScss/commit/4afdc0a6db77d86c4500ddca9a36813b20c58b50


<!-- vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8: -->
