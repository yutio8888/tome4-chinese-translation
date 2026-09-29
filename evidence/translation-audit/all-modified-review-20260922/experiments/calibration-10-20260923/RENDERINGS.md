# K05 拼接分支演示

这是按冻结宿主与后缀进行的 Python 字符串组合，不是游戏运行实测。数值 30、50、10 和属性描述均为演示输入；后缀为空与非空各覆盖一次。

## 可用分支

英文：
```text
Your left hand mutates into a disgusting mass of tentacles.
		When you have your offhand empty you automatically hit your target and those on the side whenever you hit with a basic attack.
		Also increases Physical Power by 30, and increases weapon damage by 50% for your tentacles attacks.
		Each time you make an attack with your tentacle you gain 10 insanity.
		You generate a low power psionic field around you when around #{italic}#'civilized people'#{normal}# that prevents them from seeing you for the horror you are.

		Your tentacle hand currently has these stats:
		[combat description]
```
中文：
```text
你的左手异变成为一坨恶心的触手。
		副手空闲时，当使用普通攻击，触手会自动攻击目标以及目标同侧的其他单位。
		物理强度提高 30，触手武器伤害提高 50%。
		每次触手攻击时，获得 10 疯狂值。
		附近有 #{italic}# 普通人 #{normal}# 时会自动生成微弱的心灵护盾，避免被他们发现你的恐魔形态。
		你的触手当前属性为  :
		[属性描述]
```

## 禁用分支

英文：
```text
Your left hand mutates into a disgusting mass of tentacles.
		When you have your offhand empty you automatically hit your target and those on the side whenever you hit with a basic attack.
		Also increases Physical Power by 30, and increases weapon damage by 50% for your tentacles attacks.
		Each time you make an attack with your tentacle you gain 10 insanity.
		You generate a low power psionic field around you when around #{italic}#'civilized people'#{normal}# that prevents them from seeing you for the horror you are.

		Your tentacle hand currently has these stats, #CRIMSON# but is currently disabled due to non-empty offhand#WHITE#:
		[combat description]
```
中文：
```text
你的左手异变成为一坨恶心的触手。
		副手空闲时，当使用普通攻击，触手会自动攻击目标以及目标同侧的其他单位。
		物理强度提高 30，触手武器伤害提高 50%。
		每次触手攻击时，获得 10 疯狂值。
		附近有 #{italic}# 普通人 #{normal}# 时会自动生成微弱的心灵护盾，避免被他们发现你的恐魔形态。
		你的触手当前属性为 ，#CRIMSON#由于副手非空，该技能暂时被禁用#WHITE# :
		[属性描述]
```
