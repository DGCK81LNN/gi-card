# gi-card

基于 GitHub Actions，定时更新的原神个人资料卡

![](https://dgck81lnn.github.io/gi-card/857179228.jpg)

点击右上角的“Use this template”复制本仓库，在仓库设置中创建一个名为 `github-pages` 的 Environment，在其中创建变量和 Secret：

| 变量        | 说明                         | 示例        |
|-------------|------------------------------|-------------|
| `GI_SERVER` | 账号所在区服（只支持国际服） | `os_asia`   |
| `GI_UID`    | 账号 UID                     | `857179228` |

| Secret      | 说明           | 示例 |
|-------------|----------------|------|
| `GI_COOKIE` | HoYoLAB Cookie | `_MHYUUID=eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeeee; mi18nLang=zh-cn; account_mid_v2=xxxxxxxxxx_xx; account_id_v2=888888888; . . .` |

目前仅支持国际服。如果喜欢本项目，欢迎到 [Discussions](https://github.com/DGCK81LNN/gi-card/discussions/1) 中吱个声，我会考虑增加国服支持。

本模板生成的卡片显示冒险等阶、活跃天数、角色数、成就数、深渊层数这几项数据。实际上，本程序调用的 API 还返回账号头像，各角色等级、命座、好感，神瞳收集数、锚点解锁数、宝箱开启数、区域探索度，以及尘歌壶数据。
