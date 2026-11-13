06:32 boot.sh (start+load save)
06:33 setup.sh: place VOR, move ORB_ELEMENTS+HEAD to player inv, setEffect SLOW(30,power0.3) DAZED(30)
06:34 rerun effects step (con.sh setEffect SLOW/DAZED)
06:37 con.sh -k open ShowEquipInven
06:38 con.sh print HEAD inven; con.sh -k open CharacterSheet(M=Vor)
06:40 kill -9 t-engine 4016330
