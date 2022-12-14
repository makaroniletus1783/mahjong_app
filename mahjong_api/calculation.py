# 計算


from mahjong.hand_calculating.hand import HandCalculator
# 麻雀牌
from mahjong.tile import TilesConverter
#役, オプションルール
from mahjong.hand_calculating.hand_config import HandConfig, OptionalRules
# 鳴き
from mahjong.meld import Meld
# 風(場&自)
from mahjong.constants import EAST, SOUTH, WEST, NORTH

# HandCalculator(計算用クラス)のインスタンスを生成
calculator = HandCalculator()

results = {}


class Calculation:
    def __init__(self, hai, yaku):
        pin = ''
        sou = ''
        man = ''
        honors = ''
        has_aka_dora = False

        # 肺の振り分け
        for name in hai:
            if name[0] == 'p' and name[0] != 'e':
                pin += name[1]
            elif name[0] == 's' and name[0] != 'h':
                sou += name[1]
            elif name[0] == 'm':
                man += name[1]
            elif name == 'ton':
                honors += '1'
            elif name == 'nan':
                honors += '2'
            elif name == 'sha':
                honors += '3'
            elif name == 'pe':
                honors += '4'
            elif name == 'pei':
                honors += '4'
            elif name == 'haku':
                honors += '5'
            elif name == 'hatu':
                honors += '6'
            elif name == 'tyun':
                honors += '7'

            if name[1] == '0':
                has_aka_dora = True

        #アガリ形(man=マンズ, pin=ピンズ, sou=ソーズ, honors=字牌)
        tiles = TilesConverter.string_to_136_array(
            man=man, pin=pin, sou=sou, honors=honors, has_aka_dora=has_aka_dora)
        #tiles = TilesConverter.string_to_136_array(man='22224445577779999')

        # アガリ牌
        rise = yaku['win_tile']
        win_tile = self.option(rise)

        # 鳴き
        melds = []

        # チー
        for name in yaku['chi']:
            chi = ''
            for i in range(3):
                chi += str(int(name[1]) + i)
            if name[0] == 'p':
                melds.append(
                    Meld(Meld.CHI, TilesConverter.string_to_136_array(pin=chi)))
            elif name[0] == 's':
                melds.append(
                    Meld(Meld.CHI, TilesConverter.string_to_136_array(sou=chi)))
            elif name[0] == 'm':
                melds.append(
                    Meld(Meld.CHI, TilesConverter.string_to_136_array(man=chi)))

        # ポン
        for name in yaku['pon']:
            pon = ''
            for i in range(3):
                pon += name[1]
            if name[0] == 'p':
                melds.append(
                    Meld(Meld.PON, TilesConverter.string_to_136_array(pin=pon)))
            elif name[0] == 's':
                melds.append(
                    Meld(Meld.PON, TilesConverter.string_to_136_array(sou=pon)))
            elif name[0] == 'm':
                melds.append(
                    Meld(Meld.PON, TilesConverter.string_to_136_array(man=pon)))
            else:
                melds.append(
                    Meld(Meld.PON, TilesConverter.string_to_136_array(honors=pon)))

        # ミンカン
        for name in yaku['minkan']:
            minkan = ''
            for i in range(4):
                minkan += name[1]
            if name[0] == 'p':
                melds.appned(
                    Meld(Meld.KAN, TilesConverter.string_to_136_array(pin=minkan), True))
            elif name[0] == 's':
                melds.append(
                    Meld(Meld.KAN, TilesConverter.string_to_136_array(sou=minkan), True))
            elif name[0] == 'm':
                melds.append(
                    Meld(Meld.KAN, TilesConverter.string_to_136_array(man=minkan), True))
            else:
                melds.append(
                    Meld(Meld.KAN, TilesConverter.string_to_136_array(honors=minkan), True))

        # アンカン
        for name in yaku['annkan']:
            annkan = ''
            for i in range(4):
                annkan += name[1]
            if name[0] == 'p':
                melds.append(
                    Meld(Meld.KAN, TilesConverter.string_to_136_array(pin=annkan), False))
            elif name[0] == 's':
                melds.append(
                    Meld(Meld.KAN, TilesConverter.string_to_136_array(sou=annkan), False))
            elif name[0] == 'm':
                melds.append(
                    Meld(Meld.KAN, TilesConverter.string_to_136_array(man=annkan), False))
            else:
                melds.append(
                    Meld(Meld.KAN, TilesConverter.string_to_136_array(honors=annkan), False))

        # カカン
        for name in yaku['chankan']:
            chankan = ''
            for i in range(4):
                chankan += name[1]
            if name[0] == 'p':
                melds.append(
                    Meld(Meld.CHANKAN, TilesConverter.string_to_136_array(pin=chankan)))
            elif name[0] == 's':
                melds.append(
                    Meld(Meld.CHANKAN, TilesConverter.string_to_136_array(sou=chankan)))
            elif name[0] == 'm':
                melds.append(
                    Meld(Meld.CHANKAN, TilesConverter.string_to_136_array(man=chankan)))
            else:
                melds.append(
                    Meld(Meld.CHANKAN, TilesConverter.string_to_136_array(honors=chankan)))

        # ドラ
        dora_names = yaku['dora']
        dora = []
        for dora_name in dora_names:
            dora.append(self.option(dora_name))

        # 裏ドラ
        ura_dora_names = yaku['ura_dora']
        ura_dora = []
        for ura_dora_name in ura_dora_names:
            ura_dora.append(self.option(ura_dora_name))

        # ドラ(表示牌,裏ドラ)
        if dora == None and ura_dora == None:
            dora_indicators = None
        else:
            dora_indicators = []
            for tmp in dora:
                dora_indicators.append(tmp)
            for tmp in ura_dora:
                dora_indicators.append(tmp)

        # 場風、自風
        player_wind = self.wind(yaku['player_wind'])
        round_wind = self.wind(yaku['round_wind'])

        config = HandConfig(is_tsumo=yaku['is_tsumo'], is_rinshan=yaku['is_rinshan'], player_wind=player_wind, round_wind=round_wind,
                            is_riichi=yaku['is_riichi'], is_ippatsu=yaku['is_ippatsu'], is_chankan=yaku['is_chankan'], is_haitei=yaku[
                                'is_haitei'], is_houtei=yaku['is_houtei'], is_daburu_riichi=yaku['is_daburu_riichi'],
                            is_nagashi_mangan=yaku['is_nagashi_mangan'], is_tenhou=yaku[
                                'is_tenhou'], is_renhou=yaku['is_renhou'], is_chiihou=yaku['is_chiihou'],
                            options=OptionalRules(has_open_tanyao=True, has_aka_dora=has_aka_dora, fu_for_open_pinfu=True, has_double_yakuman=True, kiriage=True, fu_for_pinfu_tsumo=True, renhou_as_yakuman=True, has_daisharin=True, has_daisharin_other_suits=True,
                                                  kazoe_limit=HandConfig.KAZOE_LIMITED))

        self.hand_result = calculator.estimate_hand_value(
            tiles, win_tile, melds, dora_indicators, config)

    # option判定

    def option(self, rise):
        win_tile = None
        if rise != None:
            if rise[0] == 'm':
                win_tile = TilesConverter.string_to_136_array(man=rise[1])[0]
            elif rise[0] == 's':
                win_tile = TilesConverter.string_to_136_array(sou=rise[1])[0]
            elif rise[0] == 'p':
                win_tile = TilesConverter.string_to_136_array(pin=rise[1])[0]
            else:
                win_tile = TilesConverter.string_to_136_array(honors=rise[1])[
                    0]
        return win_tile

    # オプション

    def wind(self, hougaku):
        a = None
        if hougaku == '北':
            a = NORTH
        elif hougaku == '東':
            a = EAST
        elif hougaku == '南':
            a = SOUTH
        elif hougaku == '西':
            a = WEST
        return a

    # 計算
    def print_hand_result(self):
        # 翻数, 符数
        # print(hand_result.han, hand_result.fu)
        results['han'] = self.hand_result.han
        results['fu'] = self.hand_result.fu
        # 点数(ツモアガリの場合[左：親失点, 右:子失点], ロンアガリの場合[左:放銃者失点, 右:0])
        # print(hand_result.cost['main'], result.cost['additional'])
        results['parent'] = self.hand_result.cost['main']
        results['child'] = self.hand_result.cost['additional']
        # 役
        # print(hand_result.yaku)
        results['yaku'] = self.hand_result.yaku
        # 符数の詳細
        # for fu_item in hand_result.fu_details:
        # print(fu_item)
        # print(results)
        return results
