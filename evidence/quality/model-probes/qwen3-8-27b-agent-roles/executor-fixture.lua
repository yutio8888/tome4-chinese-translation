-- Frozen synthetic executor probe. Only target strings may change.
local t = function(source, target, source_tag, special, args_order)
	return {source, target, source_tag, special, args_order}
end

return {
	t("Deals up to %d manaburn damage within radius %d.", "在%d码范围内造成%d法力燃烧伤害。", "tformat", nil, {2, 1}),
	t("Affects all other creatures within radius %d.", "影响半径%d码内的所有生物。", "tformat"),
	t("The shield lasts %d turns and blocks %d damage per cleansed debuff.", "护盾持续%d回合，并抵挡%d点伤害。", "tformat"),
}
